# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models
from openerp import fields
from openerp import _
from openerp.addons.cms_form.widgets import DEFAULT_WIDGETS

WIDGETS = DEFAULT_WIDGETS.copy()
WIDGETS['image'].data = {
    'image_preview_width': 600,
    'image_preview_height': 400,
}


class ReferenceForm(models.AbstractModel):
    """Reference model form."""

    _name = 'cms.form.project.reference'
    _inherit = 'cms.form'
    _form_model = 'project.reference'
    _form_fields_order = (
        'name',
        'implementation_date',
        'location',
        'country_id',
        'industry_ids',
        'expertise_ids',
        'website_short_description',
        'image',
        'video_url',
        'ext_website_url',
        'linked_partner_ids',
    )
    _form_required_fields = ('name', 'website_short_description', 'image')
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    _form_widgets = WIDGETS

    @property
    def form_description(self):
        return _('Register here projects '
                 'your company accomplished successfully.')

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(ReferenceForm, self).form_update_fields_attributes(_fields)
        industry_help = self.env.ref(
            'specific_project.ref_form_industry_help',
            raise_if_not_found=False)
        if industry_help:
            help_text = industry_help.render({
                'form_field': _fields['expertise_ids'],
            })
            _fields['expertise_ids']['help'] = help_text
        partner_help = self.env.ref(
            'specific_project.ref_form_partner_help',
            raise_if_not_found=False)
        if partner_help:
            help_text = partner_help.render({
                'form_field': _fields['linked_partner_ids'],
            })
            _fields['linked_partner_ids']['help'] = help_text
        if self.env.user and self.env.user.partner_id:
            _fields['linked_partner_ids']['domain'] = \
                '[["id","!=",{}]]'.format(self.env.user.partner_id.id)


class ReferenceSearchForm(models.AbstractModel):
    """Reference model search form."""

    _name = 'cms.form.search.project.reference'
    _inherit = 'cms.form.search'
    _form_model = 'project.reference'
    _form_fields_order = (
        'name',
        'industry_ids',
        'expertise_ids',
        'country_id',
        'location',
        'only_my',
    )
    form_template = 'specific_project.search_form'
    form_fields_template = 'specific_project.search_form_fields'

    only_my = fields.Boolean(string="Show only my references")

    def form_search_domain(self, search_values):
        """Adapt domain to filter on personal items."""
        _super = super(ReferenceSearchForm, self)
        domain = _super.form_search_domain(search_values)
        # make sure only_my is not used
        domain = [x for x in domain if x[0] != 'only_my']
        # if value is submitted then filter by owner
        if self.o_request.session.uid and search_values.get('only_my'):
            domain.append(('create_uid', '=', self.env.user.id))
        return domain