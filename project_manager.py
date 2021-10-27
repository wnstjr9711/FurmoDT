from datetime import datetime, timezone, timedelta
import pandas as pd

KST = timezone(timedelta(hours=9))


class ProjectManager:
    def __init__(self):
        self.client = dict()  # key: websocket.client, value: room
        self.projects = dict()

    def join(self, ws_client, room, client_id):
        if ws_client not in self.projects[room]['worker']:
            self.projects[room]['worker'][ws_client] = list()
            self.client[ws_client] = dict()
            self.client[ws_client]['room'] = room
            self.client[ws_client]['client_id'] = client_id
            self.client[ws_client]['cell'] = None

            full_data = dict(self.projects[room])
            full_data['work'] = self.projects[room]['work'].to_json()
            full_data['worker'] = list()
            return full_data
        else:
            update = self.projects[room]['worker'][ws_client]
            partial_data = {'update': list(), 'header': list(self.projects[room]['work'])}
            while update:
                partial_data['update'].append(update.pop(0))
            partial_data['worker'] = [{self.client[i]['client_id']: self.client[i]['cell']}
                                      for i in self.projects[room]['worker']]

            return partial_data

    def default_connection(self, ws_client):
        if ws_client in self.client:
            self.projects[self.client[ws_client]['room']]['worker'].pop(ws_client)
            self.client.pop(ws_client)
        return list(self.projects)

    def save(self, data, ws_client):
        """
        :param data: {1: create_project, 2: delete_project,
                      3: add_language, 4: delete_language,
                      5: update_work, 6: update_cur_cell}
        :param ws_client: websocket.client
        """
        if '0' in data:
            pass
        elif '1' in data:
            pid, url, video = data['1']
            num = 1
            if pid in self.projects:
                while '{} ({})'.format(pid, num) in self.projects:
                    num += 1
                pid = '{} ({})'.format(pid, num)
            header = ['TC_IN', 'TC_OUT', '원어']
            work = pd.DataFrame([['' for i in range(len(header))] for j in range(9999)], columns=header)
            self.projects[pid] = {
                'metadata': {'url': url, 'video': video, 'date': datetime.now(KST).strftime('%Y.%m.%d %H:%M')},
                'work': work,
                'worker': dict()
                }
        elif '3' in data:
            room = self.client[ws_client]['room']
            language = data['3'][0]
            self.projects[room]['work'][language] = ''

        elif '4' in data:
            room = self.client[ws_client]['room']
            language = data['4'][0]
            del self.projects[room]['work'][language]

        elif '5' in data:
            room = self.client[ws_client]['room']
            for d in data['5']:
                row, column, text = d
                self.projects[room]['work'].iloc[row, column] = text
                for client in self.projects[room]['worker']:
                    self.projects[room]['worker'][client].append((row, column, text))

        if '6' in data:
            if ws_client in self.client:
                self.client[ws_client]['cell'] = data['6']

