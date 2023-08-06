from logging import Logger
from typing import List

from .. import OptimizationProblem, TerminatorInterface
from ..optimization import Evaluations
from ..socrates.socrates_api_client import SocratesApiClient


class Supervisor:
    """
    Decides whether more evaluations should be started or not.
    """

    def __init__(
        self,
        api_client: SocratesApiClient,
        terminators: List[TerminatorInterface],
        logger: Logger,
        problem: OptimizationProblem,
    ):
        self.__api_client = api_client
        self.__terminators = terminators
        self.__logger = logger
        self.__problem = problem

    def is_process_finished(self, evaluations: Evaluations):
        try:
            progress = self.__api_client.track_progress(
                problem=self.__problem, evaluations=evaluations
            )
        except Exception as api_tracking_error:
            self.__logger.error("Unable to update optimization progress.")
            raise api_tracking_error

        is_process_finished = any(
            [
                terminator.should_terminate(progress=progress)
                for terminator in self.__terminators
            ]
        )

        return is_process_finished
