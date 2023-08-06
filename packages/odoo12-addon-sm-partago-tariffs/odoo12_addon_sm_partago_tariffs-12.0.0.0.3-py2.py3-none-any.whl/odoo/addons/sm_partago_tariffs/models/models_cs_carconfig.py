# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class smp_car_config(models.Model):
  _inherit = 'sm_carsharing_structure.cs_carconfig'
  _name = 'sm_carsharing_structure.cs_carconfig'

  related_price_group_id = fields.Many2one('smp.sm_carconfig_price_group', string=_("Related price group"))
  initial_price = fields.Float(string=_("Initial price (sense IVA)"))