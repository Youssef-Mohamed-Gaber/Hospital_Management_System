# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "appointment_date desc"


    def _get_default_value(self):
        return ("best wishes")


    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: ('New'), related='patient_id.name_seq')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string='Registration Note', default=_get_default_value)
    appointment_date = fields.Date(string='Date', required=True)
    appointment_date_end = fields.Date(string='End Date')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointments Lines')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    assistant_doctors = fields.Many2many('hospital.doctor', string='Assistant Doctors')
    product_id = fields.Many2one('product.template', string='Product Tamplate')
    partner_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    order_id_domain = fields.Char(compute="_compute_order_id_domain", readonly=True, store=False)
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ], string='Status', readonly=True, default='draft')
    amount = fields.Integer(string='Total Amount')


    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.Appointment') or ('New')
        result = super(Appointment, self).create(vals)
        return result


    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thank You!',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Done... Thank You!',
                    'type': 'rainbow_man',
                }
            }

    def action_concelled(self):
        for rec in self:
            rec.state = 'cancel'

    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_info('Appointment Draft')

    def delete_lines(self):
        for rec in self:
            rec.appointment_lines = [(5, 0, 0)]

    def test_recordset(self):
        for rec in self:
            partners = self.env['res.partner'].search([])
            print("Mapped Partners...", partners.mapped('email'))
            #  attribute sorted orders the partners based on create_date or write_date ...etc
            print("Sorted Partners...", partners.sorted(lambda o: o.create_date, reverse=True))
            print("Sorted Partners...", partners.sorted(lambda o: o.create_date, reverse=True).mapped('name'))
            print("Filtered Partners...", partners.filtered(lambda o: not o.property_stock_customer))

    # How To Give Domain For A Field Based on Another Field
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.product_id.product_variant_ids:
                val = {
                    'product_id': line.id,
                    'product_qty': 5
                }
                lines.append((0, 0, val))
            rec.appointment_lines = lines

    # How To Give Domain For A Field Dynamically Based on Another Field
    @api.depends('partner_id')
    def _compute_order_id_domain(self):
        for rec in self:
            rec.order_id_domain = json.dumps([('partner_id', '=', rec.partner_id.id)])


    @api.model
    def default_get(self, fields):
        res = super(Appointment, self).default_get(fields)
        product_rec = self.env['product.product'].search([])
        appointment_added_lines = []
        for product in product_rec:
            line = (0, 0, {
                'product_id': product.id,
                'product_qty': 1
            })
            appointment_added_lines.append(line)
        res.update({
            'appointment_lines': appointment_added_lines,
        })
        return res
