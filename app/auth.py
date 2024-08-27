import os
import logging

logger = logging.getLogger(__name__)

def verify_api_key(app_id: str, app_key: str) -> bool:
    try:
        return app_id == os.environ.get("APP_ID") and app_key == os.environ.get("APP_KEY")
    except Exception as e:
        logger.error(f"Error verifying API key: {str(e)}", exc_info=True)
        return False