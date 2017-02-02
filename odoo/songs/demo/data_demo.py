# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv


@anthem.log
def load_expertises(ctx):
    load_csv(
        ctx, 'data/demo/partner.project.expertise.csv',
        'partner.project.expertise')


@anthem.log
def load_partner_categories(ctx):
    load_csv(
        ctx, 'data/demo/res.partner.category.csv',
        'res.partner.category')


@anthem.log
def main(ctx):
    """ Installing demo data """
    load_expertises(ctx)
    load_partner_categories(ctx)
