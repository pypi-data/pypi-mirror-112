"""Utility functions for the library.
"""
from typing import Any, Optional, Union

# type aliases
ActionArgs = Optional[list[Union[list[Any], dict[str, Any]]]]


def give_action_args(action_args: ActionArgs) -> tuple[list[Any], dict[str, Any]]:
    """Takes provided `action_args`, which may contains either list of `args` and
    dict of `kwargs` or both and returns them in the tuple.

    If either of those is not in the `action_args`, they are represented as `[]` or `{}`
    in the returned `<tuple>`

    Args:
        action_args (ActionArgs): action args needed for the action to be successfully
        triggered

    Returns:
        tuple[list[Any], dict[str, Any]]: returned `args` and `kwargs` in the tuple
    """
    args_: list[Any] = []
    kwargs_: dict[str, Any] = {}

    if action_args:
        for arg in action_args:
            if isinstance(arg, list):
                args_ = arg
            else:
                kwargs_ = arg

    return (args_, kwargs_)
