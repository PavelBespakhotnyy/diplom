import io, json, requests
from pprint import pprint

url = 'https://api.vk.com/method/'

vk_token = str(input('Введите Ваш VK token: '))
vk_id = str(input('Введите VK id человека, фото которого хотите сохранить: '))
vk_token2 = str(input('Введите VK token человека, фото которого хотите сохранить: '))
yandex_token = str(input('Введите яндекс token: '))

def enter_values():
    vk_token = str(input('Введите Ваш VK token: '))
    vk_id = str(input('Введите VK id человека, фото которого хотите сохранить: '))
    vk_token2 = str(input('Введите VK token человека, фото которого хотите сохранить: '))
    yandex_token = str(input('Введите яндекс token: '))
    return vk_token, vk_id, vk_token2, yandex_token

def show_yandex_disk():
    headers = {
        'accept': 'application/json',
        'authorization': f'OAuth {yandex_token}'
    }
    res = requests.get('https://cloud-api.yandex.net/v1/disk/resources/files', headers=headers)
    pprint(res.json())

def show_file():
    with open('new_file1.json', 'r', encoding='UTF-8') as file:
        pprint(file.read())

def upload_photo():
    method = 'photos.get'
    params = {
        'album_id': 'profile',
        'photo_sizes': 1,
        'access_token': vk_token2,
        'v': '5.131',
        'extended': '1'
    }
    res = requests.get(url + method, params=params)
    list = res.json()['response']['items']
    for i in list:
        user_photo = i['sizes'][-1]['url']
        likes = i['likes']['count']
        photo_name = f'{likes}.jpg'
        type = i['sizes'][-1]['type']
        headers = {
            'accept': 'application/json',
            'authorization': f'OAuth {yandex_token}'
        }

        params = {
            'path': f'Фото/{likes}.jpg',
            'url': user_photo
        }

        requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)

        with io.open('new_file1.json', 'a', encoding='UTF-8') as file:
            data = dict({"file_name": f'{likes}.jpg', 'size': type})
            file.write(json.dumps(data, ensure_ascii=False))

    return user_photo, likes, photo_name, type

method = 'photos.get'
params = {
    'album_id': 'profile',
    'photo_sizes': 1,
    'access_token': vk_token2,
    'v': '5.131',
    'extended': '1'
}

res = requests.get(url + method, params=params)
list = res.json()['response']['items']

for i in list:
    user_photo = i['sizes'][-1]['url']
    likes = i['likes']['count']
    photo_name = f'{likes}.jpg'
    type = i['sizes'][-1]['type']
    headers = {
        'accept': 'application/json',
        'authorization': f'OAuth {yandex_token}'
    }

    params = {
        'path': f'Фото/{likes}.jpg',
        'url': user_photo
    }

    requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)

    with io.open('new_file1.json', 'a', encoding='UTF-8') as file:
        data = dict({"file_name": f'{likes}.jpg', 'size': type})
        file.write(json.dumps(data, ensure_ascii=False))

commands = {
    'Show disk': show_yandex_disk,
    'Show file': show_file,
    'Enter values': enter_values,
    'Upload photo': upload_photo
}

def main():
    command = str(input('Введите команду (Break - выход, Help - список команд): '))
    while command != 'Break':
        if command != 'Help':
            if command in commands.keys():
                commands[command]()
            else:
                print('Что-то пошло не так...')
        else:
            print(commands.keys())
        command = str(input('Введите команду(Break - выход): '))

main()