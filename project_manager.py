import pandas as pd
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))


class ProjectManager:
    def __init__(self):
        self.client = dict()  # key: websocket.client, value: room
        self.projects = dict()

    def join(self, websocket, room):
        if websocket.client not in self.projects[room]['worker']:
            self.projects[room]['worker'][websocket.client] = list()
            self.client[websocket.client] = room

            full_data = dict(self.projects[room])
            full_data['work'] = self.projects[room]['work'].to_json()
            full_data['worker'] = None
            return full_data
        else:
            update = self.projects[room]['worker'][websocket.client]
            partial_data = {'update': list(), 'header': list(self.projects[room]['work'])}
            while update:
                partial_data['update'].append(update.pop())
            return partial_data

    def default_connection(self, websocket):
        if websocket.client in self.client:
            self.projects[self.client[websocket.client]]['worker'].pop(websocket.client)
            self.client.pop(websocket.client)
        return list(self.projects)

    def save(self, data):
        """
        :param data: {1: create_project, 2: delete_project, 3: add_language, 4: update_work}
        """
        if '0' in data:
            pass
        elif '1' in data:
            # TODO key 값 중복일때 예외처리
            room, url, video = data['1']
            header = ['TC_IN', 'TC_OUT', '원어']
            work = pd.DataFrame([['' for i in range(len(header))] for j in range(9999)], columns=header)
            self.projects[room] = {'metadata': {'url': url, 'video': video, 'date': datetime.now(KST).strftime('%Y.%m.%d %H:%M')},
                                   'work': work,
                                   'worker': dict()
                                   }
        elif '3' in data:
            room, language = data['3']
            self.projects[room]['work'][language] = ''

        elif '4' in data:
            room, row, column, text = data['4']
            self.projects[room]['work'].iloc[row, column] = text
            for client in self.projects[room]['worker']:
                self.projects[room]['worker'][client].append((row, column, text))



