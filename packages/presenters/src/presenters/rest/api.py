from fastapi import FastAPI
from logger.log import get_logger_from_env
from presenters.rest.controllers.agent_controller import router as agent_router
from presenters.rest.controllers.auth_controller import router as auth_router

log = get_logger_from_env(__file__)

app = FastAPI(
    title="Agents Service API",
    description="API for managing agents and authentication.",
    version="1.0.0",
)

# Register routers
app.include_router(agent_router)
app.include_router(auth_router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint for service status check."""
    return {
        "message": "Welcome to Agents Service!",
        "auth_info": "Use `/auth/login` to get a token before accessing `/agents`",
    }


@app.on_event("shutdown")
def shutdown_event():
    log.info("REST API shutting down... Cleaning up resources.")
