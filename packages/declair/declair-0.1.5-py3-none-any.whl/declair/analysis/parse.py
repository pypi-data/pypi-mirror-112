"""
This module contains code for sieving through a Declair/Sacred runs directory
to find individual hyperparameter search runs.

Much of the code here is borrowed from
https://gitlab.com/k-cybulski/deepsolaris-declair/-/blob/master/results_analysis.py
"""
import os
import functools
import jsonpickle
from dateutil.parser import isoparse
from typing import List, Callable, Union, Any
from sys import version_info
import re

import pandas as pd
from declair import Environment
from declair.env import get_cwd_env
from declair.const import (DEF_KEY_EXPERIMENT_NAME,
    DEF_STORED_RUN_CONFIG_NAME, DEF_STORED_SEARCH_CONFIG_NAME,
    DEF_KEY_SEARCH_PARAMS)
from declair.search.grid import define_gridsearch_runs

from .functional import list_to_df, FunctionalList, AttrDict

# These filenames are never artifacts, they're created by Declair/Sacred
NON_ARTIFACT_NAMES = {
    'metrics.json', 'config.json', 'run.json', 'cout.txt',
    DEF_STORED_RUN_CONFIG_NAME, DEF_STORED_SEARCH_CONFIG_NAME
}

def cached_property(func):
    # cached_property was introduced in 3.8, however we want to be compatible
    # with 3.5. So, this is a little hack to maintain compatibility and similar
    # behaviour.
    try:
        return functools.cached_property(func)
    except AttributeError:
        return property(functools.lru_cache(maxsize=1)(func))

class Artifact:
    def __init__(self, path):
        self._name = os.path.basename(path)
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "<Artifact: {}>".format(self.name)

class Run:
    """A single training/experiment run.

    Args:
        path    - Path to the run directory.
    """

    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @cached_property
    def id(self):
        return int(os.path.basename(self.path))

    @cached_property
    def _sacred_run(self):
        with open(os.path.join(self.path, 'run.json')) as file_:
            return jsonpickle.loads(file_.read())

    @property
    def sacred_run(self):
        return AttrDict(self._sacred_run)

    @cached_property
    def _definition(self):
        with open(os.path.join(self.path, DEF_STORED_RUN_CONFIG_NAME)) as file_:
            return jsonpickle.loads(file_.read())

    @property
    def definition(self):
        return AttrDict(self._definition)

    @cached_property
    def _search_definition(self):
        try:
            with open(os.path.join(self.path, DEF_STORED_SEARCH_CONFIG_NAME)) as file_:
                return jsonpickle.loads(file_.read())
        except:
            return None

    @property
    def search_definition(self):
        if self._search_definition is not None:
            return AttrDict(self._search_definition)

    @cached_property
    def metrics_full(self):
        with open(os.path.join(self.path, 'metrics.json')) as file_:
            return jsonpickle.loads(file_.read())

    @cached_property
    def metrics(self):
        return AttrDict({
            metric_name: dict_['values']
            for metric_name, dict_ in self.metrics_full.items()
        })

    def metric_last(self, metric_name):
        """
        Returns last metric value, or None if metric is not found.
        """
        if metric_name in self.metrics:
            return self.metrics[metric_name][-1]
        else:
            return None

    def metric_best(self, metric_name, order_func):
        """
        Returns the best metric value obtained in this run. Order func decides
        what "best" means, i.e. `max` or `min` (or some other function that
        takes a list and returns the "best" item).
        """
        if metric_name in self.metrics:
            return order_func(self.metrics[metric_name])
        else:
            return None

    @cached_property
    def start_time(self):
        return isoparse(self.sacred_run['start_time'])

    @cached_property
    def search_start_time(self):
        if self.search_definition is None:
            return None
        else:
            if 'execute_time' in self.search_definition:
                return isoparse(self.search_definition['execute_time'])
            else:
                return None

    @cached_property
    def name(self):
        return self.definition[DEF_KEY_EXPERIMENT_NAME]

    @cached_property
    def _artifacts(self):
        return tuple(sorted([
            Artifact(entry.path)
            for entry in os.scandir(self.path)
            if entry.name not in NON_ARTIFACT_NAMES
            and entry.is_file()
        ], key=lambda artifact: artifact.name))

    @property
    def artifacts(self):
        """Returns a FunctionalList of Artifact objects."""
        return FunctionalList(self._artifacts)

    def artifacts_regex(self, pattern):
        return self.artifacts.name_regex(pattern)

    @cached_property
    def is_completed(self):
        return self.sacred_run['status'] == 'COMPLETED'

    def __repr__(self):
        # This representation breaks official recommendations, since the
        # representation it returns should be directly _parseable_ into a Run
        # object in a REPL. However, this representation makes managing stuff
        # easier in an interactive manner, so here it is.
        is_comleted_str = "completed" if self.is_completed else "not completed"
        return "<Run: {}, {}, {}, {}>".format(self.path,
                                        self.name, self.start_time, is_comleted_str)

