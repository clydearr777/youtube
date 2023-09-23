
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    __api_key = 'AIzaSyA8nWym5j1mj2RTuPqvr9TsQI2EndrPe30'
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet, statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.about = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/'+self.channel["items"][0]["id"]
        self.subscribes = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.watches = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(self):
        """класс-метод для получение обьекта для работы с АПИ"""
        youtube = build('youtube', 'v3', developerKey=Channel.__api_key)
        return youtube

    def to_json(self, json_file) -> None:
        """метод сохраняющий данные канала в файл json"""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'about': self.about,
            'url': self.url,
            'subscribes': self.subscribes,
            'video_count': self.video_count,
            'watches': self.watches
        }
        path = '../src/'+json_file
        with open(path, 'w'):
            json.dumps(data, indent=4)

    def __str__(self):
        """homework-3 реализован магический метод __str__ выдающий """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """ homework-3 метод по суммированию экземпляров класса (по подписчикам)"""
        return int(self.subscribes) + int(other.subscribes)

    def __sub__(self, other):
        """ homework-3 метод для вычитания подписчиков"""
        return int(self.subscribes) - int(other.subscribes)

    def __lt__(self, other):
        """hw-3 метод для опирации сравнения (меньше)"""
        return self.subscribes < other.subscribes

    def __le__(self, other):
        """hw-3 метод для опирации сравнения (меньше или равно)"""
        return self.subscribes <= other.subscribes

