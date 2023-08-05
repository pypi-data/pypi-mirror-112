import os
from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.utils.external_proxy import get_external_proxies
import requests
import json


class DynamicElementLocator(object):
    element_locator_alternatives = []
    dynamic_element_preprocessing_requests = []

    def load_dynamic_elements(self, block_id):
        try:
            if SdkAuthentication.isAuthorized:
                headers = {'content-type': 'application/json',
                           'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}

                request = requests.get(Shield34Properties.api_base_url + '/dynamic-element-locator/locators',
                                       params={'blockId': block_id},
                                       headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                       proxies=get_external_proxies())
                if request.status_code == 200:
                    self.element_locator_alternatives = request.json(object_hook=decode_locator)
        except Exception as e:
            pass

    def save_dynamic_elements(self, json_file_directory, json_file_name):
        try:
            with open(os.path.join(json_file_directory, json_file_name), 'w') as f:
                json.dump(self.dynamic_element_preprocessing_requests, f, default=encode_locator)
        except Exception as e:
            pass

    def web_element_found(self, web_element, by, locator):
        if web_element is not None:
            web_driver = web_element.parent
            if web_driver is not None and by is not None:
                page = web_driver.page_source
                locator = Locator(by, locator)
                self.dynamic_element_preprocessing_requests.append(DynamicElementPreprocessingRequest(page, locator))

    def current_locator_alternatives(self, by, locator):
        if len(self.element_locator_alternatives) <= len(self.dynamic_element_preprocessing_requests):
            return []
        alternatives = self.element_locator_alternatives[len(self.dynamic_element_preprocessing_requests)]
        if alternatives.original is None:
            return []
        if Locator(by, locator).__eq__(alternatives.original):
            return alternatives.alternatives
        return []


class ElementLocatorAlternatives(object):
    original = None
    alternatives = []

    def __init__(self, locator, alternative_locators):
        self.alternatives = alternative_locators
        self.original = locator


def encode_locator(obj):
    if isinstance(obj, Locator):
        return obj.__dict__
    if isinstance(obj, DynamicElementPreprocessingRequest):
        return obj.__dict__
    if isinstance(obj, ElementLocatorAlternatives):
        return obj.__dict__
    return obj


def decode_locator(obj):
    if 'locator' in obj:
        return DynamicElementPreprocessingRequest(obj['page'], obj['locator'])
    if 'by' in obj:
        return Locator(obj['by'], obj['expression'])
    if 'original' in obj:
        return ElementLocatorAlternatives(obj['original'], obj['alternatives'])
    return obj


class Locator(object):
    by = None
    expression = None

    def __init__(self, by, locator):
        self.by = by
        self.expression = locator

    def __eq__(self, other):
        return self.by == other.by and self.expression == other.expression


class DynamicElementPreprocessingRequest(object):
    page = None
    locator = None

    def __init__(self, page, locator):
        self.page = page
        self.locator = locator
