# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.translate import _
import datetime

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    @api.multi
    def unlink(self):
        ''' Employees can delete their owns leaves even when they are validated
        '''
        for holiday in self:
            if holiday.date_to < datetime.datetime.today():
                continue
            if holiday.state not in ['draft', 'cancel', 'confirm', 'refuse']:
                holiday.sudo().action_refuse()
            if holiday.state not in ['draft', 'cancel', 'confirm']:
                holiday.sudo().action_draft()

        res = super(HolidaysRequest, self).unlink()
        if res:
            return {
		'name': _('New Request'),
		'view_type': 'calendar',
		'view_mode': 'calendar',
		'res_model': 'hr.leave',
		'view_id': 'hr_holidays.hr_leave_view_calendar',
		'type': 'ir.actions.act_window',
		'target': 'current',
		'nodestroy': True
	    }

    @api.model
    def get_leaves(self, start_date, end_date):
        """
        This function returns leaves from start_date to end_date in the following
        format: {'worker': email, 'start_time': '2021-12-30','end_time': '2021-12-31'}
        """
        res = []
        resources_calendar_leaves_model = self.env["resource.calendar.leaves"]
        resource_resource_model = self.env["resource.resource"]
        search_params = [
            ('date_to','>=', start_date),
            ('date_from', '<=', end_date),
            ('holiday_id','!=', False)
        ]
        leaves = resources_calendar_leaves_model.search(search_params)

        for leave_id in leaves.ids:
            leave_data = resources_calendar_leaves_model.browse(leave_id)
            worker = leave_data.resource_id.user_id.email
            res.append({
                'worker': worker,
                'start_time': leave_data.date_from,
                'end_time': leave_data.date_to
            })

        return res
