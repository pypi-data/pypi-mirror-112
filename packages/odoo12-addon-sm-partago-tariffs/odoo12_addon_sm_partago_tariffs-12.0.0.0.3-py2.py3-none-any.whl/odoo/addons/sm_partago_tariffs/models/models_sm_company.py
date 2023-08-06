# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
  _inherit = 'res.company'

  default_tariff_model_id = fields.Many2one('smp.sm_carsharing_tariff_model',
    string=_("Default tariff model"))
  welcome_tariff_model_id = fields.Many2one('smp.sm_carsharing_tariff_model',
    string=_("Welcome tariff model"))
  pocketbook_threshold = fields.Float(string=_("Pocketbook threshold for tariffs"))
  default_welcome = fields.Text(string=_("Default name for welcome tariffs"))
  notification_tariff_creation_id = fields.Many2one('mail.template',
    string=_("Notification tariff creation template"))
  abouttoexpire_mail_template_id = fields.Many2one('mail.template',
    string=_("About to expire tariffs notification template"))

sm_company()
