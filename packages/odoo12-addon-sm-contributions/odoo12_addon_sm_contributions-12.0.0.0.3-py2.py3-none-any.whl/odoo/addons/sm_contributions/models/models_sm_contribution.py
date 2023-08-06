# -*- coding: utf-8 -*-

from datetime import datetime
import datetime as dt
from monthdelta import monthdelta
from odoo import models, fields, api
from odoo.tools.translate import _


def get_datetime_object_from_string(string_date):
  formatter_string = "%Y-%m-%d"
  return datetime.strptime(str(string_date), formatter_string)


def get_first_day_of_a_year(year):
  return dt.date(year, 1, 1)


def get_last_day_of_a_year(year):
  return dt.date(year, 12, 31)


def clean_contributions_line(record):
  for line in record.contributions_line:
    line.unlink()


class sm_contribution(models.Model):
  _name = 'sm_contributions.sm_contribution'

  name = fields.Char(string=_("Name"), compute="compute_name")
  associated_member = fields.Many2one('res.partner', string=_("Member"), required=True)
  initial_import = fields.Float(string=_("Import"), required=True, digits=(16, 0))
  initial_import_txt = fields.Char(string=_("Import text"), required=True)

  contributions_quantity = fields.Float(string=_("Number of contributions"), digits=(16, 0),
    compute="compute_contributions_quantity")

  contract_number = fields.Integer(string=_("Contract number"))
  initial_day = fields.Date(string=_("Initial day"), required=True)
  expiration_day = fields.Date(string=_("Expiration day"), compute="compute_expiration_day")

  returned = fields.Float(string=_("Returned"), digits=(16, 0))

  contributions_line = fields.One2many('sm_contributions.sm_contribution_line',
    'associated_contribution', "Lines",
    compute="compute_contributions_lines", store=True)

  contribution_type = fields.Many2one('sm_contributions.sm_contribution_type', string=_("Type"), required=True)
  
  contribution_email_template_id = fields.Many2one('mail.template', string=_('Plantilla'),
    compute="compute_contribution_email_template")

  closed_day = fields.Date(string=_("Closed day"))
  contract_email_sent = fields.Boolean(string=_("Contract email sent"), default=False)

  upload_file = fields.Binary(string="Contract signed")
  file_name = fields.Char(string="File Name")

  @api.model
  def create(self, vals):
    vals['contract_number'] = self.get_new_id()
    result = super(sm_contribution, self).create(vals)
    return result

  def get_new_id(self):
    count = self.env['sm_contributions.sm_contribution'].search([],
      order="contract_number desc",limit=1).contract_number
    new_id = count + 1
    return new_id

  @api.constrains('closed_day')
  def compute_closing_day(self):
    for record in self:
      if record.closed_day:
        clean_contributions_line(record)
        record.returned = record.initial_import

  @api.depends('initial_day', 'contribution_type.duration')
  def compute_expiration_day(self):
    for record in self:
      if record.initial_day:
        type_months = record.contribution_type.duration
        initial_date = get_datetime_object_from_string(str(record.initial_day))
        record.expiration_day = str(initial_date + monthdelta(type_months) + dt.timedelta(days=1))

  @api.depends('initial_import')
  def compute_contributions_quantity(self):
    for record in self:
      record.contributions_quantity = record.initial_import / 100

  @api.multi
  def compute_name(self):
    for record in self:
      first_year = ''
      last_year = ''

      if record.initial_day:
        first_year = get_datetime_object_from_string(str(record.initial_day)).year
      if record.expiration_day:
        last_year = get_datetime_object_from_string(str(record.expiration_day)).year

      years = str(first_year) + "-" + str(last_year)

      record.name = str(record.contract_number) + "-" + record.associated_member.name + "-" + years


  @api.constrains('initial_day', 'expiration_day', 'closed_day')
  def compute_contributions_lines(self):
    for record in self:

      if record.initial_day:
        clean_contributions_line(record)
        initial_day = get_datetime_object_from_string(str(record.initial_day))

        if record.closed_day:
          final_day = get_datetime_object_from_string(str(record.closed_day))
        else:
          final_day = get_datetime_object_from_string(str(record.expiration_day))

        first_year = initial_day.year
        last_year = final_day.year
  
        diff_years = abs(last_year - first_year)

        total_year = diff_years + 1

        for index_year in range(0, total_year):
          current_year = first_year + index_year

          if current_year == first_year:
            first_day = initial_day
          else:
            first_day = get_first_day_of_a_year(current_year)

          if current_year == last_year:
            last_day = final_day
          else:
            last_day = get_last_day_of_a_year(current_year)

          self.create_contribution_line(first_day, last_day)
 
  @api.depends('contribution_type.template_id')
  def compute_contribution_email_template(self):
    for record in self:
      if record.contribution_type:
        record.contribution_email_template_id = record.contribution_type.template_id

  def create_contribution_line(self, initial_day, final_day):
    con_lin_mod = self.env['sm_contributions.sm_contribution_line']
    self.ensure_one()

    new_contribution_line = con_lin_mod.create({
      'associated_contribution': self.id,
      'initial_day': initial_day,
      'final_day': final_day
    })

    return new_contribution_line

  # Methods from actions

  @api.model
  def close_contribution_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        active_contributions = self.env['sm_contributions.sm_contribution'].browse(
          self.env.context['active_ids'])
        if active_contributions.exists():
          for contribution in active_contributions:
            clean_contributions_line(contribution)
            now = datetime.now()

            contribution.returned = contribution.initial_import
            contribution.expiration_day = now

  @api.model
  def select_closing_date(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        active_contributions = self.env['sm_contributions.sm_contribution'].browse(
          self.env.context['active_ids'])
        if active_contributions.exists():
          for contribution in active_contributions:
            view_id = self.env['sm_contributions.date_picker.wizard']
            new = view_id.create({
              'parent_model': contribution.id,
              'year': contribution.contributions_line,
            })

            return {
              'type': 'ir.actions.act_window',
              'name': 'Date picker',
              'res_model': 'sm_contributions.date_picker.wizard',
              'view_type': 'form',
              'view_mode': 'form',
              'res_id': new.id,
              'view_id': self.env.ref('sm_contributions.data_picker_wizard', False).id,
              'target': 'new',
            }

  @api.model
  def send_year_report_email_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        active_contributions = self.env['sm_contributions.sm_contribution'].browse(
          self.env.context['active_ids'])
        if active_contributions.exists():
          for contribution in active_contributions:
            view_id = self.env['sm_contributions.contribution_line_selectable.wizard']
            new = view_id.create({
              'parent_model': contribution.id,
            })

            return {
              'type': 'ir.actions.act_window',
              'name': 'Date picker',
              'res_model': 'sm_contributions.contribution_line_selectable.wizard',
              'view_type': 'form',
              'view_mode': 'form',
              'res_id': new.id,
              'view_id': self.env.ref('sm_contributions.contribution_line_selectable_wizard', False).id,
              'target': 'new',
            }

  def send_year_report_mail(self, record=None):
    if record is None:
      record = self

    company = record.env.user.company_id
    email_template = company.contribution_year_report_email_template_id
    if email_template.id:
      current_year = datetime.now().year
      for line in record.contributions_line:
        if int(line.year) == current_year:
          email_values = {'send_from_code': True}
          email_template.with_context(email_values).send_mail(line.id, True)
          line.year_report_sent = True
          break

  @api.model
  def send_contract_email_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        active_contributions = self.env['sm_contributions.sm_contribution'].browse(
          self.env.context['active_ids'])
        if active_contributions.exists():
          for contribution in active_contributions:
            contribution.send_contract_email()

  def send_contract_email(self):
    email_template = self.contribution_type.template_id
    if email_template.id and self.contract_email_sent == False:
      email_values = {'send_from_code': True}
      email_template.with_context(email_values).send_mail(self.id, True)
      self.write({
        'contract_email_sent': True
      })
