# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class smp_reservation_compute(models.Model):
  _inherit = 'smp.sm_reservation_compute'
  _name = 'smp.sm_reservation_compute'

  applied_tariff_id = fields.Many2one('smp.sm_carsharing_tariff', string=_("Applied tariff"))
