from dataclasses import dataclass
from typing import Optional, Tuple, Union

import regex as re
from bs4.element import Tag


@dataclass
class SpanStyle:
    """Parsed HTML span style element attributes"""

    size: Optional[float]
    weight: Optional[int]
    style: Optional[str]
    relative: bool

    def __init__(self, node_or_style: Union[str, Tag]) -> None:
        _font_size_re = re.compile(r"font-size:(\d+\.?\d*);?")
        _font_weight_re = re.compile(r"font-weight:(\d+);?")
        _font_style_re = re.compile(r"font-style:([a-zA-Z]+);?")
        _relative_re = re.compile(r"position:relative;?")

        span_style = self._get_style_string(node_or_style)

        size = _font_size_re.search(span_style)
        self.size = None if size is None else float(size.group(1))

        weight = _font_weight_re.search(span_style)
        self.weight = None if weight is None else int(weight.group(1))

        style = _font_style_re.search(span_style)
        self.style = None if style is None else style.group(1)

        relative = _relative_re.search(span_style)
        self.relative = False if relative is None else True

    def to_tuple(self) -> Tuple[float, int, int]:
        """
        Convert SpanStyle to a tuple object.

        This should be used when comparing two SpanStyle objects
        in order to check which one is a 'child' of the other.

        None size or weight is converted to -1.
        Italic font style is converted to a 1, all others (and None) to a -1.

        Since relative spans can never be a child or have children, the relative
        property is not added to the tuple.

        Example:
            ```python
            A = SpanStyle("<span font-size:1pt;font-style:italic/>")
            B = SpanStyle("<span font-size:1pt/>")

            assert A.to_tuple() < B.to_tuple()
            ```

        Returns (font_size, font_weight, font_style)
        """

        return (self.size or -1, self.weight or -1, 1 if self.style == "italic" else -1)

    @staticmethod
    def _get_style_string(node_or_style: Union[str, Tag]) -> str:
        """Get a style string from a string or a bs4 Node"""

        if isinstance(node_or_style, str):
            return node_or_style
        elif isinstance(node_or_style, Tag):
            node_style = node_or_style.get("style")
            if node_style is not None:
                return node_style
            else:
                raise ValueError("Given node didn't have a 'style' attribute")
        else:
            raise ValueError(
                "Can't create FontStyle from object"
                f"of type '{node_or_style.__class__.__name__}'"
            )
