# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools.translate import _


class smp_carconfig_price_group(models.Model):
  _name = 'smp.sm_carconfig_price_group'

  name = fields.Char(string=_("Name"))
  applied_carconfigs_id = fields.One2many(comodel_name='sm_carsharing_structure.cs_carconfig',
  inverse_name='related_price_group_id',string=_("Applied carconfigs"))

  _order = "name desc"
