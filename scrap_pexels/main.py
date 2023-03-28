import math
import os

import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


def scrap_pexels(query=''):
    headers = {'Authorization': f'{os.getenv("API_KEY")}'}
    query_str = f'https://api.pexels.com/v1/search?query={query}&per_page=80&orientation=landscape'

    response = requests.get(url=query_str, headers=headers)

    if response.status_code != 200:
        return f'Ошибка: Статус код - {response.status_code}, {response.json()}'

    img_dir_path = '_'.join(i for i in query.split(' ') if i.isalnum())

    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)

    json_data = response.json()

    images_count = json_data.get('total_results')

    if not json_data.get('next_page'):
        img_urls = [item.get('src', {}).get('original') for item in json_data.get('photos')]
        download_images(img_list=img_urls, img_dir_path=img_dir_path)
    else:
        print(f'[INFO] Bceго изображений: {images_count}. Сохранение может занять какое-то время.')

        images_list_urls = []
        for page in range(1, math.ceil(images_count/80)+1):
            query_str = f'{query_str}&page={page}'
            response = requests.get(url=query_str, headers=headers)
            json_data = response.json()
            img_urls = [item.get('src', {}).get('original') for item in json_data.get('photos')]
            images_list_urls.extend(img_urls)
        download_images(img_list=images_list_urls, img_dir_path=img_dir_path)


def download_images(img_list: list, img_dir_path: str):
    for item_url in tqdm(img_list):
        response = requests.get(url=item_url)

        if response.status_code == 200:
            with open(f'./{img_dir_path}/{item_url.split("-")[-1]}', 'wb') as file:
                file.write(response.content)
        else:
            print('Что-то пошло не так при скачивании изображения')


def main():
    query = input('Введите запрос:')
    scrap_pexels(query=query)


if __name__ == '__main__':
    main()
