# -*- coding: utf-8 -*-
from odoo import api,models, fields
from odoo.tools.translate import _


class smp_tariffmodel_price_group(models.Model):
  _name = 'smp.sm_tariffmodel_price_group'

  name = fields.Char(string=_("Name"),compute="_get_price_group_name")
  rel_tariff_model_id = fields.Many2one('smp.sm_carsharing_tariff_model', string=_("Rel. Tariff Model"))
  applied_carconfig_price_group_id = fields.Many2one('smp.sm_carconfig_price_group',
    string=_("Applied. Carconfig Price Group"))
  cs_mins_product_id = fields.Many2one('product.product', string=_("Mins product"))
  cs_days_product_id = fields.Many2one('product.product', string=_("Days product"))
  cs_mileage_product_id = fields.Many2one('product.product', string=_("Mileage product"))

  _order = "name desc"

  @api.depends('rel_tariff_model_id')
  def _get_price_group_name(self):
    for record in self:
      record.name = ''
      if record.applied_carconfig_price_group_id:
        record.name = record.applied_carconfig_price_group_id.name
