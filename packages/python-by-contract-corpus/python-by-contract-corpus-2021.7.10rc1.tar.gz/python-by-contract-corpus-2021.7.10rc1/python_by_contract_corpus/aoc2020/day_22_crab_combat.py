import re
from typing import Tuple, List, Sequence, overload, Union, Final, Iterator

from icontract import require, ensure, DBC


# crosshair: on


class Deck(DBC):
    """Represent a deck of cards.

    Please make sure that you transfer the "ownership" immediately to ``Deck``
    and don't modify the original list of strings any more:

       .. code-block:: python

           ##
           # OK
           ##

           deck = Deck([1, 2, 3])

           ##
           # Not OK
           ##

           cards = [1, 2, 3]
           deck = Deck(cards)
           # ... do something assuming ``deck`` is immutable ...

           cards[0] = 2
           # ERROR! cards[0] now breaks the invariant!

    """

    cards: Final[Sequence[int]]  #: Cards in the deck

    @require(lambda cards: all(card >= 0 for card in cards))
    @require(lambda cards: len(set(cards)) == len(cards), "Unique cards")
    def __init__(self, cards: Sequence[int]) -> None:
        """Initialize with the given values."""
        self.cards = cards

    @overload
    def __getitem__(self, index: int) -> int:
        """Get the item at the given integer index."""
        raise NotImplementedError("Only for type annotation.")

    @overload
    def __getitem__(self, index: slice) -> "Deck":
        """Get the slice of the deck."""
        raise NotImplementedError("Only for type annotation.")

    def __getitem__(self, index: Union[int, slice]) -> Union[int, "Deck"]:
        """Get the card(s) at the given index."""
        if isinstance(index, slice):
            return Deck(cards=self.cards[index])
        else:
            return self.cards[index]

    def __len__(self) -> int:
        """Return the number of the cards in the deck."""
        return len(self.cards)

    def __iter__(self) -> Iterator[int]:
        """Iterate through the cards in the deck."""
        return self.cards.__iter__()

    # fmt: off
    @require(
        lambda self, other:
        (
                sum := list(self.cards) + other.cards,
                len(set(sum)) == len(sum)
        )[1],
        "Unique cards after the addition")
    # fmt: on
    def __add__(self, other: "Deck") -> "Deck":
        """Join two decks together."""
        sum_of_cards = list(self.cards)
        sum_of_cards.extend(other.cards)
        return Deck(cards=sum_of_cards)

    def __repr__(self) -> str:
        """Represent the deck for easier debugging."""
        return repr(self.cards)

    def __eq__(self, other: object) -> bool:
        """
        Compare with ``other`` by :py:attr:`.cards`.

        If ``other`` is not a :py:class:`Deck` or :py:class:`List:, propagate to generic
        ``__eq__``.
        """
        if isinstance(other, Deck):
            return self.cards.__eq__(other.cards)
        elif isinstance(other, list):
            return self.cards.__eq__(other)
        else:
            return object.__eq__(self, other)


class Split(DBC):
    """Represent a split of one big deck of cards into two sub-decks."""

    deck1: Final[Deck]  #: The deck for the player 1
    deck2: Final[Deck]  #: The deck for the player 2

    @require(
        lambda deck1, deck2: not set(deck1).intersection(deck2), "No overlapping cards"
    )
    def __init__(self, deck1: Deck, deck2: Deck) -> None:
        """Initialize with the given values."""
        self.deck1 = deck1
        self.deck2 = deck2


# fmt: off
@require(lambda split: len(split.deck1) > 0, "Not game over for player 1")
@require(lambda split: len(split.deck2) > 0, "Not game over for player 2")
@ensure(
    lambda split, result:
    set(split.deck1).union(split.deck2) == set(result.deck1).union(result.deck2),
    "No new cards"
)
@ensure(
    lambda split, result:
    split.deck1[1:] == result.deck1[0:len(split.deck1) - 1],
    "Only the prefix and the suffix of the deck 1 change"
)
@ensure(
    lambda split, result:
    split.deck2[1:] == result.deck2[0:len(split.deck2) - 1],
    "Only the prefix and the suffix of the deck 2 change"
)
@ensure(
    lambda split, result:
    (
            len(split.deck1) == len(result.deck1) + 1
            and len(split.deck2) == len(result.deck2) - 1)
    or (
            len(split.deck1) == len(result.deck1) - 1
            and len(split.deck2) == len(result.deck2) + 1),
    "Either lost or won two cards"
)
# fmt: on
def play_a_round(split: Split) -> Split:
    """
    Play a round of the game given the current ``split``.

    :return: A new split after the round
    """
    card1 = split.deck1[0]
    card2 = split.deck2[0]

    if card1 > card2:
        new_deck1 = split.deck1[1:] + Deck([card1, card2])
        new_deck2 = split.deck2[1:]
    else:
        new_deck1 = split.deck1[1:]
        new_deck2 = split.deck2[1:] + Deck([card2, card1])

    result = Split(deck1=new_deck1, deck2=new_deck2)

    return result


# fmt: off
@require(
    lambda lines:
    all(
        re.match(r'^(Player 1:|Player 2:|0|[1-9][0-9]*|)\Z', line)
        for line in lines
    )
)
# fmt: on
@require(lambda lines: 'Player 2:' in lines[1:])
@require(lambda lines: lines[0] == 'Player 1:')
@require(lambda lines: len(lines) > 3)
def parse_lines(lines: List[str]) -> Tuple[List[int], List[int]]:
    """Parse the input lines into two decks, as list of cards."""
    deck1 = []  # type: List[int]
    deck2 = []  # type: List[int]

    target_deck = deck1

    for line in lines[1:]:
        if line == '':
            pass
        elif line == 'Player 2:':
            target_deck = deck2
        else:
            target_deck.append(int(line))

    return deck1, deck2


@ensure(lambda result: result >= 0)
def compute_score(deck: Deck) -> int:
    """Compute the score for the given deck based on its cards."""
    score = 0
    for i, card in enumerate(deck):
        score += (len(deck) - i) * card

    return score


# fmt: off
@require(lambda split: len(split.deck1) > 0, "Not game over for player 1")
@require(lambda split: len(split.deck2) > 0, "Not game over for player 2")
@ensure(
    lambda split, result:
    (
            len(split.deck1) + len(split.deck2) == len(result.deck1)
            and len(result.deck2) == 0
    )
    or (
            len(result.deck1) == 0
            and len(split.deck1) + len(split.deck2) == len(result.deck2)
    )
)
@ensure(
    lambda split, result:
    set(split.deck1).union(split.deck2) == set(result.deck1).union(result.deck2)
)
# fmt: on
def play(split: Split) -> Split:
    """Play the game starting with the ``split`` until one of the players wins."""
    while True:
        split = play_a_round(split=split)

        if len(split.deck1) == 0 or len(split.deck2) == 0:
            break

    return split
