from .utils import monte_carlo_valuator_multi_phase, valuation_describer
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_valuation(monte_carlo_input, shares_outstanding):
    start_time = time.time()
    start_datetime = datetime.now().isoformat()
    
    logger.info(f"[VALUATION] Starting scenario generation at {start_datetime}")
    
    try:
        logger.info(f"[VALUATION] Running Monte Carlo simulation...")
        df_valuation = monte_carlo_valuator_multi_phase(**monte_carlo_input)
        logger.info(f"[VALUATION] Monte Carlo simulation completed. Generated {len(df_valuation)} scenarios")
        
        logger.info(f"[VALUATION] Generating charts and descriptions...")
        charts = valuation_describer(
            df_valuation,
            sharesOutstanding=shares_outstanding
        )
        
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"[VALUATION] Valuation generation completed successfully in {duration:.2f} seconds")
        logger.info(f"[VALUATION] Generated {len(charts)} chart objects")
        
        return charts
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"[VALUATION] ERROR in valuation generation after {duration:.2f} seconds: {str(e)}")
        logger.error(f"[VALUATION] Error type: {type(e).__name__}")
        raise