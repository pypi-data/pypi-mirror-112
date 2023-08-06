from typing import Callable, Union, Any
import re
from tqdm import tqdm
from copy import copy

import pandas as pd

from .ipython_snippet import _seq_pprinter_factory, _dict_pprinter_factory

def filter_name_regex(list_of_objects, pattern):
    if len(list_of_objects) == 0:
        return []
    elif hasattr(list_of_objects[0], 'name'):
        # assume if one has it, all do
        return FunctionalList(filter(
            lambda obj: re.search(pattern, obj.name) is not None,
            list_of_objects))
    else:
        raise ValueError("Objects in list do not have a `name` attribute")

def list_to_df(list_,
               entry_to_record: Callable,
               filterfunc: Union[Callable[[Any], bool], None]=None,
               progress: bool=False, default_index: bool=True,
               **from_records_kwargs):
    """
    Returns a pandas dataframe representation of runs in this search. Runs are
    transformed into records and forwarded to `pandas.DataFrame.from_records`,
    along with optional keyword arguments. An optional `filterfunc` can be
    given that maps `Run` objects to booleans, and only the `True` objects will
    be put into the dataframe. If `default_index` is true, then a column `id`
    is created from Run.id of runs, and set to be the dataframe index.
    """
    if filterfunc is not None:
        list_ = filter(filterfunc, list_)
    if default_index:
        def _entry_to_record(entry):
            record = entry_to_record(entry)
            record['id'] = entry.id
            return record
    else:
        _entry_to_record = entry_to_record
    if not progress:
        records = map(_entry_to_record, list_)
    else:
        records = [
            _entry_to_record(entry)
            for entry in tqdm(list_)
        ]
    if default_index:
        from_records_kwargs = copy(from_records_kwargs)
        from_records_kwargs['index'] = 'id'
    return pd.DataFrame.from_records(records, **from_records_kwargs)

def _map(self, _mapfunc):
    return self.__class__(map(_mapfunc, self))

def _filter(self, _filterfunc):
    return self.__class__(filter(_filterfunc, self))

def _parse_sorted_positional_args(*args):
    kwargs = {}
    if len(args) > 0:
        kwargs['key'] = args[0]
        if len(args) > 1:
            kwargs['reverse'] = args[1]
    return kwargs

def _sorted(self, *args, **kwargs):
    complete_kwargs = {
        **_parse_sorted_positional_args(*args),
        **kwargs
    }
    return self.__class__(sorted(self, **complete_kwargs))

def _parse_min_max_positional_args(*args):
    kwargs = {}
    if len(args) > 0:
        kwargs['key'] = args[0]
        if len(args) > 1:
            kwargs['default'] = args[1]
    return kwargs

def _min(self, *args, **kwargs):
    complete_kwargs = {
        **_parse_min_max_positional_args(*args),
        **kwargs
    }
    return min(self, **complete_kwargs)

def _max(self, *args, **kwargs):
    complete_kwargs = {
        **_parse_min_max_positional_args(*args),
        **kwargs
    }
    return max(self, **complete_kwargs)

def _latest(self):
    """Helper attribute for lists of elements with a `start_time`
    attribute."""
    if not all(hasattr(obj, 'start_time') for obj in self):
        raise AttributeError("Not all elements have `start_time` attribute.")
    return self.max(lambda x: x.start_time)

class FunctionalList(list):
    """Helper class to make dealing with lists of things easier.

    It allows for chaining function calls for handy functions like map or
    filter with dot notation.
    """
    map = _map
    filter = _filter
    max = _max
    min = _min
    sorted = _sorted
    to_df = list_to_df
    name_regex = filter_name_regex
    latest = property(_latest)

    def get(self, filter_func):
        """Returns the first item which passes the filter, or None if none
        does."""
        for idx in range(len(self)):
            if filter_func(self[idx]):
                return self[idx]
        return None

    def __repr__(self):
        return "FunctionalList({})".format(super().__repr__())

    def __add__(self, other):
        # To ensure commutativity, addition is defined as following:
        #  - The sum of two FunctionalLists is a FunctionalList
        #  - The sum of one FunctionalList and normal list is a normal list
        # If we just always cast the output of __add__ to be a FunctionalList, then
        # the output type in case of list + FunctionalList will depend on the
        # order of arguments.
        if isinstance(other, FunctionalList):
            added = super().__add__(other)
            return FunctionalList(added)
        else:
            return super().__add__(other)

    # ipython pretty print
    _repr_pretty_  = _seq_pprinter_factory("FunctionalList([", "])")

def _attr_item(item):
    if isinstance(item, dict):
        return AttrDict(item)
    elif isinstance(item, list):
        return AttrList(item)
    elif isinstance(item, tuple):
        return AttrTuple(item)
    else:
        return item

class AttrDict(dict):
    """Helper class for accessing entries of dictionaries like attributes
    (dict.attr) instead of square brackets (dict[attr]).
    """
    def __getattr__(self, attr):
        return self[attr]

    def __getitem__(self, key):
        item = super().__getitem__(key)
        return _attr_item(item)

    def _ipython_key_completions_(self):
        return self.keys()

    def __repr__(self):
        return "AttrDict({})".format(super().__repr__())

    # ipython pretty print
    _repr_pretty_  = _dict_pprinter_factory("AttrDict({", "})")

class AttrList(list):
    """Helper class which ensures that dictionaries inside of it are AttrDicts."""
    def __getitem__(self, idx):
        item = super().__getitem__(idx)
        return _attr_item(item)

    def __repr__(self):
        return "AttrList({})".format(super().__repr__())

    # ipython pretty print
    _repr_pretty_  = _seq_pprinter_factory("AttrList([", "])")

class AttrTuple(list):
    """Helper class which ensures that dictionaries inside of it are AttrDicts."""
    def __getitem__(self, idx):
        item = super().__getitem__(idx)
        return _attr_item(item)

    def __repr__(self):
        return "AttrTuple({})".format(super().__repr__())

    # ipython pretty print
    _repr_pretty_  = _seq_pprinter_factory("AttrTuple((", "))")
