from odoo import models, fields, api, _
import datetime 

class EmployeeDocumentsManagement(models.Model):
    _name = 'employee.documents.management'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    name = fields.Char('Document Name', required=True)
    document_id = fields.Char('Document ID', required=True)
    document_type = fields.Selection([
            ('id', 'Identity'), ('marksheet', 'Education'), ('personal', 'Personal')], required=True)
    attachment = fields.Binary('Attachment')
    issue_date = fields.Datetime('Issue Date')
    not_expired = fields.Boolean('Lifetime Validity', default=False)
    expiry_date = fields.Datetime('Expiry Date')
    description = fields.Text('description')
    valid_status = fields.Selection([
            ('valid', 'Valid'), ('exp_today', 'Expired Today'), ('expired', 'Expired')
        ], readonly=True)

    def validate_document(self):
        employee = self.employee_id.name
        current_date = datetime.date.today().strftime('%d-%m-%Y')
        
        if self.not_expired:
            self.valid_status = 'valid'
        else:
            exp_date = self.expiry_date.strftime('%d-%m-%Y')
            if current_date == exp_date:
                self.valid_status = 'exp_today'
            elif exp_date < current_date:
                self.valid_status = 'expired'
            else:
                self.valid_status = 'valid'

    def send_expiry_mail(self):
        documents = self.env['employee.documents.management'].search([])
        if documents:
            mail_template = self.env.ref('ak_employee_document_management.documents_email_template')
            cur_date = datetime.date.today().strftime('%d-%m-%Y')

        for document in documents:
            if document.valid_status != 'expired':
                if document.expiry_date:
                    exp_date = document.expiry_date.strftime('%d-%m-%Y')
                    if cur_date == exp_date:
                        document.valid_status = 'exp_today'
                    elif exp_date < cur_date:
                        document.valid_status = 'expired'
                    else:
                        document.valid_status = 'valid'

                    if document.valid_status == 'exp_today' or document.valid_status == 'expired':
                        mail_template.send_mail(document.id, force_send=True)

class EmployeeDocuments(models.Model):
    _inherit = 'hr.employee'
    
    document_ids = fields.One2many('employee.documents.management', 'employee_id', string="Document IDs")
