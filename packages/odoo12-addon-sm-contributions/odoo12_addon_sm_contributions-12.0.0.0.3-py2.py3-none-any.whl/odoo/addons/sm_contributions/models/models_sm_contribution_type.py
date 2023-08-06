# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_contribution_type(models.Model):
  _name = 'sm_contributions.sm_contribution_type'

  name = fields.Char(string=_("Name"))
  historical = fields.One2many(comodel_name='sm_contributions.sm_contribution_interest',
    inverse_name='type',string=_("Interests"))
  template_id = fields.Many2one('mail.template', string=_("Plantilla Email"))
  duration = fields.Integer(string=_("Duration (Month)"), default=1)
