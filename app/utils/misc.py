from functools import wraps


def exception(logger, reraise=False):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"There was an exception in {func.__name__}")
            if reraise:
                raise

        return wrapper

    return decorator
