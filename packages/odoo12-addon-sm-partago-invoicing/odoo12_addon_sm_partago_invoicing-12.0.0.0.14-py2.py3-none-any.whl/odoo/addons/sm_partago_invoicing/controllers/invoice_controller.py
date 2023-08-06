# -*- coding: utf-8 -*-

from odoo.addons.base_rest.controllers import main
from odoo.http import route
from odoo.addons.sm_rest_api.models.models import validate_request


class PartnerRestPublicApiController(main.RestController):
  _root_path = '/invoice/public/'
  _collection_name = 'invoice.rest.public.services'
  _default_auth = 'public'

  @route([
    _root_path + '<string:_service_name>/test/<int:_id>'
  ], methods=['GET'], auth="public", csrf=False)
  def test(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'test', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/invoices/'
  ], methods=['GET'], auth="public", csrf=False)
  def get_invoices(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'get_invoices', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/invoice/<int:_id>'
  ], methods=['GET'], auth="public", csrf=False)
  def get_invoice(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'get_invoice', _id, params)
