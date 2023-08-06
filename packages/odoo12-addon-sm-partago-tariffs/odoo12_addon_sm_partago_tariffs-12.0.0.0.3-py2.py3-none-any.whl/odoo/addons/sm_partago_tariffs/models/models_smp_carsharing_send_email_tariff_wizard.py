# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_connect.models.models_sm_carsharing_db_utils import sm_carsharing_db_utils


class sm_carsharing_send_email_tariff_wizard(models.TransientModel):
  _name = "sm_carsharing_send_email_tariff.wizard"

  name = fields.Char(string=_("Name"))
  reason = fields.Char(string=_("Reason"))
  current_member_id = fields.Many2one(
    'res.partner', string=_('Member'))  # ocult

  tariff_model_id = fields.Many2one(
    'smp.sm_carsharing_tariff_model', string=_("Related tariff model"))

  tariff_type = fields.Selection([
    ('pocketbook', 'PocketBook'),
    ('time_frame', 'Time Frame'),
    ('rel_car', 'Related car')],
    string=_('Type'))

  date = fields.Date(string=_("Date"))
  date_active = fields.Date(string=_("Start Date"))

  pocketbook_initial = fields.Integer(string=_("Initial Pocketbook"))
  pocketbook_threshold = fields.Float(string=_("Pocketbook threshold"))
  pocketbook = fields.Float(string=_("Pocketbook"))

  date_valid = fields.Date(string=_("Valid until"))

  time_restricted = fields.Boolean(string=_("Has time restrictions?"))
  related_carconfig_id = fields.Many2one(
    'smp.sm_car_config', string=_("Related CarConfig"))

  carconfig_availability = fields.Char(string=_("CarConfig availability"))
  extra_tariff_model_id = fields.Many2one(
    'smp.sm_carsharing_tariff_model', string=_("Extra time related tariff model"))

  description = fields.Html(string=_("Description"))

  notify = fields.Boolean(string=_("Send notification?"), default=True)

  @api.multi
  def send_email_tariff(self):
    self.create_tariff()
    return True

  @api.multi
  def create_tariff(self):
    record = self.env['smp.sm_carsharing_tariff'].create({
      'name': self.name,
      'reason': self.reason,
      'related_member_id': self.current_member_id.id,
      'tariff_model_id': self.tariff_model_id.id,
      'tariff_type': self.tariff_type,
      'date': self.date,
      'date_active': self.date_active,
      'pocketbook_initial': self.pocketbook_initial,
      'pocketbook_threshold': self.pocketbook_threshold,
      'pocketbook': self.pocketbook,
      'date_valid': self.date_valid,
      'time_restricted': self.time_restricted,
      'related_carconfig_id': self.related_carconfig_id.id,
      'carconfig_availability': self.carconfig_availability,
      'extra_tariff_model_id': self.extra_tariff_model_id.id,
      'description': self.description
    })
    if self.notify:
      sm_utils.send_email_from_template(
        record, 'notification_tariff_creation_id')

    return True
