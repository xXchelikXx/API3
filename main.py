import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

def is_bitlink(bitlink, bitly_token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }
    response = requests.get(url, headers=headers)
    return response.ok


def shorten_link(bitly_token, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }
    params = {
        'long_url':long_url
    }
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(bitlink, bitly_token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }
    params = {
        'unit':'month',
        'units':'-1'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def main():
    
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Сокращает ссылку, показывает клики по сокращённой ссылке')
    parser.add_argument('--url', type=str, help='Введите ссылку')
    short_link = parser.parse_args()
    parsed_url = urlparse(short_link.url)
    parsed_url = f'{parsed_url.netloc}{parsed_url.path}'
    try:
        if is_bitlink(parsed_url, bitly_token):
            print(count_clicks(parsed_url, bitly_token))
        else:
            print(shorten_link(bitly_token, short_link.url))
    except requests.exceptions.HTTPError:
        print('Ошибка ввода')


if __name__ == '__main__':
    main()
