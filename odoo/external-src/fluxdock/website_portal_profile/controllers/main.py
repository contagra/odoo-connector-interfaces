# -*- coding: utf-8 -*-
import json
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.tools.translate import _

from openerp.addons.website_portal.controllers.main import website_account

class website_account(website_account):
    @http.route(['/my/account'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        if redirect:
            redirect = redirect
        else:
            redirect = ('/my/profile_success')
        response = super(website_account, self).details(redirect, **post)
        categories = [dict(id=category.id, name=category.name) for category in partner.category_id]
        categories = json.dumps(categories)
        expertise = [dict(id=expertise.id, name=expertise.name) for expertise in partner.expertise_ids]
        expertises = json.dumps(expertise)
        response.qcontext.update({
            'categories': categories,
            'expertises': expertises,
        })
        # FIXME: Workaround for problem with saving of fields website. If required
        # fields are not set, website will be taken out of response dictionary
        # in order to avoid server errors
        if 'website' in response.qcontext:
            del response.qcontext['website']
        # if 'image_medium' in post:
            # partner = request.env['res.users'].browse(request.uid).partner_id
            # partner.sudo().write({'image_medium':post['image_medium']})
        if post:
            if post['post_categories']:
                categ_ids = post['post_categories'].split(',')
                partner.sudo().write({'category_id':[(4, int(category_id)) for category_id in categ_ids]})
            if post['post_expertises']:
                expertise_ids = post['post_expertises'].split(',')
                partner.sudo().write({'expertise_ids':[(4, int(expertise_id)) for expertise_id in expertise_ids]})
        return response

    @http.route('/my/get_expertises', type='http', auth="user", methods=['GET'], website=True)
    def expertise_read(self, q='', l=25, **post):
        data = request.env['partner_project_expertise.expertise'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route('/my/get_categories', type='http', auth="user", methods=['GET'], website=True)
    def categories_read(self, q='', l=25, **post):
        data = request.env['res.partner.category'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route('/my/profile_success', type='http', auth='user', website=True)
    def profile_success(self, *args, **kw):
        return request.render('website_portal_profile.profile_success', {})

    # @http.route('/my/upload', type='http', auth="user", website=True)
    # def image_handle(self, **post):
    #     post_file = []  # List of file to add to ir_attachment once we have the ID
    #     post_description = []  # Info to add after the message
    #     values = {}
    #
    #     for field_name, field_value in post.items():
    #         if hasattr(field_value, 'filename'):
    #             post_file.append(field_value)
    #
    #             partner = request.registry['res.partner']
    #             for field_value in post_file:
    #                 attachment_value = {
    #                     'name': field_value.filename,
    #                     'res_name': field_value.filename,
    #                     'res_model': 'res.partner',
    #                     'res_id': partner.id,
    #                     'datas': base64.encodestring(field_value.read()),
    #                     'datas_fname': field_value.filename,
    #                 }
    #                 request.registry['ir.attachment'].create(request.cr, SUPERUSER_ID, attachment_value, context=request.context)
    #     return request.render('website_portal_profile.fluxdock_upload')
