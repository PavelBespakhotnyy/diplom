import io, json
import requests

with open('token.txt', 'r', encoding='UTF-8') as file:
    vk_token = file.read()


yandex_token = str(input('Введите токен яндекс диска: '))

url = 'https://api.vk.com/method/'
vk_id = 'begemot_korovin'
vk_token2 = str(input('Введите VK токен: '))


def get_user_photo(access_token=vk_token2):
    method = 'photos.get'
    params = {
        'album_id': 'profile',
        'photo_sizes': 1,
        'access_token': access_token,
        'v': '5.131',
        'extended': '1'
    }
    res = requests.get(url + method, params=params)
    global likes
    likes = res.json()['response']['items'][-1]['likes']['count']
    global user_photo
    user_photo = res.json()['response']['items'][-1]['sizes'][-1]['url']
    global type
    type = res.json()['response']['items'][-1]['sizes'][-1]['type']


def post_photo(token=yandex_token):
    global photo_name
    photo_name = f'{likes}.jpg'
    headers = {
        'accept': 'application/json',
        'authorization': f'OAuth {yandex_token}'
    }
    params = {
        'path': f'{likes}.jpg',
        'url': user_photo
    }
    res = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)


def save_json_file():
    with io.open('new_file.json', 'a', encoding='UTF-8') as file:
        data = dict({"file_name": f'{likes}.jpg', 'size': type})
        file.write(json.dumps(data, ensure_ascii=False))
    with open('new_file.json', 'r', encoding='UTF-8') as file:
        print(file.read())


def show_yandex_disk():
    headers = {
        'accept': 'application/json',
        'authorization': f'OAuth {yandex_token}'
    }
    res = requests.get('https://cloud-api.yandex.net/v1/disk/resources/files', headers=headers)
    pprint(res.json())


commands = {
    'User photo': get_user_photo(),
    'Post photo': post_photo(),
    'Show file': save_json_file(),
    'Show yandex disk': show_yandex_disk()
}


def main():
    while True:
        command = str(input('Введите команду (Help - список команд, Break - для выхода): '))
        if command != 'Break':
            if command == 'Help':
                print(commands.keys())
            else:
                commands[command]
        else:
            break


main()
