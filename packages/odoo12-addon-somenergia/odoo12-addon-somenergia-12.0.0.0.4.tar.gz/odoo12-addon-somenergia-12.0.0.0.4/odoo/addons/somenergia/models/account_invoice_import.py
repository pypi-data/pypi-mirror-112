from odoo import models, api


class AccountInvoiceImport(models.TransientModel):
    _inherit = 'account.invoice.import'

    @api.model
    def _prepare_create_invoice_vals(self, parsed_inv, import_config=False):
        (vals, import_config) = (
            super()._prepare_create_invoice_vals(parsed_inv, import_config)
        )
        vals['name'] = parsed_inv.get('name')
        return vals, import_config

    @api.model
    def parse_facturae_invoice(self, xml_root, xsd_file):
        parsed_inv = super().parse_facturae_invoice(xml_root, xsd_file)
        if (
            parsed_inv['type'] == 'out_invoice' and 
            '86025558' in parsed_inv['partner'].get('vat')
        ):
            invoice = xml_root.find('Invoices/Invoice')
            inv_series_code = invoice.find('InvoiceHeader/InvoiceSeriesCode').text
            parsed_inv['name'] = inv_series_code + "/" + parsed_inv['invoice_number']
        return parsed_inv

