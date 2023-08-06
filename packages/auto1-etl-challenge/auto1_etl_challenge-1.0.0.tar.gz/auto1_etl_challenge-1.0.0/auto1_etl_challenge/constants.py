"""Constants module"""

class Constants:
    """
    Class for defining constant values for the pipeline

    Attributes
    ----------

    Public:
        ENGINE_LOCATION : dict
            numeric values for the engine location

        NUMBERS : dict
            numeric values for the numbers

        ASPIRATION : dict
            numeric values for the aspiration
    """

    ENGINE_LOCATION = {
        'rear': 0,
        'front': 1
    }

    NUMBERS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    ASPIRATION = {
        'std': 0,
        'turbo': 1
    }
