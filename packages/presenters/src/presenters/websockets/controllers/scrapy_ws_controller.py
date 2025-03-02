import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from application.usecases.agentic.orchestrator_usecase import OrchestratorUseCase

log = logging.getLogger("scrapy_ws_controller")
router = APIRouter()

# Instantiate the orchestrator use case once.
orchestrator_usecase = OrchestratorUseCase()


@router.websocket("/ws/scrapy/{bot_name}")
async def websocket_scrapy(websocket: WebSocket, bot_name: str):
    """
    Unprotected WebSocket endpoint for receiving scraping payloads.
    The URL includes the bot's name for identification.
    This endpoint processes the payload via the Orchestrator Use Case and streams back the generated report.
    """
    await websocket.accept()
    log.info(f"Scrapy WebSocket connection accepted for bot: {bot_name}")
    try:
        while True:
            data = await websocket.receive_text()
            log.debug(f"Received payload from bot '{bot_name}': {data}")

            # Assume the payload is JSON formatted.
            payload = json.loads(data)

            # Process the payload through the Orchestrator Use Case.
            report = await orchestrator_usecase.process_bot_payload(bot_name, payload)
            log.debug(f"Generated report for bot '{bot_name}': {report}")

            # Send the final report back to the client.
            await websocket.send_json(report)
    except WebSocketDisconnect:
        log.info(f"Bot '{bot_name}' WebSocket disconnected.")


@router.websocket("/ws/scrapy/{bot_name}/errors")
async def websocket_scrapy_errors(websocket: WebSocket, bot_name: str):
    """
    Unprotected WebSocket endpoint for receiving error payloads.
    The URL includes the bot's name for identification.
    This endpoint processes the error payload and logs it locally.
    """
    await websocket.accept()
    log.info(f"Scrapy Error WebSocket connection accepted for bot: {bot_name}")
    try:
        while True:
            data = await websocket.receive_text()
            log.debug(f"Received error payload from bot '{bot_name}': {data}")

            # Assume the payload is JSON formatted.
            payload = json.loads(data)
            report = await orchestrator_usecase.process_bot_payload(bot_name, payload)
            log.debug(f"Generated error report for bot '{bot_name}': {report}")
            # Log the error message locally.
            log.error(f"Error from bot '{bot_name}': {payload['error']}")
    except WebSocketDisconnect:
        log.info(f"Bot '{bot_name}' Error WebSocket disconnected.")
