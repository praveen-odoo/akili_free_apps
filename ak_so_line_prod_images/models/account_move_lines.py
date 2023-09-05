from odoo import models, fields, api

class InvoiceLineImage(models.Model):
	_inherit = 'account.move.line'

	product_image = fields.Binary(string='Product Image', related="product_id.image_1920")
	is_image = fields.Boolean(string='Is Image', compute="_compute_is_image")

	def _compute_is_image(self):
		res = self.env['ir.config_parameter'].sudo().search([('key', '=', 'report_with_image')])
		self.is_image = res.value