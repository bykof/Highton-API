import logging
import xmltodict
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class Highton:
    GET_REQUEST = 'GET'
    POST_REQUEST = 'POST'
    PUT_REQUEST = 'PUT'
    DELETE_REQUEST = 'DELETE'
    HIGHRISE_URL = 'highrisehq.com'

    class RequestException(Exception):
        pass

    class Fields:
        pass

    def __init__(self, user, api_key):
        """
        :param user: Your personal username for the Highrise API
        :param api_key: Your personal API-Key for the Highrise API
        """
        self._user = user
        self._api_key = api_key

    """
    General methods
    """

    @staticmethod
    def _parse_from_xml_to_dict(xml):
        return xmltodict.parse(xml)

    @staticmethod
    def _parse_from_dict_to_xml(dictionary):
        return xmltodict.unparse(dictionary)

    def _send_request(self, method, endpoint, params=None, data=None):
        response = requests.request(
            method=method,
            url=f'https://{self._user}.{Highton.HIGHRISE_URL}/{endpoint}.xml',
            headers={'Content-Type': 'application/xml'},
            auth=HTTPBasicAuth(username=self._api_key, password=''),
            params=params,
            data=data,
        )

        if not response.ok:
            raise Highton.RequestException(response.status_code)
        else:
            return response

    def _make_request(self, method, endpoint, params=None, data=None):
        try:
            response = self._send_request(
                method=method,
                endpoint=endpoint,
                params=params,
                data=self._parse_from_dict_to_xml(data) if data else {}
            )

            if len(response.content) > 1:
                return self._parse_from_xml_to_dict(response.content)
            else:
                return response.status_code
        except Highton.RequestException as e:
            logger.error(
                f'The {method}-request towards the endpoint "/{endpoint}.xml" failed with HTTP-Code {str(e)}'
            )

    """
    API methods
    """

    """
    Section: People
    Docs: https://github.com/basecamp/highrise-api/blob/master/sections/people.md
    """
    def get_person(self, subject_id):
        return self._make_request(
            method=Highton.GET_REQUEST,
            endpoint=f'people/{subject_id}',
        ).get('person')

    def create_person(self, last_name, **kwargs):
        return self._make_request(
            method=Highton.POST_REQUEST,
            endpoint='people',
            data='',
        )

    def update_person(self, person):
        return self._make_request(
            method=Highton.PUT_REQUEST,
            endpoint=f'people/{person["id"]["#text"]}',
            data={'person': person},
        )

    def destroy_person(self, subject_id):
        return self._make_request(
            method=Highton.DELETE_REQUEST,
            endpoint=f'people/{subject_id}',
        )
