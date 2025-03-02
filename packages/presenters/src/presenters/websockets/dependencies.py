from presenters.websockets.websocket_manager import WebSocketManager


def get_websocket_manager() -> WebSocketManager:
    """
    Provide the WebSocket manager instance.
    """
    return WebSocketManager()
