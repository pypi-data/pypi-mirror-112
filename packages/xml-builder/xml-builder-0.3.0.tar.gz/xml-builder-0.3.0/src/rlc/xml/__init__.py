import xml.etree.ElementTree as etree
from typing import Optional, Type, Union, overload, Any
from types import TracebackType


class Node:
    def __init__(self, builder: etree.TreeBuilder):
        self._builder = builder


class Tag(Node):
    def __init__(self, builder: etree.TreeBuilder, name: str, **attrs: str) -> None:
        super().__init__(builder)
        self.name = name
        self.attrs = attrs

    def __enter__(self) -> "Tag":
        self._builder.start(self.name, {k: v for k, v in self.attrs.items()})
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._builder.end(self.name)


class Text(Node):
    def __init__(self, builder: etree.TreeBuilder, data: str):
        super().__init__(builder)
        self._builder.data(data)


class XmlBuilder:
    def __init__(self) -> None:
        self._builder = etree.TreeBuilder()

    def tag(self, name: str, **attrs: str) -> Tag:
        return Tag(self._builder, name, **attrs)

    @overload
    def text(self, data: str) -> Text:
        ...

    @overload
    def text(self, data: int) -> Text:
        ...

    @overload
    def text(self, data: bool) -> Text:
        ...

    def text(self, data: Union[str, bool, int]) -> Text:
        if isinstance(data, str):
            return Text(self._builder, data)
        elif isinstance(data, bool):
            return Text(self._builder, str(data).lower())
        elif isinstance(data, int):
            return Text(self._builder, str(data))

    def build(self) -> etree.Element:
        return self._builder.close()


__all__ = ["XmlBuilder", "Tag", "Text"]
__version__ = "0.3.0"
