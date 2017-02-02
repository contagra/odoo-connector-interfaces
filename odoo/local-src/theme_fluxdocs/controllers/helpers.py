# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website.models.website import slug

IMG_FOLDER_PATH = '/theme_fluxdocs/static/img/'


class JSHelpers(http.Controller):
    """Controller for some JS stuff."""

    @http.route(['/members/json'], type='http', auth="public", website=True)
    def member_aggr(self, *arg, **post):
        """Return JSON data for members aggregation.

        Members are loaded randomly as requested here:
        https://redmine.iart.ch/issues/15336
        """

        env = request.env
        # http://stackoverflow.com/questions/8674718/
        # best-way-to-select-random-rows-postgresql/14450321#14450321
        query = (
            "select * from ("
            "select distinct id from res_partner "
            "where membership_state in ('invoiced','paid','free')"
            ") members "
            "ORDER BY random()"
        )
        env.cr.execute(query)
        ids = [x[0] for x in env.cr.fetchall()]
        res = []
        if ids:
            members = env['res.partner'].sudo().browse(ids)
            for item in members:
                if item.image:
                    avatar_url = request.website.image_url(
                        item, 'image', '135x135')
                else:
                    # use default avatar
                    avatar_url = IMG_FOLDER_PATH \
                        + 'content-icons/member-placeholder.png'
                res.append({
                    'id': item.id,
                    'name': item.name,
                    'url': '/members/{}'.format(slug(item)),
                    'avatar_url': avatar_url
                })
        return json.dumps({
            'ok': True,
            'members': res,
        })