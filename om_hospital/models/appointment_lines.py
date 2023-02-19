# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointments lines'

    product_id = fields.Many2one('product.product', string='Medicines')
    product_qty = fields.Integer('Quantity')
    sequence = fields.Integer('Sequence')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')