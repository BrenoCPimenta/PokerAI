
#Standart Libraries
import numpy as np
import pandas as pd
import re
import time
import os

#External Libraries
from treys import Card
from treys import Evaluator

#Local Imports
from pokerRNN import env
##saveCSVplays
from pokerRNN.data.file_handler import getPluribusData, getPreFlopCSV, getTrainTestRawSets
from pokerRNN.data.treatment.get_plays import getPlays
from pokerRNN.data.treatment.extract_raises import extractRaises
from pokerRNN.data.treatment.order_plays import orderPlays
from pokerRNN.data.calculated_information.hand_strength import setHandsStrenght
from pokerRNN.data.treatment.linearize_data import linearizeData, linearizedDataToDataFrame
from pokerRNN.data.conversion.assemble_plays import getGameState, gameStateToDataFrame, assembleAfterBoardTexture, separatingByPlayer
from pokerRNN.data.calculated_information.pot_raise import changePotRaiseMetrics, raiseAsPotPercentage, raiseAsPotPercentageAfterPreFlop, categorizeRaises
from pokerRNN.data.calculated_information.pot_odds import setValueToRaise, getPotOdds
from pokerRNN.data.calculated_information.board_texture import applyBoardTexture

##createFeedData
from pokerRNN.data.conversion.separate_sets import calculatePlaysPerRounds, getTrainTestSetsHandIds, createTrainTestSets
from pokerRNN.data.conversion.normalize_data import normalizeNumberData, removeBlindPlaysAndResetIndex, encodeCategoricalData, turnIntoNPArray


def helpTreat(line):
   
  print("------------------RAW DATA------------------")  
  pluribus_raw_lines = getPluribusData()
  print("Raw line: ", pluribus_raw_lines[line])

  print("------------------GET PLAYS------------------")
  game = getPlays(pluribus_raw_lines[line])
  print("Players         ", game['players'])
  print()
  print("Actions:        ", game['play'])
  print()
  print("Bets:           ", game['bets'])
  print()
  print("Players Cards:  ", game['cardsPlayers'])
  print()
  print("Cards on Table: ", game['cardsTable'])
  print()
  print("Rounds:         ", game['rounds_quantity'])


  print("\n------------------EXTRACTING RAISES------------------")
  print("Play before treating raises: ", game['play'])
  print()
  print("Play after treating raises: ", extractRaises(game['play']))


  print("\n------------------ORDERING PLAYS------------------")
  print("After ordering pays:")
  st_cnt = -1
  for situation in orderPlays(game['play']):
    st_cnt += 1
    print("---Sit", st_cnt)
    for turn in situation:
      print(turn)

  print("\n------------------SETTING HANDSTREGHT------------------")
  preflopRank = getPreFlopCSV()
  hands = setHandsStrenght(orderPlays(game['play']),
                      game['cardsPlayers'],
                      game['cardsTable'],
                      preflopRank)
  print("After setting handstrenght:")
  cnt = -1
  for round in hands:
    cnt+=1
    print("Round "+str(cnt))
    for hand in round:
      print(hand)

  print("\n------------------LINEARIZE DATA------------------")
  
  print("After linearized hand:")
  linear_hand = linearizeData(hands)
  print(linearizedDataToDataFrame(linear_hand))

  print("\n------------------ASSEMBLE PLAYS------------------")
  gameState = getGameState(linear_hand)
  print(gameStateToDataFrame(gameState)) 

  print("\n------------------NEW POTRAISE METRICS------------------")
  potRaise = changePotRaiseMetrics(linear_hand)
  df = pd.DataFrame(potRaise)
  print(df)

  print("\n------------------GET RAISED VALUE FOR POT ODDs------------------")
  prePotOdds = setValueToRaise(orderPlays(game['play']), potRaise)
  df = pd.DataFrame(prePotOdds)
  print(df)
  
  print("\n------------------GET POT ODDs------------------")
  pot_odd = getPotOdds(prePotOdds)
  df = pd.DataFrame(pot_odd)
  print(df)

  print("\n------------------RAISE PERCENTAGE AFTER PREFLOP------------------")
  raise_percentage = raiseAsPotPercentageAfterPreFlop(pot_odd)
  df = pd.DataFrame(raise_percentage)
  print(df)

  print("\n------------------CATEGORISE RAISE------------------")
  categorised_raises = categorizeRaises(raise_percentage)
  df = pd.DataFrame(categorised_raises)
  print(df)

  print("\n------------------APPLY BOARD TEXTURE------------------")
  data_with_board_texture = applyBoardTexture(game['cardsTable'], game['cardsPlayers'], categorised_raises)
  df = pd.DataFrame(data_with_board_texture)
  print(df)

  print("\n------------------ASSEMBLE PLAYS AFTER BOARD TEXTURE------------------")
  assembled_data_afterBoardTexture = assembleAfterBoardTexture(data_with_board_texture)
  df = pd.DataFrame(assembled_data_afterBoardTexture)
  print(df)

  print("\n------------------SEPARATE GAMES BY PLAY------------------")
  concat_hads = {
    'Action' : [],
    'HandId' : [],
    'Position' : [],
    'Situation' : [],
    'Turn' : [],
    'Pot' : [],
    'Hand' : [],
    'PotOdds' : [],
    'BoardPairs' : [],
    'BoardColor' : [],
    'BoardStraight' : [],
    'P1-Action' : [],
    'P2-Action' : [],
    'P3-Action' : [],
    'P4-Action' : [],
    'P5-Action' : []}

  concated_hands, hand_id = separatingByPlayer(2, 2, assembled_data_afterBoardTexture)
  df = pd.DataFrame(concated_hands)
  print(df)


  print("\n------------------RAW TRAIN TEST------------------")
  train_raw_df, test_raw_df = getTrainTestRawSets()
  print(train_raw_df)



  print("\n------------------NUMBER NORMALIZED------------------")
  train_numbers_normalized = normalizeNumberData(train_raw_df, use_calculated_scaler=True)
  print(train_numbers_normalized[[
        'Position',
        'Situation',
        'Turn',
        'Pot',
        'Hand',
        'PotOdds',
        'BoardPairs',
        'BoardColor',
        'BoardStraight']])







