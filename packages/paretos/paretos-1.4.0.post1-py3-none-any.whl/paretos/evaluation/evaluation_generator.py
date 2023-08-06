from logging import Logger
from typing import List

from .. import OptimizationProblem
from ..database.sqlite_persistence import SQLitePersistence
from ..optimization import Evaluation, Evaluations, Project
from ..socrates.socrates_api_client import SocratesApiClient


class EvaluationGenerator:
    """
    Provides new evaluations by fetching designs from the Socrates API and
    saving them to the database.
    """

    def __init__(
        self,
        api_client: SocratesApiClient,
        persistence: SQLitePersistence,
        problem: OptimizationProblem,
        project: Project,
        logger: Logger,
    ):
        self.__api_client = api_client
        self.__problem = problem
        self.__persistence = persistence
        self.__project = project
        self.__logger = logger

    def generate(
        self, existing_evaluations: Evaluations, quantity: int
    ) -> List[Evaluation]:
        self.__logger.debug(
            "Fetching new designs from Socrates API", extra={"quantity": quantity}
        )
        designs = self.__api_client.predict_design(
            problem=self.__problem, evaluations=existing_evaluations, quantity=quantity
        )

        new_evaluations = [Evaluation(design=design) for design in designs]

        self.__persistence.save_planned_evaluations(
            evaluations=new_evaluations, project=self.__project
        )

        return new_evaluations
