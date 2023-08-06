"""Module with the visitor class that is used to transform
the syntax tree into the final layout.
"""
from typing import Any, List, Mapping, Tuple, Union

from parsimonious.nodes import Node, NodeVisitor, RegexNode

from .exceptions import MismatchedTagsError
from .transforms import unescape_html_string, strip_string_quotes


class DashlangVisitor(NodeVisitor):
    """Visitor class that implements all the logic that transforms
    the parsed syntax tree into the final layout.
    """

    _default_namespace: str

    def __init__(self, default_namespace="dash_html_components") -> None:
        self._default_namespace = default_namespace

    @property
    def default_namespace(self) -> str:
        """Access the default namespace as set during the initialization of the node visitor
        class instance.
        """
        return self._default_namespace

    def generic_visit(self, node: Node, visited_children: List[Any]) -> Union[List[Any], Node]:
        """Generic visitor method. This is the visitor method called on nodes for
        rules that don't implement a specific visitor method.
        """
        return visited_children or node

    def visit_whitespace(self, node: Node, *args) -> None:
        """Visit a node that matches the whitespace rule. Since this rules is used only
        to filter whitespace elements on the original text, this visitor method does not
        perform any operation, instead simply returning a `None` value so that we can filter
        this value up ahead while parsing the tree.
        """
        return None

    def visit_free_text(self, node: RegexNode, *args) -> str:
        """Visit a free_text rule node. This node is represented by a
        `RegexNode` instance and this visitor method transforms the
        matched text into a parsed and cleaned string.

        Args:
            node: The matched `RegexNode` node

        Returns:
            The transformed result of the matched text by the regular
            expression that is defined on the free_text grammar rule.
        """
        return unescape_html_string(strip_string_quotes(node.text))

    def visit_ascii_word(self, node: RegexNode, *args) -> str:
        """Visit a `RegexNode` that matches `the ascii_word` rule. Since this is a simple
        regex node, all parser logic is already included on the regular expression used to
        define the rule.

        Args:
            node: The `RegexNode` instance that matched

        Returns:
            The text that was matched by the regular expression.
        """
        return node.text

    def visit_whitespaces(self, node: Node, *args) -> None:
        """Visit node that matches the rule for a collection of zero or more whitespace
        characters. As for the whitespace rule visitor method, this method simply returns a
        `None` value to make it easier to filter it.
        """
        return None

    def visit_false_value(self, node: RegexNode, *args) -> bool:
        """Visitor method for a node that matched the `false_value` rule. This method always
        returns the constant `False`, since that is the semantic meaning of any expression that
        matches the regular expression for this rule.
        """
        return False

    def visit_true_value(self, node: RegexNode, *args) -> bool:
        """Visitor method for a node that matched the `true_value` rule. This method always
        returns the constant `True`, since that is the semantic meaning of any expression that
        matches the regular expression for this rule.
        """
        return True

    def visit_boolean_value(self, node: Node, children: bool) -> bool:
        """Return the child value for the node that matches the `boolean_value` rule."""
        return children

    def visit_boolean_attribute(self, node: Node, children: Tuple[str, str, str, str, bool]) -> Mapping[str, Any]:
        """Return an attribute in boolean form."""
        _, _, name, _, value = children
        return {"name": name, "value": value}

    def visit_float_attribute(self, node: Node, children: Tuple[str, str, str, str, str]) -> Mapping[str, Any]:
        """Return an attribute in float form."""
        _, _, name, _, value = children
        return {"name": name, "value": float(value)}

    def visit_integer_attribute(self, node: Node, children: Tuple[str, str, str, str, str]) -> Mapping[str, Any]:
        """Return an attribute in integer form."""
        _, _, name, _, value = children
        return {"name": name, "value": int(value)}

    def visit_string_attribute(self, node: Node, children: Tuple[str, str, str]) -> Mapping[str, str]:
        """Return an attribute in string form. This rule is the fallback rule for element attributes
        in the case that no other attribute flag was used on the attribute.

        Args:
            node: The current node in the parsed tree
            children: A tuple of three strings, containing the name of the attribute and its value

        Returns:
            A mapping containing the attribute name and the attribute value, in string format.
        """
        name, _, value = children
        return {"name": name, "value": value}

    def visit_attribute(self, node: Node, children: Mapping[str, Any]) -> Mapping[str, Any]:
        """Visit an `attribute` rule node. This visitor method discards the equal sign
        that is part of the attribute syntax, converting the information into a dictionary
        containing the attribute name and the attribute value.

        Args:
            node: The matched node for the `attribute` grammar rule.
            children: A mapping containing the result of parsing the children of the node.

        Returns:
            A mapping containing the attribute name and the attribute value, mapped to the
            correct type according to the attribute flag.
        """
        return children

    def visit_element_attribute(self, node: Node, children: Tuple[str, Mapping[str, Any]]) -> Mapping[str, Any]:
        _, attribute = children
        return attribute

    def visit_element_attributes(self, node: Node, children: List[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
        return children

    def visit_element_name_simple(self, node: Node, *args) -> Mapping[str, str]:
        return {"namespace": self._default_namespace, "name": node.text}

    def visit_element_name_complete(self, node: Node, children) -> Mapping[str, str]:
        namespace, _, name = children
        return {"namespace": namespace, "name": name}

    def visit_element_name(self, node: Node, children) -> Mapping[str, str]:
        return children[0]

    def visit_element_start_tag(self, node: Node, children) -> Mapping[str, str]:
        _, _, name, attributes, _, _ = children
        return {"component": name, "props": attributes}

    def visit_element_close_tag(self, node: Node, children) -> Mapping[str, str]:
        contents: List[str] = list(filter(None, children))
        return {"component": contents[2]}

    def visit_element_content(self, node: Node, children) -> Mapping[str, Any]:
        _, element, _ = children
        return element

    def visit_element_contents(self, node: Node, children):
        return children if children else None

    def visit_element(self, node: Node, children) -> Mapping[str, Any]:
        open_tag, content, close_tag = children

        if open_tag["component"] != close_tag["component"]:
            raise MismatchedTagsError

        return {
            "component": open_tag,
            "children": content if content else [],
        }
