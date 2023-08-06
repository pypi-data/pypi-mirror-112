# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime

from werkzeug import urls

from odoo import api, fields, models, tools, _


class ResConfigSettings(models.TransientModel):
  _name = 'res.config.settings'
  _inherit = 'res.config.settings'

  tariff_default_model_id = fields.Many2one(
    related='company_id.default_tariff_model_id',
    string=_("Default tariff model (predefined)"), 
    readonly=False)

  welcome_tariff_model_id = fields.Many2one(
    related='company_id.welcome_tariff_model_id',
    string=_("Default welcome tariff model (predefined)"), 
    readonly=False)
   
  pocketbook_threshold = fields.Float(
    related='company_id.pocketbook_threshold',
    string=_("Pocketbook threshold for tariffs"), 
    readonly=False)

  welcome_default = fields.Text(
    related='company_id.default_welcome',
    string=_("Default name for welcome tariffs"), 
    readonly=False)

  notification_tariff_creation_id = fields.Many2one(
    related='company_id.notification_tariff_creation_id',
    string=_("Notification tariff creation template"),
    readonly=False)

  abouttoexpire_mail_template_id = fields.Many2one(
    related='company_id.abouttoexpire_mail_template_id',
    string=_("About to expire tariffs notification template"),
    readonly=False)
    