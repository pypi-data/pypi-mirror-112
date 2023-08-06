# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources


def get_datetime_object_from_string(string_date):
  formatter_string = "%Y-%m-%d"
  return datetime.strptime(str(string_date), formatter_string)


def calculate_days_between_two_dates(date1, date2):
  return abs((date1 - date2).days)


YEAR_DAYS = 364


class sm_contribution_line(models.Model):
  _name = 'sm_contributions.sm_contribution_line'

  _resources = sm_resources.getInstance()

  name = fields.Char(string=_("Name"), compute="compute_name")
  id = fields.Char(string=_("Id"))
  associated_contribution = fields.Many2one('sm_contributions.sm_contribution',
    string=_("Associated contribution"),ondelete='cascade')
  initial_day = fields.Date(string=_("Initial day"))
  final_day = fields.Date(string=_("Final day"))
  number_of_days = fields.Integer(string=_("Number of days"), compute="compute_number_of_days")
  interest = fields.Float(string=_("Interest"), compute="compute_interest")
  import_free_tax = fields.Float(string=_("Import free tax"), compute="compute_import_free_tax",
    store=False,digits=(16, 2))
  tax = fields.Float(string=_("Tax"), compute="compute_tax", store=False, digits=(16, 2))
  import_to_deposit_to_account = fields.Float(string=_("Import to deposit"),
    compute="compute_import_to_deposit_to_account",store=False,digits=(16, 2))
  iva = fields.Float(string=_("IVA"), compute="compute_iva")
  year = fields.Char(string=_("Year"), compute="compute_year", store=True)
  interest_model = fields.Many2one('sm_contributions.sm_contribution_interest', 'Related interest',
    compute="compute_interest_model")

  year_report_sent = fields.Boolean(string=_("Report sent"), default=False)

  related_member_id = fields.Many2one("res.partner",string=_("Related Member"),compute="_get_related_member",store=False)

  @api.depends('associated_contribution')
  def _get_related_member(self):
    for record in self:
      if record.associated_contribution.id != False:
        record.related_member_id = record.associated_contribution.associated_member


  @api.depends('initial_day')
  def compute_year(self):
    for record in self:
      if record.initial_day:
        record.year = str(get_datetime_object_from_string(str(record.initial_day)).year)

  @api.depends('interest_model.interest')
  def compute_interest(self):
    for record in self:
      record.interest = record.interest_model.interest

  @api.depends('interest_model.iva')
  def compute_iva(self):
    for record in self:
      record.interest = record.interest_model.iva

  @api.multi
  def compute_name(self):
    for record in self:
      current_year = get_datetime_object_from_string(str(record.initial_day)).year
      current_year_string = str(current_year)

      if record.associated_contribution:
        if record.associated_contribution.name:
          record.name = record.associated_contribution.name + "_" + current_year_string

  @api.multi
  def compute_number_of_days(self):
    for record in self:
      initial_day = get_datetime_object_from_string(str(record.initial_day))
      final_day = get_datetime_object_from_string(str(record.final_day))

      record.number_of_days = calculate_days_between_two_dates(initial_day, final_day)

  @api.depends('number_of_days', 'interest', 'associated_contribution.initial_import')
  def compute_import_free_tax(self):
    for record in self:
      interest_percentage = float(record.interest) / 100

      import_free_tax = float(record.number_of_days) / YEAR_DAYS * float(
        record.associated_contribution.initial_import) * interest_percentage

      record.import_free_tax = import_free_tax

  @api.depends('import_free_tax')
  def compute_tax(self):
    for record in self:
      record.tax = float(record.import_free_tax) * (float(record.interest_model.iva) / 100)

  @api.depends('import_free_tax', 'tax')
  def compute_import_to_deposit_to_account(self):
    for record in self:
      record.import_to_deposit_to_account = record.import_free_tax - record.tax

  @api.depends('associated_contribution.contribution_type', 'year')
  def compute_interest_model(self):
    for record in self:
      model_interests = record.associated_contribution.contribution_type.historical
      record.interest_model = self.get_interest_model(model_interests, int(record.year))

  def get_interest_model(self, interest_list, year_to_search):
    for interest in interest_list:
      if interest.year == year_to_search:
        return interest.id

    return self.get_closet_year(interest_list, year_to_search)

  def get_closet_year(self, interest_year, year):
    from collections import OrderedDict
    import collections

    diff_dict = OrderedDict()

    for line in interest_year:
      diff = int(line.year) - year
      if diff < 0:
        diff_dict[line] = diff * (-1)
      else:
        diff_dict[line] = diff

    diff_dict = collections.OrderedDict(reversed(list(diff_dict.items())))
    sort_dict_keys = sorted(diff_dict.keys())

    closer_less = None

    for closer in sort_dict_keys:
      if closer.year < year:
        closer_less = closer

    return closer_less

  @api.model
  def generate_related_invoice(self):
    if self.env.context:
      company = self.env.user.company_id
      if 'active_ids' in self.env.context:
        active_contribution_lines = self.env['sm_contributions.sm_contribution_line'].browse(self.env.context['active_ids'])
        if active_contribution_lines.exists():
          for line in active_contribution_lines:
            related_member = line.related_member_id
            if related_member.id != False:
              # not grouped
              invoice = self.env['account.invoice'].create({
                'partner_id': related_member.id,
                'company_id': 1,
                'state': 'draft',
                'type': 'in_invoice',
                'invoice_email_sent': False,
                'date_invoice': datetime.now()
              })
              invoice_line_name = _("Interessos totals anuals ")+"("+line.year+")"
              aportacio_line = self.env['account.invoice.line'].create({
                'name': invoice_line_name,
                'invoice_id': invoice.id,
                'price_unit': line.import_free_tax,
                'quantity': 1,
                'discount': 0,
                'account_id': company.sm_contribution_account_id.id,
                'line_type': 'default',
              })
              invoice_line_name = _("Retenció IRPF IS ") + "(" + line.year + ")"
              tax_line = self.env['account.invoice.line'].create({
                'name': invoice_line_name,
                'invoice_id': invoice.id,
                'price_unit': -1 * line.tax,
                'quantity': 1,
                'discount': 0,
                'account_id': company.sm_contribution_tax_account_id.id,
                'line_type': 'default',
              })
          return self._resources.get_successful_action_message(self,_('Invoice successfully created'),self._name)
    return self._resources.get_successful_action_message(self,_("ERROR: operation couldn't be done"),self._name)

