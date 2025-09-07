from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dcf_valuation.apis import router as dcf_valuation_router
import logging
import uvicorn
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the routers
app.include_router(dcf_valuation_router)

# Root route
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Application is running"}

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("DCF Backend application starting up")
    logger.info("Server started at %s", datetime.now().isoformat())

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("DCF Backend application shutting down")
    logger.info("Server stopped at %s", datetime.now().isoformat())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)