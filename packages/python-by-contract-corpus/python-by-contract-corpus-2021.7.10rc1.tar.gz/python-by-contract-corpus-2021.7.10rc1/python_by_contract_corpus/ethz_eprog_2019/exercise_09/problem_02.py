"""Reverse a linked list (extension from Exercise 6, Problem 4)."""
from typing import Optional

from icontract import ensure, snapshot

from python_by_contract_corpus.ethz_eprog_2019.exercise_06.problem_04 import (
    LinkedList,
    Node,
)


class ReversibleLinkedList(LinkedList):
    """Extend a :py:class:`LinkedList` with reverse operation."""

    # fmt: off
    @snapshot(lambda self: list(self.values()), name="values")
    @snapshot(lambda self: self.count(), name="count")
    @ensure(
        lambda self, OLD:
        list(self.values()) == list(reversed(OLD.values))
    )
    @ensure(
        lambda self, OLD:
        self.count() == OLD.count
    )
    # fmt: on
    def reverse(self) -> None:
        """Reverse the elements of the list."""
        prev = None  # type: Optional[Node]
        cur = self._first

        while cur is not None:
            old_next_node = cur.next_node
            cur.next_node = prev

            prev = cur
            cur = old_next_node

        old_first = self._first
        self._first = self._last
        self._last = old_first
