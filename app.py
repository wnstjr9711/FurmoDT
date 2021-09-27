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
            print("receive : " + str(data))
            post_data = data['POST']
            if post_data:
                PM.save(post_data)

            pid = data['GET']
            ret = list(PM.projects.keys()) if not pid else PM.get_project_json(pid)
            await websocket.send_json(ret)

        except WebSocketDisconnect:
            break
