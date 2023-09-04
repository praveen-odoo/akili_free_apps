from odoo import models, fields
from datetime import date

class CustomerBirthdayReminder(models.Model):
	_inherit = 'res.partner'

	dob = fields.Datetime(string="Date Of Birth")
	

	def send_birthday_mail(self):
		customer = self.env['res.partner']
		current_date = date.today().strftime('%m-%d')
		mail_template = self.env.ref('ak_birthday_reminder.custom_email_template')
		customer_ids = customer.search([])
		matched_ids = []
		for ids in customer_ids:
			if type(ids.dob) == bool:
				pass
			else:
				if ids.dob.strftime('%m-%d') == current_date:
					matched_ids.append(ids)
		if len(matched_ids) > 0:
			for i in matched_ids:
				mail_template.send_mail(i.id, force_send=True)	
