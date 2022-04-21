import re
from typing import Union


MATCH_NONE_REGEX = re.compile('$^')
INPUT_MODIFIER_REGEX = re.compile(r'^Hi my name is .*$')
OUTPUT_MODIFIER_REGEX = re.compile(r'^Hi my name is .*$')


def modify_message_text(message_text: str, modifier: Union[None, dict]) -> str:
    regex_match = re.match(modifier.get('regex', MATCH_NONE_REGEX), message_text)
    if modifier and regex_match:
        return modifier.get('function')(message_text)

    return message_text


def input_modifier_function(message_text: str) -> str:
    if message_text:
        return 'Hi my name is Bob'

    return ''


def output_modifier_function(message_text: str) -> str:
    if message_text:
        return 'Hi my name is Alice'

    return ''


INPUT_MODIFIER = {
    'regex': INPUT_MODIFIER_REGEX,
    'function': input_modifier_function
}

OUTPUT_MODIFIER = {
    'regex': OUTPUT_MODIFIER_REGEX,
    'function': output_modifier_function
}
