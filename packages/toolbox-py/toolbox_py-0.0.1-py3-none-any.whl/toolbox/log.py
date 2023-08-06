import logging



def setup_logging(name: str) -> None:
    """
    Sets up some basic logging 

    Parameter
    ----------
    name : `str`
        Name of the log file (__name__ or project name is recommended)
    """
    fmt_kwargs = {
        "format": "[{levelname:<7}] - {message}", 
        "style": "{"
    }

    logging.basicConfig(level=logging.INFO, **fmt_kwargs)

    handler = logging.FileHandler("/logs/{}.log".format(name))
    handler.setFormatter(logging.Formatter(**fmt_kwargs))

    root = logging.getLogger()
    root.addHandler(handler)