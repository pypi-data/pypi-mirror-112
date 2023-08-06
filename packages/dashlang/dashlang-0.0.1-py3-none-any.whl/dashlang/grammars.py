"""Module with grammars used to parse the input tree"""
from parsimonious.expressions import Literal, OneOf, OneOrMore, Regex, Sequence, ZeroOrMore
from parsimonious.grammar import LazyReference

# Regex expressions. These are quite fast to parse, so we can put as
# much as we can into them.
ASCII_WORD = Regex(r"[-\w]+", name="ascii_word")
FREE_TEXT = Regex(r'"([ \S]+?)"', name="free_text", unicode=True)
WHITESPACE = Regex(r"\s", name="whitespace")
WHITESPACES = ZeroOrMore(WHITESPACE, name="whitespaces")

# Literals used by the markup language. These are very fast to parse, so we
# try to use as many as we can.
EQUAL_SIGN = Literal("=", name="equal_sign")
OPEN_BRACKET = Literal("<", name="open_bracket")
CLOSE_BRACKET = Literal(">", name="close_bracket")
FORWARD_SLASH = Literal("/", name="forward_slash")
DOT = Literal(".", name="dot")

# Sequences
ATTRIBUTE = Sequence(ASCII_WORD, EQUAL_SIGN, FREE_TEXT, name="attribute")

ELEMENT_NAME_SIMPLE = Sequence(ASCII_WORD, name="element_name_simple")
ELEMENT_NAME_COMPLETE = Sequence(ASCII_WORD, DOT, ASCII_WORD, name="element_name_complete")
ELEMENT_NAME = OneOf(ELEMENT_NAME_COMPLETE, ELEMENT_NAME_SIMPLE, name="element_name")

ELEMENT_ATTRIBUTE = Sequence(OneOrMore(WHITESPACE), ATTRIBUTE, name="element_attribute")
ELEMENT_ATTRIBUTES = ZeroOrMore(ELEMENT_ATTRIBUTE, name="element_attributes")

ELEMENT_START_TAG = Sequence(
    OPEN_BRACKET,
    ELEMENT_NAME,
    ELEMENT_ATTRIBUTES,
    CLOSE_BRACKET,
    name="element_start_tag"
)

ELEMENT_CLOSE_TAG = Sequence(
    OPEN_BRACKET,
    FORWARD_SLASH,
    ELEMENT_NAME,
    CLOSE_BRACKET,
    name="element_close_tag"
)

ELEMENT_CONTENT = Sequence(WHITESPACES, LazyReference("element"), WHITESPACES, name="element_content")
ELEMENT_CONTENTS = ZeroOrMore(ELEMENT_CONTENT, name="element_contents")
ELEMENT = Sequence(ELEMENT_START_TAG, ELEMENT_CONTENTS, ELEMENT_CLOSE_TAG, name="element")

DASHLANG_GRAMMAR = r"""
element               = element_start_tag element_contents element_close_tag

element_contents      = element_content*
element_content       = whitespaces element whitespaces

element_start_tag     = open_bracket whitespaces element_name element_attributes whitespaces close_bracket
element_close_tag     = open_bracket forward_slash whitespaces element_name whitespaces close_bracket

element_name          = element_name_complete / element_name_simple
element_name_complete = ascii_word dot ascii_word
element_name_simple   = ascii_word

element_attributes    = element_attribute*
element_attribute     = whitespaces attribute

attribute             = float_attribute / integer_attribute / boolean_attribute / string_attribute
string_attribute      = ascii_word equal_sign free_text
integer_attribute     = integer_flag colon ascii_word equal_sign ascii_word
float_attribute       = float_flag colon ascii_word equal_sign ascii_word
boolean_attribute     = boolean_flag colon ascii_word equal_sign boolean_value

integer_flag          = "i"
float_flag            = "f"
boolean_flag          = "b"

boolean_value         = true_value / false_value
true_value            = ~'"true"'i
false_value           = ~'"false"'i

open_bracket          = "<"
close_bracket         = ">"
forward_slash         = "/"
dot                   = "."
colon                 = ":"
equal_sign            = "="

whitespaces           = whitespace*

ascii_word            = ~"[-\w]+"
free_text             = ~'"([ \S]+?)"'
whitespace            = ~"\s"
"""
