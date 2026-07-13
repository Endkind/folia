from functools import wraps
from inspect import Parameter, signature
from typing import Any, Callable, ParamSpec, TypeVar

from pydantic import ValidationError
from result import Err, Result

P = ParamSpec("P")
T = TypeVar("T")


def validation_error_to_result(
    function: Callable[P, Result[T, str]],
) -> Callable[P, Result[T, str]]:
    function_signature = signature(function)

    positional_parameters = [
        parameter.name
        for parameter in function_signature.parameters.values()
        if parameter.kind
        in (
            Parameter.POSITIONAL_ONLY,
            Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]

    def format_location(location: tuple[Any, ...]) -> str:
        if not location:
            return "input"

        first, *remaining = location

        if isinstance(first, int) and first < len(positional_parameters):
            formatted = positional_parameters[first]
        else:
            formatted = str(first)

        for part in remaining:
            if isinstance(part, int):
                formatted += f"[{part}]"
            else:
                formatted += f".{part}"

        return formatted

    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, str]:
        try:
            return function(*args, **kwargs)
        except ValidationError as exc:
            details = "; ".join(
                f"{format_location(error['loc'])}: {error['msg']}"
                for error in exc.errors(include_url=False)
            )
            return Err(details)

    return wrapper
