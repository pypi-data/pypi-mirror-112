import csv

def write_file(file_name, data_dict):
    list_matrix=[]
    header = list(data_dict[0].keys())
    list_matrix.append(header)

    for item in data_dict:
        list_matrix.append(list(item.values()))

    with open(file_name, 'w', encoding='UTF8' , newline='') as file:
        writer = csv.writer(file)
        writer.writerows(list_matrix)
    
    if 'staging' in file_name:
        return file_name


def cents_to_euro(cents, euro = 0.000120):
    return int(cents)*euro


def isRowClean(row_data, fields):
    dictionary = {}
    is_clean_row = True
    for field in fields:
                if row_data[field].strip() != '-':
                    dictionary[field] = row_data[field].strip()
                else:
                    is_clean_row = False
                    break
    return {'is_clean_row':is_clean_row, 'dict_data':dictionary}