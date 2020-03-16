import functools


def exception(logger, reraise=False):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

            # re-raise the exception
            if reraise:
                raise

        return wrapper

    return decorator