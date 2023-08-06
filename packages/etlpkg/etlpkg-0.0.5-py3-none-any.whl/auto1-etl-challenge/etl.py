import csv
from constants import Constants
import utils

dataFile = r'challenge_me.txt'

def load(file):
    staging_data=[]
    required_fields = ['engine-location','num-of-cylinders','engine-size','weight','horsepower','aspiration','price','make']
    
    with open(file) as data:
        reader = csv.DictReader(data, delimiter=";")
        for row in reader:
            data = utils.isRowClean(row_data=row,fields=required_fields)
            
            if data['is_clean_row']:
                staging_data.append(data['dict_data'])
    
    global dataFile
    dataFile = utils.write_file(file_name='challenge_me_staging.csv',data_dict=staging_data)


def transform(file):
    transformed_data=[]
    with open(file) as data:
        staging_data = csv.DictReader(data)
        for count,item in enumerate(staging_data, start=2):
            dictionary = {}

            try:
                if Constants.ENGINE_LOCATION.get(item['engine-location']) is not None:
                    dictionary['engine-location'] = Constants.ENGINE_LOCATION.get(item['engine-location'])
                else:
                    raise Exception
                
                if Constants.NUMBERS.get(item['num-of-cylinders']) is not None:
                    dictionary['num-of-cylinders'] = Constants.NUMBERS.get(item['num-of-cylinders'])
                else:
                    raise Exception
                
                dictionary['engine-size'] = int(item['engine-size']) 
                dictionary['weight'] = int(item['weight']) 
                dictionary['horsepower'] = float(item['horsepower'].replace(',','.')) 

                if Constants.ASPIRATION.get(item['aspiration']) is not None:
                    dictionary['aspiration'] = Constants.ASPIRATION.get(item['aspiration'])
                else:
                    raise Exception
                
                dictionary['price'] = utils.cents_to_euro(item['price']) 
                dictionary['make'] = item['make'].encode()

            except Exception as e:
                print(f'{e.__class__} occured in file on line number: {count}')
                continue

            transformed_data.append(dictionary)
        
        utils.write_file(file_name='challenge_me_transfomred.csv',data_dict=transformed_data)
        return transformed_data


load(dataFile)
result = transform(dataFile)
print(f'Transformed Data Length {len(result)}')










