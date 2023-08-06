from typing import Union

from .....database.sqlite_dashboard_persistence import SQLiteDashboardPersistence
from .....optimization import Evaluations
from ...command_handler.command_handler import CommandHandler
from ...command_handler.outcome.not_found_failure import NotFoundFailure
from ...command_handler.outcome.outcome import Outcome
from ...service.logger import Logger
from ...service.response_mapper import DataApiResponseMapper


class Get(CommandHandler):
    _methods = ["POST"]
    _schema = {
        "type": "object",
        "properties": {
            "project": {"type": "string"},
            "only_paretos": {"type": "boolean"},
        },
        "required": ["project"],
    }

    def __init__(self, logger: Logger, persistence: SQLiteDashboardPersistence):
        self.__logger = logger
        self.__persistence = persistence

    def process(self, request_data: dict) -> Union[dict, Outcome]:

        only_paretos = True

        if "only_paretos" in request_data.keys():
            only_paretos = request_data["only_paretos"]

        self.__logger.info(
            "getting project solutions",
            solutions_input={
                "project": request_data["project"],
                "only_paretos": only_paretos,
            },
        )

        project, evaluations = self.__persistence.load_project_data_by_id(
            request_data["project"]
        )

        if not project:
            return NotFoundFailure()

        if only_paretos:
            evaluations = Evaluations(evaluations.get_pareto_optimal_evaluations())

        return {
            "evaluations": DataApiResponseMapper.evaluations_to_request(evaluations)
        }
