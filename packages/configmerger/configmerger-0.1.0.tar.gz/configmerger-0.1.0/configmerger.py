# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import itertools

class Merger:
    connect_list: bool = True
    skip_none_when_filter: bool = True

    def merge(self, values: List[Any]):
        'merge multi values, latest have highest priority.'
        return self._merge_core((), values)

    def _merge_core(self, keys: Tuple[Union[str, int]], values: List[Any]):
        if not values:
            raise ValueError
        trimed_values = self._trim_none_from_end(values)
        if not trimed_values:
            return None
        last_value = trimed_values[-1]
        if not self._should_merge(keys, trimed_values):
            return last_value
        if isinstance(last_value, dict):
            return self._merge_for_dict(keys, trimed_values)
        if isinstance(last_value, list):
            return self._merge_for_list(keys, trimed_values)
        return self._merge_for_object(keys, trimed_values)

    def _should_merge(self, keys: Tuple[Union[str, int]], values: List[Any]):
        return len(values) > 1

    def _merge_for_dict(self, keys: Tuple[Union[str, int]], values: List[Any]):
        rv = {}
        typed_values = self._get_typed_values_from_end(keys, values, (dict, ))
        values_keys = set(itertools.chain(*typed_values))
        for k in values_keys:
            rv[k] = self._merge_core(keys + (k, ), [tv.get(k) for tv in typed_values])
        return rv

    def _merge_for_list(self, keys: Tuple[Union[str, int]], values: List[Any]):
        return self._connect_list(
            keys,
            self._get_typed_values_from_end(keys, values, (list, ))
        )

    def _connect_list(self, keys: Tuple[Union[str, int]], values: List[Any]):
        assert len(values) > 0, 'it should never be empty.'

        if not self.connect_list:
            return values[-1]
        rv = []
        for val in reversed(values):
            rv.extend(val)
        return rv

    def _merge_for_object(self, keys: Tuple[Union[str, int]], values: List[Any]):
        return values[-1]

    def _get_typed_values_from_end(self, keys: Tuple[Union[str, int]], values: List[Any], types: Tuple[type, ...]):
        rv = []
        for value in reversed(values):
            if isinstance(value, types):
                rv.append(value)
            elif self.skip_none_when_filter and value is None:
                continue
            else:
                break
        rv.reverse()
        return rv

    @staticmethod
    def _trim_none_from_end(items: list):
        tl = len(items)
        assert tl > 0
        for i in range(tl):
            if items[-1-i] is not None:
                return items[:tl-i]
        return []
