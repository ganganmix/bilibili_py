import os
import httpx
import subprocess
import winreg
import json
from lxml import etree
class Bilibili_Requ(object):
    def __init__(self, url):
        self._headers = {
            "user-agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
            "referer": "https://www.bilibili.com/"
        }
        self._data = httpx.get(url=url, headers=self._headers)
        self._xpath = etree.HTML(text=self._data.text)
        self._lis = json.loads(self._xpath.xpath('//script')[2].text.strip('window.__playinfo__='))
        self._path = os.getcwd()


    def _Title(self):
        xpath_title = self._xpath.xpath('//title')
        title = xpath_title[0].text
        return title

    def _Video_Url(self):
        video_data = self._lis['data']['dash']['video'][0]['baseUrl']
        return video_data
    # 下载视频

    def _Audio_Url(self):
        audio_data = self._lis['data']['dash']['audio'][0]['baseUrl']
        return audio_data
    # 下载音频

    def _Download(self):
        with open(file=fr'{self._path}\MUTE{Bilibili_Requ._Title(self)}'+'.mp4', mode='wb') as f:
            f.write(httpx.get(Bilibili_Requ._Video_Url(self), headers=self._headers).content)
        with open(file=fr'{self._path}\{Bilibili_Requ._Title(self)}'+'.mp3', mode='wb') as f:
            f.write(httpx.get(Bilibili_Requ._Audio_Url(self), headers=self._headers).content)
        return True
    # 源文件

    def _get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    def Download(self):
        b = Bilibili_Requ._Download(self)
        if b:
            COMMAND = fr'ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe -i "{self._path}\MUTE{Bilibili_Requ._Title(self)}.mp4" -i "{self._path}\{Bilibili_Requ._Title(self)}.mp3" -c copy -y "{Bilibili_Requ._get_desktop(self)}\{Bilibili_Requ._Title(self)}.mp4"'
            os.system(COMMAND)
            os.remove(f"{self._path}\MUTE{Bilibili_Requ._Title(self)}.mp4")
            os.remove(fr'{self._path}\{Bilibili_Requ._Title(self)}'+'.mp3')
        return '下载完成'