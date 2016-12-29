# -*- coding: utf-8 -*-
#
# inventory/locations/api/serializers.py
#
"""
LocationSetName, LocationFormat, and LocationCode serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin
from inventory.accounts.models import User
from inventory.projects.models import Project

from ..models import LocationSetName, LocationFormat, LocationCode

log = logging.getLogger('api.locations.serializers')
User = get_user_model()


#
# LocationSetNameSerializer
#
class LocationSetNameSerializer(SerializerMixin, serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail', queryset=Project.objects.all(),
        lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    location_formats = serializers.HyperlinkedRelatedField(
        view_name='location-format-detail', many=True, read_only=True,
        lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='location-set-name-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return LocationSetName.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.project = validated_data.get('project', instance.project)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.shared = validated_data.get('shared', instance.shared)
        instance.separator =  validated_data.get(
            'separator', instance.separator)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = LocationSetName
        fields = ('id', 'project', 'name', 'description', 'shared',
                  'separator', 'location_formats', 'creator', 'created',
                  'updater', 'updated', 'uri',)
        read_only_fields = ('id', 'creator', 'created', 'updater', 'updated',)


#
# LocationFormatSerializer
#
class LocationFormatSerializer(SerializerMixin, serializers.ModelSerializer):
    location_set_name = serializers.HyperlinkedRelatedField(
        view_name='location-set-name-detail',
        queryset=LocationSetName.objects.all(), lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    location_codes = serializers.HyperlinkedRelatedField(
        view_name='location-code-detail', many=True, read_only=True,
        lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='location-format-detail', lookup_field='public_id')

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return LocationFormat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.char_definition = validated_data.get(
            'char_definition', instance.char_definition)
        instance.location_set_name = validated_data.get(
            'location_set_name', instance.location_set_name)
        instance.segment_order =  validated_data.get(
            'segment_order', instance.segment_order)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = LocationFormat
        fields = ('id', 'location_set_name', 'char_definition',
                  'segment_order', 'segment_length', 'description',
                  'location_codes', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('id', 'segment_length', 'creator', 'created',
                            'updater', 'updated',)


#
# LocationCodeSerializer
#
class LocationCodeSerializer(SerializerMixin, serializers.ModelSerializer):
    location_format = serializers.HyperlinkedRelatedField(
        view_name='location-format-detail', lookup_field='public_id',
        queryset=LocationFormat.objects.all())
    parent = serializers.HyperlinkedRelatedField(
        view_name='location-code-detail', default=None,
        queryset=LocationCode.objects.all(), lookup_field='public_id')
    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    updater = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, lookup_field='public_id')
    items = serializers.HyperlinkedRelatedField(
        view_name='item-detail', many=True, read_only=True,
        lookup_field='public_id')
    uri = serializers.HyperlinkedIdentityField(
        view_name='location-code-detail', lookup_field='public_id')

    def validate_segment(self, value):
        """
        Disallow any change to root items.
        """
        request = self.get_request()

        if (value == LocationCode.ROOT_NAME
            and request.method not in ('GET', 'HEAD', 'OPTIONS')):
            msg = _("Segment is '{}', This is an unalterable root location."
                    ).format(LocationCode.ROOT_NAME)
            raise serializers.ValidationError(msg)

        return value

    def create(self, validated_data):
        user = self.get_user_object()
        validated_data['creator'] = user
        validated_data['updater'] = user
        return LocationCode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.location_format = validated_data.get(
            'location_format', instance.location_format)
        instance.segment = validated_data.get(
            'segment', instance.segment)
        instance.parent = validated_data.get(
            'parent', instance.parent)
        instance.updater = self.get_user_object()
        instance.save()
        return instance

    class Meta:
        model = LocationCode
        fields = ('id', 'location_format', 'segment', 'parent', 'path',
                  'level', 'items', 'creator', 'created', 'updater',
                  'updated', 'uri',)
        read_only_fields = ('id', 'path', 'level', 'items', 'creator',
                            'created', 'updater', 'updated',)
