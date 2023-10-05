import datetime
import isodate
import os
from googleapiclient.discovery import build
from src.video import Video


class PlayList:
    """ класс для плелиста ютуб-канала
    """
    # __api_key = 'AIzaSyA8nWym5j1mj2RTuPqvr9TsQI2EndrPe30'
    __api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_videos = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        self.playlist_info = PlayList.youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        """ метод класса для вычисления суммарной длительности плейлиста"""

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        youtube = build('youtube', 'v3', developerKey=self.__api_key)
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        duration = datetime.timedelta(seconds=0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """ метод класса для нахождения видео с наибольшим количеством лайков"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        list_likes = []             # пусто список для количества лайков
        dict_videos = {}            # словарь для количества лайков (key) и ID канала (value)
        for video in video_ids:
            video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video
                                                   ).execute()
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            list_likes.append(like_count)
            dict_videos[like_count] = video
        return "https://youtu.be/"+(dict_videos[max(list_likes)])






