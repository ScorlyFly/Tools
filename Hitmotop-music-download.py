#https://rus.hitmotop.com/artist/343974/start/48  -- скачивание происходит только в одной странице формат ссылки такой скачивается только с rus.hitmotop

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from colorama import Fore, init
from pathlib import Path
import os

# Инициализация colorama
init()

# Заголовки для запросов
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"{Fore.RED}Ошибка получения страницы: {response.status_code}{Fore.RESET}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Произошла ошибка: {e}{Fore.RESET}")
        return None

def find_tracks(html):
    soup = BeautifulSoup(html, 'lxml')
    tracks = []
    
    # Ищем все треки на странице
    for link in soup.find_all('a', href=True):
        if '/get/music/' in link['href']:
            tracks.append(link['href'])
    return tracks

def download_track(url, path):
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            file_size = int(response.headers.get('Content-Length', 0))
            filename = Path(url).name
            filepath = Path(path) / filename
            
            # Корректная обработка прогресса
            downloaded = 0
            with open(filepath, 'wb') as file:
                for chunk in tqdm(
                    response.iter_content(chunk_size=8192),
                    total=file_size,
                    unit='B',
                    unit_scale=True,
                    desc=f"{Fore.GREEN}Загрузка: {filename}{Fore.RESET}",
                    ascii=True,  # Для корректной работы в некоторых терминалах
                    ncols=80  # Ширина прогрессбара
                ):
                    file.write(chunk)
                    downloaded += len(chunk)
            print(f"{Fore.GREEN}Файл {filename} успешно скачан{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Ошибка при скачивании {url}: {e}{Fore.RESET}")

def main():
    url = input(f"{Fore.CYAN}Введите URL страницы с треками: {Fore.RESET}")
    if not url.startswith("http"):
        print(f"{Fore.RED}Некорректная ссылка!{Fore.RESET}")
        return
    
    html = get_html(url)
    if not html:
        return
    
    tracks = find_tracks(html)
    if not tracks:
        print(f"{Fore.RED}Треки не найдены{Fore.RESET}")
        return
    
    # Создаем папку для сохранения
    artist_name = input(f"{Fore.CYAN}Введите имя исполнителя/название папки: {Fore.RESET}")
    save_path = Path.cwd() / artist_name
    os.makedirs(save_path, exist_ok=True)
    
    # Скачиваем треки
    for track_url in tracks:
        download_track(track_url, save_path)

if __name__ == "__main__":
    main()

