# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.tools.translate import _

from odoo.addons.sm_partago_invoicing.models.batch_type_enum import BatchType


def clean_maintenance_users_reservation(initial_list):
  return initial_list.filtered(lambda r: r.member_id.cs_user_type != 'maintenance')


def clean_promo_users_reservation(initial_list):
  return initial_list.filtered(lambda r: r.member_id.cs_user_type != 'promo')


def clean_maintenance_users_teletacs(initial_list):
  return initial_list.filtered(lambda r: r.reservation_compute_id.member_id.cs_user_type != 'maintenance')


def clean_promo_users_teletacs(initial_list):
  return initial_list.filtered(lambda r: r.reservation_compute_id.member_id.cs_user_type != 'promo')


class sm_batch_reservation_compute_wizard(models.TransientModel):
  _name = "sm_partago_invoicing.sm_batch_reservation_compute.wizard"

  description = fields.Char(string=_('Description'))

  compute_reservations = fields.Boolean(string=_("Compute reservations"))
  compute_teletacs = fields.Boolean(string=_("Compute teletacs"))

  batch_type = fields.Selection([
    (str(BatchType.USAGES.value), 'Reservations'),
    (str(BatchType.TELETAC.value), 'Teletacs'),
  ], string=_("Batch type"), store=True)

  reservations = fields.Many2many(
    'smp.sm_reservation_compute',
    relation="smp_reservation_wizard_relation",
    # column1="wizard_id",
    # column2="reservation_id",
    string=_("Reservations"),
    ondelete='cascade'
  )

  teletacs = fields.Many2many(
    'smp.sm_teletac',
    relation="smp_teletacs_wizard_relation",
    # column1="wizard_id",
    # column2="teletac_id",
    string=_("Teletacs"),
    ondelete='cascade'
  )

  @api.multi
  def create_batch(self):
    self.create_batch_compute()

  @api.model
  def create_batch_compute(self):

    if self.compute_reservations:
      list_to_process = self.discard_invalid_reservations()
      self.create_reservation_batch_for_companies(list_to_process)
      self.create_reservation_gl_batch(list_to_process)

    if self.compute_teletacs:
      list_to_process = self.discard_invalid_teletacs()
      self.create_teletac_batch_for_companies(list_to_process)
      self.create_teletac_gl_batch(list_to_process)

  def discard_invalid_reservations(self):
    final_list = clean_maintenance_users_reservation(self.reservations)
    final_list = clean_promo_users_reservation(final_list)

    return final_list

  def discard_invalid_teletacs(self):
    final_list = clean_maintenance_users_teletacs(self.teletacs)

    return final_list

  def create_teletac_gl_batch(self, list_to_process):
    individual_usages = list_to_process.filtered(
      lambda t: t.reservation_compute_id.related_company_object.id is False and 
      t.related_member_id.parent_id.id is False and t.related_member_id.is_company is False)
    local_groups_configs_list = self.env['smp.smp_car_config_groups_locals'].search([])

    self.create_teletacs_batch_for_users_with_different_local_groups(batch_list=individual_usages,
      local_group_list=local_groups_configs_list)

    for local_group in local_groups_configs_list:
      teletac_usages = individual_usages.filtered(
        lambda t: t.reservation_compute_id.carconfig_id in local_group.car_configs_related)

      if len(teletac_usages) > 0:
        self.process_teletacs(batch_to_process=teletac_usages, local_group=local_group.name)

  def create_teletac_batch_for_companies(self, list_to_process):
    company_usages = list_to_process.filtered(
      lambda t: t.reservation_compute_id.related_company_object.id is not False or 
      t.related_member_id.parent_id or t.related_member_id.is_company)

    companies = {}

    for teletac_usage in company_usages:
      company = teletac_usage.reservation_compute_id.related_company_object

      if not company:
        company = teletac_usage.related_member_id.parent_id

      if company.paymaster.id is not False:
        company = company.paymaster

      company_batches = companies.get(company)

      if company_batches is None:
        companies[company] = []

      companies.get(company).append(teletac_usage)

    for company, company_teletacs in companies.items():
      self.process_teletacs(batch_to_process=company_teletacs, company=company)

  def create_reservation_gl_batch(self, list_to_process):
    individual_usages = list_to_process.filtered(
      lambda r: r.related_company_object.id is False and r.member_id.parent_id.id is False and 
      r.member_id.is_company is False)
    local_groups_configs_list = self.env['smp.smp_car_config_groups_locals'].search([])

    self.create_batch_for_users_with_different_local_groups(batch_list=individual_usages,
      local_group_list=local_groups_configs_list)

    for local_group in local_groups_configs_list:
      car_usages = individual_usages.filtered(lambda r: r.carconfig_id in local_group.car_configs_related)

      if len(car_usages) > 0:
        self.process_reservations(batch_to_process=car_usages, local_group=local_group.name)

  def create_batch_for_users_with_different_local_groups(self, batch_list, local_group_list):
    members = batch_list.mapped('member_id')

    for member in members:
      member_usages = batch_list.filtered(lambda r: r.member_id in member)
      if len(member_usages) > 1:
        used_car_configs = member_usages.mapped('carconfig_id')

        if len(used_car_configs) > 1:
          locals_groups = []

          for local_group in local_group_list:
            local_group_car_configs = local_group.car_configs_related

            car_confis_used_per_zone = local_group_car_configs.filtered(
              lambda car_config: car_config in used_car_configs)

            if len(car_confis_used_per_zone) > 0:
              locals_groups.append(local_group)

          if len(locals_groups) > 1:
            local_group_name_computed = ""
            for lg in locals_groups:
              local_group_name_computed += lg.name + "/"
            local_group_name_computed = local_group_name_computed[:-1]

            self.process_reservations(batch_to_process=member_usages, local_group=local_group_name_computed)

  def create_teletacs_batch_for_users_with_different_local_groups(self, batch_list, local_group_list):
    members = batch_list.mapped('related_member_id')

    for member in members:
      member_usages = batch_list.filtered(lambda r: r.related_member_id in member)
      if len(member_usages) > 1:
        used_car_configs = member_usages.mapped('reservation_compute_id.carconfig_id')

        if len(used_car_configs) > 1:
          locals_groups = []

          for local_group in local_group_list:
            local_group_car_configs = local_group.car_configs_related

            car_confis_used_per_zone = local_group_car_configs.filtered(
              lambda car_config: car_config in used_car_configs)

            if len(car_confis_used_per_zone) > 0:
              locals_groups.append(local_group)

          if len(locals_groups) > 1:
            local_group_name_computed = ""
            for lg in locals_groups:
              local_group_name_computed += lg.name + "/"
            local_group_name_computed = local_group_name_computed[:-1]

            self.process_teletacs(batch_to_process=member_usages, local_group=local_group_name_computed)

  def create_reservation_batch_for_companies(self, list_to_process):
    company_usages = list_to_process.filtered(
      lambda r: r.related_company_object.id is not False or r.member_id.parent_id or r.member_id.is_company)

    companies = {}

    for reservation in company_usages:
      company = reservation.related_company_object  # Looks for reservation compute related company

      if not company:
        company = reservation.member_id.parent_id  # Looks for reservation member parent

        if not company and reservation.member_id.is_company:  # Looks if the reservation member is a company
          company = reservation.member_id

      if company.paymaster.id is not False:
        company = company.paymaster

      company_batches = companies.get(company)

      if company_batches is None:
        companies[company] = []

      companies.get(company).append(reservation)

    for company, company_reservations in companies.items():
      self.process_reservations(company=company, batch_to_process=company_reservations)

  @api.model
  def process_teletacs(self, batch_to_process, local_group=None, company=False):

    batch = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_batch_reservation_compute'],
      query=[('name', '=', datetime.now())], creation_data={'name': datetime.now(),
      'batch_type': BatchType.TELETAC.value})

    for teletac in batch_to_process:
      member = teletac.reservation_compute_id.member_id
      report_name = batch.name + '-' + member.name

      report = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_report_reservation_compute'],
        query=[('name', '=', report_name)],creation_data={
        'name': report_name,'report_type': BatchType.TELETAC.value,'member_id': member.id,
        'batch_reservation_compute_id': batch.id})

      teletac.write({
        'report_reservation_compute_id': report.id,
        'reservation_compute_invoiced': True
      })

    batch.description = self.compute_batch_description(batch_to_process=batch_to_process,
      local_group=local_group,company=company,batch_type=BatchType.TELETAC.value)

    return True

  @api.model
  def process_reservations(self, batch_to_process, local_group=None, company=False):

    batch = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_batch_reservation_compute'],
      query=[('name', '=', datetime.now())],creation_data={
      'name': datetime.now(),'batch_type': BatchType.USAGES.value})

    for compute in batch_to_process:
      if not compute.compute_invoiced and not compute.compute_forgiven:
        report_name = batch.name + '-' + compute.member_id.name
        report = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_report_reservation_compute'],
          query=[('name', '=', report_name)],creation_data={
          'name': report_name,'member_id': compute.member_id.id,
          'report_type': BatchType.USAGES.value,'batch_reservation_compute_id': batch.id})

        compute.write({
          'report_reservation_compute_id': report.id,
          'compute_invoiced': True
        })

    batch.description = self.compute_batch_description(batch_to_process=batch_to_process,
      local_group=local_group,company=company,batch_type=BatchType.USAGES.value)

    return True

  def compute_batch_description(self, batch_to_process, local_group, company, batch_type):
    if local_group is None:
      local_group = self.search_local_group(batch_to_process, batch_type)

    batch_description = local_group + " - " + self.description

    if company:
      batch_description += " - " + company.name

    return batch_description

  def search_local_group(self, batch_to_search, batch_type):
    local_groups_configs = self.env['smp.smp_car_config_groups_locals'].search([])

    local_name = ""
    if batch_type == BatchType.USAGES.value:
      for reservation in batch_to_search:
        for config in local_groups_configs:
          for car_config in config.car_configs_related:
            if car_config.name == reservation.carconfig_id.name:
              local_name = config.name
              break
          if local_name != "":
            break
        if local_name != "":
          break

    elif batch_type == BatchType.TELETAC.value:
      for teletac in batch_to_search:
        for config in local_groups_configs:
          for car_config in config.car_configs_related:
            if car_config.name == teletac.reservation_compute_id.carconfig_id.name:
              local_name = config.name
              break
          if local_name != "":
            break
        if local_name != "":
          break

    if local_name == "":
      local_name = "gl_catalunya"

    return local_name
