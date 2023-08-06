# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _


def get_datetime_object_from_string(string_date):
  formatter_string = "%Y-%m-%d"
  return datetime.strptime(str(string_date), formatter_string)


class date_picker(models.TransientModel):
  _name = 'sm_contributions.date_picker.wizard'
  _inherit = ['mail.thread']

  date_chosen = fields.Date(string=_("Date to close"))
  parent_model = fields.Many2one('sm_contributions.sm_contribution', 'Parent')

  @api.multi
  def proceed(self):
    for record in self:
      if record.date_chosen:
        record.parent_model.closed_day = record.date_chosen

  @api.multi
  def send_year_report_email(self):
    for record in self:
      if record.date_chosen:
        record.send_year_report_mail(record)

  def send_year_report_mail(self, record=None):
    if record is None:
      record = self
    
    company = record.env.user.company_id
    email_template = company.contribution_year_report_email_template_id
    if email_template.id:
      for line in record.parent_model.contributions_line:
        line_year = int(line.year)
        formal_date = get_datetime_object_from_string(record.date_chosen)
        year_chose = formal_date.year
        if line_year == year_chose:
          email_values = {'send_from_code': True}
          email_template.with_context(email_values).send_mail(line.id, True)
          line.year_report_sent = True
          break
