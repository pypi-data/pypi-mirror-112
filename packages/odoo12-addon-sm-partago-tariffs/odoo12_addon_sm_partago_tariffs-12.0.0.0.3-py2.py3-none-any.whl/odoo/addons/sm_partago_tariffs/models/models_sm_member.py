# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

class sm_member(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  cs_tariffs_id = fields.One2many(comodel_name='smp.sm_carsharing_tariff',
    inverse_name='related_member_id', string='Tariffs')
  default_tariff_model_id = fields.Many2one('smp.sm_carsharing_tariff_model', string=_("Default tariff model"))
  has_active_tariffs = fields.Boolean(compute="_has_active_tariffs",store=False)
  has_active_notabouttoexpire_tariffs = fields.Boolean(compute="_has_active_notabouttoexpire_tariffs",store=False)

  @api.depends('cs_tariffs_id')
  def _has_active_tariffs(self):
    for record in self:
      record.has_active_tariffs = False
      for tariff in record.cs_tariffs_id:
        if tariff.closed == False:
          record.has_active_tariffs = True
          break

  @api.depends('cs_tariffs_id')
  def _has_active_notabouttoexpire_tariffs(self):
    for record in self:
      record.has_active_notclosetoexpire_tariffs = False
      for tariff in record.cs_tariffs_id:
        if tariff.closed == False and tariff.abouttoexpire == False:
          record.has_active_notclosetoexpire_tariffs = True
          break

  def setup_cs_default_tariff(self):
    company = self.env.user.company_id
    if not self.default_tariff_model_id:
      self.write({
        'default_tariff_model_id': company.default_tariff_model_id.id
      })
    return True

  def validate_cs_default_tariff_registration(self):
    if not self.default_tariff_model_id.id:
      return False
    return True

  def update_member_tariff_by_invoice_line(self, invoice_line, compute_pb):
    carconfig_id = invoice_line.related_reservation_compute_id.carconfig_id
    if self.has_special_tariff(carconfig_id):
      tariff = self.get_special_tariff(carconfig_id)
      if tariff.tariff_type == 'pocketbook' and compute_pb == True:
        resting_money = tariff.pocketbook - invoice_line.price_total
        # update pocketbook tariff
        if resting_money > 0:
          tariff.write({'pocketbook': resting_money})
        else:
          tariff.write({'pocketbook': 0, 'closed': True})
        # create tariff history entry
        self.env['smp.sm_carsharing_tariff_history'].create({
          'name': invoice_line.name,
          'date': time.strftime("%Y-%m-%d"),
          'amount': -1 * invoice_line.price_total,
          'obs': 'REPORT: ' + str(invoice_line.invoice_report_id.name),
          'related_invoice_line_id': invoice_line.id,
          'related_tariff_id': tariff.id
        })
        invoice_line.write({'related_tariff_id': tariff.id})

  def sanitize_tariffs(self):
    if self.cs_tariffs_id.exists():
      for tariff in self.cs_tariffs_id:
        close_tariff = False
        if tariff.tariff_type == 'pocketbook':
          if tariff.pocketbook <= 0:
            close_tariff = True
        if tariff.tariff_type == 'time_frame':
          now = datetime.now()
          if tariff.date_valid:
            date_valid = datetime.strptime(str(tariff.date_valid) + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
            if date_valid < now:
              close_tariff = True
        if close_tariff:
          tariff.write({
            'closed': True
          })
    return True

  def get_special_tariff(self, rel_carconfig_id=False):
    if rel_carconfig_id:
      tariffs = self.env['smp.sm_carsharing_tariff'].sudo().search(
        [('closed', '=', False), ('related_member_id', '=', self.id),
         ('related_carconfig_id', '=', rel_carconfig_id.id)])
      if tariffs.exists():
        if tariffs[0].id:
          return tariffs[0]
      # if rel_carconfig_id.rel_tariff_model_id.id:
      #     return {'tariff_model': rel_carconfig_id.rel_tariff_model_id}

    tariffs = self.env['smp.sm_carsharing_tariff'].sudo().search(
      [('closed', '=', False), ('related_member_id', '=', self.id), ('tariff_type', '!=', 'rel_car')])
    if tariffs.exists():
      if tariffs[0].id:
        return tariffs[0]
    return False

  def create_welcome_tariff_if_mising(self):
    company = self.env.user.company_id
    welcome_tariff = company.welcome_tariff_model_id
    if not welcome_tariff:
      return

    e_tariffs = self.env['smp.sm_carsharing_tariff'].search([
      ('related_member_id', '=', self.id)
    ])
    if e_tariffs.exists():
      e_active = datetime.strptime(str(e_tariffs[0].date_active), "%Y-%m-%d") + timedelta(-1)
    else:
      e_active = datetime.now()
    query = [
      ('name', '=', company.default_welcome),
      ('related_member_id', '=', self.id)
    ]
    
    date_valid = e_active + timedelta(3 * 365 / 12) + timedelta(7)
    creation_data = {
      'name': company.default_welcome,
      'date': e_active.isoformat(),
      'date_active': e_active.isoformat(),
      'date_valid': date_valid.isoformat(),
      'tariff_model_id': welcome_tariff.id,
      'related_member_id': self.id,
      'tariff_type': 'time_frame',
      'description': "<p>4€/hora 40€/dia<br/>Tarifa vàlida fins al " + date_valid.strftime(
        "%d/%m/%Y") + "</p>"
    }
    member_welcome_tariff = sm_utils.get_create_existing_model(
      self.env['smp.sm_carsharing_tariff'], query, creation_data)

  def get_default_tariff(self):
    return {
      # 'tariff_model_type': 'tariff',
      'tariff_model_id': self.default_tariff_model_id,
      'tariff_name': self.default_tariff_model_id.name,
      'tariff_type': 'default',
      'tariff_id': 0,
      'tariff_aval': False
    }

  def get_current_tariff(self, rel_carconfig_id=False):
    self.setup_cs_default_tariff()
    self.create_welcome_tariff_if_mising()
    special_tariff = self.get_special_tariff(rel_carconfig_id)
    tariff_aval = False
    extra_tariff_model_id = False
    if not special_tariff:
      return self.get_default_tariff()

    if special_tariff.time_restricted:
      tariff_aval = special_tariff.carconfig_availability
      extra_tariff_model_id = special_tariff.extra_tariff_model_id
    return {
      'tariff_model_id': special_tariff.tariff_model_id,
      'extra_tariff_model_id': extra_tariff_model_id,
      'tariff_name': special_tariff.name,
      'tariff_type': special_tariff.tariff_type,
      'tariff_id': special_tariff.id,
      'tariff_aval': tariff_aval
      }

  def create_carsharing_tariff(self, company_tariff, days_to_subtract, tariff_valid_months, date):
    if date == "Today":
      date = datetime.today() - timedelta(days=days_to_subtract)  # Subtract one day
    else:
      date = datetime.strptime(str(date), "%Y/%m/%d") - timedelta(days=days_to_subtract)

    date_valid = date + timedelta(tariff_valid_months * 365 / 12)  # Add 3 months

    date = date.strftime("%Y/%m/%d")
    date_valid = date_valid.strftime("%Y/%m/%d")

    self.env['smp.sm_carsharing_tariff'].create({
      'name': company_tariff.name,
      'date': date,
      'date_active': date,
      'date_valid': date_valid,
      'tariff_model_id': company_tariff.id
    })

  def tariff_already_defined(self, tariff_to_check, tariff_list):
    for tariff in tariff_list:
      if tariff.tariff_model_id == tariff_to_check:
        return True

  def has_special_tariff(self, rel_carconfig_id=False):
    special_tariff = self.get_special_tariff(rel_carconfig_id)
    if not special_tariff:
      return False
    return True
    
  @api.model
  def get_send_email_tariff_wizard_view(self):
    view_ref = self.env['ir.ui.view'].sudo().search(
      [('name', '=', 'sm_partago_tariffs.carsharing_send_email_tariff.wizard.form')])
    return view_ref.id

  @api.model
  def get_send_email_tariff_view(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            data = {'current_member_id': member.id}
            return {
              'type': 'ir.actions.act_window',
              'name': "Create tariff",
              'res_model': 'sm_carsharing_send_email_tariff.wizard',
              'view_type': 'form',
              'view_mode': 'form',
              'res_id': self.env['sm_carsharing_send_email_tariff.wizard'].create(data).id,
              'view_id': self.get_send_email_tariff_wizard_view(),
              'target': 'new',
            }

sm_member()
