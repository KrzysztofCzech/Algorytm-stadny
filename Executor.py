from __future__ import annotations

import json
from typing import Type, List, Optional, Tuple,Union, TypeVar
import numpy as np
from dataclasses import dataclass, field, replace
from jmetal.core.algorithm import Algorithm
from tqdm import tqdm
from Agent import Agent
import matplotlib.pyplot as plt

S = TypeVar('S')
R = TypeVar('R')

def plot_average_series_results(
    series_results: List[Optional[PlotSeries]]
) -> None:
    xs = np.array([p.xs for p in series_results if p is not None]).mean(axis=0)
    all_ys = np.array([p.ys for p in series_results if p is not None])
    label = [p.label for p in series_results if p is not None][0]
    ys = np.mean(all_ys, axis=0)
    if all_ys.shape[0] > 1:
        y_err = np.std(all_ys, axis=0)
        _, _, bars = plt.errorbar(xs, ys, label=label, yerr=y_err)
        [bar.set_alpha(0.35) for bar in bars]
    else:
        plt.plot(xs, ys, label=label)

def plot_algorithm_results(
    drawing_properties: DrawingProperties,
    series: List[List[Optional[PlotSeries]]]
) -> None:
    plt.figure(figsize=drawing_properties.fig_size)
    for s in series:
        plot_average_series_results(series_results=s)
    plt.title(drawing_properties.title)
    plt.xlabel(drawing_properties.x_label)
    plt.ylabel(drawing_properties.y_label)
    plt.legend()
    if drawing_properties.target_location is not None:
        plt.savefig(drawing_properties.target_location)
    if drawing_properties.verbose:
        plt.show()


@dataclass
class DrawingProperties:
    title: str
    x_label: str = "Iterations"
    y_label: str = "Fitness"
    fig_size: Tuple[int, int] = (16, 9)
    target_location: Optional[str] = None
    verbose: bool = True


@dataclass
class PlotSeries:
    xs: Union[np.ndarray, List[Union[int, float]]]
    ys: Union[np.ndarray, List[Union[int, float]]]
    label: str

@dataclass
class ExecutionResult:
    success: bool
    algorithm_name: str
    solution: Optional[R] = None
    fitness: Optional[List[float]] = None
    execution_time: Optional[float] = None
    error_description: Optional[str] = None


class ExecutionHistory:
    run_results: List[List[ExecutionResult]] = field(default_factory=list)

    def register_run_results(
        self,
        results: List[List[ExecutionResult]]
    ) -> ExecutionHistory:
        new_run_results = self.run_results
        new_run_results.extend(results)
        return replace(self, run_results=new_run_results)


class MultiAlgorithmRunner:

    def __init__(
        self,
        execution_units: Optional[List[Agent]] = None,
        drawing_properties: Optional[DrawingProperties] = None
    ):
        if execution_units is None:
            self.__execution_units: List[Agent] = []
        else:
            self.__execution_units = execution_units
        self.__drawing_properties = drawing_properties

    def register_running_unit(self, running_unit: Agent) -> None:
        self.__execution_units.append(running_unit)

    def run_all(self, iterations = 100) -> ExecutionHistory:
        execution_history = ExecutionHistory()
        global_plot_series = []
        for execution_unit in tqdm(self.__execution_units):
            run_results, plot_series = self.__run_execution_unit(execution_unit=execution_unit, iterations = iterations)
            execution_history = execution_history.register_run_results(
                results=run_results
            )
            global_plot_series.extend(plot_series)
        if self.__drawing_properties is not None and len(global_plot_series) > 0:
            plot_algorithm_results(
                drawing_properties=self.__drawing_properties,
                series=global_plot_series
            )
        return execution_history

    def __run_execution_unit(
        self,
        execution_unit: Agent,
        iterations: int
    ) -> Tuple[List[List[ExecutionResult]], List[List[Optional[PlotSeries]]]]:
        run_results, plot_series = [], []
        run_result, plot_serie = self.__repeat_algorithm_execution(execution_unit=execution_unit, iterations = iterations)
        run_results.append(run_result)
        plot_series.append(plot_serie)
        return run_results, plot_series

    def __repeat_algorithm_execution(
        self,
        execution_unit: Agent,
        iterations: int
    ) -> Tuple[List[ExecutionResult], List[Optional[PlotSeries]]]:
        result, plot_serie = self.__execute_algorithm(execution_unit=execution_unit, iterations= iterations)
        return result, plot_serie

    def __execute_algorithm(
        self,
        execution_unit: Agent,
        iterations: int
    ) -> Tuple[ExecutionResult, Optional[PlotSeries]]:
        try:
            execution_unit.run(iterations)
            result = execution_unit.get_result()
            algorithm = execution_unit.Island.get_algorithm()
            plot_series = execution_unit.drawing_fun(
                algorithm, execution_unit.drawing_series_labels
            ) if execution_unit.drawing_fun is not None else None
            return ExecutionResult(
                success=True,
                algorithm_name=algorithm.get_name(),
                problem_name=execution_unit.problem_name,
                solution=result.variables,
                fitness=result.objectives,
                execution_time=algorithm.total_computing_time
            ), plot_series
        except Exception as e:
            error_description = f"Error of type: {type(e)} occurred. Cause: {e}"
            return ExecutionResult(
                success=False,
                algorithm_name=execution_unit.algorithm_cls.__name__,
                problem_name=execution_unit.problem_name,
                error_description=error_description
            ), None
