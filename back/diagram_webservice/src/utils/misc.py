import os
from dotenv import dotenv_values
from aliases import ENV_DEVELOPMENT_PATH

# Load development environment files if it exists and production mode is off
# This environment variable is set in docker-compose.yml

# For slightly decluttering flask routes
def check_debug(error):
    if bool(os.getenv("DEBUG")):
        return f"500 - {error}"
    return 500

