# /usr/bin/env python
# -*- coding: utf-8 -*

import requests
import resources.utility as utility


class EncounterResource(utility.CacheablePropertyResource):
    yaml_tag = '!EncounterResource'

    class Meta:
        name = 'Encounters'
        resource_name = 'encounter'
        cache_folder = 'encounters/encounters/'
        identifier = 'id'
        attributes = (
            'version_details',
            'location_area'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @staticmethod
    def get_url(url, **kwargs):
        if 'from_url' in kwargs:
            return kwargs['from_url']
        # Remove the "encounter" Beckett automatically adds.
        url = '/'.join(url.split('/')[0:-1])
        return '{}/pokemon/{}/encounters/'.format(url, kwargs.get('uid'))

class EncounterMethodResource(utility.CacheablePropertyResource):
    yaml_tag = '!EncounterMethodResource'

    class Meta:
        name = 'Encounter Method'
        resource_name = 'encounter-method'
        cache_folder = 'encounters/encounter-methods/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'order',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )