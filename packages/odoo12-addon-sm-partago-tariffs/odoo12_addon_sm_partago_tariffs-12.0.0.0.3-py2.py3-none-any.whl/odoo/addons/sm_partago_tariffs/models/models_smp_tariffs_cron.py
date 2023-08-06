from odoo import models, fields, api
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

class smp_tariffs_cron(models.Model):
  _name = 'sm_partago_tariffs.smp_tariffs_cron'

  @api.model
  def maintenance_welcome_tariffs(self):
    company = self.env.user.company_id
    tariffs = self.env['smp.sm_carsharing_tariff'].search([(
      'name', '=', company.default_welcome
    )])
    if tariffs.exists():
      for tariff in tariffs:
        if not tariff.tariff_model_id.id:
          company = self.env.user.company_id
          welcome_tariff_model = company.welcome_tariff_model_id
          tariff.write({
            'tariff_model_id': welcome_tariff_model.id
          })

  @api.model
  def notify_members_abouttoexpire_tariffs(self):
    members = self.env['res.partner'].search([
      ('cooperator_register_number', '>', 0)
    ])
    if members.exists():
      for member in members:
        if member.cs_tariffs_id.exists():
          if member.has_active_notabouttoexpire_tariffs is False:
            for tariff in member.cs_tariffs_id:
              if (tariff.abouttoexpire
                and not tariff.closed 
                and not tariff.abouttoexpire_member_notified 
                and tariff.check_if_primary_tariff()):
                sm_utils.send_email_from_template(
                  tariff, 'abouttoexpire_mail_template_id')
                tariff.write(
                  {'abouttoexpire_member_notified': True})