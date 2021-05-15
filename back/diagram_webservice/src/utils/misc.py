import os
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
