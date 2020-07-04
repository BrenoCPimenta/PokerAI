import matplotlib.pyplot as plt
import numpy as np
import os
import time

from pokerRNN import env
from pokerRNN.data.file_handler import getPluribusData, getPreFlopCSV
from pokerRNN.data.treatment.get_plays import getPlays
from pokerRNN.data.treatment.extract_raises import extractRaises
from pokerRNN.data.treatment.order_plays import orderPlays
from pokerRNN.data.calculated_information.hand_strength import setHandsStrenght
from pokerRNN.data.treatment.linearize_data import linearizeData
from pokerRNN.data.calculated_information.pot_raise import changePotRaiseMetrics, raiseAsPotPercentage
from pokerRNN.data.calculated_information.pot_odds import setValueToRaise, getPotOdds



def populateRaiseFilesData():
    raises_per_stack = []
    raises_per_stack_preflop = []
    raises_per_stack_afterflop = []
    raises_per_pot_preflop = []
    raises_per_pot_afterflop = []

    pluribus_raw_lines = getPluribusData()

    cnt =0
    for line in pluribus_raw_lines:
        if cnt%300 == 0:
            print(cnt)
        cnt +=1
        game = getPlays(line)

        #-----Stack
        for situation, data in enumerate(orderPlays(game['play'])):
            for hand in data:
                if hand[2] == 'r':
                    #Overall stack:
                    raise_value = hand[3]
                    raises_per_stack.append(raise_value)
                    #Preflop:
                    if situation == 0:
                        raises_per_stack_preflop.append(raise_value)
                    else:
                        raises_per_stack_afterflop.append(raise_value)


        #-----Pot
        preflopRank = getPreFlopCSV()
        hands = setHandsStrenght(orderPlays(game['play']),
                            game['cardsPlayers'],
                            game['cardsTable'],
                            preflopRank)
        linear_hand = linearizeData(hands)
        potRaise = changePotRaiseMetrics(linear_hand)
        prePotOdds = setValueToRaise(orderPlays(game['play']), potRaise)
        pot_odd = getPotOdds(prePotOdds)
        data = raiseAsPotPercentage(pot_odd)

        for i in range(len(data['Raise'])):
            if data['Action'][i] == 'r':
                if data['Situation'][i] == 0:
                    raises_per_pot_preflop.append(data['Raise'][i])
                else:
                    raises_per_pot_afterflop.append(data['Raise'][i])
    print(cnt)
    print("Stack ", len(raises_per_stack))
    print("PotPre ", len(raises_per_pot_preflop))
    print("PotAfter ", len(raises_per_pot_afterflop))

    createFileData('RAISE_STACK', raises_per_stack)
    createFileData('RAISE_STACK_PREFLOP', raises_per_stack_preflop)
    createFileData('RAISE_STACK_AFTERFLOP', raises_per_stack_afterflop)
    createFileData('RAISE_POT_PREFLOP', raises_per_pot_preflop)
    createFileData('RAISE_POT_AFTERFLOP', raises_per_pot_afterflop)

def createFileData(data_file, data_list):
    with open(os.environ.get(data_file), 'w+') as f:
        for value in data_list:
            f.write(str(value) + "\n")

start_time = time.time()
populateRaiseFilesData()
print("--- %s seconds ---" % (time.time() - start_time))