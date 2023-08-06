from icontract import require, ensure


@require(lambda loop_size: loop_size >= 0)
@require(lambda subject: subject >= 0)
@ensure(lambda result: 0 <= result < 20201227)
def transform(subject: int, loop_size: int) -> int:
    """Transform the ``subject`` in ``loop_size`` steps of a hard-coded algorithm."""
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value


# fmt: off
@require(lambda subject: subject >= 0)
@ensure(
    lambda result, subject, public_key:
    not (result != -1) or transform(subject, result) == public_key
)
# fmt: on
def deduce_loop_size(subject: int, public_key: int) -> int:
    """
    Deduce the loop size for ``public_key`` by transforming the ``subject``.

    :return: The loop size, or -1 if no success
    """
    value = 1
    for loop_ct in range(100000000):
        if value == public_key:
            return loop_ct
        value *= subject
        value %= 20201227
    return -1


@require(lambda door_public_key: door_public_key >= 0)
@require(lambda card_public_key: card_public_key >= 0)
def deduce_encryption_key(door_public_key: int, card_public_key: int) -> int:
    """Figure out the subject number."""
    card_loop_size = deduce_loop_size(7, card_public_key)
    return transform(door_public_key, card_loop_size)
