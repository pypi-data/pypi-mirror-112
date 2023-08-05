from __future__ import annotations # required until python 4.0 in order for a method to be able to return var of type parent class -> https://stackoverflow.com/questions/15853469/putting-current-class-as-return-type-annotation

from enum import Enum
from typing import Any, Dict, List

ex_request = {
  "responseId": "response-id",
  "session": "projects/project-id/agent/sessions/session-id",
  "queryResult": {
    "queryText": "End-user expression",
    "parameters": {
      "param-name": "param-value"
    },
    "allRequiredParamsPresent": True,
    "fulfillmentText": "Response configured for matched intent",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Response configured for matched intent"
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/project-id/agent/sessions/session-id/contexts/context-name",
        "lifespanCount": 5,
        "parameters": {
          "param-name": "param-value"
        }
      }
    ],
    "intent": {
      "name": "projects/project-id/agent/intents/intent-id",
      "displayName": "matched-intent-name"
    },
    "intentDetectionConfidence": 1,
    "diagnosticInfo": {},
    "languageCode": "en"
  },
  "originalDetectIntentRequest": {}
}

color_dict = {
    # "PURPLE": "\033[95m",
    # "BLUE": "\033[94m",
    # "CYAN": "\033[96m",
    # "GREEN": "\033[92m",
    # "ORANGE": "\033[93m",
    # "RED": "\033[91m",
    # "WHITE": "\033[1m",
    "UNDERLINE": "\033[4m",
    "ENDC": "\033[0m",

    "Black": "\u001b[30m",
    # "Black": "\u001b[30m",

    "Red": "\u001b[31m",
    "ERROR": "\u001b[31m",

    "Green": "\u001b[32m",
    "CHECK_PASS": "\u001b[32m",

    "Yellow": "\u001b[33m",
    "WARNING": "\u001b[33m",

    "Blue": "\u001b[34m",
    # "Blue": "\u001b[34m",

    "Magenta": "\u001b[35m",
    "HEADER": "\u001b[35m",

    "Cyan": "\u001b[36m",
    "INFO": "\u001b[36m",

    "White": "\u001b[37m",
    # "White": "\u001b[37m",

    "Reset": "\u001b[0m"
}

class CONSOLE_COLORS(str, Enum):
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"

    ERROR = "\u001b[31m",
    CHECK_PASS = "\u001b[32m",
    WARNING = "\u001b[33m",
    INFO = "\u001b[36m",

    Black = "\u001b[30m"
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    Cyan = "\u001b[36m"
    White = "\u001b[37m"
    Reset = "\u001b[0m"

color_list = [
    "\u001b[33m", "\u001b[35m", "\u001b[34m", "\u001b[36m", "\u001b[37m",
    "\u001b[33m", "\u001b[35m", "\u001b[34m", "\u001b[36m", "\u001b[37m",
    "\u001b[33m", "\u001b[35m", "\u001b[34m", "\u001b[36m", "\u001b[37m",
    "\u001b[33m", "\u001b[35m", "\u001b[34m", "\u001b[36m", "\u001b[37m",
    "\u001b[33m", "\u001b[35m", "\u001b[34m", "\u001b[36m", "\u001b[37m",
    "\u001b[33m", "\u001b[35m", "\u001b[34m", "\u001b[36m", "\u001b[37m",
]
def cprint(var: ..., color: str="", count=0) -> str:
    # if count == 0: print()

    final_str = ""

    if isinstance(var, str):
        str_color = color_dict.get(color)
        var = f"{str_color} {var} \033[0m"
        print(var)
        final_str += str(var)

    elif isinstance(var, dict):

        delimiter = "  "

        indent = delimiter * count
        second_brace_indent = indent[:len(indent)]
        brace_color = color_list[count]

        print( (brace_color + "{" + "\033[0m") )
        for key, val in var.items():

            colored_key = "\u001b[32m" + key + "\033[0m"
            key_str = delimiter + f"{colored_key}: "

            if isinstance(val, dict):
                recursion_count = count + 1
                print(key_str, end="")
                cprint(val, count=recursion_count)

            else:
                line = indent + (key_str + str(val))
                print(line)

                count = 0

        print(second_brace_indent + (brace_color + "}" + "\033[0m"))


    # elif isinstance(var, list):
    #     for some_item in var:
    #         print(some_item)
        
    else:
      var = str(var)
      cprint(var, color=color)
      final_str += var

    # if count == 0: print()
    return final_str
# cprint(ex_request)

def rec_cprint(var, count=0):
    
    # line += color_list[count] + "{" + "\033[0m"

    # line += "\n" + spacing + color_list[count] + "}" + "\033[0m"

    spacing = "    "

    for k, v in var.items():
        line = ""        

        line += (spacing * count)

        col_k = "\u001b[32m" + k + "\033[0m" + ": "
        line += col_k

        if isinstance(v, str): #  or isinstance(v, int) or isinstance(v, float)
            line += v
            line += ","

        if isinstance(v, dict):
            rec_cprint(v, count+1)

        if isinstance(v, list):
            pass

        print(line)

# rec_cprint(ex_request)

def rec_cprint2(var, count=0):
    
    line = ""
    spacing = "    "

    iterable = True
    try:
        iter_test = iter(var)
    except:
        iterable = False

    if iterable:
        if isinstance(var, dict):
            def rec_cprint_dict(dictionary: Dict[str, Any], delimiter: str):
                line = "" + (delimiter * count)
                line += color_list[count] + "{" + "\033[0m"
                for k, v in dictionary.items():
                    line += "\n" + (delimiter * count)
                    col_k = "\u001b[32m" + k + "\033[0m" + ": "
                    line += col_k
                    rec_cprint2(v, count+1)

                line += "\n" + (delimiter * count) + color_list[count] + "}" + "\033[0m"

                return line

            line += rec_cprint_dict(var, spacing)

        if isinstance(var, list):
            pass
    else:
        line += str(var)

    print(line)
