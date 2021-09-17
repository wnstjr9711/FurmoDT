# -*-coding: utf-8 -*-
import datetime

import websockets
import asyncio
import json
from project_manager import ProjectManager

PM = ProjectManager()

# 한국시간
timezone_kst = datetime.timezone(datetime.timedelta(hours=9))


# 클라이언트 접속이 되면 호출된다.
async def accept(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    print("receive : " + str(data))

    # 프로젝트 생성
    if data['create_project']:
        k, v = map(lambda x: x[0], zip(data['create_project']))
        try:
            PM.projects[k] = {'metadata': [v, PM.getfilename(v),
                                           datetime.datetime.now(timezone_kst).strftime('%Y.%m.%d %H:%M')],
                              'work': {}}
        except:
            print("공유링크 오류")

    pid = data['get_project_work']
    # 프로젝트 리스트 반환
    if not pid:
        ret = list(map(lambda x: x['metadata'], PM.projects.values()))
    # 선택한 프로젝트 작업 반환
    else:
        ret = PM.projects[pid]['work']

    await websocket.send("echo : " + json.dumps(ret))


if __name__ == "__main__":
    pm = ProjectManager()
    # 비동기로 서버를 대기한다.
    start_server = websockets.serve(accept, "0.0.0.0", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
