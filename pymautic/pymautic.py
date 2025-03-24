from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

import requests
from requests.auth import HTTPBasicAuth

from pymautic.countries import clean_country


class MauticException(Exception):
    def __init__(self, detail=None, code=None, details=None):
        if details is None:
            details = {}

        self.detail = detail
        self.code = code
        self.details = details

    def __str__(self):
        return str(self.detail)


class MauticAPI:
    def __init__(self, username: str, password: str, host: str):
        self.username = username
        self.password = password
        self.host = host

    def perform_request(self, method, endpoint, data=None) -> Dict[str, Any]:
        r = requests.request(
            method.lower(),
            f"{self.host}/api/{endpoint}",
            verify=False,
            json=data,
            # params=params,
            timeout=3,
            headers={
                'Content-Type': 'application/json',
            },
            auth=HTTPBasicAuth(self.username, self.password)
        )

        r.raise_for_status()

        # if r.status_code >= 300:
        #     text = r.text
        #     if text.startswith('{'):
        #         errors = r.json()
        #         if len(errors.get('errors', [])) > 0:
        #             error = errors.get('errors')[0]
        #             if error['message'] == 'email: This field must be unique.':
        #                 return self.find_contact(email=data['email'])
        #             raise MauticException(error['message'], error['code'])
        #
        #     r.raise_for_status()

        return r.json()


class ContactClient(MauticAPI):
    def get(self, contact_id: str):
        """
        Retrieve lead from campaign system
        :param contact_id: ID of lead in campaign system
        """
        return self.perform_request('get', f'contacts/{contact_id}').get('contact')

    def find(self, email: Optional[str] = None, phone: Optional[str] = None):
        query = None
        if email:
            query = f'email:{email}'
        elif phone:
            query = f'phone:{phone}'

        if not query:
            return None

        l = self.list(query)
        try:
            total = int(l.get('total'))
            if total > 0:
                contacts = l.get('contacts')
                return contacts[list(contacts.keys())[0]]

            return None
        except Exception:
            return None

    def list(self, search: str, start: Optional[int] = 0, limit: Optional[int] = 50, order_by: Optional[str] = '', order_by_dir: Optional[str] = '', published_only: Optional[bool] =True):
        data = {
            'search': search,
            'start': start,
            'limit': limit,
            'orderBy': order_by,
            'orderByDir': order_by_dir,
            'publishedOnly': published_only,
        }

        r = self.perform_request('get', f'contacts?{urlencode(data)}')
        return r

    def upsert(self, contact_id: str, data: Dict[str, Any]):
        if 'country' in data:
            data['country'] = clean_country(data['country'])
        if not id:
            return self.create(data)

        return self.perform_request('put', f'contacts/{contact_id}/edit', data=data).get('contact')

    def update(self, contact_id: str, data: Dict[str, Any]):
        if 'country' in data:
            data['country'] = clean_country(data['country'])
        return self.perform_request('patch', f'contacts/{contact_id}/edit', data=data).get('contact')

    def create(self, data: Dict[str, Any]):
        if 'country' in data:
            data['country'] = clean_country(data['country'])
        return self.perform_request('post', 'contacts/new', data=data).get('contact')

    def dnc(self, contact_id: str, channel: str, reason: int):
        return self.perform_request('post', f'contacts/{contact_id}/dnc/{channel}/add',
                                    data={'reason': reason}).get('contact')


class FCMDeviceClient(MauticAPI):
    def create(self, data: Dict[str, Any]):
        return self.perform_request('post', 'fcm/devices/add', data=data)

    def update(self, device_id: str, data: Dict[str, Any]):
        return self.perform_request('patch', f'fcm/devices/{device_id}/edit', data=data)

    def delete(self, device_id: str):
        return self.perform_request('delete', f'fcm/devices/{device_id}')


class EmailClient(MauticAPI):
    def get(self, email_id: str):
        return self.perform_request('get', f'emails/{email_id}')

    def create(self, name: str, subject: str, content: Optional[str] = None, type: Optional[str] = 'list', extra: Optional[dict] = None):
        json = {'name': name, 'subject': subject, 'emailType': type}
        if content:
            json['customHtml'] = content
        if extra is not None:
            json.update(extra)
        return self.perform_request('post', 'emails/new', data=json)

    def update(self, email_id: str, name: str, subject: str, content: Optional[str] = None, type: Optional[str] = 'list', extra: Optional[dict] = None):
        json = {'name': name, 'subject': subject, 'emailType': type}
        if content:
            json['customHtml'] = content
        if extra is not None:
            json.update(extra)
        return self.perform_request('put', f'emails/{email_id}/edit', data=json)

    def email_to_contact(self, email_id: str, contact_id: str):
        return self.perform_request('post', f'emails/{email_id}/contact/{contact_id}/send', data={})


class SegmentClient(MauticAPI):
    def create(self, name: str, description: Optional[str] = None, is_published: Optional[bool] = True, category: Optional[str] = None):
        data = {'name': name, 'isPublished': is_published}
        if category:
            data['category'] = category
        if description:
            data['description'] = description

        return self.perform_request('post', 'segments/new', data=data)['list']

    def add_contact(self, segment_id: str, contact_id: str):
        return self.perform_request('post', f'segments/{segment_id}/contact/{contact_id}/add')

    def add_contacts(self, segment_id: str, contact_ids: List[str]):
        return self.perform_request('post', f'segments/{segment_id}/contacts/add', data={'ids': contact_ids})

    def remove_contact(self, segment_id: str, contact_id: str):
        return self.perform_request('post', f'segments/{segment_id}/contact/{contact_id}/remove')


class CategoryClient(MauticAPI):
    def get(self):
        return self.perform_request('get', 'categories')

    def create(self, title: str, bundle: Optional[str] = 'global'):
        return self.perform_request('post', 'categories/new', data={'title': title, 'bundle': bundle})


class AnalyticClient(MauticAPI):
    def log_event(self, contact: int, event: str, properties: Dict[str, Any], date: Optional[datetime] = None):
        data = {
            'name': event,
            'properties': properties,
            'contact': contact
        }

        if date is not None:
            data['date'] = date.isoformat()

        return self.perform_request('post', 'analytic/log/event', data=data)


class MauticClient:
    def __init__(self, username: str, password: str, host: str):
        self.username = username
        self.password = password
        self.host = host

        self.contacts = ContactClient(username, password, host)
        self.devices = FCMDeviceClient(username, password, host)
        self.emails = EmailClient(username, password, host)
        self.segments = SegmentClient(username, password, host)
        self.categories = CategoryClient(username, password, host)
        self.analytics = AnalyticClient(username, password, host)


    # @staticmethod
    # def send_telegram_msg(self, bot_id, data):
    #     r = requests.post(self.get_url('tbots/{}/send/message'.format(bot_id)), json=data,
    #                       auth=self.get_auth())
    #     return r.json()




