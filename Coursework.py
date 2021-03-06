from pprint import pprint
import os
import requests
import pyprind
import shutil

with open('token_vk.txt', 'r') as file_token_vk:
    token_vk = file_token_vk.read().strip()

with open('token_yan.txt', 'r') as file_token_yan:
    token_yan = file_token_yan.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/photos.get'
    def __init__(self, token_vk, version):
        self.params = {
            'access_token': token_vk,
            'v': version    
        }
        
    def get_photos(self, owner_id=1, album_id='profile', extended=1, count=5):
        photos_get_params = {
            "owner_id": owner_id,
            "album_id": album_id,
            "extended": extended,
            "count": count
        }
        req = requests.get(self.url, params={**self.params , **photos_get_params}).json()
        if 'response' not in req:
            print('В словаре "req" нет ключа "response"')
            return
        elif 'items' not in req['response']:
            print('В словаре "req" нет ключа "items"')
            return 
        req1 = req['response']['items']
        may_list = []
        may_buffer_check = []
        files=[]
        file_path = os.path.join(os.path.join(os.getcwd()))
        files = [f for f in sorted(os.listdir(file_path))]
        owner_id_str = str(owner_id)
        if owner_id_str in files:
            shutil.rmtree(owner_id_str)
        os.mkdir(owner_id_str)
        for date in req1:
            likes = date['likes']['count']
            size = date['sizes'][-1]['type']
            file_url = date['sizes'][-1]['url']
            file_name = f'{likes}.jpg'
            if file_name in may_buffer_check:
                file_name = f'{size}_{file_name}'
            may_buffer_check.append(file_name)
            may_list.append(
                    {'file_name': file_name, 'size': size}
            )
            api = requests.get(file_url)
            with open(f"{owner_id}/%s" % file_name, "wb") as file:
                file.write(api.content)
        pprint(may_list)
        return may_list

class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def resources(self, directory):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': directory}
        requests.put(url, headers=headers, params=params)
        
    def _upload_link(self, disk_file_path):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        return requests.get(url, headers=headers, params=params).json()

    def upload(self, owner_id):
        vk_client = VkUser(token_vk, '5.131')
        vk_cl = vk_client.get_photos(owner_id)
        self.resources(owner_id)
        for filename in vk_cl:
            filename1 = filename['file_name']
            href = self._upload_link(disk_file_path=f'{str(owner_id)}/{filename1}').get("href", "")
            file_path = os.path.join(os.path.join(os.getcwd(), str(owner_id)), filename1)
            requests.put(href, data=open(file_path, 'rb'))

def Upload_photo(owner_id, token_yan):
    yan_client = YaUploader(token_yan)
    yan_client.upload(owner_id)

    n = 1000000
    bar = pyprind.ProgBar(n)

    for i in range(n):    
        bar.update()
    
if __name__ == '__main__':

    owner_id = input('Введите идентификатор владельца акаунта VK: ')

    Upload_photo(owner_id=owner_id, token_yan=token_yan)

    
    