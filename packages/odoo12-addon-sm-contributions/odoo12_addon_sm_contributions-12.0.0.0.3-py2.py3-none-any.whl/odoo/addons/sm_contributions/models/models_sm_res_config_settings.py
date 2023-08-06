# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  contribution_year_report_email_template_id = fields.Many2one(
    related='company_id.contribution_year_report_email_template_id',
    string=_("Contribution year report"),
    readonly=False)

  sm_contribution_account_id = fields.Many2one(
    related='company_id.sm_contribution_account_id',
    string=_("Compte d'aportació"),
    readonly=False)

  sm_contribution_tax_account_id = fields.Many2one(
    related='company_id.sm_contribution_tax_account_id',
    string=_("Compte d'interessos d'aportació"),
    readonly=False)
