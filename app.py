# -*-coding: utf-8 -*-


import websockets
import asyncio
import json
from project_manager import ProjectManager

ret = {"project": {},
       "caption": {}}


# 클라이언트 접속이 되면 호출된다.
async def accept(websocket, path):
    data = await websocket.recv()
    print("receive : " + data)
    await websocket.send("echo : " + json.dumps(ret))

if __name__ == "__main__":
    pm = ProjectManager()
    # 비동기로 서버를 대기한다.
    start_server = websockets.serve(accept, "0.0.0.0", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
