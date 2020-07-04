import pandas as pd
import numpy as np
def linearizeData(raw_data):
    data = []
    situation_name = ''

    for situation in range(len(raw_data)):
        #In order to keep numerical values this block is drepecated
        '''
        if situation == 0: situation_name = "preflop" 
        if situation == 1: situation_name = "flop" 
        if situation == 2: situation_name = "turn" 
        if situation == 3: situation_name = "river"
        '''
        turns_per_players = [0, 0, 0, 0, 0, 0]

        for turn in range(len(raw_data[situation])):
            players_turn = turns_per_players[raw_data[situation][turn][0]]
            
            turns_per_players[raw_data[situation][turn][0]] += 1

            raw_data[situation][turn].insert(1,situation)
            raw_data[situation][turn].insert(2,players_turn)

            data.append(raw_data[situation][turn])

    return data

def linearizedDataToDataFrame(data):
    df = pd.DataFrame(np.array(data),
                        columns=['Position',
                                  'Situation',
                                  'Turn',
                                  'Pot',
                                  'Hand',
                                  'Action',
                                  'Raise'])
    return df