#------------------------------------------------------------------------------------------------------
def saveCSVplays():
  concat_hands = {
    'Action' : [],
    'TableId' : [],
    'HandId' : [],
    'Position' : [],
    'Situation' : [],
    'Turn' : [],
    'Pot' : [],
    'Hand' : [],
    'PotOdds' : [],
    'BoardPairs' : [],
    'BoardColor' : [],
    'BoardStraight' : [],
    'P1-Action' : [],
    'P2-Action' : [],
    'P3-Action' : [],
    'P4-Action' : [],
    'P5-Action' : []}

  start_time = time.time()
  pluribus_raw_lines = getPluribusData()
  preflopRank = getPreFlopCSV()
  cnt = 0
  last_hand_id = 0
  for table_id, line in enumerate(pluribus_raw_lines):
    print(cnt)
    cnt+=1
    game = getPlays(line)
    hands = setHandsStrenght(orderPlays(game['play']),
                        game['cardsPlayers'],
                        game['cardsTable'],
                        preflopRank)
    linear_hand = linearizeData(hands)
    potRaise = changePotRaiseMetrics(linear_hand)
    prePotOdds = setValueToRaise(orderPlays(game['play']), potRaise)
    pot_odd = getPotOdds(prePotOdds)
    raise_percentage = raiseAsPotPercentageAfterPreFlop(pot_odd)
    categorised_raises = categorizeRaises(raise_percentage)
    data_with_board_texture = applyBoardTexture(game['cardsTable'], game['cardsPlayers'], categorised_raises)
    assembled_data_afterBoardTexture = assembleAfterBoardTexture(data_with_board_texture)
    new_concated_hands, last_hand_id = separatingByPlayer(table_id, last_hand_id, assembled_data_afterBoardTexture)

    concat_hands['Action'].extend(new_concated_hands['Action'])
    concat_hands['TableId'].extend(new_concated_hands['TableId'])
    concat_hands['HandId'].extend(new_concated_hands['HandId'])
    concat_hands['Position'].extend(new_concated_hands['Position'])
    concat_hands['Situation'].extend(new_concated_hands['Situation'])
    concat_hands['Turn'].extend(new_concated_hands['Turn'])
    concat_hands['Pot'].extend(new_concated_hands['Pot'])
    concat_hands['Hand'].extend(new_concated_hands['Hand'])
    concat_hands['PotOdds'].extend(new_concated_hands['PotOdds'])
    concat_hands['BoardPairs'].extend(new_concated_hands['BoardPairs'])
    concat_hands['BoardColor'].extend(new_concated_hands['BoardColor'])
    concat_hands['BoardStraight'].extend(new_concated_hands['BoardStraight'])
    concat_hands['P1-Action'].extend(new_concated_hands['P1-Action'])
    concat_hands['P2-Action'].extend(new_concated_hands['P2-Action'])
    concat_hands['P3-Action'].extend(new_concated_hands['P3-Action'])
    concat_hands['P4-Action'].extend(new_concated_hands['P4-Action'])
    concat_hands['P5-Action'].extend(new_concated_hands['P5-Action'])


  pd.DataFrame(concat_hands).to_csv(os.environ.get('CONCATED_HANDS'), encoding='utf-8', index=False)

  final_time = time.time() - start_time
  if final_time / 60 > 0:
    print("in minutes:")
    final_time = final_time / 60 
  print(final_time)




#----------------------------------------------------------------------------------------------------
def createFeedData(create_new_sets=False, verbose=False):
  if create_new_sets:
    calculatePlaysPerRounds()
    createTrainTestSets()

  train_raw_df, test_raw_df = getTrainTestRawSets()

  if create_new_sets:
    train_numbers_normalized = normalizeNumberData(train_raw_df, use_calculated_scaler=False)
  else:
    train_numbers_normalized = normalizeNumberData(train_raw_df, use_calculated_scaler=True)

  #Test always use train scalers
  test_numbers_normalized = normalizeNumberData(test_raw_df, use_calculated_scaler=True)

  train_without_blinds = removeBlindPlaysAndResetIndex(train_numbers_normalized)
  test_without_blinds = removeBlindPlaysAndResetIndex(test_numbers_normalized)

  train_full_normalized = encodeCategoricalData(train_without_blinds)
  test_full_normalized = encodeCategoricalData(test_without_blinds)

  if verbose == True:
    sample_columns = [ 
          'P1-R',
          'P1-C',
          'P1-BB',
          'P1-SB',
          'P1-Hold',
          'P1-F',
          'P1-Out',
          'P5-R',
          'P5-C',
          'P5-BB',
          'P5-SB',
          'P5-Hold',
          'P5-F',
          'P5-Out',
          'Act-F',
          'Act-C',
          'Act-Rs',
          'Act-Rm',
          'Act-Rb']
    
    sample = train_full_normalized[sample_columns]
    print(sample[200:240])
    sample = test_full_normalized[sample_columns]
    print(sample[200:240])

  return (train_full_normalized, test_full_normalized)



def saveDataAsNumpy(create_new_sets=False, verbose=False):
  train_full_normalized, test_full_normalized = createFeedData(create_new_sets, verbose)
  turnIntoNPArray(train_full_normalized, 'train')
  turnIntoNPArray(test_full_normalized, 'test')
