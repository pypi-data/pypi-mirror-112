from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple, Union

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

from sec_html_parser.div_style import DivStyle
from sec_html_parser.span_style import SpanStyle


class Parser:
    def _is_span_child(self, node: Tag, other: Tag) -> bool:
        """Check if node is a child of other with respect to font styles"""

        # check that other has a style
        try:
            ostyle = SpanStyle(other)
        except ValueError:
            return False

        # a node with no style is always a child
        try:
            nstyle = SpanStyle(node)
        except ValueError:
            return True

        # text in relative position (top or bottom) is never a child
        # and can never have children
        if nstyle.relative or ostyle.relative:
            return False

        # compare style tuples
        return nstyle.to_tuple() < ostyle.to_tuple()

    def _is_div_child(self, node: Tag, other: Tag) -> bool:
        """Check if node is a child of other with respect to div styles"""

        # check that other has a style
        try:
            ostyle = DivStyle(other)
        except ValueError:
            return False

        # a div with no style is always a child
        try:
            nstyle = DivStyle(node)
        except ValueError:
            return True

        # check if div has a smaller margin than other
        return nstyle.to_tuple() < ostyle.to_tuple()

    def _walk_soup(
        self,
        element: Union[BeautifulSoup, PageElement],
        not_into: Optional[List[str]] = None,
    ) -> Iterator[PageElement]:
        """
        Iterate given element and all its children in a depth-first manner

        Will not yield elements without a `name` (e.g. a text element in a span),
        neither will it yield elements whose `name` is in the `not_into` list.

        If given a `BeautifulSoup` object, only the children will be yielded
        (and recursed into if appropriate), not the `BeautifulSoup` object itself.
        """

        element_is_not_soup = not isinstance(element, BeautifulSoup)
        element_has_name = element.name is not None

        if element_is_not_soup and element_has_name:
            yield element

        element_has_children = hasattr(element, "children")
        if element_has_children:

            should_recurse = not_into is None or element.name not in not_into
            if should_recurse:
                for child in element.children:
                    yield from self._walk_soup(child, not_into)

    def get_file_hierarchy(self, path: Path, keep_nodes: bool = False) -> dict:
        """
        Get text hierarchy of text in a file, with respect to the style attribute
        of the elements in the soup.
        """

        soup = BeautifulSoup(path.read_text(), features="html.parser")

        return self.get_hierarchy(soup, keep_nodes)

    def get_hierarchy(self, soup: BeautifulSoup, keep_nodes: bool = False) -> dict:
        """
        Get text hierarchy of text in soup, with respect to the style attribute
        of the elements in the soup.
        """

        hierarchy = {"root": []}

        # this stack is used to check at what depth the next
        # element in the soup should go in the new hierarchy
        parents_metadata_stack = []

        # keep track of the current div the elements are in
        element_div = None

        for element_node in self._walk_soup(soup, not_into=["span", "table"]):
            if element_node.name == "div":
                element_div = element_node
            elif element_node.name == "span":
                self._add_span_to_hierarchy(
                    element_node, element_div, parents_metadata_stack, hierarchy
                )
            elif element_node.name == "table":
                if element_node.text != "":
                    _, _, parent_children = parents_metadata_stack[-1]
                    parent_children.append({"table": [str(element_node)]})

        hierarchy = self._clean_leaves(hierarchy)

        return hierarchy

    def _add_span_to_hierarchy(
        self,
        element_node: Tag,
        element_div: Tag,
        parents_metadata_stack: List[Tuple[Tag, Tag, List]],
        hierarchy: Dict,
    ) -> None:
        """
        Pop the stack until a parent is found for the element,
        add the element as a child of that parent,
        and push the element to the stack.

        If no parent is found then the element is added as a child of the 'root'
        node of the hierarchy.

        This modifies both the parent_stack and the hierarchy objects.
        """

        # create element tuple for the stack
        element_content = element_node.text.strip()
        element_children = []
        element_metadata = (element_div, element_node, element_children)

        # create element hierarchy node
        element_hierarchy_node = {element_content: element_children}

        # pop elements from the stack until a parent is found
        for p_div, p_style, p_children in reversed(parents_metadata_stack):

            # check if the current top of the element_stack is a parent of
            # the current node
            if self._is_parent(p_div, p_style, element_div, element_node):

                # add the element hierarchy node as a child of the parent
                p_children.append(element_hierarchy_node)

                # update the stack so that this element's metadata is at the top
                parents_metadata_stack.append(element_metadata)

                # the element has been added to the hierarchy, we are done
                return
            else:
                parents_metadata_stack.pop()

        # if no parent was found add the element as a child
        # of the root node
        hierarchy["root"].append(element_hierarchy_node)

        # update the stack so that this element's metadata is at the top
        parents_metadata_stack.append(element_metadata)

    def _is_parent(
        self,
        parent_div: Optional[Tag],
        parent_style: Tag,
        child_div: Optional[Tag],
        child_style: Tag,
    ) -> bool:
        """Check if parent is a parent of element based on its div and span"""

        # check if parent by div or span
        parent_by_div = (
            True if parent_div is None else self._is_div_child(child_div, parent_div)
        )
        parent_by_span = self._is_span_child(child_style, parent_style)

        # if parent by span then it is always a parent
        # but if parent by div then it is a parent only if it isn't
        # a parent by span (for an example see
        # test `test_get_hierarchy_div_child_but_not_span_child`)
        is_parent = parent_by_span or (parent_by_div and not parent_by_span)

        return is_parent

    def _clean_leaves(self, hierarchy: Union[dict, str]) -> Union[dict, str]:
        """Convert leaf nodes to strings instead of dictionaries with an empty list"""

        # if hierarchy is a leaf we have nothing to do
        if isinstance(hierarchy, str):
            return hierarchy

        # first we get the name of the node
        name = list(hierarchy)[0]

        # then we check if it is a leaf
        if len(hierarchy[name]) == 0:

            # if so then we return the name of the node
            return name
        else:

            # if not then we clean all the child nodes of the current node
            return {name: [self._clean_leaves(child) for child in hierarchy[name]]}

    def hierarchy_to_string(self, hierarchy: dict, depth: int = 0) -> str:
        """Get a string representation of a hierarchy"""

        if isinstance(hierarchy, str):
            return "\t" * depth + hierarchy + "\n"

        key = list(hierarchy.keys())[0]
        string = "\t" * depth + key + "\n"
        for child in hierarchy[key]:
            string += self.hierarchy_to_string(child, depth + 1)

        return string
