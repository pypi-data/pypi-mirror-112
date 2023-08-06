"""Module to handle custom error exceptions during transformation"""

class EngineLocationError(Exception):
    """EngineLocationError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class NumOfCylindersError(Exception):
    """NumOfCylindersError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class EngineSizeError(Exception):
    """EngineSizeError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class WeightError(Exception):
    """WeightError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class HorsepowerError(Exception):
    """HorsepowerError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class AspirationError(Exception):
    """AspirationError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class PriceError(Exception):
    """PriceError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class MakeError(Exception):
    """MakeError Exception on the specified line"""
    def __init__(self,row_number):
        super().__init__()
        print(f'{self.__class__} exception occured in file on line number: {row_number}')
