import requests
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

KST = timezone(timedelta(hours=9))


class ProjectManager:
    def __init__(self):
        self.projects = dict()

    def save(self, data):
        '''
        :param data: {1: create_project, 2: delete_project, 3: upload_work}
        :return:
        '''
        if data['0']:
            pass
        elif data['1']:
            key, url, video = data['1']
            self.projects[key] = {'metadata': [url, video, datetime.now(KST).strftime('%Y.%m.%d %H:%M')],
                                  'work': {}}
            # TODO k값 중복일때 예외처리
