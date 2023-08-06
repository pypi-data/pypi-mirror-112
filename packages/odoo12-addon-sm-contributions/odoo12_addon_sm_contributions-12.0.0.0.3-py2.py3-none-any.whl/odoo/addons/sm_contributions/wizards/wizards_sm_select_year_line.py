# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _


def get_datetime_object_from_string(string_date):
  formatter_string = "%Y-%m-%d"
  return datetime.strptime(str(string_date), formatter_string)


class contribution_line_selectable(models.TransientModel):
  _name = 'sm_contributions.contribution_line_selectable.wizard'
  _inherit = ['mail.thread']

  parent_model = fields.Many2one('sm_contributions.sm_contribution', string=_("Current contribution"), readonly=True)
  year = fields.Many2one('sm_contributions.sm_contribution_line', string=_("Year report"))

  @api.multi
  def send_year_report_email(self):
    for record in self:
      if record.year:
        record.send_year_report_mail(record)

  def send_year_report_mail(self, record=None):
    if record is None:
      record = self

    company = record.env.user.company_id
    email_template = company.contribution_year_report_email_template_id
    
    if email_template.id:
      line_chose = record.year
      email_values = {'send_from_code': True}
      email_template.with_context(email_values).send_mail(line_chose.id, True)
      line_chose.year_report_sent = True
