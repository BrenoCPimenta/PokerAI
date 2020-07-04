from treys import Card
from treys import Evaluator

def findPreFlopRank(cards, suit_char, preflopRank):
    """
    Receive pocket cards and returns the preflop rank for them. 
    """
    for index in range(len(preflopRank)):
        if (cards == preflopRank[index][1] or cards[::-1] == preflopRank[index][1]) and suit_char == preflopRank[index][2]:
            rank_before_conversion_range = int(preflopRank[index][0])
            #This multiplication is to acert the range of this rank to be the same as the trey's librarie:
            rank_after_conversion_range = ((rank_before_conversion_range - 1) * 44 ) + 1
            return rank_after_conversion_range
            


def setHandsStrenght(data, cards_players, cards_table, preflopRank):
  #Setting Board cards
  table_cards = []
  if cards_table[0] != '':
    for rounds in range(len(cards_table)):
      if rounds == 0:
        table_cards.append([Card.new(cards_table[rounds][:2]),
                            Card.new(cards_table[rounds][2:4]),
                            Card.new(cards_table[rounds][4:6])
                            ])
      if rounds == 1:
        table_cards.append((table_cards[0]).copy())
        table_cards[1].append(Card.new(cards_table[rounds]))
      
      if rounds == 2:
        table_cards.append(table_cards[1].copy())
        table_cards[2].append(Card.new(cards_table[rounds]))
      

  #Setting hand strenght into data
  evaluator = Evaluator()

  for game_state in range(len(data)):
    if 1 ==1: #data[game_state] != []:
      for hand in range(len(data[game_state])):
        hand_cards = cards_players[data[game_state][hand][0]]

        if game_state == 0:
          if hand_cards[1] == hand_cards[3]:
            suit_char = 's'
          else:
            suit_char = 'o'
          
          if hand_cards[0] == hand_cards[2]:
            suit_char = 'p'

          only_cards = hand_cards[0] + hand_cards[2]
          hand_strength = findPreFlopRank(only_cards, suit_char, preflopRank)
          
        else:
          if len(table_cards) != 0:
            hand_cards_obj = [Card.new(hand_cards[:2]),
                              Card.new(hand_cards[2:])                          
            ]
            hand_strength = evaluator.evaluate(table_cards[game_state - 1], hand_cards_obj)

        data[game_state][hand].insert(2,hand_strength)

  return data
