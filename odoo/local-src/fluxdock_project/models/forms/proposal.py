
from odoo import models
from odoo import fields
from odoo import _

# FIXME: widgets have changed
# from odoo.addons.cms_form.widgets import DEFAULT_WIDGETS
#
# WIDGETS = DEFAULT_WIDGETS.copy()
# WIDGETS['image'].data = {
#     'image_preview_width': 600,
#     'image_preview_height': 400,
# }


class ProposalForm(models.AbstractModel):
    """Proposal model form."""

    _name = 'cms.form.project.proposal'
    _inherit = 'cms.form'
    _form_model = 'project.proposal'
    _form_fields_order = (
        'name',
        'location',
        'country_id',
        'website_short_description',
        'website_description',
        'start_date',
        'stop_date',
        'industry_ids',
        'expertise_ids',
        'contact_name',
        'contact_email',
        'contact_phone',
    )
    _form_required_fields = (
        'name',
        'website_short_description',
        'industry_ids',
        'expertise_ids',
    )
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    # FIXME
    # _form_widgets = WIDGETS

    @property
    def form_description(self):
        return _('Announce here a project your looking for collaborators. ')

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(ProposalForm, self).form_update_fields_attributes(_fields)
        industry_help = self.env.ref(
            'fluxdock_project.ref_form_industry_help',
            raise_if_not_found=False)
        if industry_help:
            help_text = industry_help.render({
                'form_field': _fields['expertise_ids'],
            })
            _fields['expertise_ids']['help'] = help_text

        # limit claim length
        # FIXME
        # _fields['website_short_description']['widget'].maxlength = 200

    def form_validate(self, request_values=None):
        errors, errors_message = super(
            ProposalForm, self).form_validate(request_values=request_values)
        request_values = request_values or self.form_get_request_values()
        start_date = request_values.get('start_date')
        stop_date = request_values.get('stop_date')
        if start_date > stop_date:
            errors['stop_date'] = 'validation'
            errors_message['stop_date'] = _(
                'End Date cannot be set before Start Date.')
        return errors, errors_message


class ProposalSearchForm(models.AbstractModel):
    """Proposal model search form."""

    _name = 'cms.form.search.project.proposal'
    _inherit = 'cms.form.search.project.reference'
    _form_model = 'project.proposal'

    only_my = fields.Boolean(string="Show only my proposals")
    fluxdock_search_header_template = \
        'fluxdock_project.proposal_search_form_header'