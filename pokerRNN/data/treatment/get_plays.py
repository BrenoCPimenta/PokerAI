
def getPlays(line):
  """
    A partir da linha inicial de dados do Pluribus,
    separa as informações.
  """
  data = {
          'handIndex' : '',
              'play'  : [],
       'cardsPlayers' : [],
         'cardsTable' : [],
              'bets'  : [],
             'players': []    
  }
  cards = ""

  line = list(line)
  twoPoints = 0
  for currentState in line:
    if (currentState == ':'):
      twoPoints += 1
    elif twoPoints == 1 :
      data['handIndex'] = currentState
    elif twoPoints == 2 :
      data['play'].append(currentState)
    elif twoPoints == 3 :
      cards += currentState
    elif twoPoints == 4 :
      data['bets'].append(currentState)
    elif twoPoints == 5 :
      data['players'].append(currentState)

  #Treating players name
  # data['players'].pop() #Remove '\n'
  data['players'] = ''.join(data['players']).split('|') #Join the name of the players

  #Treating bets
  data['bets'] = ''.join(data['bets']).split('|') #Join bet values

  #Treating Rounds
  data['rounds_quantity'] = data['play'].count('/')
  data['play'] = ''.join(data['play']).split('/')
  

  #Treating Cards:
  if data['rounds_quantity'] == 0:
    data['cardsPlayers'] = cards
  else:
    data['cardsPlayers'], data['cardsTable'] = cards.split('/', 1)

  data['cardsPlayers'] = ''.join(data['cardsPlayers']).split('|')
  data['cardsTable'] = ''.join(data['cardsTable']).split('/')

  return data
