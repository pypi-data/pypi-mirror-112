class EngineLocationError(Exception):
    def __init__(self,row_number):
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class NumOfCylindersError(Exception):
    def __init__(self,row_number):
        print(f'{self.__class__} exception occured in file on line number: {row_number}')
 

class EngineSizeError(Exception):
    def __init__(self,row_number):
        print(f'{self.__class__} exception occured in file on line number: {row_number}')


class WeightError(Exception):
    def __init__(self,row_number):
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class HorsepowerError(Exception):
    def __init__(self,row_number):
        print(f'{self.__class__} exception occured in file on line number: {row_number}')

class AspirationError(Exception):
    def __init__(self,row_number):
       print(f'{self.__class__} exception occured in file on line number: {row_number}')

class PriceError(Exception):
    def __init__(self,row_number):
        print(f'{self.__class__} exception occured in file on line number: {row_number}')