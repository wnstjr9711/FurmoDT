import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))


class ProjectManager:
    def __init__(self):
        self.projects = dict()
        self.work = dict()

    def save(self, data):
        """
        :param data: {1: create_project, 2: delete_project, 3: add_language, 4: update_work}
        """
        if '0' in data:
            pass
        elif '1' in data:
            # TODO key 값 중복일때 예외처리
            key, url, video = data['1']
            header = ['번호', 'TC_IN', 'TC_OUT', '원어']
            self.work[key] = pd.DataFrame([['' for i in range(len(header))] for j in range(2000)],
                                          columns=header)
            self.projects[key] = {'metadata': {'url': url, 'video': video, 'date': datetime.now(KST).strftime('%Y.%m.%d %H:%M'), 'key': key},
                                  'work': self.work[key]
                                  }
        elif '3' in data:
            key, language = data['3']
            self.work[key][language] = ''

        elif '4' in data:
            key, row, column, text = data['4']
            self.work[key].iloc[row, column] = text

    def get_project_json(self, pid):
        project = dict(self.projects[pid])
        project['work'] = self.work[pid].to_json()
        return project


