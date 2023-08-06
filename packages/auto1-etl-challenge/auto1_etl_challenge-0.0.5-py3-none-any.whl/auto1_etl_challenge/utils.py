"""Utilities module for ETL"""

import csv

class FileUtils:
    """
    Utility for file relation operations.

    Methods:
    --------

    Static:
        write_file: Writes data into the file
    """

    @staticmethod
    def write_file(file_name, data_dict):
        """
        Writes data into the file

        Parameters
        ----------
            file_name : str
                path of the file
            data_dict : dict
                data to be written into the file

        Returns:
        --------
            dict
                key/value pair for file_name and list_matrix
        """
        list_matrix=[]
        header = list(data_dict[0].keys())
        list_matrix.append(header)

        for item in data_dict:
            list_matrix.append(list(item.values()))

        with open(file_name, 'w', encoding='UTF8' , newline='') as file:
            writer = csv.writer(file)
            writer.writerows(list_matrix)


        return {'file_name':file_name,'list_matrix':list_matrix}


class ConversionsUtils:

    """
    Utility for conversions.

    Methods:
    -------

    Static:
        cents_to_euro: Writes data into the file
    """

    @staticmethod
    def cents_to_euro(cents, euro = 0.000120):
        """
        Converts cents to euros

        Parameters
        ----------
            cents : int
                cents in integer
            euro : int
                euro rate for conversion

        Returns:
        --------
            int
                returns euro
        """
        return int(cents)*euro


class DataCleanUtils:
    """
    Utility for data cleaning.

    Methods:
    -------

    Static:
        isRowClean: Cleans the data row
    """

    @staticmethod
    def is_row_clean(row_data, fields):
        """
        Cleans the data in the row

        Parameters
        ----------
            row_data : dict
                row in data file
            fields : list
                required fields for output

        Returns:
        --------
            dict
                returns boolean flag and output in dictionary
        """
        dictionary = {}
        garbage = {'-':''}
        is_clean_row = True

        for field in fields:
            if garbage.get(row_data[field].strip()):
                dictionary[field] = row_data[field].strip()
            else:
                is_clean_row = False
                break

        return {'is_clean_row':is_clean_row, 'dict_data':dictionary}
