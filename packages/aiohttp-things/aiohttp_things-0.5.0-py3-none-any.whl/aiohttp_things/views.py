from abc import ABCMeta
from typing import Any, Callable, Dict, Iterable

from aiohttp.abc import AbstractView
from aiohttp.web import Request, Response, json_response

try:
    import aiohttp_jinja2
    HAS_AIOHTTP_JINJA2 = True
except ImportError:
    HAS_AIOHTTP_JINJA2 = False


class ContextMixin(AbstractView, metaclass=ABCMeta):
    """
    Class based view mixin with context attribute.
    """
    #: Dictionary for JSON response or HTML template response.
    context: Dict[str, Any]

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.context = {}


class PrimaryKeyMixin(AbstractView, metaclass=ABCMeta):
    """
    Class based view mixin with primary key attribute.
    """
    #: Primary key from path variable for select an object from database.
    #: Use regular expressions in routes for safe input
    pk: Any

    #: Callable object for converting a primary key.
    pk_factory: Callable[..., Any] = lambda pk: pk

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.pk = self.pk_factory(self.request.match_info.get('pk'))


class ItemMixin(ContextMixin, PrimaryKeyMixin, metaclass=ABCMeta):
    pass


class ListMixin(ContextMixin, metaclass=ABCMeta):
    items: Iterable[Any]

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.items = []


class Jinja2Mixin(ContextMixin, metaclass=ABCMeta):
    template: str

    def __init__(self, request: Request):
        super().__init__(request)
        if not HAS_AIOHTTP_JINJA2:
            raise ImportError(
                'If you want use `Jinja2Mixin`, '
                'then you need install `aiohttp-jinja2` package.'
            )

    async def finalize_response(self, **kwargs: Any) -> Response:
        return await aiohttp_jinja2.render_template_async(
            self.template,
            self.request,
            self.context,
            **kwargs,
        )


class JSONMixin(ContextMixin, metaclass=ABCMeta):
    async def finalize_response(self, **kwargs: Any) -> Response:
        return json_response(self.context, **kwargs)
