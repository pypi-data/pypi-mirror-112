from __future__ import annotations # required until python 4.0 in order for a method to be able to return var of type parent class -> https://stackoverflow.com/questions/15853469/putting-current-class-as-return-type-annotation

from enum import Enum
from typing import Any, Optional, Union

ex_request = {'responseId': '1a6188f5-95da-4ec1-97ab-a4dec4b747ef-06f725e1', 'session': 'projects/knockout-kutz-84057-0-himl/locations/global/agent/sessions/7fa683df-da91-b9d5-9110-b77535ce6150', 'queryResult': {'queryText': 'aweecae', 'parameters': {}, 'allRequiredParamsPresent': True, 'fulfillmentText': 'I missed that, say that again?', 
'fulfillmentMessages': [{'text': {'text': ['I missed that, say that again?']}}], 'outputContexts': [{'name': 'projects/knockout-kutz-84057-0-himl/locations/global/agent/sessions/7fa683df-da91-b9d5-9110-b77535ce6150/contexts/__system_counters__', 'lifespanCount': 1, 'parameters': {'no-input': 0.0, 'no-match': 9.0}}], 'intent': 
{'name': 'projects/knockout-kutz-84057-0-himl/locations/global/agent/intents/7ef18083-e560-473e-beeb-6f6fdc42cb65', 'displayName': 'Default Fallback Intent'}, 'intentDetectionConfidence': 1, 'diagnosticInfo': None, 'languageCode': 'en'}, 'originalDetectIntentRequest': {'payload': {}, 'source': 'DIALOGFLOW_CONSOLE', 'knowledge_connector_error': None}}

ex_list = [
    "123",
    431,
    True,
    [ "happy", "sad", "grumpy" ],
    { "the proof": "is in the pudding" }
]

class ANSI_COMMANDS(str, Enum):
    UNDERLINE = "\033[4m"
    END_FORMAT = "\033[0m"
    RESET_FORMAT = "\u001b[0m"

class HIGHLIGHT_COLORS(str, Enum):
    bright_white = "\033[1m"

    black = "\u001b[40m"
    red = "\u001b[41m"
    dark_green = "\u001b[42m"
    orange = "\u001b[43m"
    blue = "\u001b[44m"
    purple = "\u001b[45m"
    cyan = "\u001b[46m"
    white = "\u001b[47m"

    gray = "\033[100m"
    light_red = "\033[101m"
    light_green = "\033[102m"
    yellow = "\033[103m"
    light_blue = "\033[104m"
    light_purple = "\033[105m"
    sea_blue = "\033[106m"
    pink = "\033[107m"

class TEXT_COLORS(str, Enum):
    bright_white = "\033[1m"

    black = "\u001b[30m"
    red = "\u001b[31m"
    dark_green = "\u001b[32m"
    orange = "\u001b[33m"
    blue = "\u001b[34m"
    purple = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    gray = "\033[90m"
    light_red = "\033[91m"
    light_green = "\033[92m"
    yellow = "\033[93m"
    light_blue = "\033[94m"
    light_purple = "\033[95m"
    sea_blue = "\033[96m"
    pink = "\033[97m"

color_list = [
    TEXT_COLORS.yellow, TEXT_COLORS.purple, TEXT_COLORS.light_red, TEXT_COLORS.cyan, TEXT_COLORS.light_green,
    TEXT_COLORS.blue, TEXT_COLORS.white, TEXT_COLORS.light_purple, TEXT_COLORS.light_blue,
    TEXT_COLORS.pink, TEXT_COLORS.sea_blue, 
]

def non_iter_print(var, _color: Optional[Union[TEXT_COLORS, HIGHLIGHT_COLORS]] = None) -> str:

    logic_col, str_col = (TEXT_COLORS.orange, TEXT_COLORS.blue) if not _color else (_color, _color)

    if isinstance(var, (int, float, bool)):
        col_var = logic_col + str(var) + ANSI_COMMANDS.END_FORMAT
        return col_var

    if isinstance(var, str):
        col_var = str_col + f'"{var}"' + ANSI_COMMANDS.END_FORMAT
        return col_var

    return var

def get_iter_pair(iterable):
    return iterable.items() if isinstance(iterable, dict) else enumerate(iterable)

def cprint(var: Any, color: Optional[Union[TEXT_COLORS, HIGHLIGHT_COLORS]] = None, _rec_depth: int = 0) -> str:
    """prints out the given var using ANSI color values, and returns whatever is printed to the console as a string (that includes the ANSI escape commands)
    This is so that you can save the string for viewing in another text editor if you would like. In VSCode there is an extension for viewing
    ANSI strings that is particularly useful if you would like the things you print to console as logs and have them look just as nice!

    Args:
        var (Any): Any python primitive data type.
        color (TEXT_COLORS or HIGHLIGHT_COLORS, Optional): Used to set the color when you are printing a non iterable primitive (int, float, bool, or str). Default is TEXT_COLORS.gray.
        _rec_depth (int, DO NOT SET): Private, used to keep track of the recursion depth.

    Returns:
        str: formatted ANSI string (whatever is printed out to console)
    """

    if not var: var = {}

    if not isinstance(var, (list, dict)):

        if isinstance(var, (int, float, bool, str)):
            colored_var = non_iter_print(var, color)
            print(colored_var)
            return colored_var

        else:
            try:
                return cprint(vars(var))
            except:
                raise TypeError("The var you would like to print does not support the __dict__ method and can therefore not be cprinted!\nTry converting the var to a python primitive or implementing the __dict__ method to proceed.")

    def get_recursion_color(list_of_colors: list, depth: int):
        while True:
            try:
                current_color = list_of_colors[depth]
                break
            except:
                depth -= len(list_of_colors)

        return current_color

    final_str = "" # the ANSI formatted string that will be printed to the console when this function is run

    spacing = "  " * _rec_depth
    current_color = get_recursion_color(color_list, _rec_depth)

    op_br = current_color + "{" + ANSI_COMMANDS.END_FORMAT
    cl_br = current_color + "}" + ANSI_COMMANDS.END_FORMAT

    for k, v in get_iter_pair(var):
        colored_k = spacing + TEXT_COLORS.dark_green + str(k) + ANSI_COMMANDS.END_FORMAT + ": "

        if isinstance(v, (dict, list)): # if while iterating through the iterable we find another iterable, recurse
            _rec_depth += 1
            print(colored_k, end=f"{op_br}"); final_str += str(colored_k) + f"{op_br}"
            if v:
                print(); final_str += "\n"
                final_str += cprint(v, _rec_depth=_rec_depth)
                print(spacing + cl_br); final_str += str(spacing) + str(cl_br) + "\n"
            else:
                print(cl_br); final_str += str(cl_br) + "\n"
            _rec_depth -= 1
        else: # else, just print the noniterable variable
            formatted_v = non_iter_print(v)
            print(colored_k, end=""); final_str += str(colored_k)
            print(formatted_v); final_str += str(formatted_v) + "\n"

    return final_str
