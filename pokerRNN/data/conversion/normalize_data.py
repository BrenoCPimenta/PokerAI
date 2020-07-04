import json
import os
import pandas as pd
import numpy as np

from pokerRNN import env


def normalizeNumberData(df, use_calculated_scaler=True):
    if use_calculated_scaler:
        scaler = json.load( open( os.environ.get('SCALER') ))
    else:
        scaler = {}

    columns_to_normalize = [
        'Position',
        'Situation',
        'Turn',
        'Pot',
        'Hand',
        'PotOdds',
        'BoardPairs',
        'BoardColor',
        'BoardStraight']

    #Normalizing data betwen 0-1
    for feature_name in columns_to_normalize:
        #If is real data, the scales values must be from train data
        if use_calculated_scaler:
            min_value = scaler[feature_name][0]
            max_value = scaler[feature_name][1]
        #If is train data, scale must be calculated
        else:
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            scaler[feature_name] = [min_value, max_value]

        if min_value == max_value:
            df[feature_name] = 0.0
        else:
            df[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)

    # Save scaler values to reuse for test and production data
    if not use_calculated_scaler:
        json.dump( scaler, open( os.environ.get('SCALER'), 'w' ) )

    return df


def encodeCategoricalData(df):
    """
    Input data:
    out fold  hold  c   rs/ rm /rb
     0    0    0    0   0.34/0.67/1


     Output data:
     fold  c   rs/ rm /rb
       0   0  0.34/0.67/1
    """
    #Creating empty new encoded action columns
    empty_list = ([0.0] * len(df['Action']))

    enconded_columns = {
        'P1-R' : ([0.0] * len(df['Action'])),
        'P1-C' : ([0.0] * len(df['Action'])),
        'P1-BB' : ([0.0] * len(df['Action'])),
        'P1-SB' : ([0.0] * len(df['Action'])),
        'P1-Hold' : ([0.0] * len(df['Action'])),
        'P1-F' : ([0.0] * len(df['Action'])),
        'P1-Out' : ([0.0] * len(df['Action'])),
        'P2-R' : ([0.0] * len(df['Action'])),
        'P2-C' : ([0.0] * len(df['Action'])),
        'P2-BB' : ([0.0] * len(df['Action'])),
        'P2-SB' : ([0.0] * len(df['Action'])),
        'P2-Hold' : ([0.0] * len(df['Action'])),
        'P2-F' : ([0.0] * len(df['Action'])),
        'P2-Out' : ([0.0] * len(df['Action'])),
        'P3-R' : ([0.0] * len(df['Action'])),
        'P3-C' : ([0.0] * len(df['Action'])),
        'P3-BB' : ([0.0] * len(df['Action'])),
        'P3-SB' : ([0.0] * len(df['Action'])),
        'P3-Hold' : ([0.0] * len(df['Action'])),
        'P3-F' : ([0.0] * len(df['Action'])),
        'P3-Out' : ([0.0] * len(df['Action'])),
        'P4-R' : ([0.0] * len(df['Action'])),
        'P4-C' : ([0.0] * len(df['Action'])),
        'P4-BB' : ([0.0] * len(df['Action'])),
        'P4-SB' : ([0.0] * len(df['Action'])),
        'P4-Hold' : ([0.0] * len(df['Action'])),
        'P4-F' : ([0.0] * len(df['Action'])),
        'P4-Out' : ([0.0] * len(df['Action'])),
        'P5-R' : ([0.0] * len(df['Action'])),
        'P5-C' : ([0.0] * len(df['Action'])),
        'P5-BB' : ([0.0] * len(df['Action'])),
        'P5-SB' : ([0.0] * len(df['Action'])),
        'P5-Hold' : ([0.0] * len(df['Action'])),
        'P5-F' : ([0.0] * len(df['Action'])),
        'P5-Out' : ([0.0] * len(df['Action'])),
        'Act-F' : ([0.0] * len(df['Action'])),
        'Act-C' : ([0.0] * len(df['Action'])),
        'Act-Rs' : ([0.0] * len(df['Action'])),
        'Act-Rm' : ([0.0] * len(df['Action'])),
        'Act-Rb' : ([0.0] * len(df['Action']))
    }
    
    #Populating new encoded actions
    for index, row in df.iterrows():
        action = row['Action']

        if action == 'f':
            enconded_columns['Act-F'][index] = 1.0
        elif action == 'c':
            enconded_columns['Act-C'][index] = 1.0
        elif action == 'rs':
            enconded_columns['Act-Rs'][index] = 1.0
        elif action == 'rm':
            enconded_columns['Act-Rm'][index] = 1.0
        elif action == 'rb':
            enconded_columns['Act-Rb'][index] = 1.0

        for i in range(1, 6):
            row_key = "P"+str(i)+"-Action"
            action = row[row_key]
            
            if action == 'f':
                key = "P"+str(i)+"-F"
                enconded_columns[key][index] = 1.0
            elif action == 'out':
                key = "P"+str(i)+"-Out"
                enconded_columns[key][index] = 1.0
            elif action == 'hold':
                key = "P"+str(i)+"-Hold"
                enconded_columns[key][index] = 1.0
            elif action == 'sb':
                key = "P"+str(i)+"-SB"
                enconded_columns[key][index] = 1.0
            elif action == 'bb':
                key = "P"+str(i)+"-BB"
                enconded_columns[key][index] = 1.0
            elif action == 'c':
                key = "P"+str(i)+"-C"
                enconded_columns[key][index] = 1.0
            elif action == 'rs':
                key = "P"+str(i)+"-R"
                enconded_columns[key][index] = 0.37
            elif action == 'rm':
                key = "P"+str(i)+"-R"
                enconded_columns[key][index] = 0.67
            elif action == 'rb':
                key = "P"+str(i)+"-R"
                enconded_columns[key][index] = 1.0


    #Add new columns with encoded actions
    for key in enconded_columns:
        df[key] = pd.Series(enconded_columns[key])

    #Remove old columns with not encoded actions
    columns_to_drop = [
        'Action',
        'P1-Action',
        'P2-Action',
        'P3-Action',
        'P4-Action',
        'P5-Action']
    df.drop(columns_to_drop, axis=1, inplace=True)

    return df



    

