import pandas as pd
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))


class ProjectManager:
    def __init__(self):
        self.client = dict()  # key: websocket.client, value: room
        self.projects = dict()

    def join(self, ws_client, room):
        if ws_client not in self.projects[room]['worker']:
            self.projects[room]['worker'][ws_client] = list()
            self.client[ws_client] = room

            full_data = dict(self.projects[room])
            full_data['work'] = self.projects[room]['work'].to_json()
            full_data['worker'] = None
            return full_data
        else:
            update = self.projects[room]['worker'][ws_client]
            partial_data = {'update': list(), 'header': list(self.projects[room]['work'])}
            while update:
                partial_data['update'].append(update.pop())
            return partial_data

    def default_connection(self, ws_client):
        if ws_client in self.client:
            self.projects[self.client[ws_client]]['worker'].pop(ws_client)
            self.client.pop(ws_client)
        return list(self.projects)

    def save(self, data, ws_client):
        """
        :param data: {1: create_project, 2: delete_project, 3: add_language, 4: update_work}
        :param ws_client: websocket.client
        """
        if '0' in data:
            pass
        elif '1' in data:
            pid, url, video = data['1']
            num = 1
            while pid in self.projects:
                pid = pid + '({})'.format(num)
            header = ['TC_IN', 'TC_OUT', '원어']
            work = pd.DataFrame([['' for i in range(len(header))] for j in range(9999)], columns=header)
            self.projects[pid] = {'metadata': {'url': url, 'video': video, 'date': datetime.now(KST).strftime('%Y.%m.%d %H:%M')},
                                  'work': work,
                                  'worker': dict()
                                  }
        elif '3' in data:
            room = self.client[ws_client]
            language = data['3'][0]
            self.projects[room]['work'][language] = ''

        elif '4' in data:
            room = self.client[ws_client]
            for data in data['4']:
                row, column, text = data
                self.projects[room]['work'].iloc[row, column] = text
                for client in self.projects[room]['worker']:
                    self.projects[room]['worker'][client].append((row, column, text))



