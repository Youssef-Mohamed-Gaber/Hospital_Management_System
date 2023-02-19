# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    patient_name = fields.Char(string='Name', required=True, tracking=True, translate=True)
    patient_age = fields.Integer(string='Age', tracking=True)
    patient_age2 = fields.Integer(string='Age2')
    notes = fields.Text(string='Registration Note')
    doctor_note = fields.Text(string='Note')
    pharmacy_note = fields.Text(string='Note')
    image = fields.Binary(string='Image')
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: ('New'))
    Phone_number = fields.Integer(string='Contact Number')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')],
        default='male', string='Gender')
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    active = fields.Boolean("Active", default=True)
    doctor_id = fields.Many2one('hospital.doctor', ondelete='cascade', string='Doctor')
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Doctor Gender", related='doctor_id.gender')
    email = fields.Char(string='Email')
    user_id = fields.Many2one('res.users', string='Pro')
    create_appointment = fields.One2many('create.appointment', 'patient_id', string='Appointments')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    model_viewer = fields.Binary(string='Model Viewer')


    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or ('New')
        result = super(Patient, self).create(vals)
        return result

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError("The Age Must be Greater than 5")

    def open_patient_appointments(self):
        return {
            'name': ('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count


    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name_seq, rec.patient_name)))
        return res


    def action_send_card(self):
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)


    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        for rec in appointments:
            print('Appointment Name', rec.patient_id.patient_name)


    @api.model
    def test_cron_job(self):
        print("Test The Automated Action (cron)")


    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)


    def print_report_excel(self):
        return self.env.ref('om_hospital.report_patient_card_xlsx').report_action(self)


    def action_patients(self):
        return {
            'name': ('Patients Server Action'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|', ('name_seq', operator, name), ('patient_name', operator, name)]
        return super(Patient, self).search(domain, limit=limit).name_get()