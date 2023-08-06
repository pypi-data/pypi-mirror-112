from logging import Logger

from paretos import OptimizationResultInterface, optimization
from paretos.database.sqlite_persistence import SQLitePersistence
from paretos.exceptions import ProjectNotFoundError
from paretos.export import OptimizationResult


class ObtainHandler:
    def __init__(self, logger: Logger, persistence: SQLitePersistence):
        self.__logger = logger
        self.__persistence = persistence

    def obtain(self, name: str) -> OptimizationResultInterface:
        done_evaluations = optimization.Evaluations()

        project, previous_evaluations = self.__persistence.load_project_data_by_name(
            project_name=name
        )

        if project is None:
            self.__logger.error("Project not found.", extra={"projectName": name})

            raise ProjectNotFoundError()

        if not isinstance(project.get_status(), optimization.project_status.Done):
            self.__logger.warning(
                "Optimization was not finished correctly, data might be incomplete."
            )

        for previous_evaluation in previous_evaluations.get_evaluations():
            if previous_evaluation.get_kpis() is not None:
                done_evaluations.add_evaluation(evaluation=previous_evaluation)

        return OptimizationResult(done_evaluations)
