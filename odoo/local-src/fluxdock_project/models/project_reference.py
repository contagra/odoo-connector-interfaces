# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug

STATIC_FOLDER = '/fluxdock_project/static'


class ProjectReference(models.Model):
    """ProjectReference contains projects to be shown on member's profile. Can
    link to other partners.
    """

    _name = 'project.reference'
    _description = "Project reference"
    _inherit = [
        'mail.thread',
        'website.published.mixin',
    ]

    # we use this for website template add action
    cms_add_url = '/dock/references/add'
    cms_after_delete_url = '/my/home'
    cms_search_url = '/dock/references'

    @api.multi
    def _compute_cms_edit_url(self):
        for item in self:
            item.cms_edit_url = item.website_url + '/edit'

    @api.multi
    def _compute_website_url(self):
        for item in self:
            item.website_url = self.cms_search_url + '/' + slug(item)

    name = fields.Char(
        string="Reference title",
        required=True
    )
    implementation_date = fields.Date(
        string="Implementation date",
        required=False,
    )
    location = fields.Char()
    industry_ids = fields.Many2many(
        comodel_name="res.partner.category",
        string="Industries",
        help="To which industries belongs the project?",
    )
    expertise_ids = fields.Many2many(
        comodel_name="project.partner.expertise",
        string="Expertises",
        help="Which expertises did your company bring to the project?",
    )
    image = fields.Binary(
        "Reference image",
        attachment=True,
    )
    website_short_description = fields.Text(string="Description")
    video_url = fields.Char(
        string='Video URL',
    )
    ext_website_url = fields.Char(
        string='External Website URL',
    )
    linked_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Referenced partners",
    )
    create_uid = fields.Many2one(
        'res.users',
        'Owner',
        select=True,
        readonly=True,
    )
    country_id = fields.Many2one(comodel_name='res.country', string="Country")

    @api.multi
    @api.depends('image')
    def _compute_image_url(self):
        ws_model = self.env['website']
        for item in self:
            if item.image:
                image_url = ws_model.image_url(item, 'image')
            else:
                image_url = STATIC_FOLDER \
                    + '/src/img/reference_placeholder.png'
            item.image_url = image_url

    @api.multi
    def toggle_published(self):
        """ Inverse the value of the field ``published`` on the records in
        ``self``.
        """
        for record in self:
            record.website_published = not record.website_published

    @api.model
    def create(self, vals):
        res = super(ProjectReference, self).create(vals)
        if not self.env.context.get('no_profile_update'):
            partner = res.create_uid.partner_id
            if partner:
                # TODO: set proper rule/permission to do this w/ no sudo
                partner.sudo().update_profile_state()
        return res

    @api.multi
    def unlink(self):
        # drop image attachments before deletion
        # since this commit here
        # https://github.com/odoo/odoo/commit/eb9113c04d66627fbe04b473b9010e5de973c6aa  # noqa
        # prevents a normal portal user to delete the attachment
        # if you are not an employee.
        # Reported issue https://github.com/odoo/odoo/issues/15311
        self.write({'image': False})
        res = super(ProjectReference, self).unlink()
        return res

    @api.multi
    def redirect_after_publish(self):
        self.ensure_one()
        return len(self.env.user.references_ids) == 1
