import os
from dotenv import load_dotenv
from .aliases import ENV_DEVELOPMENT_PATH

# Load development environment files if it exists and production mode is off
# This environment variable is set in docker-compose.yml

# For slightly decluttering flask routes
def check_debug(error):
    """Used in flask endpoints. Returns an error message depending on a DEBUG environment variable

    :param error: Generic exception
    :type error: Exception
    :return: Error code. Includes error message if debug. Returns either int or string.
    :rtype: int or String.
    """
    if bool(os.getenv("DEBUG")):
        return f"500 - {error}"
    return 500


def load_variables():
    """Checks for environment variable called "CONTAINERIZED_VARIABLES"
    This variable is set in the container upon execution.
    It's basically like a switch which will make the project load the environment variables,
    which are set in the docker compose file instead of the .env files.
    """
    if not os.getenv("CONTAINERIZED_VARIABLES"):
        load_dotenv(ENV_DEVELOPMENT_PATH)