def _planned_runs(search_definition):
    if search_definition['mode'] == 'grid':
        runs_per_configuration = search_definition.get(
            DEF_KEY_SEARCH_PARAMS, {}).get('runs_per_configuration', 1)
        # cast to dict because define_gridsearch_runs checks for dict type
        return len(define_gridsearch_runs(dict(search_definition))) * runs_per_configuration
    elif search_definition['mode'] == 'hyperopt':
        return search_definition[DEF_KEY_SEARCH_PARAMS]['fmin_kwargs']['max_evals']
    else:
        raise ValueError("Invalid search definition, has no 'mode' entry")

class Search:
    """A search composed of multiple runs, e.g. grid or hyperopt search."""
    def __init__(self, runs):
        self._start_time = runs[0].search_start_time
        assert all(run.search_start_time == self._start_time for run in runs)
        self._runs = tuple(sorted(runs, key=lambda run: run.id)) # tuple for immutability

    @property
    def start_time(self):
        return self._start_time

    @property
    def runs(self):
        return FunctionalList(self._runs)

    @cached_property
    def definition(self):
        return self._runs[0].search_definition

    @cached_property
    def runs_completed(self):
        return tuple(
            filter(
                lambda x: x.is_completed,
                self._runs
            )
        )

    def to_df(self,
              run_to_record: Callable,
              filter_func: Union[Callable[[Run], bool], None]=None,
              progress: bool=False, default_index: bool=True,
              **from_records_kwargs):
        return list_to_df(self._runs,
                          run_to_record,
                          filter_func,
                          progress=progress,
                          default_index=default_index,
                          **from_records_kwargs)

    @cached_property
    def count_completed(self):
        return len(
            list(
                filter(
                    lambda x: x.is_completed,
                    self._runs
                )
            )
        )

    @cached_property
    def count_started(self):
        return len(
            self._runs
        )
        

    @cached_property
    def count_planned(self):
        return _planned_runs(self.definition)

    @cached_property
    def name(self):
        if len(self._runs) > 0:
            return self.definition[DEF_KEY_EXPERIMENT_NAME]
        else:
            return None

    def __repr__(self):
        # Going against __repr__ recommendations like Run
        return "<Search: {}, {}, {} completed/{} started/{} planned runs>".format(
            self.name, self.start_time, self.count_completed, self.count_started, self.count_planned)

def _is_scandir_entry_a_run(candidate_entry: os.DirEntry):
    return (
        candidate_entry.is_dir()
        and os.path.isfile(os.path.join(candidate_entry.path, 'run.json'))
    )

def runs_from_dir(dir_path=None):
    if dir_path is None:
        env = get_cwd_env()
        try:
            dir_path = env['observers']['file']['path']
        except KeyError:
            raise ValueError("dir_path not given but environment does not define a file observer path")
    return FunctionalList([
        Run(candidate.path)
        for candidate in os.scandir(dir_path)
        if _is_scandir_entry_a_run(candidate)
    ])

def list_runs_env(env: Environment):
    root_dir = env.get_nested_key(['observers', 'file', 'path'])
    return runs_from_dir(root_dir)

def searches_runs_from_run_list(run_list: List[Run]):
    """
    Aggregates a list of runs into searches within which these runs were
    executed and standalone runs, which were executed without a search. Returns
    a list of searches and a list of standalone runs.
    """
    standalone_runs = []
    searches = {}
    for run in run_list:
        search_start_time = run.search_start_time
        if search_start_time is None:
            standalone_runs.append(run)
        else:
            if search_start_time in searches:
                searches[search_start_time].append(run)
            else:
                searches[search_start_time] = [run]
    standalone_runs = sorted(standalone_runs, key=lambda x: x.start_time)
    searches = [
        Search(runs)
        for runs in searches.values()
    ]
    searches = sorted(searches, key=lambda x: x.start_time)
    return FunctionalList(searches), FunctionalList(standalone_runs)

def searches_runs_from_dir(dir_path=None):
    """
    Returns a FunctionalList of searches and another of runs without searches
    from a given directory, or the default taken from the local Declair config
    (`declair_env.yaml`) if not given.
    """
    if dir_path is None:
        env = get_cwd_env()
        try:
            dir_path = env['observers']['file']['path']
        except KeyError:
            raise ValueError("dir_path not given but environment does not define a file observer path")
    return searches_runs_from_run_list(
        runs_from_dir(dir_path)
    )

def searches_from_run_list(run_list: List[Run]):
    """
    Aggregates a list of runs into searches within which these runs were
    executed. Returns a list of searches. Runs without searches are ignored.
    """
    searches, runs = searches_runs_from_run_list(run_list)
    return searches

def searches_from_dir(dir_path=None):
    """
    Returns a FunctionalList of searches from a given directory, or the default
    taken from the local Declair config (`declair_env.yaml`) if not given. Runs
    without searches are ignored.
    """
    searches, runs = searches_runs_from_dir(dir_path)
    return searches
