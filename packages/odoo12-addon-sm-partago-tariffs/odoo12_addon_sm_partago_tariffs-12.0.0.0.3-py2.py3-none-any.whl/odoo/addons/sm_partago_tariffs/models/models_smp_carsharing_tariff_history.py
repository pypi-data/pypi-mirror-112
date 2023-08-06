# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools.translate import _


class smp_carsharing_tariff(models.Model):
  _name = 'smp.sm_carsharing_tariff_history'

  name = fields.Char(string=_("Name"), required=True)
  date = fields.Date(string=_("Date"))
  amount = fields.Float(string=_("Amount"))
  obs = fields.Char(string=_("Observations"))
  related_invoice_line_id = fields.Many2one('account.invoice.line', string=_("Related Invoice Line"))
  related_tariff_id = fields.Many2one('smp.sm_carsharing_tariff', string=_("Related Tariff"))

  _order = "date desc"
