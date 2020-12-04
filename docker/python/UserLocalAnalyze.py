from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import requests

class UserLocalAnalyze(object):
    """
    UserLocalをスクレイピングするクラス
    """

    BASE_URL = "https://virtual-youtuber.userlocal.jp"
    OFFICE_URL = "https://virtual-youtuber.userlocal.jp/office/"
    ALL_URL = "https://virtual-youtuber.userlocal.jp/office/all"

    def __init__(self, youtube_api):
        self.youtube_api = youtube_api


    def get_channel_id_list(self):
        """
        UserLocalにリンクされているYoutubeチャンネルのIDを取得する
        """

        # プロジェクトURLの取得
        project_url_list = self.__get_project_url_list()

        ### プロジェクト数が多いと非常に時間がかかるためある程度間引き ###
        project_url_list = project_url_list[:16]
        ##################################################################

        # メンバーURLの取得
        member_url_list = []
        for project_url in project_url_list:
            member_url_list.extend(self.__get_member_url_list(project_url))

        # チャンネルIDの取得
        channel_list = []
        for member_url in member_url_list:
            channel_list.append(self.__get_channel_id(member_url))

        return channel_list


    def __get_project_url_list(self):
        """
        プロジェクトごとのURLリストを取得する
        """

        # プロジェクトごとのリンクブロックを取得
        r = requests.get(self.ALL_URL)
        soup = BeautifulSoup(r.text,"lxml")
        table = soup.find_all("table", class_="table table-sm table-hover table-common table-ranking table-office-list")
        project_list = table[0].find_all("tr")

        # プロジェクトごとのURLをリスト化
        project_url_list = []
        for project in project_list:
            a = project.select("a")
            project_url = UserLocalAnalyze.OFFICE_URL + a[0].attrs["href"]
            project_url_list.append(project_url)

        return project_url_list


    def __get_member_url_list(self, project_url):
        """
        プロジェクトに所属するメンバーのURLリストを取得する
        """

        # メンバーリストを取得
        r = requests.get(project_url)
        soup = BeautifulSoup(r.text,"lxml")

        table = soup.find("table", class_="table table-sm table-hover table-common table-ranking table-ranking-yt")
        member_list = table.find_all("tr")

        # メンバーURLリストを取得
        member_url_list = []
        for member in member_list:

            profile = member.find_all("a", class_="no-propagation")[1]
            member_url = UserLocalAnalyze.BASE_URL + profile.attrs["href"]
            member_url_list.append(member_url)

        return member_url_list

    def __get_channel_id(self, member_url):
        """
        メンバーURLからチャンネルIDを取得
        ※ページ内に直接リンクが無いため動画情報からチャンネルIDを取得する
        """

        # 動画IDの取得
        r = requests.get(member_url)
        soup = BeautifulSoup(r.text,"lxml")

        movie_id_list = []
        movies = soup.find_all("div", class_="card card-video")

        for movie in movies:
            movie_url = movie.attrs["data-link"]
            movie_id = movie_url.split("=")[1]
            movie_id_list.append(movie_id)

        # チャンネルIDの取得
        channel_id = ""
        for movie_id in movie_id_list:
            try:
                response = self.youtube_api.videos().list(
                    part = 'snippet',
                    id = movie_id
                    ).execute()

                channel_id = response['items'][0]["snippet"]["channelId"]

            except:
                channel_id = ""

            if channel_id != "":
                break;

        return channel_id













        



