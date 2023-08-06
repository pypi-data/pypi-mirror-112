from dataclasses import dataclass
from typing import Optional, Tuple, Union

import re
from bs4.element import Tag

from sec_html_parser.span_style import SpanStyle


@dataclass
class DivStyle:
    """Parsed HTML div style element attributes"""

    margin_top: Optional[float]

    def __init__(self, node_or_style: Union[str, Tag]) -> None:
        _margin_top_re = re.compile(r"margin-top:(\d+\.?\d*)pt;?")

        div_style_str = SpanStyle._get_style_string(node_or_style)

        size = _margin_top_re.search(div_style_str)
        self.margin_top = None if size is None else float(size.group(1))

    def to_tuple(self) -> Tuple[float]:
        """
        Convert DivStyle to a tuple object.

        This should be used when comparing two DivStyle objects
        in order to check which one is a 'child' of the other.

        None margin-top is converted to -1.

        Example:
            ```python
            A = DivStyle("<div margin-top:12/>")
            B = DivStyle("<div margin-top:10/>")

            assert A.to_tuple() < B.to_tuple()
            ```

        Returns (margin_top, )
        """

        return (self.margin_top or -1.0,)
