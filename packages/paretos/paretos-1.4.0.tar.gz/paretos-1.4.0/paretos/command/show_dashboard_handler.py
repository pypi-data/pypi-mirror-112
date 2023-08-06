from logging import Logger

from paretos.app.run import run


class ShowDashboardHandler:
    def __init__(
        self,
        data_source_name: str,
        logger: Logger,
        dashboard_host: str,
        dashboard_port: str,
    ):
        self.__data_source_name = data_source_name
        self.__logger = logger
        self.__dashboard_host = dashboard_host
        self.__dashboard_port = dashboard_port

    def show(self) -> None:
        run(
            data_source_name=self.__data_source_name,
            logger=self.__logger,
            dashboard_host=self.__dashboard_host,
            dashboard_port=self.__dashboard_port,
        )
