from googleapiclient.discovery import build
import json


class Video():
    '''
    Класс для ютуб-видео
    '''
    __api_key = 'AIzaSyA8nWym5j1mj2RTuPqvr9TsQI2EndrPe30'
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        self.channel = Video.youtube.videos().list(id=self.video_id, part='snippet, statistics').execute()

        try:
            if len(self.channel['items']) == 0:         # блок try\except работает по количеству полученых ['items']
                self.title = None
                self.url = None
                self.count_watches = None
                self.like_count = None
                raise FileNotFoundError
            else:
                self.title = self.channel['items'][0]['snippet']['title']
                self.url = 'https://www.youtube.com/' + self.channel['items'][0]['id']
                self.count_watches = self.channel['items'][0]['statistics']['viewCount']
                self.like_count = self.channel['items'][0]['statistics']['likeCount']
        except FileNotFoundError:
            print('Видео с таким id не существует')

    def __str__(self):
        return self.title

    # def print_info(self) -> None:
    #     """функция тестирования"""
    #     print(json.dumps(self.channel, indent=2, ensure_ascii=False))


class PLVideo(Video):
    '''
    Наследник класса для ютуб-видео
    '''

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

# broken_video = Video('broken_video_id')
# print(broken_video.url)
# print(broken_video.title)
# video1 = Video('AWX4JnAnjBE')
# print(video1.url)
# print(video1.title)





