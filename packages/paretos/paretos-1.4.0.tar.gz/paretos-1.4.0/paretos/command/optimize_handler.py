from logging import Logger
from typing import List, Optional, Union

from .. import (
    CONTINUITY_DISCRETE,
    AsyncEnvironmentInterface,
    EnvironmentInterface,
    KpiGoalMaximum,
    KpiGoalMinimum,
    OptimizationProblem,
    TerminatorInterface,
    optimization,
)
from ..database.exceptions import ProjectAlreadyExists
from ..database.sqlite_persistence import SQLitePersistence
from ..evaluation.evaluation_generator import EvaluationGenerator
from ..evaluation.evaluator import Evaluator
from ..evaluation.kpi_sanitizer import KpiSanitizer
from ..evaluation.scheduler import Scheduler
from ..evaluation.supervisor import Supervisor
from ..socrates.socrates_api_client import SocratesApiClient


class OptimizeHandler:
    def __init__(
        self,
        logger: Logger,
        persistence: SQLitePersistence,
        api_client: SocratesApiClient,
    ):
        self.__logger = logger
        self.__persistence = persistence
        self.__api_client = api_client

    async def optimize_async(
        self,
        name: str,
        optimization_problem: OptimizationProblem,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
        terminators: Optional[List[TerminatorInterface]] = None,
        n_parallel: int = 1,
        max_number_of_runs: int = 10000,
        resume: bool = False,
    ) -> None:
        """
        Main function the user calls when optimizing with socrates
        :param name: project name which will be added to database then!
        :param optimization_problem: hyper space definition of the problem
        :param environment: simulation environment to use for the execution
            :param terminators: list of all terminator functions which can lead to stop
        :param n_parallel: Number of parallel simulations that can be run on customer side
        :param max_number_of_runs: Absolute maximum to have hard stopping criteria
        :param resume: Set to true to resume the optimization if it already exists.
        """

        project = None
        evaluations = optimization.Evaluations()

        if resume:
            (
                project,
                previous_evaluations,
            ) = self.__persistence.load_project_data_by_name(project_name=name)

            for previous_evaluation in previous_evaluations.get_evaluations():
                evaluations.add_evaluation(evaluation=previous_evaluation)

        if project is None:
            problem = self.__create_problem_definition(optimization_problem)
            project = optimization.Project(name=name, problem=problem)

            try:
                self.__persistence.save_project(project)
            except ProjectAlreadyExists as already_exists_error:
                self.__logger.error(
                    msg="Project already exists. Set the resume parameter to continue "
                    "an already started project or use a different project name.",
                    extra={"project_name": project.get_name()},
                )

                raise already_exists_error

            self.__logger.info(
                "Started optimization project.",
                extra={
                    "projectId": project.get_id(),
                    "projectName": project.get_name(),
                },
            )
        else:
            self.__logger.info(
                "Resuming project.", extra={"projectName": project.get_name()}
            )

        if terminators is None:
            terminators = [optimization.DefaultTerminator()]

        await self.__optimize(
            project=project,
            evaluations=evaluations,
            terminators=terminators,
            max_number_of_runs=max_number_of_runs,
            n_parallel=n_parallel,
            environment=environment,
        )

    def __create_problem_definition(
        self, definition: OptimizationProblem
    ) -> optimization.OptimizationProblem:

        design_parameters = []
        kpi_parameters = []

        for definition_kpi_parameter in definition.get_kpi_parameters():
            name = definition_kpi_parameter.get_name()
            goal_string = definition_kpi_parameter.get_goal()

            if goal_string == KpiGoalMinimum:
                parameter_goal = optimization.goals.Minimum()
            elif goal_string == KpiGoalMaximum:
                parameter_goal = optimization.goals.Maximum()
            else:
                raise RuntimeError("Unexpected KPI parameter goal.")

            kpi_parameter = optimization.kpi.KpiParameter(
                name=name, goal=parameter_goal
            )

            kpi_parameters.append(kpi_parameter)

        for definition_design_parameter in definition.get_design_parameters():
            interface_continuity = definition_design_parameter.get_continuity()
            continuity = optimization.design.continuity.Continuous()

            if interface_continuity == CONTINUITY_DISCRETE:
                continuity = optimization.design.continuity.Discrete()

            design_parameter = optimization.design.DesignParameter(
                name=definition_design_parameter.get_name(),
                minimum=definition_design_parameter.get_minimum(),
                maximum=definition_design_parameter.get_maximum(),
                continuity=continuity,
            )

            design_parameters.append(design_parameter)

        design_space = optimization.design.DesignSpace(design_parameters)
        kpi_space = optimization.kpi.KpiSpace(kpi_parameters)

        return optimization.OptimizationProblem(
            design_space=design_space, kpi_space=kpi_space
        )

    async def __optimize(
        self,
        project: optimization.Project,
        evaluations: optimization.Evaluations,
        terminators: List[TerminatorInterface],
        max_number_of_runs: int,
        n_parallel: int,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
    ):
        problem = project.get_optimization_problem()

        kpi_sanitizer = KpiSanitizer(
            kpi_space=problem.get_kpi_space(), logger=self.__logger
        )

        evaluator = Evaluator(
            logger=self.__logger,
            environment=environment,
            persistence=self.__persistence,
            kpi_sanitizer=kpi_sanitizer,
        )

        generator = EvaluationGenerator(
            api_client=self.__api_client,
            problem=problem,
            logger=self.__logger,
            persistence=self.__persistence,
            project=project,
        )

        supervisor = Supervisor(
            api_client=self.__api_client,
            terminators=terminators,
            logger=self.__logger,
            problem=problem,
        )

        scheduler = Scheduler(
            logger=self.__logger,
            max_number_of_evaluations=max_number_of_runs,
            max_parallel=n_parallel,
            evaluation_collection=evaluations,
            evaluator=evaluator,
            evaluation_generator=generator,
            supervisor=supervisor,
        )

        await scheduler.run()

        self.__logger.info("Optimization finished.")

        project.finish()

        try:
            self.__persistence.update_project_status(project)
        except Exception as project_status_update_failed:
            self.__logger.error("Unable to set project to finished.")
            raise project_status_update_failed

        self.__logger.info("Analyzing result.")

        pareto_optimal_ids = self.__api_client.get_pareto_optimal_evaluation_ids(
            problem, evaluations
        )

        for evaluation in evaluations.get_evaluations():
            is_pareto_optimal = evaluation.get_id() in pareto_optimal_ids
            evaluation.update_pareto_optimality(is_pareto_optimal)

        self.__persistence.update_evaluation_pareto_states(evaluations=evaluations)

        self.__logger.info(
            "Result analyzed.",
            extra={
                "evaluations": len(evaluations.get_evaluations()),
                "paretoPoints": len(evaluations.get_pareto_optimal_evaluations()),
            },
        )
