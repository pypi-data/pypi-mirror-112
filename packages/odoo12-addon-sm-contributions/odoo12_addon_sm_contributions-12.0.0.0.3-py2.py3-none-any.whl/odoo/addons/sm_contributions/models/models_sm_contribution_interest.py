# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_contribution_interest(models.Model):
  _name = 'sm_contributions.sm_contribution_interest'

  name = fields.Char(string=_("Name"), compute="compute_name")
  year = fields.Integer(string=_("Year"))
  interest = fields.Float(string=_("Interest"))
  iva = fields.Float(string=_("IVA"))
  type = fields.Many2one('sm_contributions.sm_contribution_type', string=_("Type"))

  _order = "year desc"

  @api.depends('year', 'type.name')
  def compute_name(self):
    for record in self:
      if record.type.name and record.year:
        record.name = record.type.name + "-" + str(record.year)
