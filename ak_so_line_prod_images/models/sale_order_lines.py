from odoo import models, fields, api

class SaleLineImage(models.Model):
	_inherit = 'sale.order.line'

	product_image = fields.Binary(string='Product Image', related="product_id.image_1920")
	is_image = fields.Boolean(string='Is Image', compute="_compute_is_image")

	def _compute_is_image(self):
		res = self.env['ir.config_parameter'].sudo().search([('key', '=', 'report_with_image')])
		self.is_image = res.value

class SaleLineImageSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	report_with_image = fields.Boolean(string="Report with Product Image", default=False)
	@api.model
	def get_values(self):
		res = super(SaleLineImageSettings, self).get_values()
		res['report_with_image'] = self.env['ir.config_parameter'].sudo().get_param('report_with_image')
		return res

	@api.model
	def set_values(self):
		self.env['ir.config_parameter'].sudo().set_param('report_with_image', self.report_with_image)
		res = super(SaleLineImageSettings, self).set_values()
		return res