def removeBlindPlaysAndResetIndex(df):
    df = df[df.Action != 'bb']
    df = df[df.Action != 'sb']
    df = df.reset_index(drop=True)
    return df


def turnIntoNPArray(df, df_type):
    """
    Array Dimensions:

    Jogos[
        Uma Mao[
            rodadas[
                []...[]
            ]
            resultado[
                []...[]
            ]
        ]
        .
        .
        .
    ]
    """

    input_columns = [
        'Position',
        'Situation',
        'Turn',
        'Pot',
        'Hand',
        'PotOdds',
        'BoardPairs',
        'BoardColor',
        'BoardStraight',
        'P1-R',
        'P1-C',
        'P1-BB',
        'P1-SB',
        'P1-Hold',
        'P1-F',
        'P1-Out',
        'P2-R',
        'P2-C',
        'P2-BB',
        'P2-SB',
        'P2-Hold',
        'P2-F',
        'P2-Out',
        'P3-R',
        'P3-C',
        'P3-BB',
        'P3-SB',
        'P3-Hold',
        'P3-F',
        'P3-Out',
        'P4-R',
        'P4-C',
        'P4-BB',
        'P4-SB',
        'P4-Hold',
        'P4-F',
        'P4-Out',
        'P5-R',
        'P5-C',
        'P5-BB',
        'P5-SB',
        'P5-Hold',
        'P5-F',
        'P5-Out']
        
    output_columns = [
        'Act-F',
        'Act-C',
        'Act-Rs',
        'Act-Rm',
        'Act-Rb']

    build_list = []

    hand_ids = df.HandId.unique()

    #Iterating over hands
    for hand in hand_ids:
        rows = df.loc[df['HandId'] == hand]
        input_list = []
        output_list = []
        #Iterating over actions per hands
        for index, row in rows.iterrows():
            input_list.append(row[input_columns].tolist())
            output_list.append(row[output_columns].tolist())
        build_list.append([input_list, output_list])


    
    if df_type == 'train':
        file_path = os.environ.get('TRAIN')
    elif  df_type == 'test':
        file_path = os.environ.get('TEST')
    else:
        file_path = df_type

    #transforming into a np multidimensional array and saving:
    np_array = np.array(build_list)
    np.save(file_path, np_array)


     