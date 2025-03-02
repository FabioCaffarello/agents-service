from fastapi import FastAPI
from logger.log import get_logger_from_env
from presenters.websockets.controllers.auth_ws_controller import (
    router as auth_ws_router,
)
from presenters.websockets.controllers.scrapy_ws_controller import (
    router as scrapy_ws_router,
)

log = get_logger_from_env(__file__)

app = FastAPI(title="Agents WebSocket API")

# Register WebSocket routes
app.include_router(auth_ws_router)
app.include_router(scrapy_ws_router)


@app.on_event("shutdown")
def shutdown_event():
    log.info("WebSocket server shutting down... Cleaning up connections.")
