import pandas as pd
import numpy as np
from datetime import datetime




def morning_trip():
    df = pd.read_excel('BC-PS-BC-Hari-Bekerja-10072023.xlsx', sheet_name="Table 2")

    depart_destination = ["Pulau Sebang", "KL Sentral"]
    train_scedule = df.loc[df['Nombor Tren'].isin(depart_destination)]

    # check destination route if nan, drop col
    idx = 0
    column_to_be_drop = []
    for x in train_scedule:
        try:
            datetime.strptime((train_scedule.iat[0,idx]), '%H:%M').time()
        except:
            column_to_be_drop.append(idx)
        
        idx = idx + 1

    train_scedule.drop(train_scedule.columns[column_to_be_drop], axis=1, inplace=True)

    return train_scedule
    



def evening_trip():
    df = pd.read_excel('BC-PS-BC-Hari-Bekerja-10072023.xlsx', sheet_name="Table 1")

    depart_destination = [ "Kuala Lumpur", "Pulau Sebang"]
    train_scedule = df.loc[df['Nombor Tren'].isin(depart_destination)]

    # check destination route if nan, drop col
    idx = 0
    column_to_be_drop = []
    for y in train_scedule:
        try:
            datetime.strptime((train_scedule.iat[1,idx]), '%H:%M').time()
        except:
            column_to_be_drop.append(idx)
        
        idx = idx + 1

    train_scedule.drop(train_scedule.columns[column_to_be_drop], axis=1, inplace=True)

    return train_scedule
    


pergi = morning_trip()
balik = evening_trip()

print(">>>>>>> Morning trip")
print(pergi.to_string())

print(">>>>>>> Evening trip")
print(balik.to_string())

