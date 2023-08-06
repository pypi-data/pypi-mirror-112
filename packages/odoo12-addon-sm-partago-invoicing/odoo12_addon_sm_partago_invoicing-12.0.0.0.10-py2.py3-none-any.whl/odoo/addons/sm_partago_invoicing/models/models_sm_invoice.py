# -*- coding: utf-8 -*-
import json
from distutils.util import strtobool

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources
from odoo.tools import float_is_zero, float_compare, pycompat


class sm_invoice(models.Model):
  _inherit = 'account.invoice'

  invoice_email_sent = fields.Boolean(string=_("Email sent"))
  invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Inv report"))
  invoice_template = fields.Selection([
    ('default', 'Default'),
    ('cs_default', 'Carsharing default'),
    ('cs_teletac', 'Carsharing Teletac')
  ], string=_("Invoice Template"), default="default")
  hide_payment_info = fields.Boolean(string=_("Hide payment info"))
  prepaid_pocketbook = fields.Float(string=_("Prepaid pocketbook"),compute="_get_prepaid_pocketbook",store=False)

  @api.depends('outstanding_credits_debits_widget')
  def _get_prepaid_pocketbook(self):
    for record in self:
      pocketbook = 0
      if record.outstanding_credits_debits_widget:
        outstanding = json.loads(record.outstanding_credits_debits_widget)
        if outstanding:
          for credit in outstanding['content']:
            pocketbook += float(credit['amount'])
      record.prepaid_pocketbook = pocketbook

  @api.one
  def _get_outstanding_info_JSON(self):
    self.outstanding_credits_debits_widget = json.dumps(False)
    # if self.state == 'open':
    domain = [('account_id', '=', self.account_id.id),
          ('partner_id', '=', self.env['res.partner']._find_accounting_partner(self.partner_id).id),
          ('reconciled', '=', False),
          '|',
          '&', ('amount_residual_currency', '!=', 0.0), ('currency_id', '!=', None),
          '&', ('amount_residual_currency', '=', 0.0), '&', ('currency_id', '=', None),
          ('amount_residual', '!=', 0.0)]
    if self.type in ('out_invoice', 'in_refund'):
      domain.extend([('credit', '>', 0), ('debit', '=', 0)])
      type_payment = _('Outstanding credits')
    else:
      domain.extend([('credit', '=', 0), ('debit', '>', 0)])
      type_payment = _('Outstanding debits')
    info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': self.id}
    lines = self.env['account.move.line'].search(domain)
    currency_id = self.currency_id
    if len(lines) != 0:
      for line in lines:
        # get the outstanding residual value in invoice currency
        if line.currency_id and line.currency_id == self.currency_id:
          amount_to_show = abs(line.amount_residual_currency)
        else:
          amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(
            abs(line.amount_residual), self.currency_id)
        if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
          continue
        if line.ref:
          title = '%s : %s' % (line.move_id.name, line.ref)
        else:
          title = line.move_id.name
        info['content'].append({
          'journal_name': line.ref or line.move_id.name,
          'title': title,
          'amount': amount_to_show,
          'currency': currency_id.symbol,
          'id': line.id,
          'position': currency_id.position,
          'digits': [69, self.currency_id.decimal_places],
        })
      info['title'] = type_payment
      self.outstanding_credits_debits_widget = json.dumps(info)
      self.has_outstanding = True

  @api.multi
  def sm_invoice_notify(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        c_invoices = self.env['account.invoice'].browse(self.env.context['active_ids'])
        if c_invoices.exists():
          for inv in c_invoices:

            template = self.env.ref('account.email_template_edi_invoice', False)

            values = template.generate_email(inv.id)

            ctx = dict(
              default_model='account.invoice',
              default_res_id=inv.id,
              default_use_template=bool(template),
              default_template_id=template.id,
              default_composition_mode='comment',
              mark_invoice_as_sent=True,
              send_from_code=True
            )

            attachment = False
            if len(values['attachments']):
              for attach in values['attachments']:
                if attachment is False:
                  filename = attach[0]
                  filedata = attach[1]
                  attachment = self.env['ir.attachment'].create(
                    {'res_model': 'account.invoice', 'res_id': inv.id, 'name': filename,
                     'datas': filedata, 'datas_fname': filename})

            message = self.env['mail.compose.message'].create({
              'template_id': template.id,
              'body': values['body'],
              'attachment_ids': [(4, attachment.id)],
              'partner_ids': [(4, inv.partner_id.id)]
            })

            if not self.invoice_email_sent:
              message.with_context(ctx).send_mail()
              self.write({'invoice_email_sent': True})

    return sm_resources.getInstance().get_successful_action_message(self, _('SM invoice notify done successfully'),
                                    self._name)

  @api.model
  def send_invoice_email_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        c_invoices = self.env['account.invoice'].browse(self.env.context['active_ids'])
        if c_invoices.exists():
          for inv in c_invoices:
            self.send_invoices_email(inv)

  def send_invoices_email(self, record=None):
    if record is None:
      record = self

    company = record.env.user.company_id
    email_template = company.invoice_mail_template_id

    if email_template.id and record.invoice_email_sent == False:
      email_values = {'send_from_code': True}
      email_template.with_context(email_values).send_mail(record.id, True)
      record.write({'invoice_email_sent':True})


sm_invoice()
