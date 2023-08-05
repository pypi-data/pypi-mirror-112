from odoo import api, models


class HelpdeskTicket(models.Model):

    @api.multi
    def name_get(self):
        data = []
        for ticket in self:
            if ticket.name:
                data.append((ticket.id, ticket.number+" "+ticket.name))
            else:
                data.append((ticket.id, ticket.number))
        return data

