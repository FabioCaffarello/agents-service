from fastapi import WebSocket
from typing import List


class WebSocketManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection on disconnect."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Broadcast a message to all WebSocket clients."""
        for connection in self.active_connections:
            await connection.send_text(message)
