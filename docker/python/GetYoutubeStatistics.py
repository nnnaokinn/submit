import os
import sys
import MySQLdb
from datetime import datetime
from UserLocalAnalyze import UserLocalAnalyze
from googleapiclient.discovery import build

# エスケープ用
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')

def regist_channel(cur, channel_id, response):
    """
    チャンネル情報の登録
    """

    # 登録項目取得
    table = str.maketrans("'", "’")
    name = response["items"][0]["snippet"]["title"].translate(table).translate(non_bmp_map)
    description = response["items"][0]["snippet"]["description"].translate(table).translate(non_bmp_map)
    publishedAt = response["items"][0]["snippet"]["publishedAt"][:10]
    thumbnail_s = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]
    thumbnail_m = response["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
    thumbnail_l = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    keyword = ""
    if "keywords" in response["items"][0]["brandingSettings"]["channel"]:
        keyword = response["items"][0]["brandingSettings"]["channel"]["keywords"].translate(table).translate(non_bmp_map)

    # 登録
    sql = \
        " INSERT INTO " \
            "channel (channel_id, name, description, published_date, keyword, thumbnail_s, thumbnail_m, thumbnail_l, created_at, updated_at)" \
        " VALUES " \
            f"('{channel_id}','{name}','{description}','{publishedAt}','{keyword}','{thumbnail_s}','{thumbnail_m}','{thumbnail_l}','{now_time}','{now_time}')" \
        " ON DUPLICATE KEY UPDATE " \
            f"name = '{name}'," \
            f"description = '{description}'," \
            f"keyword = '{keyword}'," \
            f"thumbnail_s = '{thumbnail_s}'," \
            f"thumbnail_m = '{thumbnail_m}'," \
            f"thumbnail_l = '{thumbnail_l}'," \
            f"updated_at = '{now_time}';"

    cur.execute(sql)

    return

def regist_statistics(cur, channel_id, response):
    """
    日別統計情報の登録
    """

    # 登録項目取得
    collect_day = datetime.now().strftime("%Y%m%d")
    table = str.maketrans("'", "’")
    name = response["items"][0]["snippet"]["title"].translate(table).translate(non_bmp_map)
    subscriber_count = response["items"][0]["statistics"]["subscriberCount"]
    view_count = response["items"][0]["statistics"]["viewCount"]
    video_count = response["items"][0]["statistics"]["videoCount"]

    # 登録
    sql = \
        " INSERT INTO " \
            "statistics (collect_day, channel_id, name, subscriber, view_count, video_count)" \
        " VALUES " \
            f"('{collect_day}','{channel_id}','{name}','{subscriber_count}','{view_count}','{video_count}')" \
        " ON DUPLICATE KEY UPDATE " \
            f"name = '{name}'," \
            f"subscriber = '{subscriber_count}'," \
            f"view_count = '{view_count}'," \
            f"video_count = '{video_count}';"

    cur.execute(sql)

    return

if __name__ == '__main__':

    # Youtube Data API
    youtube_api = build('youtube','v3',developerKey=os.environ["YOUTUBE_API_KEY"])

    # MySQL
    conn = MySQLdb.connect(user='user', passwd='password', host='mysql_db', port=3306, db='youtube', charset="utf8")
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    # UserLocalから取得対象チャンネルのIDを取得
    ul_analyze = UserLocalAnalyze(youtube_api)
    channel_id_list = ul_analyze.get_channel_id_list()

    try:
        for channel_id in channel_id_list:

            # チャンネル情報の取得
            response = youtube_api.channels().list(
                part = 'snippet,brandingSettings,statistics',
                id = channel_id
                ).execute()

            # チャンネルが削除されていたらスキップ
            if "items" not in response :
                continue

            # チャンネル情報の登録
            regist_channel(cur, channel_id, response)

            # 日別統計情報の登録
            regist_statistics(cur, channel_id, response)

        conn.commit()

    except Exception as exception:
        print(exception)
        conn.rollback()

    cur.close()
    conn.close()
