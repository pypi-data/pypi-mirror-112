import logging
import os
from pathlib import Path
from typing import Callable

from dependency_injector import containers, providers
from flask import Flask

from ...database.sqlite_dashboard_persistence import SQLiteDashboardPersistence
from ...database.sqlite_database import SQLiteDatabase
from ...version import VERSION
from .request_handler.jsend import JSend
from .request_handler.request_handler import RequestHandler
from .routes.project_meta.get import Get as ProjectMetaGet
from .routes.projects.get import Get as ProjectsGet
from .routes.solutions.get import Get as SolutionsGet
from .service.error_handler import ErrorHandler
from .service.logger import Logger
from .service.request_id_provider import RequestIdProvider


class Container(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    App: Callable[[], Flask] = providers.Singleton(
        Flask, "Data API", template_folder=Path(dir_path).parent / "templates"
    )

    Request_Id_Provider: Callable[[], RequestIdProvider] = providers.Singleton(
        RequestIdProvider
    )

    Version_Obj: Callable[[], str] = providers.Object(VERSION)

    Logger_Obj: Callable[[], logging.Logger] = providers.Singleton(
        Logger, request_id_provider=Request_Id_Provider, api_version=Version_Obj
    )

    JSend = providers.Singleton(
        JSend, request_id_provider=Request_Id_Provider, api_version=Version_Obj
    )

    ErrorHandler = providers.Singleton(
        ErrorHandler, application_protocol=JSend, logger=Logger_Obj
    )

    SQLiteDatabase = providers.Singleton(
        SQLiteDatabase, data_source_name=config.data_source_name.required()
    )

    SQLiteDashboardPersistence = providers.Singleton(
        SQLiteDashboardPersistence, database=SQLiteDatabase
    )

    RequestHandler = providers.Singleton(
        RequestHandler,
        application_protocol=JSend,
        logger=Logger_Obj,
    )

    Projects_Get: Callable[[], ProjectsGet] = providers.Factory(
        ProjectsGet, logger=Logger_Obj, persistence=SQLiteDashboardPersistence
    )

    Project_Meta_Get: Callable[[], ProjectMetaGet] = providers.Factory(
        ProjectMetaGet, logger=Logger_Obj, persistence=SQLiteDashboardPersistence
    )

    Solutions_Get: Callable[[], SolutionsGet] = providers.Factory(
        SolutionsGet, logger=Logger_Obj, persistence=SQLiteDashboardPersistence
    )
