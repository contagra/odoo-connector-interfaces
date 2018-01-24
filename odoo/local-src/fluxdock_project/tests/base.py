# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# import odoo.tests.common as test_common
from odoo import exceptions


class BaseTestCase(object):
    """Base klass to test your model basic permissions.

    Look at `ir_rules_example.xml` to know which rules you must create.
    """

    def setUp(self):
        super(BaseTestCase, self).setUp()
        user_model = self.env['res.users'].with_context(
            {'no_reset_password': True,
             'tracking_disable': True, })
        self.user1 = user_model.create({
            'name': 'User 1 (test ref)',
            'login': 'testref_user1',
            'email': 'testref_user1@email.com',
            # make sure to have only portal group
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.user2 = user_model.create({
            'name': 'User2',
            'login': 'testref_user2',
            'email': 'testref_user2@email.com',
            # make sure to have only portal group
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.group_public = self.env.ref('base.group_public')
        self.user_public = user_model.create({
            'name': 'Public User',
            'login': 'publicuser',
            'email': 'publicuser@example.com',
            'groups_id': [(6, 0, [self.group_public.id])]}
        )

    @property
    def model(self):
        raise NotImplementedError()

    def test_perm_create(self):
        obj = self.model.sudo(self.user1.id).create({'name': 'Foo'})
        self.assertTrue(self.model.browse(obj.id))

    def test_perm_write(self):
        obj = self.model.sudo(self.user1.id).create({'name': 'Foo'})
        obj.name = 'Baz'
        self.assertEqual(obj.name, 'Baz')

    def test_perm_write_only_owner(self):
        obj = self.model.sudo(self.user1.id).create({'name': 'Foo'})
        with self.assertRaises(exceptions.AccessError):
            obj.sudo(self.user2.id).name = 'cannot do this!'
        obj = self.model.sudo(self.user2.id).create({'name': 'Foo 2'})
        with self.assertRaises(exceptions.AccessError):
            obj.sudo(self.user1.id).name = 'cannot do this!'

    def test_delete(self):
        obj = self.model.sudo(self.user1.id).create({'name': 'Foo'})
        obj_id = obj.id
        obj.unlink()
        self.assertFalse(self.model.browse(obj_id).exists())
        if 'image' in obj:
            # test delete w/ attachment field
            # Reported issue https://github.com/odoo/odoo/issues/15311
            # Overridden unlink method in ProjectReference
            ref = self.model.sudo(self.user1.id).create({
                'name': 'Foo',
                'image': 'fake image here!'.encode('base64')
            })
            ref_id = ref.id
            ref.unlink()
            self.assertFalse(self.model.browse(ref_id).exists())

    def test_delete_only_owner(self):
        ref = self.model.sudo(self.user1.id).create({'name': 'Foo'})
        with self.assertRaises(exceptions.AccessError):
            ref.sudo(self.user2.id).unlink()

    def test_published(self):
        ref = self.model.sudo(self.user1.id).create({'name': 'Foo'})
        self.assertFalse(ref.website_published)
        # admin
        self.assertTrue(ref.read())
        # owner
        self.assertTrue(ref.sudo(self.user1.id).read())
        # public user
        with self.assertRaises(exceptions.AccessError):
            ref.sudo(self.user_public.id).read()
        # another portal user
        with self.assertRaises(exceptions.AccessError):
            ref.sudo(self.user2.id).read()
        # publish it!
        ref.website_published = True
        # now public user can see it
        self.assertTrue(ref.sudo(self.user_public.id).read())
        # and other portal user too
        self.assertTrue(ref.sudo(self.user2.id).read())