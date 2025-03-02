from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from security.dependencies import get_current_user_ws
from logger.log import get_logger_from_env
from presenters.websockets.websocket_manager import WebSocketManager


log = get_logger_from_env(__file__)

router = APIRouter(tags=["Authentication"])
ws_manager = WebSocketManager()


@router.websocket("/ws/auth")
async def websocket_auth(websocket: WebSocket, user=Depends(get_current_user_ws)):
    await ws_manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
            await websocket.send_json(
                {"message": f"Hello {user['sub']}! You are authenticated."}
            )
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        log.info(f"User {user['sub']} WebSocket disconnected.")
