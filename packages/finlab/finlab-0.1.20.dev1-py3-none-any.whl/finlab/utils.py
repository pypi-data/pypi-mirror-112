import os
import logging

# Get an instance of a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def raise_permission_error(*args, **kwargs):
    raise Exception("Only VIP users can access backtest.sim function")

def auth_permission(allow_roles=None):
    def decorator(func):
        def warp(*args, **kwargs):
            if allow_roles is None:
                return func(*args, **kwargs)
            role = os.environ.get('role')
            if role in allow_roles:
                return func(*args, **kwargs)
            else:
                logger.error(f"Your role is {role} that don't have permission to use this function.")
        return warp
    return decorator
