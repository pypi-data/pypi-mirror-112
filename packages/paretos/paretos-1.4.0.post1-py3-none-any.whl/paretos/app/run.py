import logging
import multiprocessing
from os import name as os_name

from .create_app import create_app


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def import_application():
    import paretos.app.src.application as app

    return app


def run(
    data_source_name: str,
    logger: logging.Logger,
    dashboard_host: str,
    dashboard_port: str,
):
    app = create_app(data_source_name)

    # TODO Gunicorn needs python package fcntl which is not available on windows
    if os_name == "nt":
        app.run(host=dashboard_host, port=dashboard_port)
    else:
        options = {
            "bind": "%s:%s" % (dashboard_host, dashboard_port),
            "workers": number_of_workers(),
            "loglevel": logging.getLevelName(logger.getEffectiveLevel()),
        }
        application_module = import_application()

        application = application_module.Application(app, options)
        application.run()
