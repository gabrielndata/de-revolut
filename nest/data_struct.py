import json
from collections import defaultdict, deque
from itertools import groupby
from typing import DefaultDict, Hashable

from .utils import traverse_dict, traverse_to_hashable


class NestedDefaultDict(DefaultDict):
    """ Nested default dictionary implementation. """

    def __init__(self):
        tree = lambda: defaultdict(tree)
        self._tree = tree()
        self._memo = {}
        self._node = None

    def group_by_values(self, dicts, *keys):
        """
        Fill NestedDefaultDict with data from plain dictionaries list and
        group them by selected keys values::

            nd = NestedDefaultDict()
            nd.group_by_values([{'currency': "USD", 'country': 'US'}...], 'currency', 'country'...)


        :param list[dict] dicts:        list of objects you want to group
        :param list[str] keys:          keys to group objects by. Non existing keys will be ignored
        """
        grouped = self._group_by_keys(dicts, *keys)
        self._add_nested(*grouped)

    def as_dict(self) -> dict:
        return self._tree

    def _add_nested(self, *nodes):
        """

        :param Node nodes:
        :return:
        """
        for node in nodes:

            if not isinstance(node.value, Hashable):
                if not node.prev:
                    self._tree['root'] = node.value
                else:
                    _tree = self._memo[node.prev.prev.value] if node.prev.prev else self._tree
                    _tree[node.prev.value] = [*_tree[node.prev.value], *node.value]
            else:

                if not node.prev:
                    tree = self._tree[node.value]
                else:
                    tree = self._memo[node.prev.value][node.value]

                self._memo[node.value] = tree

    def _group_by_keys(self, dicts, *keys):
        """
        Generates linked nodes with values of provided
        dictionaries grouped by provided keys

        :param list[dict] dicts:        list of objects you want to group
        :param list[str] keys:          keys to group objects by. Non existing keys will be ignored
        """

        current = self._node
        queue = deque(keys)
        if not queue:
            yield _Node(value=dicts, prev=current)
        else:
            k = queue.popleft()
            for value, group in groupby(dicts, key=lambda d: d.pop(k, None)):
                if value:
                    self._node = _Node(value, prev=current)
                    yield self._node
                yield from self._group_by_keys(list(group), *queue)

    def __setitem__(self, key, value):
        self._tree[key] = value

    def __getitem__(self, item):
        return self._tree[item]

    def __eq__(self, other):
        eq = set(traverse_to_hashable(other)) == set(traverse_to_hashable(self._tree))
        return eq

    def __delitem__(self, key):
        del self._tree[key]

    def __contains__(self, item):
        for i in self:
            if i == item:
                return True

    def __iter__(self):
        return traverse_dict(self._tree)

    def __len__(self):
        return len(self._tree)

    def __repr__(self):
        return json.dumps(self._tree, ensure_ascii=False)


class _Node:
    def __init__(self, value, prev=None):
        self.value = value
        self.prev = prev
