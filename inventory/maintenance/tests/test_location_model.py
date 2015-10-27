# -*- coding: utf-8 -*-
#
# inventory/maintenance/tests/test_location_model.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import LocationDefault, LocationFormat, LocationCode

User = get_user_model()


class BaseLocation(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseLocation, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True):
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    def _create_location_default_record(self, name, description):
        kwargs = {}
        kwargs['owner'] = self.user
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationDefault.objects.create(**kwargs)

    def _create_location_format_record(self, char_definition, segment_order,
                                       description, location_default):
        kwargs = {}
        kwargs['char_definition'] = char_definition
        kwargs['location_default'] = location_default
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationFormat.objects.create(**kwargs)

    def _create_location_code_record(self, segment, char_definition,
                                     parent=None):
        kwargs = {}
        kwargs['char_definition'] = char_definition
        kwargs['segment'] = segment
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationCode.objects.create(**kwargs)


class TestLocationDefaultModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationDefaultModel, self).__init__(name)

    def test_create_location_default_record(self):
        #self.skipTest("Temporarily skipped")
        name = "Test Location Default"
        desc = "Test description."
        obj = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            obj.name, name, obj.description, desc)
        self.assertEqual(obj.name, name, msg)
        self.assertEqual(obj.description, desc, msg)










class TestLocationFormatModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationFormatModel, self).__init__(name)

    def test_create_location_format_record(self):
        #self.skipTest("Temporarily skipped")
        # Create a valid location default object.
        name = "Test Location Default"
        desc = "Test description."
        loc_def = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            loc_def.name, name, loc_def.description, desc)
        self.assertEqual(loc_def.name, name, msg)
        self.assertEqual(loc_def.description, desc, msg)
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        obj = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        msg = "{} should be {} and {} should be {}".format(
            obj.char_definition, char_definition,
            obj.location_default.name, name)
        self.assertEqual(obj.char_definition, char_definition, msg)
        self.assertEqual(obj.location_default.name, name, msg)








class TestLocationCodeModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationCodeModel, self).__init__(name)

    def test_create_location_code(self):
        #self.skipTest("Temporarily skipped")
        # Create a valid location default object.
        name = "Test Location Default"
        desc = "Test description."
        loc_def = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            loc_def.name, name, loc_def.description, desc)
        self.assertEqual(loc_def.name, name, msg)
        self.assertEqual(loc_def.description, desc, msg)
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        loc_fmt = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        msg = "{} should be {} and {} should be {}".format(
            loc_fmt.char_definition, char_definition,
            loc_fmt.location_default.name, name)
        self.assertEqual(loc_fmt.char_definition, char_definition, msg)
        self.assertEqual(loc_fmt.location_default.name, name, msg)
        # Create a location code object.
        segment = "T01"
        obj = self._create_location_code_record(segment, loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj.segment, segment,
            obj.char_definition.location_default.name, name)
        self.assertEqual(obj.segment, segment, msg)
        self.assertEqual(obj.char_definition.location_default.name, name, msg)






