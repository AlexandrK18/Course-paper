from pprint import pprint
import os
import requests
import pyprind
import shutil

token_vk = ""

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token_vk, version):
        self.params = {
            'access_token': token_vk,
            'v': version    
        }
        
    def get_photos(self, owner_id=1, album_id='profile', extended=1, count=5):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            "owner_id": owner_id,
            "album_id": album_id,
            "extended": extended,
            "count": count
        }
        req = requests.get(photos_get_url, params={**self.params , **photos_get_params}).json()
        if 'response' not in req:
            print(req.get('response', 'Нет ключа "response"'))
        elif 'items' not in req['response']:
            print(req['response'].get('items', 'Нет ключа "items"')) 
        else:
            req1 = req['response']['items']
            may_list = []
            may_buffer_check = []
            files=[]
            file_path = os.path.join(os.path.join(os.getcwd()))
            files = [f for f in sorted(os.listdir(file_path))]
            if str(owner_id) in files:
                shutil.rmtree(str(owner_id))
                os.mkdir(str(owner_id))
            else:
                os.mkdir(str(owner_id))
            for date in req1:
                likes = date['likes']['count']
                size = date['sizes'][-1]['type']
                file_url = date['sizes'][-1]['url']
                file_name = f'{likes}.jpg'
                if file_name not in may_buffer_check:
                    may_buffer_check.append(file_name)  
                else:
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

    token_yan = ""
    Upload_photo(owner_id=552934290, token_yan=token_yan)

    
    