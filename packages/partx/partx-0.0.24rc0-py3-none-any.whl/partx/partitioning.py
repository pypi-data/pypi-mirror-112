from __future__ import annotations

from datetime import datetime
from typing import List, Sequence
from enum import IntEnum

from staliro.options import StaliroOptions
from staliro.optimizers import ObjectiveFn, Optimizer, Run
from staliro.results import StaliroResult

import pathlib

from .models import SamplingMethod, PartitioningOptions, PartitioningResult, PartXBehavior
from .continued_sampling import part_optimize_with_continued_sampling
from .controlled_budget import part_optimize_with_controlled_budget

def _optimize(func: ObjectiveFn, options: StaliroOptions, optimizer_options: PartitioningOptions) -> PartitioningRun:
    subregions = [bound.astuple() for bound in options.bounds]
    start_time = datetime.now()

    replications = 50
    iterations = 100
    if optimizer_options.continue_sampling_budget is not None:
        result = part_optimize_with_continued_sampling(
            subregion_file=optimizer_options.subregion_file,
            subregion=subregions,
            region_dimension=optimizer_options.region_dimension,
            num_partition=optimizer_options.num_partition,
            confidence_level=0.05,
            func=func,
            num_sampling=optimizer_options.num_sampling,
            levels=optimizer_options.level,
            replications=replications,
            iterations=iterations,
            min_volume=optimizer_options.min_volume,
            budget=optimizer_options.max_budget,
            fal_num=optimizer_options.fal_num,
            n_model=optimizer_options.n_model,
            n_bo=optimizer_options.n_bo,
            n_b=optimizer_options.n_b,
            sample_method=optimizer_options.sample_method,
            part_num=optimizer_options.part_num,
            continue_sampling_budget=optimizer_options.continue_sampling_budget,
            seed=None
        )
    else:
        result = part_optimize_with_controlled_budget(
            subregion_file=optimizer_options.subregion_file,
            subregion=subregions,
            region_dimension=optimizer_options.region_dimension,
            num_partition=optimizer_options.num_partition,
            confidence_level=0.05,
            func=func,
            num_sampling=optimizer_options.num_sampling,
            levels=optimizer_options.level,
            replications=replications,
            iterations=iterations,
            min_volume=optimizer_options.min_volume,
            budget=optimizer_options.max_budget,
            fal_num=optimizer_options.fal_num,
            n_model=optimizer_options.n_model,
            n_bo=optimizer_options.n_bo,
            n_b=optimizer_options.n_b,
            sample_method=optimizer_options.sample_method,
            part_num=optimizer_options.part_num,
            seed=None
        )

    end_time = datetime.now()

    partitioning_result = PartitioningResult(
        result.seed,
        start_time - end_time,
        result.theta_plus,
        result.theta_minus,
        result.theta_undefined,
        result.evl,
        result.budgets,
        result.falsification_volumes,
        result.p_iter,
        result.number_subregion,
        result.fal_ems)

    return partitioning_result


def partitioning(
    func: ObjectiveFn,
    options: StaliroOptions,
    optimizer_options: PartitioningOptions
) -> List[PartitioningResult]:
    return _optimize(func, options, optimizer_options)

class PartX(Optimizer[Run]):
    def __init__(self, **kwargs):
        self.optimizer_options = PartitioningOptions(
            subregion_file=kwargs['subregion_file'],
            region_dimension=kwargs['region_dimension'],
            num_partition=kwargs['num_partition'],
            miscoverage_level=kwargs['miscoverage_level'],
            num_sampling=kwargs['num_sampling'],
            level=kwargs['level'],
            min_volume=kwargs['min_volume'],
            max_budget=kwargs['max_budget'],
            fal_num=kwargs['fal_num'],
            n_model=kwargs['n_model'],
            n_bo=kwargs['n_bo'],
            n_b=kwargs['n_b'],
            sample_method=kwargs['sample_method'],
            part_num=kwargs['part_num'],
            continue_sampling_budget=kwargs['continue_sampling_budget']
        )


    def optimize(self, func: ObjectiveFn, 
                 options: StaliroOptions) -> PartitioningRun:
        return _optimize(func, options, self.optimizer_options)
