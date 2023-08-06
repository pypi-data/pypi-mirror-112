from typing import Union

from .....database.sqlite_dashboard_persistence import SQLiteDashboardPersistence
from .....optimization import Evaluations
from .....optimization.project_status import Done
from ...command_handler.command_handler import CommandHandler
from ...command_handler.outcome.outcome import Outcome
from ...service.logger import Logger


class Get(CommandHandler):
    _methods = ["POST"]

    def __init__(self, logger: Logger, persistence: SQLiteDashboardPersistence):
        self.__logger = logger
        self.__persistence = persistence

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        self.__logger.info("getting projects", projects_input={})
        projects = self.__persistence.get_projects()

        result_projects = []

        # TODO: Add Status / Measurement how to see if it is finished?
        for project in projects:
            project_data, evaluations = self.__persistence.load_project_data_by_id(
                project.get_id()
            )

            status = project.get_status()
            n_status = 0.0

            if project_data is None:
                raise RuntimeError("There are no data for this project available")

            if type(status) is Done:
                n_status = 100.0

            evaluations = Evaluations(evaluations.get_pareto_optimal_evaluations())

            problem = project_data.get_optimization_problem()
            kpis = [kpi.get_name() for kpi in problem.get_kpi_space()]
            result_projects.append(
                {
                    "id": project.get_id(),
                    "description": None,
                    "name": project.get_name(),
                    "targets": kpis,
                    "status": n_status,
                    "number_pareto": evaluations.size(),
                }
            )

        return {"projects": result_projects}
