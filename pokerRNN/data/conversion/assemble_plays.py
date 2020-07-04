import pandas as pd
import numpy as np

def zero_games(games):
  for it in range(len(games)):
    # print(games[it][0])

    games[it][1] = 0
    if games[it][0] != 'f' and games[it][0] != 'out':
      games[it][0] = 'hold'
    else:
      games[it][0] = 'out'
  
  return games

def treatingFolds(games, player, last_player):
  # print("Entrou treating Folds: Last_Player:", last_player, " e player:", player)
  if player < last_player:
    last_player = last_player-6
    
  distance = player - last_player
  
  if distance == 1:
    return games
  else:
    while(distance != 1):
      # print("Entrou while com distance:", distance)
      distance -= 1

      last_player += 1

      if last_player > 5:
        last_player = 0
      # print("Player zerado é o ", player)
      games[last_player][0] = "out"
      games[last_player][1] = 0
    return games
      
      

def getGameState(data):
  games = [['sm', 0.005],
          ['bb', 0.015],
          ['hold', 0],
          ['hold', 0],
          ['hold', 0],
          ['hold', 0]]
  last_player = 1
  last_situation = data[0][1]

  for it in range(len(data)):
    # print(0)
    if(it != 0 and it != 1):
      current_situation = data[it][1]

      if current_situation != last_situation:
        games = zero_games(games)
        last_situation = current_situation

      player = data[it][0]    
      action = data[it][5]
      bet = data[it][6]

      games[player][0] = action
      games[player][1] = bet

      if current_situation == last_situation:
        games = treatingFolds(games, player, last_player)

      for i in range(6):
        if i == player:
          pass
        else:
          data[it].append(games[i][0])
          data[it].append(games[i][1])

      last_player = player

  
  return data


def gameStateToDataFrame(gameState):
  test_df = pd.DataFrame(np.array(gameState[2:]),
                          columns=['Position',
                                    'Situation',
                                    'Turn',
                                    'Pot',
                                    'Hand',
                                    'Action',
                                    'Raise',
                                    'P1-Action',
                                    'P1-Bet',
                                    'P2-Action',
                                    'P2-Bet',
                                    'P3-Action',
                                    'P3-Bet',
                                    'P4-Action',
                                    'P4-Bet',
                                    'P5-Action',
                                    'P5-Bet'])
            
  return test_df




def assembleAfterBoardTexture(data):
  data['P1-Action'] = []
  data['P2-Action'] = []
  data['P3-Action'] = []
  data['P4-Action'] = []
  data['P5-Action'] = []
  other_plays = ['hold', 'hold', 'hold', 'hold', 'hold', 'hold']
  players_folded = [False, False, False, False, False, False]

  last_situation = 0
  last_turn = 0
  for i in range(len(data['Action'])):
    player = data['Position'][i]
    round_action = data['Action'][i]

    #Situation or Turn changes
    if last_situation != data['Situation'][i]:# or last_turn != data['Turn'][i]:
      last_situation = data['Situation'][i]
      #last_turn = data['Turn'][i]
      for i in range(6):
        if players_folded[i] and other_plays[i] != 'out':
          other_plays[i] = 'out'
        elif other_plays[i] != 'out':
          other_plays[i] = 'hold'

    #Setting actual action and extractind other actions
    temp_list = []
    for j in range(6):
      if j == player:
        other_plays[j] = round_action
        if round_action == 'f':
          players_folded[j] = True
      else:
        temp_list.append(other_plays[j])
      
    #Setting other actions
    data['P1-Action'].append(temp_list[0])
    data['P2-Action'].append(temp_list[1])
    data['P3-Action'].append(temp_list[2])
    data['P4-Action'].append(temp_list[3])
    data['P5-Action'].append(temp_list[4])

  return data
          
        


def separatingByPlayer(table_id, last_hand_id, hand_data):
  concat_data = {
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
  
  for position in range(6):
    last_hand_id += 1
    for i in range(len(hand_data['Action'])):
      if hand_data['Position'][i] == position:
        concat_data['TableId'].append(table_id)
        concat_data['HandId'].append(last_hand_id)
        concat_data['Position'].append(hand_data['Position'][i])
        concat_data['Situation'].append(hand_data['Situation'][i])
        concat_data['Turn'].append(hand_data['Turn'][i])
        concat_data['Pot'].append(hand_data['Pot'][i])
        concat_data['Hand'].append(hand_data['Hand'][i])
        concat_data['Action'].append(hand_data['Action'][i])
        concat_data['PotOdds'].append(hand_data['PotOdds'][i])
        concat_data['BoardPairs'].append(hand_data['BoardPairs'][i])
        concat_data['BoardColor'].append(hand_data['BoardColor'][i])
        concat_data['BoardStraight'].append(hand_data['BoardStraight'][i])
        concat_data['P1-Action'].append(hand_data['P1-Action'][i])
        concat_data['P2-Action'].append(hand_data['P2-Action'][i])
        concat_data['P3-Action'].append(hand_data['P3-Action'][i])
        concat_data['P4-Action'].append(hand_data['P4-Action'][i])
        concat_data['P5-Action'].append(hand_data['P5-Action'][i])
  
  return (concat_data, last_hand_id)



