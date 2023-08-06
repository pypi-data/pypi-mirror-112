import csv
import os
from constants import Constants
from utils import FileUtils, ConversionsUtils, DataCleanUtils
import transformations

class ETL_Package_Auto1:

    REQUIRED_FIELDS = ['engine-location','num-of-cylinders','engine-size','weight','horsepower','aspiration','price','make']
    dataFile = ''
    file_directory = ''

    def __init__(self, file_path):
        ETL_Package_Auto1.dataFile = file_path
        ETL_Package_Auto1.file_directory = os.path.splitext(file_path)[0]

    @staticmethod
    def load(file):
        staging_data=[]
        
        with open(file) as data:
            reader = csv.DictReader(data, delimiter=";")
            for row in reader:
                data = DataCleanUtils.isRowClean(row_data=row,fields=ETL_Package_Auto1.REQUIRED_FIELDS)
                
                if data['is_clean_row']:
                    staging_data.append(data['dict_data'])

        ETL_Package_Auto1.dataFile = FileUtils.write_file(file_name=f'{ETL_Package_Auto1.file_directory}_staging.csv',data_dict=staging_data)

    @staticmethod
    def transform1(file):
        transformed_data=[]
        with open(file) as data:
            staging_data = csv.DictReader(data)
            for row_number,item in enumerate(staging_data, start=2):
                dictionary = {}

                try:
                    if Constants.ENGINE_LOCATION.get(item['engine-location']) is not None:
                        dictionary['engine-location'] = Constants.ENGINE_LOCATION.get(item['engine-location'])
                    else:
                        raise transformations.EngineLocationError(row_number)
                    
                    if Constants.NUMBERS.get(item['num-of-cylinders']) is not None:
                        dictionary['num-of-cylinders'] = Constants.NUMBERS.get(item['num-of-cylinders'])
                    else:
                        raise transformations.NumOfCylindersError(row_number)
                    
                    try:
                        dictionary['engine-size'] = int(item['engine-size']) 
                    except:
                        raise transformations.EngineSizeError(row_number)

                    try:
                        dictionary['weight'] = int(item['weight']) 
                    except:
                        raise transformations.WeightError(row_number)

                    try:    
                        dictionary['horsepower'] = float(item['horsepower'].replace(',','.')) 
                    except:
                        raise transformations.HorsepowerError(row_number)
            
                    if Constants.ASPIRATION.get(item['aspiration']) is not None:
                        dictionary['aspiration'] = Constants.ASPIRATION.get(item['aspiration'])
                    else:
                        raise transformations.AspirationError(row_number)
                    
                    try:
                        dictionary['price'] = ConversionsUtils.cents_to_euro(item['price']) 
                    except:
                        raise transformations.PriceError(row_number)
                        
                    dictionary['make'] = item['make'].encode()

                except Exception:
                    continue

                transformed_data.append(dictionary)
            FileUtils.write_file(file_name=f'{ETL_Package_Auto1.file_directory}_transformed.csv',data_dict=transformed_data)
            return transformed_data




    # @staticmethod
    # def transform(file):
    #     transformed_data=[]
    #     with open(file) as data:
    #         staging_data = csv.DictReader(data)
    #         for row_number,item in enumerate(staging_data, start=2):
    #             dictionary = {}

    #             try:
    #                 if Constants.ENGINE_LOCATION.get(item['engine-location']) is not None:
    #                     dictionary['engine-location'] = Constants.ENGINE_LOCATION.get(item['engine-location'])
    #                 else:
    #                     raise Exception
                    
    #                 if Constants.NUMBERS.get(item['num-of-cylinders']) is not None:
    #                     dictionary['num-of-cylinders'] = Constants.NUMBERS.get(item['num-of-cylinders'])
    #                 else:
    #                     raise Exception
                    
    #                 dictionary['engine-size'] = int(item['engine-size']) 
    #                 dictionary['weight'] = int(item['weight']) 
    #                 dictionary['horsepower'] = float(item['horsepower'].replace(',','.')) 

    #                 if Constants.ASPIRATION.get(item['aspiration']) is not None:
    #                     dictionary['aspiration'] = Constants.ASPIRATION.get(item['aspiration'])
    #                 else:
    #                     raise Exception
                    
    #                 dictionary['price'] = ConversionsUtils.cents_to_euro(item['price']) 
    #                 dictionary['make'] = item['make'].encode()

    #             except Exception as e:
    #                 print(f'{e.__class__} occured in file on line number: {row_number}')
    #                 continue

    #             transformed_data.append(dictionary)
    #         FileUtils.write_file(file_name=f'{ETL_Package_Auto1.file_directory}_transformed.csv',data_dict=transformed_data)
    #         return transformed_data



ETL_Package_Auto1(r'challenge_me.txt')

ETL_Package_Auto1.load(ETL_Package_Auto1.dataFile)
result = ETL_Package_Auto1.transform1(ETL_Package_Auto1.dataFile)
print(f'Transformed Data Length {len(result)}')










