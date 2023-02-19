# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'


    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_date = fields.Date(string="Appointment Date")


    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date
        }
        self.patient_id.message_post(body="The Appointment Created Successfully", subject="Appointment Creation")
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': new_appointment.id,
            'context': context
        }


    def print_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        selected_patient = data['form']['patient_id'][0]
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])
        appointment_list = []
        for app in appointments:
            vals = {
                'name': app.patient_id.patient_name,
                'appointment_date': app.appointment_date,
                'notes': app.notes
            }
            appointment_list.append(vals)
        print('data', appointment_list)
        data['docs'] = appointment_list
        return self.env.ref('om_hospital.appointment_report').report_action(self, data=data)
