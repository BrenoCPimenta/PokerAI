import pandas as pd
import os
import time
from random import shuffle

from pokerRNN import env
from pokerRNN.data.file_handler import getConcatedHands, getHandIdsPerSituation



def calculatePlaysPerRounds():
    start_time = time.time()
    concated_hands_df = getConcatedHands()
    #print(concated_hands_df[115:138])
    print(concated_hands_df)

    hands = concated_hands_df['HandId'].values.tolist()
    situations_list = concated_hands_df['Situation'].values.tolist()

    ids_per_situation = {
        'preflop' : [],
        'flop' : [],
        'turn' : [],
        'river' : []
    }

   
    #Go through all hands and save their last situation:
    for i in range(1, (hands[-1] + 1)):
        indice = len(hands) - hands[::-1].index(i) - 1
        situation = situations_list[indice]
        if situation == 0:
            ids_per_situation['preflop'].append(indice)
        elif situation == 1:
            ids_per_situation['flop'].append(indice)
        elif situation == 2:
            ids_per_situation['turn'].append(indice)
        elif situation == 3:
            ids_per_situation['river'].append(indice)

    print("PREFLOP: ", len(ids_per_situation['preflop']))
    print("FLOP: ", len(ids_per_situation['flop']))
    print("TURN: ", len(ids_per_situation['turn']))
    print("RIVER: ", len(ids_per_situation['river']))

    
    pd.Series(ids_per_situation['preflop']).to_csv(os.environ.get('HANDIDS_PER_SITUATIONS_PREFLOP'), encoding='utf-8', index=False)
    pd.Series(ids_per_situation['flop']).to_csv(os.environ.get('HANDIDS_PER_SITUATIONS_FLOP'), encoding='utf-8', index=False)
    pd.Series(ids_per_situation['turn']).to_csv(os.environ.get('HANDIDS_PER_SITUATIONS_TURN'), encoding='utf-8', index=False)
    pd.Series(ids_per_situation['river']).to_csv(os.environ.get('HANDIDS_PER_SITUATIONS_RIVER'), encoding='utf-8', index=False)



    final_time = time.time() - start_time
    if final_time / 60 > 0:
        print("in minutes:")
        final_time = final_time / 60 
    print(final_time)



def getTrainTestSetsHandIds():
    preflop_series, flop_series, turn_series, river_series = getHandIdsPerSituation()

    #Shuffle values
    preflop_list = preflop_series.tolist()
    flop_list = flop_series.tolist()
    turn_list = turn_series.tolist()
    river_list = river_series.tolist()


    shuffle(preflop_list)
    shuffle(flop_list)
    shuffle(turn_list)
    shuffle(river_list)


    #Getting the 80% indice
    train_preflop_indice = int(round(len(preflop_list)*.8))
    train_flop_indice = int(round(len(flop_list)*.8))
    train_turn_indice = int(round(len(turn_list)*.8))
    train_river_indice = int(round(len(river_list)*.8))

    #Join hand ids
    train_hand_ids = []
    test_hand_ids = []

    train_hand_ids.extend(preflop_list[:train_preflop_indice])
    train_hand_ids.extend(flop_list[:train_flop_indice])
    train_hand_ids.extend(turn_list[:train_turn_indice])
    train_hand_ids.extend(river_list[:train_river_indice])

    test_hand_ids.extend(preflop_list[train_preflop_indice:])
    test_hand_ids.extend(flop_list[train_flop_indice:])
    test_hand_ids.extend(turn_list[train_turn_indice:])
    test_hand_ids.extend(river_list[train_river_indice:])

    #Shufle values to mix the situations:
    shuffle(train_hand_ids)
    shuffle(test_hand_ids)

    return (train_hand_ids, test_hand_ids)
    

def createTrainTestSets():
    start_time = time.time()
    concated_hands_df = getConcatedHands()
    train_hand_ids, test_hand_ids = getTrainTestSetsHandIds()

    #Creating Empty dataframes:
    ##train
    train_raw_dataset = pd.DataFrame().reindex_like(concated_hands_df)
    train_raw_dataset = train_raw_dataset[train_raw_dataset['HandId'].notna()]
    ##test
    test_raw_dataset = pd.DataFrame().reindex_like(concated_hands_df)
    test_raw_dataset = test_raw_dataset[test_raw_dataset['HandId'].notna()]


    #Populating dataframes:
    ##train
    for i in train_hand_ids:
        train_raw_dataset = train_raw_dataset.append(concated_hands_df[concated_hands_df['HandId'] == i])
    ##test
    for i in test_hand_ids:
        test_raw_dataset = test_raw_dataset.append(concated_hands_df[concated_hands_df['HandId'] == i])
    
    print(train_raw_dataset)

    #Saving DFs as CSVs
    train_raw_dataset.to_csv(os.environ.get('NOT_NORMALIZED_TRAIN'), encoding='utf-8', index=False)
    test_raw_dataset.to_csv(os.environ.get('NOT_NORMALIZED_TEST'), encoding='utf-8', index=False)

    final_time = time.time() - start_time
    if final_time / 60 > 0:
        print("in minutes:")
        final_time = final_time / 60 
    print(final_time)
    
