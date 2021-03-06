# -*- coding: utf-8 -*-
#
# inventory/regions/api/serializers.py
#
"""
Regions serializers.
"""
__docformat__ = "restructuredtext en"

import logging

from rest_framework import serializers

from inventory.common.api.serializer_mixin import SerializerMixin

from ..models import Country, Subdivision, Language, TimeZone, Currency


log = logging.getLogger('api.regions.serializers')


#
# CountrySerializer
#
class CountrySerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='country-detail')

    class Meta:
        model = Country
        fields = ('id', 'code', 'country', 'active', 'href',)
        read_only_fields = ('id', 'code', 'country', 'active',)


#
# SubdivisionSerializer
#
class SubdivisionSerializer(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='subdivision-detail')

    class Meta:
        model = Subdivision
        fields = ('id', 'subdivision_name', 'country', 'code', 'active',
                  'href',)
        read_only_fields = ('id', 'subdivision_name', 'country', 'code',
                            'active',)


#
# LanguageSerializer
#
class LanguageSerializer(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='language-detail')

    class Meta:
        model = Language
        fields = ('id', 'locale', 'country', 'code', 'active', 'href',)
        read_only_fields = ('id', 'locale', 'country', 'code', 'active',)


#
# TimeZoneSerializer
#
class TimeZoneSerializer(serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='timezone-detail')

    class Meta:
        model = TimeZone
        fields = ('id', 'zone', 'country', 'coordinates', 'country', 'desc',
                  'active', 'href',)
        read_only_fields = ('id', 'zone', 'country', 'coordinates', 'country',
                            'desc', 'active',)


#
# CurrencySerializer
#
class CurrencySerializer(SerializerMixin, serializers.ModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail', read_only=True)
    href = serializers.HyperlinkedIdentityField(view_name='currency-detail')

    class Meta:
        model = Currency
        fields = ('id', 'country', 'currency', 'alphabetic_code',
                  'numeric_code', 'minor_unit', 'symbol', 'active', 'href',)
        read_only_fields = ('id', 'country', 'currency', 'alphabetic_code',
                            'numeric_code', 'minor_unit', 'symbol', 'active',)
