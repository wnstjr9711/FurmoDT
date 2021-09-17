import requests
from bs4 import BeautifulSoup


class ProjectManager:
    def __init__(self):
        self.projects = dict()

    @staticmethod
    def getfilename(fid):
        # 공유링크로 파일이름 가져오기
        res = requests.get(fid)
        soup = BeautifulSoup(res.text, 'html.parser')
        f_name = soup.find('title').text.split()[0]
        return f_name
