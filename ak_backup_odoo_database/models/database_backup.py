# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.fields import Datetime
from odoo.http import content_disposition
import odoo
import subprocess
import io
import datetime
import os



class BackupDatabase(models.Model):
    _name = 'backup.database'
    _description = 'backup.database'
    _order = 'sequence'

    sequence = fields.Integer(help="Used to order the sequence of the backup record")
    name = fields.Char()
    frequency = fields.Integer(string="Frequency", default="1")	
    frequency_interval = fields.Selection([('days','Daily'),('weeks','Weekly'),('months','Monthly')], string="Frequency Interval")
    backup_datetime = fields.Datetime(string="Backup Start Time")
    storage_path = fields.Char(string="Storage Path")
    db_backup_details_ids = fields.One2many('db.backup.database','backup_db_id', string="Backup Details")
    state = fields.Selection([('draft','Draft'),('active','Active'),('inactive','Inactive')], default='draft')
    cron_id = fields.Many2one("ir.cron", string="Cron ID")

    def active(self):
        cron = self.env['ir.cron']
        model_id = self.env['ir.model'].search([('name', "=", "backup.database")]).id
        vals = {
            'name': self.name,
            'model_id': model_id,
            'interval_number': 1,
            'interval_type': self.frequency_interval.lower(),
            'active': True,
            'nextcall': self.backup_datetime,
            'numbercall': -1,
            'state':'code',
            'code': 'model.backup()',
            }
        
        cron_id = cron.create(vals)
        self.cron_id = cron_id
        self.write({'state':'active'})
  
    def inactive(self):
        cron = self.env['ir.cron'].search([('name',"=", self.name)]).unlink()
        self.write({'state':'inactive'})

    def draft(self):
    	self.write({'state':'draft'})

    def backup(self):
        cron_id = self.env.context.get('cron_id')
        cron = self.env['ir.cron'].search([('id', '=', cron_id)])
        backup_database = self.env['backup.database'].search([('name', '=', cron.name)])

        is_path = os.path.exists(backup_database.storage_path)

        database_name = self.pool.db_name

        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "%s_%s.%s" % (database_name, ts, 'zip')
        headers = [
            ('Content-Type', 'application/octet-stream; charset=binary'),
            ('Content-Disposition', content_disposition(filename)),
        ]

        dump_stream = odoo.service.db.dump_db(database_name, None, "zip")
        
        filepath = backup_database.storage_path + "/" + filename
        if is_path == False:
            subprocess.call(["mkdir"+str(backup_database.storage_path)], shell=True)

        r = io.BufferedRandom.read(dump_stream)
        with open(filepath, 'wb') as file:
            file.write(r)

        if os.path.exists(filepath):
            vals = {
                "backup_datetime": backup_database.backup_datetime,
                "file_name": filepath
            }
            backup_database.write({"db_backup_details_ids": [(0,0, vals)]})


class BackupDatabaseDetails(models.Model):
    _name = 'db.backup.database'
    _description = 'db.backup.database'
    _order = 'sequence'

    sequence = fields.Integer(help="Used to order the sequence of the backup record")
    backup_db_id = fields.Many2one('backup.database', string="Backup")
    backup_datetime = fields.Datetime(string="Backup Start Time")
    file_name = fields.Char(string="File Name")

    def get_zip_backup(self):
        return True

class IrCron(models.Model):
    _inherit = 'ir.cron'

    @api.model
    def _callback(self, cron_name, server_action_id, job_id):
        """ to handle cron thread executed by Odoo."""
        self = self.with_context(cron_id=job_id)
        return super(IrCron, self)._callback(cron_name,server_action_id, job_id)

    def method_direct_trigger(self):
        """ to handle manual execution using the button."""
        for rec in self:
            rec = rec.with_context(cron_id=rec.id)
            super(IrCron, rec).method_direct_trigger()
        return True