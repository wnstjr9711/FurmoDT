from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.project_manager import ProjectManager

router = APIRouter()
PM = ProjectManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_client = websocket.client
    while True:
        try:
            data = await websocket.receive_json()

            post_data = data['POST']
            if post_data:
                PM.save(post_data, ws_client)

            # 클라이언트 작업 참여 정보
            room = data['GET']
            if room:
                ret = PM.join(ws_client, room)
            else:
                ret = PM.default_connection(ws_client)

            await websocket.send_json(ret)

        except WebSocketDisconnect:
            PM.default_connection(ws_client)
            break
