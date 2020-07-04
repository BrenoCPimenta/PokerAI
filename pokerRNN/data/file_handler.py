import os
import pandas as pd
from pokerRNN import env

def getPluribusData():
    pluribus_raw_lines = []
    with open (os.environ.get('PLURIBUS'), 'rt') as pluribus_file:
        for file_line in pluribus_file:
            pluribus_raw_lines.append(file_line)

    return pluribus_raw_lines



def getPreFlopCSV():
    preflopRank_DF = pd.read_csv(os.environ.get('PREFLOP'))
    preflopRank = preflopRank_DF.values.tolist()
    preflopRank.insert(0, preflopRank_DF.columns.tolist())

    return preflopRank


def getConcatedHands():
    concated_hands_df = pd.read_csv(os.environ.get('CONCATED_HANDS'), index_col=None)
    return concated_hands_df

def getHandIdsPerSituation():
    preflop_series = pd.read_csv(os.environ.get('HANDIDS_PER_SITUATIONS_PREFLOP'), index_col=None, squeeze=True)
    flop_series = pd.read_csv(os.environ.get('HANDIDS_PER_SITUATIONS_FLOP'), index_col=None, squeeze=True)
    turn_series = pd.read_csv(os.environ.get('HANDIDS_PER_SITUATIONS_TURN'), index_col=None, squeeze=True)
    river_series = pd.read_csv(os.environ.get('HANDIDS_PER_SITUATIONS_RIVER'), index_col=None, squeeze=True)
    return (preflop_series, flop_series, turn_series, river_series)

def getTrainTestRawSets():
    train_raw_df = pd.read_csv(os.environ.get('NOT_NORMALIZED_TRAIN'), index_col=None)
    test_raw_df = pd.read_csv(os.environ.get('NOT_NORMALIZED_TEST'), index_col=None)
    return (train_raw_df, test_raw_df)

def getDataSets():
    train_np = np.load(os.environ.get['TRAIN'])
    test_np = np.load(os.environ.get['TEST'])
    return (train_np, test_np)



