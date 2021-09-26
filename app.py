# -*-coding: utf-8 -*-

import websockets
from websockets.exceptions import ConnectionClosedError
import asyncio
import json
from project_manager import ProjectManager

PM = ProjectManager()

# 한국시간


# 클라이언트 접속이 되면 호출된다.
async def accept(websocket, path):
    while True:
        try:
            data = await websocket.recv()
            data = json.loads(data)
            print("receive : " + str(data))

            # 변경사항
            post_data = data['POST']
            if post_data:
                PM.save(post_data)

            # 프로젝트 리스트 or 선택한 프로젝트 작업 반환
            pid = data['GET']
            ret = list(PM.projects.keys()) if not pid else PM.projects[pid]
            await websocket.send(json.dumps(ret))
        except ConnectionClosedError:
            break


if __name__ == "__main__":
    # 비동기로 서버를 대기한다.
    start_server = websockets.serve(accept, "0.0.0.0", 9998)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
