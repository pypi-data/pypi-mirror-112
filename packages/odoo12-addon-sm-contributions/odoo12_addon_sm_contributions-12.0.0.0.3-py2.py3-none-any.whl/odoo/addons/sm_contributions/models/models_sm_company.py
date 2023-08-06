# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
  _inherit = 'res.company'

  sm_contribution_account_id = fields.Many2one('account.account',
    string=_("Compte d'aportació"))

  contribution_year_report_email_template_id = fields.Many2one('mail.template',
    string=_("Contribution year report"))

  sm_contribution_tax_account_id = fields.Many2one('account.account',
    string=_("Compte d'interessos d'aportació"))