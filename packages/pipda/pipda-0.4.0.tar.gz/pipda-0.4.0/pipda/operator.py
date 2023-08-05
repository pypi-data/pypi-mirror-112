"""Provide the Operator class"""
import operator
from enum import Enum
from functools import wraps
from typing import Any, Callable, Mapping, Tuple, ClassVar, Type

from .context import ContextAnnoType, ContextBase
from .function import Function


class Operator(Function):
    """Operator class, defining how the operators in verb/function arguments
    should be evaluated

    Args:
        op: The operator
        context: Should be None while initialization. It depends on the
            verb or the function that uses it as an argument
        args: The arguments of the operator
        kwargs: The keyword arguments of the operator
        datarg: Should be False. No data argument for the operator function.

    Attributes:
        REGISTERED: The registered Operator class. It's this class by default
            Use `register_operator` as a decorator to register a operator class
    """

    REGISTERED: ClassVar[Type["Operator"]] = None

    def __init__(
        self,
        op: str,
        args: Tuple,
        kwargs: Mapping[str, Any],
        datarg: bool = False,
    ) -> None:

        self.op = op
        self.data = None
        # if the function is defined directly, use it.
        # otherwise, get one from `__getattr__`
        op_func = getattr(self, self.op, None)
        if not op_func and self.op[0] == "r":
            left_op = (
                self.op[1:]
                if self.op not in ("rand", "ror")
                else f"{self.op[1:]}_"
            )
            op_func = getattr(self, left_op, None)
            if not op_func:
                raise ValueError(
                    f"No operator function defined for {self.op!r}"
                )

            @wraps(op_func)
            def left_op_func(arg_a, arg_b, *args, **kwargs):
                return op_func(arg_b, arg_a, *args, **kwargs)

            super().__init__(left_op_func, args, kwargs, datarg)
        elif op_func:
            super().__init__(op_func, args, kwargs, datarg)
        else:
            raise ValueError(f"No operator function defined for {self.op!r}")

    @staticmethod
    def set_context(
        context: ContextAnnoType,
        extra_contexts: Mapping[str, ContextAnnoType] = None,
    ) -> Callable[[Callable], Callable]:
        """Set custom context for a operator method"""

        def wrapper(func):
            func.context = (
                context.value if isinstance(context, Enum) else context
            )
            extra_contexts2 = extra_contexts or {}
            func.extra_contexts = {
                key: ctx.value if isinstance(ctx, Enum) else ctx
                for key, ctx in extra_contexts2.items()
            }
            return func

        return wrapper

    def _pipda_eval(
        self, data: Any, context: ContextBase = None
    ) -> Any:
        """Evaluate the operator

        No data passed to the operator function. It should be used to evaluate
        the arguments.
        """
        # set the context and data in case they need to be used
        # inside the function.
        self.data = data
        return super()._pipda_eval(data, context)

    def __getattr__(self, name: str) -> Any:
        """Get the function to handle the operator"""
        # See if standard operator function exists
        return getattr(operator, name)
