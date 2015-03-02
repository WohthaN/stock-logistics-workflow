# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api

report_name = 'stock_picking_pallet.report_picking_pallet'


class PickingPalletReport(models.AbstractModel):
    _name = 'report.%s' % report_name

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(report_name)
        pallets = self.env['stock.picking.pallet'].browse(self.ids)

        lines = {}
        for pallet in pallets:
            package = pallet.dest_package_id
            quants = self.env['stock.quant'].browse(package.get_content())
            lines[pallet] = quants

        docargs = {
            'doc_ids': pallets.ids,
            'doc_model': report.model,
            'docs': pallets,
            'lines': lines,
        }
        return report_obj.render(report_name, docargs)
