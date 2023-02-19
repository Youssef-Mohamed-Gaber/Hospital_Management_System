# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


        # this is how to inherit an existing controller in odoo
class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        print('Inherited odoo mates..')
        return res


class Hospital(http.Controller):
        # a sample controller for the website
    @http.route('/om_hospital/patient/', website=True, auth='public')
    def hospital_patient(self, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render('om_hospital.patients_page', {
            'patients': patients
        })

        # a simple controller to update records which connected with mobile app
    @http.route('/update_patient', type='json', auth='user')
    def update_patient(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                patient = request.env['hospital.patient'].sudo().search([('id', '=', rec['id'])])
                if patient:
                    patient.sudo().write(rec)
                args = {'success': True, 'message': 'Patient Updated'}
        return args

        # a simple controller to connect odoo with mobile app
    @http.route('/create_patients', type='json', auth='user')
    def create_patients(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'patient_name': rec['name'],
                    'email': rec['email']
                }
                new_patient = request.env['hospital.patient'].sudo().create(vals)
                args = {'success': True, 'message': 'Success', 'ID': new_patient.id}
        return args

        # a simple controller to connect odoo with mobile app
    @http.route('/get_patients', type='json', auth='user')
    def get_patients(self):
        patients_rec = request.env['hospital.patient'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                'id': rec.id,
                'name': rec.patient_name,
                'sequence': rec.name_seq
            }
            patients.append(vals)
        data = {'status': 200, 'response': patients, 'message': 'Mohsen Ma3ayaa?'}
        return data

        # a simple controller to connect odoo with mobile app
    @http.route('/patient_webform', type='http', auth='user', website=True)
    def patient_webform(self, **kw):
        doctor_rec = request.env['hospital.doctor'].sudo().search([])
        return http.request.render('om_hospital.create_patient', {'doctor_rec': doctor_rec})

        # a simple controller to connect odoo with mobile app
    @http.route('/create/webpatient', type='http', auth='user', website=True)
    def create_webpatient(self, **kw):
        request.env['hospital.patient'].sudo().create(kw)
        return request.render('om_hospital.patient_thanks', {})

        # add a banner to appointments
class AppointmentController(http.Controller):

    @http.route('/om_hospital/appointmens', type='json', auth='user')
    def appointment_banner(self):
        return {
            'html': """
                    <div>
                        <center><h1 style="margin: 10px;color: red;">Like & Subscribe The Channel...!</h1></center>
                        <center><p style="margin: 10px;font-size: 18px;"><a href="https://www.odoo.com/documentation/13.0/developer/howtos/backend.html" target="blank">View Odoo Updates...!</a></p></center>
                    </div>
                    """
        }
