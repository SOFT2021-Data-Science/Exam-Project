import os

# For slightly decluttering flask routes
def check_debug(error):
    if bool(os.getenv("DEBUG")):
        return f"500 - {error}"
    return 500
