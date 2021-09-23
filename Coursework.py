from pprint import pprint
import os
import requests
import pyprind

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
        req1 = req['response']['items']
        may_list = []
        may_list1 = []
        for date in req1:
            likes = date['likes']['count']
            size = date['sizes'][-1]['type']
            file_url = date['sizes'][-1]['url']
            file_name = f'{likes}.jpg'
            if file_name not in may_list1:
                may_list1.append(f'{likes}.jpg')
                may_list.append(
                    {'file_name': file_name, 'size': size}
                )   
            else:
                file_name = f'{size}_{file_name}'
                may_list.append(
                    {'file_name': file_name, 'size': size}
                )
            api = requests.get(file_url)
            with open("photos_disk/%s" % file_name, "wb") as file:
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

    def _upload_link(self, disk_file_path):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def upload(self, owner_id):
        vk_client = VkUser(token_vk, '5.131')
        vk_cl = vk_client.get_photos(owner_id)
        for filename in vk_cl:
            filename1 = filename['file_name']
            href = self._upload_link(disk_file_path=f'photos_yan/{filename1}').get("href", "")
            file_path = os.path.join(os.path.join(os.getcwd(), 'photos_disk'), filename1)
            response = requests.put(href, data=open(file_path, 'rb'))

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

    
    