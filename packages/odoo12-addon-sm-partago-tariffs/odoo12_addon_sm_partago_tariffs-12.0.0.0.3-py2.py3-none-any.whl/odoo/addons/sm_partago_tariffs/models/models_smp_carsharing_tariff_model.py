# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools.translate import _


class smp_carsharing_tariff_model(models.Model):
  _name = 'smp.sm_carsharing_tariff_model'

  name = fields.Char(string=_("Name"))
  description = fields.Char(string=_("Description"))
  cs_mins_product_id = fields.Many2one('product.product', string=_("Mins product"))
  cs_days_product_id = fields.Many2one('product.product', string=_("Days product"))
  cs_mileage_product_id = fields.Many2one('product.product', string=_("Mileage product"))
  price_groups_id = fields.One2many(comodel_name='smp.sm_tariffmodel_price_group',
    inverse_name='rel_tariff_model_id', string=_("Price Groups"))
  rel_tariffs_id = fields.One2many(comodel_name='smp.sm_carsharing_tariff',
    inverse_name='tariff_model_id', string=_("Related tariffs"))

  _order = "name desc"

  def get_prices(self,cs_carconfig=False):
    if cs_carconfig:
      for pg in self.price_groups_id:
        if pg.applied_carconfig_price_group_id.id == cs_carconfig.related_price_group_id.id:
          return {
            'day_price': pg.cs_days_product_id,
            'min_price': pg.cs_mins_product_id,
            'kms_price': pg.cs_mileage_product_id
          }
    return {
      'day_price': self.cs_days_product_id,
      'min_price': self.cs_mins_product_id,
      'kms_price': self.cs_mileage_product_id
    }
