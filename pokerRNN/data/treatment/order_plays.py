from pokerRNN.data.treatment.extract_raises import extractRaises

def orderPlays(playsWithRaise):
  """
  Separa as rodadas por jogadores e suas ações, com a porcentagem do raise e o valor no pote
  """

  #Initializing data structure
  #Each inside array represets a game state: preflop, flop...
  data = [[], [], [], []]
  round_counter = -1

  #Treating small and big blinds
  small_blind_value = float(50)/float(10000)
  big_blind_value = float(100)/float(10000)
  data[0].append([0, 0, 'sb', small_blind_value])  #sb stands for smallBlind
  data[0].append([1, small_blind_value, 'bb', big_blind_value])  #bb stands for bigBlind 

  #Managing players on match
  players_on_match = [0,1,2,3,4,5]
  moment_player = 2

  #Managing raise values
  raises, normalPlays = extractRaises(playsWithRaise)
  count_raise = 0
  biggest_raise = 0
  raise_value = 0
  already_payed_raises = [0,0,0,0,0,0]

  #Managing pot value
  pot = small_blind_value + big_blind_value


  for game_round in normalPlays: #Loop through game states
    round_counter += 1

    #In the beginning of every round the raise state is zero
    raise_value = 0 
    biggest_raise = 0
    already_payed_raises = [0,0,0,0,0,0]

    for bet in game_round: #Loop through player bets
      #Looping through players
      if moment_player == len(players_on_match):
        moment_player = 0

      #Call and Checks
      if(bet == 'c'):

        data[round_counter].append([players_on_match[moment_player],
                                    round(pot,3),
                                    'c',
                                    0])
        
        pay = biggest_raise - already_payed_raises[players_on_match[moment_player]]
        
        pot +=  pay 
        already_payed_raises[players_on_match[moment_player]] += pay

        moment_player += 1
        
      #Fold
      if(bet == 'f'):
        data[round_counter].append([players_on_match[moment_player],
                                    round(pot,3),
                                    'f',
                                    0])
        
        del players_on_match[moment_player]

      #Raise
      if(bet == 'r'):
        raise_value = raises[count_raise]
        biggest_raise += raise_value
        count_raise += 1
        
        data[round_counter].append([players_on_match[moment_player],
                                    round(pot,3),
                                    'r',
                                    raise_value])
        
        pay = biggest_raise - already_payed_raises[players_on_match[moment_player]]

        already_payed_raises[players_on_match[moment_player]] += pay
        pot += pay
        moment_player += 1
  return data