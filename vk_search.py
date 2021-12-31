import requests
import vk_api
from config import *
from db import DBConnector
from datetime import datetime


class PeopleSearch(object):
    sex = None
    age_from = None
    age_to = None
    city = None
    status = None
    token = None
    api = None
    client_id = None  # Тот для кого делается запрос
    ids = None  # id пользователей, которых нашли
    v = API_VERSION
    base_url = 'https://api.vk.com/method/'

    def __init__(self, client_id, **search_criteriums):
        self.client_id = client_id
        session = vk_api.VkApi(login=ADMIN_LOGIN, password=ADMIN_PASSWORD)
        session.auth()
        self.api = session.get_api()
        self.token = session.token['access_token']
        for key, value in search_criteriums.items():
            if key == 'city':
                try:
                    setattr(self, key, self.get_city_id_by_name(value))
                except:
                    print(f'\033[91m[{datetime.now()}] ERROR: Can\'t find city "{value}". Set default all.\033[0m')
            else:
                setattr(self, key, value)

    def get_city_id_by_name(self, city_name):
        method = 'database.getCities'
        url = self.base_url + method
        city_id = None
        params = {
            'count': 1,
            'q': city_name,
            'access_token': self.token,
            'v': self.v
        }

        response = requests.post(
            url=url,
            params=params
        )
        if response.status_code == '200':
            json_data = response.json()
            if len(json_data['response']['items']):
                city_id = json_data['response']['items'][0]['id']

        return city_id

    def search(self):
        method = 'users.search'
        url = self.base_url + method

        ids = None
        params = {
            # 'fields': 'photo, screen_name',
            'access_token': self.token,
            'v': self.v
        }

        params.update(vars(self))
        print(params)
        try:
            params.pop('api')
        except KeyError:
            pass
        try:
            params.pop('token')
        except KeyError:
            pass
        try:
            params.pop('base_url')
        except KeyError:
            pass
        response = requests.post(
            url=url,
            params=params
        )

        print(response.status_code)
        if response.status_code == 200:
            json_response: dict = response.json()
            print(json_response)
            # if 'items' in json_response.keys():
            ids = [item['id'] for item in json_response['response']['items'] if not item['is_closed']]
            self.remove_duplicate_results(ids)
        return self.ids

    def remove_duplicate_results(self, ids):
        db = DBConnector()
        self.ids = []
        for user_id in ids:
            if not db.is_duplicated(self.client_id, user_id):

                db.write_user(self.client_id, user_id)
                self.ids.append(user_id)

    @staticmethod
    def get_profile_link(user_id):
        return f'https://vk.com/id{user_id}'

    def get_best_3_photos(self, user_id):
        photo_dict = self.api.photos.get(owner_id=user_id, album_id='profile', extended=1)['items']
        print(photo_dict)
        sorted_photo_dict = sorted(photo_dict, key=lambda i: i['likes']['count'], reverse=True)[:3]
        print(sorted_photo_dict)
        medias = [f'photo{p["owner_id"]}_{p["id"]}' for p in sorted_photo_dict]
        print(medias)
        return medias

