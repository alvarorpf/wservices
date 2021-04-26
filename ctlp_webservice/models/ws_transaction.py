from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class WsTransaction(models.Model):
    _name = 'ws.transaction'

    partner_id = fields.Many2one('res.partner', string="Socio")
    socio_code = fields.Char("Código de Socio")
    state = fields.Selection([('consult', 'Consulta'),
                              ('process', 'Procesado'),
                              ('cancel', 'Cancelado'),
                              ('finish', 'Finalizado')], string="Estado", default='consult')
    date = fields.Date("Fecha de Consulta")
    date_time = fields.Datetime("Fecha y Hora de Consulta")
    line_ids = fields.Many2many('account.collection.various', string="Documentos")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    currency_id_sec = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id_sec)
    doc_amount_total_main = fields.Monetary('Total Bs.', currency_field="currency_id")
    doc_amount_total_sec = fields.Monetary('Total Sus.', currency_field="currency_id_sec")
    type_transaction = fields.Selection([('f', 'Facturar'), ('c', 'Cobrar')])

    @api.model
    def service_consult_due(self, socio_code):
        for r in self:
            error = False
            msg = ""
            transaction_obj = self.env['ws.transaction']
            return {
                'error': error,
                'message': "Prueba de conexion",
            }
            try:
                # Validacion de Codigo de Socio Valido
                if socio_code == "":
                    raise UserError("El código de socio ingresado no es válido")
                else:
                    socio_id = self.env['res.partner'].search([('socio_code', '=', socio_code)])
                    if not socio_id:
                        raise UserError("El código de socio ingresado no es válido")
                # Consulta de transaccion pasada
                transaction_id = transaction_obj.search([('socio_id', '=', socio_id.id), ('state', '=', 'consult')])
                if not transaction_id and transaction_id.id:
                    # Creacion de transaccion
                    transaction_id = transaction_obj.create({
                        'socio_id': socio_id and socio_id.id or False,
                        'socio_code': socio_code,
                    })
                lines = transaction_id._consult_lines()
                if lines:
                    transaction_id.line_ids = [(6, 0, lines.ids)]
                else:
                    raise UserError("El socio no cuenta con deudas pendientes")

            except Exception as e:
                error = True
                msg = e
                res = {
                    'error': error,
                    'message': msg,
                }
                return res

    def _consult_lines(self):
        for r in self:
            if not r.socio_id:
                raise UserError("Esta transacción no tiene registrado un socio.")
            else:
                lines = self.env['account.collection.various'].search([('partner_id', '=', r.socio_id.id)])
            return lines

    def _consult_amount_total(self):
        for r in self:
            lines = r.line_ids
            main = 0
            sec = 0


class WsTransactionLog(models.Model):
    _name = 'ws.transaction.log'

    transaction_id = fields.Many2one("ws.transaction", "Transaccion")
    error = fields.Boolean("Error en transaccion")
    msg = fields.Char("Mensaje de error")