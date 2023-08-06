"""Main module for ETL challenge"""

import csv
import os
from auto1_etl_challenge.constants import Constants
from auto1_etl_challenge.utils import FileUtils, ConversionsUtils, DataCleanUtils
import transformations

class EtlMetaData:
    """
    Class for metadata of the ETL process.

    Attributes
    ----------

    Protected:

        _REQUIRED_COLUMNS : list
            list of columns required for transformation
    """

    _REQUIRED_COLUMNS = ['engine-location','num-of-cylinders','engine-size','weight','horsepower','aspiration','price','make']

class EtlPackageAuto1(EtlMetaData):
    """
    Class for performing ETL operations on file.
    Attributes
    ----------

    Static:

        dataFile: Stores source file path
        file_directory: Stores source file directory

    Methods:
    -------

    Static:

        load: Loads the source file, clean it and create staging file
        transform: Performs transformation process on staging file and create transformed file
    """
    dataFile = ''
    file_directory = ''

    def __init__(self, file_path):
        """
        Creates an instance of ETL_Package_Auto1

        Parameters
        ----------

        file_path : str
            path of the source file
        """
        EtlPackageAuto1.dataFile = file_path
        EtlPackageAuto1.file_directory = os.path.splitext(file_path)[0]

    @staticmethod
    def load(file):
        """
        Loads the source file, clean the data and create a staging file

        Parameters
        ----------
            file : str
                path of the source file
        """
        staging_data=[]
        with open(file) as data:
            reader = csv.DictReader(data, delimiter=";")
            for row in reader:
                data = DataCleanUtils.is_row_clean(row_data=row,fields=EtlPackageAuto1._REQUIRED_COLUMNS)
                if data['is_clean_row']:
                    staging_data.append(data['dict_data'])

        EtlPackageAuto1.dataFile = FileUtils.write_file(file_name=f'{EtlPackageAuto1.file_directory}_staging.csv',data_dict=staging_data)['file_name']

    @staticmethod
    def transform(file):
        """
        Performs required transformation on the staging file

        Parameters
        ----------
            file : str
                path to the staging file

        Returns:
        --------
            transformed_data : list
                list matrix with first list as header and rest of the lists as values.

        """
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
                    try:
                        dictionary['make'] = item['make']
                    except:
                        raise transformations.MakeError(row_number)
                except Exception:
                    continue

                transformed_data.append(dictionary)

            list_matrix =  FileUtils.write_file(file_name=f'{EtlPackageAuto1.file_directory}_transformed.csv',data_dict=transformed_data)['list_matrix']
            return list_matrix
