from datetime import datetime
import json
import requests
from tqdm import tqdm

class VKtoYD:
    vk_id = input('Введите id пользователя: ')
    yd_token = input('Введите токен YandexDisk: ')
    vk_token = 'vk1.a.YeIHldSCNdNM3jX6hhkd_vqX6xSiqoUMikgPkO8QfabYsh3tCCGQu9BigtBw8o_5s5WYHsuxf-oafdcxjZm-8dniJzWSoIVgJzEi_tKrz0Jx1emU5UdfhnUVVBsbSY95taixcoUDEK5s52qz5AwGVVxwgOXrGHv3G-nFbon1PZ1bKm_LJOnB4PkedHlh4yr-ot0PHGQzevhu_675i16J5Q'
    BASE_URL = 'https://api.vk.com/method/'
    def __init__(self, vk_id= vk_id, yd_token= yd_token, token= vk_token, version= '5.131'):
        self.token = token
        self.owner_id = vk_id
        self.yd_token = yd_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def _get_photo(self):
        count = input('Сколько фото загрузить? Что бы оставить по умолчанию(5) нажмите Enter: ')
        if count == '': count = 5
        photo_data_list = []
        params = {'owner_id': self.owner_id,
                  'album_id': 'profile',
                  'rev': 1,
                  'extended': 1,
                  'count': count
                  }
        res = requests.get(f'{self.BASE_URL}/photos.get', params={**self.params, **params})
        for photo in res.json()['response']['items']:
            photo_data_list.append(photo)
        return photo_data_list

    def upload_photo(self):
        header = {'Authorization': 'OAuth '+ self.yd_token}
        folder_name = input('Для загрузки фото необходимо создать новую папку.\n'
                            'Введите название: ')
        requests.put(f'https://cloud-api.yandex.net/v1/disk/resources?path={folder_name}', headers=header)

        photo_json_list = []
        for photo in tqdm(self._get_photo(), desc='Загрузка фото', colour='green'):
            file_name = str(photo["likes"]["count"])
            photo_data = {'file_name': f'{file_name}.jpg',
                          'size': photo['sizes'][-1]['type']}
            for data in photo_json_list:
                if photo_data['file_name'] == data['file_name']:
                    photo_data['file_name'] = f'{file_name}_{str(datetime.fromtimestamp(photo["date"])).split(" ")[0]}.jpg'
                    file_name += f'_{str(datetime.fromtimestamp(photo["date"])).split(" ")[0]}'

            params = {'path': f'{folder_name}/{file_name}',
                      'url': photo['sizes'][-1]['url']}

            requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload?', params=params, headers=header)

            photo_json_list.append(photo_data)

            with open('photo_date.json', 'w') as f:
                json.dump(photo_json_list, f, indent=2)

        print(f'Фото успешно загружено!\n'
              f'Для просмотра перейдите по ссылке: https://disk.yandex.ru/client/disk/{folder_name}')

if __name__ == '__main__':
    user = VKtoYD()
    user.upload_photo()