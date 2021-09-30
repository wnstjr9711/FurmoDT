# -*-coding: utf-8 -*-
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from project_manager import ProjectManager

app = FastAPI()

PM = ProjectManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()

            post_data = data['POST']
            if post_data:
                PM.save(post_data)

            # 클라이언트 작업 참여 정보
            room = data['GET']
            if room:
                ret = PM.join(websocket, room)
            else:
                ret = PM.default_connection(websocket)

            await websocket.send_json(ret)

        except WebSocketDisconnect:
            PM.default_connection(websocket)
