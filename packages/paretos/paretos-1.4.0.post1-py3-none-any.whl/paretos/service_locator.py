from paretos import Config
from paretos.command.export_handler import ExportHandler
from paretos.command.obtain_handler import ObtainHandler
from paretos.command.optimize_handler import OptimizeHandler
from paretos.command.show_dashboard_handler import ShowDashboardHandler
from paretos.database.sqlite_database import SQLiteDatabase
from paretos.database.sqlite_persistence import SQLitePersistence
from paretos.socrates.socrates_api_client import SocratesApiClient
from paretos.socrates.socrates_api_http_session import SocratesApiHttpSession
from paretos.socrates.socrates_request_mapper import SocratesRequestMapper
from paretos.socrates.socrates_response_mapper import SocratesResponseMapper


class ServiceLocator:
    def __init__(self, config: Config):
        data_source_name = config.get_data_source_name()
        database = SQLiteDatabase(data_source_name=data_source_name)
        persistence = SQLitePersistence(database=database)
        logger = config.get_logger()
        api_session = SocratesApiHttpSession(
            api_url=config.get_api_url(),
            customer_token=config.get_customer_token(),
            logger=logger,
        )
        request_mapper = SocratesRequestMapper()
        response_mapper = SocratesResponseMapper()
        api_client = SocratesApiClient(
            session=api_session,
            request_mapper=request_mapper,
            response_mapper=response_mapper,
        )

        self.__optimize_handler = OptimizeHandler(
            logger=logger, persistence=persistence, api_client=api_client
        )

        self.__export_handler = ExportHandler(
            logger=logger, data_source_name=data_source_name
        )

        self.__obtain_handler = ObtainHandler(logger=logger, persistence=persistence)

        self.__show_dashboard_handler = ShowDashboardHandler(
            data_source_name=data_source_name,
            logger=logger,
            dashboard_host=config.get_dashboard_host(),
            dashboard_port=config.get_dashboard_port(),
        )

    @property
    def optimize_handler(self) -> OptimizeHandler:
        return self.__optimize_handler

    @property
    def export_handler(self) -> ExportHandler:
        return self.__export_handler

    @property
    def obtain_handler(self) -> ObtainHandler:
        return self.__obtain_handler

    @property
    def show_dashboard_handler(self) -> ShowDashboardHandler:
        return self.__show_dashboard_handler
