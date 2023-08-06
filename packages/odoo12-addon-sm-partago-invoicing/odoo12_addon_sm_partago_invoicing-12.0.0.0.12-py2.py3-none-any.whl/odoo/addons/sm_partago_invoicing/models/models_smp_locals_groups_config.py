# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class smp_car_config_groups_locals(models.Model):
  _name = 'smp.smp_car_config_groups_locals'

  name = fields.Char(string=_("Local group"))
  car_configs_related = fields.Many2many('smp.sm_car_config', string=_("Related car configs"))
