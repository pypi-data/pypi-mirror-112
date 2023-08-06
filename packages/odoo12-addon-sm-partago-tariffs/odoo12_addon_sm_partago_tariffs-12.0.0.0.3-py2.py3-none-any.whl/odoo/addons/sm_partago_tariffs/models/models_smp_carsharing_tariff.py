  # -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_load_data import load_data
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources


class smp_carsharing_tariff(models.Model):
  _name = 'smp.sm_carsharing_tariff'
  
  tariffs_durations_assigned = load_data.get_instance().tariffs_duration()
  name = fields.Char(string=_("Name"))
  reason = fields.Char(string=_("Reason"))
  date = fields.Date(string=_("Date"), required="True")
  date_active = fields.Date(string=_("Start Date"), required="True")
  date_valid = fields.Date(string=_("Valid until"))
  tariff_model_id = fields.Many2one('smp.sm_carsharing_tariff_model', string=_("Related tariff model"))
  extra_tariff_model_id = fields.Many2one('smp.sm_carsharing_tariff_model',
    string=_("Extra  time related tariff model"))
  time_restricted = fields.Boolean(string=_("Has time restrictions?"))
  related_member_id = fields.Many2one('res.partner', string=_("Related member"))
  related_carconfig_id = fields.Many2one('smp.sm_car_config', string=_("Related CarConfig"))
  carconfig_availability = fields.Char(string=_("CarConfig availability"))
  pocketbook = fields.Float(string=_("Pocketbook"))
  closed = fields.Boolean(string=_("Closed"))
  tariff_history_ids = fields.One2many(comodel_name='smp.sm_carsharing_tariff_history',
    inverse_name='related_tariff_id', string=_("Tariff history"))
  description = fields.Html(string=_("Description"))
  abouttoexpire = fields.Boolean(string=_("about to expire"), compute="_check_if_abouttoexpire",
    store=False)
  abouttoexpire_member_notified = fields.Boolean(string=_("About to expire member notified"))
  tariff_type = fields.Selection([
    ('pocketbook', 'PocketBook'),
    ('time_frame', 'Time Frame'),
    ('rel_car', 'Related car')],
    string=_('Type'), required="True")
  
  pocketbook_threshold = fields.Float(string=_("Pocketbook threshold"))
  
  pocketbook_initial = fields.Integer(string=_("Initial Pocketbook"))
  
  _order = "date_active asc"

  @api.multi
  def recompute_pb_tariff(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        tariffs = self.env['smp.sm_carsharing_tariff'].browse(self.env.context['active_ids'])
        if tariffs.exists():
          for tariff in tariffs:
            if tariff.tariff_type == 'pocketbook':
              for t_history in tariff.tariff_history_ids:
                if abs(t_history.amount) < t_history.related_invoice_line_id.price_total and t_history.amount<0:
                  remove_from_th = t_history.related_invoice_line_id.price_total + t_history.amount
                  tariff.write({
                    'pocketbook': tariff.pocketbook - remove_from_th
                  })
                  t_history.write({
                    'amount': -1*t_history.related_invoice_line_id.price_total
                  })
              tariff.related_member_id.sanitize_tariffs()

    return sm_resources.getInstance().get_successful_action_message(self,
      _('Tariff pb recomputed done successfully'),self._name)

  @api.multi
  def mark_as_notified(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        tariffs = self.env['smp.sm_carsharing_tariff'].browse(self.env.context['active_ids'])
        if tariffs.exists():
          for tariff in tariffs:
            tariff.write({'abouttoexpire_member_notified': True})
    return sm_resources.getInstance().get_successful_action_message(self,
      _('Mark as notified done successfully'), self._name)

  @api.depends('tariff_type', 'pocketbook', 'date_valid')
  def _check_if_abouttoexpire(self):
    for record in self:
      abouttoexpire = False
      if record.tariff_type == 'pocketbook':
        company = self.env.user.company_id
        if record.pocketbook_threshold > 0:
          if record.pocketbook <= record.pocketbook_initial * (record.pocketbook_threshold / 100):
            abouttoexpire = True
        else:
          if record.pocketbook <= record.pocketbook_initial * (company.pocketbook_threshold / 100):
            abouttoexpire = True

      if record.tariff_type == 'time_frame':
        if record.date_valid:
          date_valid = datetime.strptime(
            str(record.date_valid), "%Y-%m-%d").date()
          now = datetime.now().date()
          if date_valid >= now:
            if (date_valid - now).days <= 35:
              abouttoexpire = True

      record.abouttoexpire = abouttoexpire

  @api.multi
  def search_descriptions(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        tariffs = self.env['smp.sm_carsharing_tariff'].browse(self.env.context['active_ids'])
        if tariffs.exists():
          for tariff in tariffs:
            tariff_type = tariff.tariff_model_id.name
            model_tariff_description = tariff.tariff_model_id.description
            if model_tariff_description:
              company = self.env.user.company_id

              if tariff_type == company.default_welcome:

                date_valid = tariff.date_valid
                if not date_valid:
                  date_valid = self.calculateDateValid()

                new_description = model_tariff_description + " " + date_valid + "</p>"

                tariff.write({'description': new_description})
              else:
                date_valid = self.calculateDateValid()
                tariff.write({'description': tariff.tariff_model_id.description,
                        'date_valid': date_valid})

    return sm_resources.getInstance().get_successful_action_message(self,
      _('Search description done successfully'), self._name)

  @api.constrains('tariff_model_id')
  def go_for_tariff_model_description(self):
    self.write({'description': self.tariff_model_id.description})

  def calculateDateValid(self):
    tariffs_duration = self.tariffs_durations_assigned
    if self.tariff_model_id.id == self.env.user.company_id.welcome_tariff_model_id.id:
      if 'welcome' in tariffs_duration:
        duration = tariffs_duration['welcome']
        if self.date_active:
          return datetime.strptime(str(self.date_active), "%Y-%m-%d") + timedelta(duration * 365 / 12)
    return False

  def check_if_primary_tariff(self):
    current_member = self.related_member_id
    if current_member:
      primary_tariff = current_member.get_current_tariff(False)
      if self.id == primary_tariff['tariff_id']:
        return True
    return False
