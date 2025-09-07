from fastapi import APIRouter, Request, HTTPException
from http import HTTPStatus
from .run import generate_valuation
from .utils import adjust_parameters_input_to_api
import asyncio
import logging
import time
from datetime import datetime

########################################################
# VARIABLES
########################################################

router = APIRouter(prefix="/dcf")
logger = logging.getLogger(__name__)

########################################################
# GENERATE DCF VALUATION
########################################################

from pydantic import BaseModel

class InputList(BaseModel):
    input_list: list

async def monitor_client_disconnection(request, request_id):
    """Monitor if client disconnects during processing"""
    try:
        while True:
            await asyncio.sleep(0.1)  # Check every 100ms
            if await request.is_disconnected():
                logger.warning(f"[REQUEST {request_id}] Client disconnected detected")
                return True
    except Exception:
        return True

@router.post("", status_code=HTTPStatus.OK)
async def generate_dcf_valuation(input_list: InputList, request: Request):
    request_id = id(request)
    start_time = time.time()
    start_datetime = datetime.now().isoformat()
    
    logger.info(f"[REQUEST {request_id}] DCF valuation request started at {start_datetime}")
    logger.info(f"[REQUEST {request_id}] Client IP: {request.client.host if request.client else 'unknown'}")
    
    try:
        monte_carlo_input, shares_outstanding = adjust_parameters_input_to_api(input_list.input_list)
        logger.info(f"[REQUEST {request_id}] Parameters adjusted successfully")
        
        logger.info(f"[REQUEST {request_id}] Starting valuation generation")
        
        # Create the executor task
        loop = asyncio.get_event_loop()
        valuation_task = loop.run_in_executor(None, generate_valuation, monte_carlo_input, shares_outstanding)
        
        # Create a monitoring task for client disconnection
        monitor_task = asyncio.create_task(monitor_client_disconnection(request, request_id))
        
        # Wait for either completion or client disconnection
        done, pending = await asyncio.wait(
            [valuation_task, monitor_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel any pending tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Check which task completed first
        if valuation_task in done:
            try:
                charts = await valuation_task
                end_time = time.time()
                duration = end_time - start_time
                logger.info(f"[REQUEST {request_id}] Valuation completed successfully in {duration:.2f} seconds")
                return charts
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                logger.error(f"[REQUEST {request_id}] Valuation failed after {duration:.2f} seconds: {str(e)}")
                raise
        else:
            # Client disconnected
            end_time = time.time()
            duration = end_time - start_time
            logger.warning(f"[REQUEST {request_id}] REQUEST CANCELLED - Client disconnected after {duration:.2f} seconds")
            logger.warning(f"[REQUEST {request_id}] Cancellation occurred at {datetime.now().isoformat()}")
            raise HTTPException(status_code=499, detail="Request cancelled by client")
            
    except HTTPException:
        # Re-raise HTTP exceptions (including our cancellation exception)
        raise
    except Exception as e:
        # Handle other errors
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"[REQUEST {request_id}] ERROR occurred after {duration:.2f} seconds: {str(e)}")
        logger.error(f"[REQUEST {request_id}] Error type: {type(e).__name__}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")