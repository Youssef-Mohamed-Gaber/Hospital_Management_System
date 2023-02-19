# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Doctor Record'
    _rec_name = 'doctor_name'


    doctor_name = fields.Char(string='Name', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], default='male', string='Gender')
    user_id = fields.Many2one('res.users', string='Related User')
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patients')
    appointment_ids = fields.Many2many('hospital.appointment', string='Doctor Appointments')
