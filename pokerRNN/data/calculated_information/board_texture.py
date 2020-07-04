


def applyBoardTexture(board_cards, hand_cards, original_data):
    if board_cards == ['']:
        original_data['BoardPairs'] = []
        original_data['BoardColor'] = []
        original_data['BoardStraight'] = []
        for i in range(len(original_data['Action'])):
            original_data['BoardPairs'].append(0)
            original_data['BoardColor'].append(0)
            original_data['BoardStraight'].append(0)
        return original_data

    
    cards, suits = extractCardsSuit(board_cards)
    hands_by_situation = [0,0,0,0]
    for situation in original_data['Situation']:
        hands_by_situation[situation] += 1
    
    color_ranks, color_block = getBoardColors(suits)

    pairs_rank, cards_frequency = getBoardPairs(cards)
    sequence_rank = getBoardSequence(cards)

    original_data['BoardPairs'] = []
    original_data['BoardColor'] = []
    original_data['BoardStraight'] = []
    for i in range(len(original_data['Action'])):
        if original_data['Situation'][i] == 0:
            original_data['BoardPairs'].append(0)
            original_data['BoardColor'].append(0)
            original_data['BoardStraight'].append(0)
        if original_data['Situation'][i] == 1:
            original_data['BoardPairs'].append(pairs_rank['flop'])
            original_data['BoardColor'].append(color_ranks['flop'])
            original_data['BoardStraight'].append(sequence_rank['flop'])
        if original_data['Situation'][i] == 2:
            original_data['BoardPairs'].append(pairs_rank['turn'])
            original_data['BoardColor'].append(color_ranks['turn'])
            original_data['BoardStraight'].append(sequence_rank['turn'])
        if original_data['Situation'][i] == 3:
            original_data['BoardPairs'].append(pairs_rank['river'])
            original_data['BoardColor'].append(color_ranks['river'])
            original_data['BoardStraight'].append(sequence_rank['river'])

    return original_data



def extractCardsSuit(board_cards):
    cards = []
    suits = []
    for i, group in enumerate(board_cards):
        
        if i == 0:
            cards.append([group[0], group[2], group[4]])
            suits.append([group[1], group[3], group[5]])
        elif i == 1:
            cards.append(group[0])
            suits.append(group[1])
        else:
            cards.append(group[0])
            suits.append(group[1])

    return (cards, suits)




def extractCardValue(card):
    """
    Turn cards in numeric values
    """
    if card == 'A': 
        return 14
    elif card == 'K':
        return 13
    elif card == 'Q':
        return 12
    elif card == 'J':
        return 11
    elif card == 'T':
        return 11
    else:
        return int(card)



def getTableCardsValues(cards):
    """
    Get numeric values from table cards
    """
    cards_values = []
    for i, group in cards:
        if i == 0:
            for flopCard in group:
                value = extractCardValue(flopCard)
                cards_values.append(value)
        else:
            value = extractCardValue(group)
            cards_values.append(value)
    return cards_values



def getBoardLength(cards):
    board_length = {}
    for i, card in enumerate(cards):
        if i == 0:
            board_length['flop'] = 0
            for flopCard in card:
                board_length['flop'] += extractCardValue(flopCard)
        
        if i == 1:
            board_length['turn'] = board_length['flop'] +  extractCardValue(card)
        
        if i == 2:
            board_length['river'] = board_length['turn'] + extractCardValue(card)
            
    return board_length
        
   




def getBoardColors(suits):
    """
    Rank the board by the suits:
    Flop:
    - 111 = 0
    - 21 = 2
    - 3 = 4
    Turn:
    - 1111 = 0
    - 211 = 1
    - 31 = 3
    - 4 = 6
    River:
    -2111 = 0
    -221 = 0
    -311 = 2
    -32 = 2
    -41 = 5
    -5 = 7

    Returns the rank and the block suit
    """
    suits_cnt = {
                's':0,
                'd':0,
                'h':0,
                'c':0}

    color_ranks = {
            'flop' : 0,
             'turn' : 0,
             'river' : 0}
    
    color_block = {
                'flop' : '',
                'turn' : '',
                'river' : ''}

    for i, cards in enumerate(suits):
        #FLOP
        if i == 0:
            for suit in cards:
                suits_cnt[suit] += 1
            values = list(suits_cnt.values())
            values.sort(reverse=True)
            if values[0] == 1:
                color_ranks['flop'] = 0
                color_block['flop'] = ''
            elif values[0] == 2:
                color_ranks['flop'] = 2
                color_block['flop'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(2)]
            elif values[0] == 3:
                color_ranks['flop'] = 4
                color_block['flop'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(3)]

        #TURN
        elif i == 1:
            suits_cnt[cards] += 1
            values = list(suits_cnt.values())
            values.sort(reverse=True)
            if values[0] == 1:
                color_ranks['turn'] = 0
                color_block['turn'] = ''
            elif values[0] == 2:
                color_ranks['turn'] = 1
                color_block['turn'] = ''
            elif values[0] == 3:
                color_ranks['turn'] = 3
                color_block['turn'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(3)]
            elif values[0] == 4:
                color_ranks['turn'] = 6
                color_block['turn'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(4)]

        #RIVER
        elif i == 2:
            suits_cnt[cards] += 1
            values = list(suits_cnt.values())
            values.sort(reverse=True)
            if values[0] == 2:
                color_ranks['river'] = 0
            elif values[0] == 3:
                color_ranks['river'] = 2
                color_block['river'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(3)]
            elif values[0] == 4:
                color_ranks['river'] = 5
                color_block['river'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(4)]
            elif values[0] == 5:
                color_ranks['river'] = 7
                color_block['river'] = list(suits_cnt.keys())[list(suits_cnt.values()).index(5)]

    return color_ranks, color_block






def getBoardPairs(board_cards):
    """
    Return pairs strength on hand:
    Flop:
    1 pair = 2
    1 Triple = 4

    Turn:
    1 pair = 1
    1 triple = 3
    2 pairs = 5
    Four = 8

    River:
    1 pair = 1
    1 triple = 3
    2 pairs = 5
    pair+triple = 6
    Four = 8
    """

    #Separating  card frequency by turns
    frequency = { 'flop':{},
                  'turn':{},
                  'river':{}}
    for i, group in enumerate(board_cards):
        if i == 0:
            for flop_card in group:
                if flop_card in frequency['flop']:
                    frequency['flop'][flop_card] += 1
                else:
                    frequency['flop'][flop_card] = 1
        if i == 1:
            frequency['turn'] = frequency['flop']
            if group in frequency['turn']:
                frequency['turn'][group] += 1
            else:
                frequency['turn'][group] = 1
        
        if i == 2:
            frequency['river'] = frequency['turn']
            if group in frequency['river']:
                frequency['river'][group] += 1
            else:
                frequency['river'][group] = 1
            

    #Calculating rank and getting the block cards
    #Get the most repetion of the turn and verify by it
    pair_rank = {'flop':0, 'turn':0, 'river':0}
    #FLOP:
    card_frequencys_flop = list(frequency['flop'].values())
    card_frequencys_flop.sort(reverse=True)
    if card_frequencys_flop[0] == 1:
        pair_rank['flop'] = 0
    elif card_frequencys_flop[0] == 2:
        pair_rank['flop'] = 2
    elif card_frequencys_flop[0] == 3:
        pair_rank['flop'] = 4

    if len(board_cards) > 1:
        #TURN:
        card_frequencys_turn = list(frequency['turn'].values())
        card_frequencys_turn.sort(reverse=True)
        if card_frequencys_turn[0] == 1:
            pair_rank['turn'] = 0
        elif card_frequencys_turn[0] == 2:
            #case of two pairs
            if card_frequencys_turn[1] == 2:
                pair_rank['turn'] = 5
            else:
                pair_rank['turn'] = 1
        elif card_frequencys_turn[0] == 3:
            pair_rank['turn'] = 3
        elif card_frequencys_turn[0] == 4:
            pair_rank['turn'] = 8


    if len(board_cards) > 2:
        #RIVER:
        card_frequencys_river = list(frequency['river'].values())
        card_frequencys_river.sort(reverse=True)
        if card_frequencys_river[0] == 1:
            pair_rank['river'] = 0
        elif card_frequencys_river[0] == 2:
            #case of two pairs
            if card_frequencys_river[1] == 2:
                pair_rank['river'] = 5
            else:
                pair_rank['river'] = 1
        elif card_frequencys_river[0] == 3:
            if card_frequencys_river[1] == 2:
                    pair_rank['river'] = 6
            else:
                pair_rank['river'] = 3
        elif card_frequencys_river[0] == 4:
            pair_rank['river'] = 8

    
    return pair_rank, frequency





def getBoardSequence(board_cards):
    """
    Rank the board by the suits:
    00gap: 100
    0gap+:
        1 80
        2 60
        3.. 50
    1gap+:
        1
        2
        3...

    resto zero
    River:
    -2111 = 0
    -221 = 0
    -311 = 2
    -32 = 2
    -41 = 5
    -5 = 7

    Returns the rank and the block suit
    """
    flop_vector = []
    rank_straight = {'flop':0, 'turn':0, 'river':0}

    for flop_cards in board_cards[0]:
        flop_vector.append(extractCardValue(flop_cards))

    flop_vector.sort()

    #Removing Flop pairs:
    if flop_vector[1] == flop_vector[2]:
        flop_vector.pop(2)

    if flop_vector[0] == flop_vector[1]:
        flop_vector.pop(0)
    
    #Treating AceDeuce Problem
    ace_flag = False
    deuce_flag = False
    both_flag = False
    if 14 in flop_vector or 2 in flop_vector:
        if 14 in flop_vector and 2 not in flop_vector:
            ace_flag = True
        elif 14 not in flop_vector and 2 in flop_vector:
            deuce_flag = True
        else:
            both_flag = True

    #Getting flop gap scores
    size_flop = len(flop_vector)
    if  size_flop == 1:
        rank_straight['flop'] = 0
    elif size_flop == 2:
        if both_flag:
            rank_straight['flop'] = 50
        else:
            only_gap = flop_vector[1] - flop_vector[0]
            rank_straight['flop'] = getGapScore(only_gap)
    else:
        first_gap = flop_vector[1] - flop_vector[0]
        second_gap = flop_vector[2] - flop_vector[1]
        rank_straight['flop'] = getGapScore(second_gap) + getGapScore(first_gap)
        if both_flag:
            rank_straight['flop'] += 50


    if len(board_cards) > 1:
        #Verifying Turn pairs
        turn_value = extractCardValue(board_cards[1])

        #Setting Turn rank
        turn_vector = flop_vector
        if turn_value in flop_vector:
            rank_straight['turn'] = rank_straight['flop']
        else:
            turn_vector.append(turn_value)
            turn_vector.sort()
            size_turn = len(turn_vector)
            if size_turn == 2:
                only_gap = turn_vector[1] - turn_vector[0]
                rank_straight['turn'] = getGapScore(only_gap)

            elif size_turn == 3:
                first_gap = turn_vector[1] - turn_vector[0]
                second_gap = turn_vector[2] - turn_vector[1]
                rank_straight['turn'] = getGapScore(second_gap) + getGapScore(first_gap)
            
            elif size_turn == 4:
                first_gap = turn_vector[1] - turn_vector[0]
                second_gap = turn_vector[2] - turn_vector[1]
                third_gap = turn_vector[3] - turn_vector[2]
                rank_straight['turn'] = getGapScore(third_gap) + getGapScore(second_gap) + getGapScore(first_gap)

            #New ace with deuce in turn treat
            if turn_value == 14 and deuce_flag and not both_flag:
                rank_straight['turn'] += 50
            elif turn_value == 2 and deuce_flag and not both_flag:
                rank_straight['turn'] += 50
            
            #New Ace or Deuce in Turn treat
            if turn_value == 14 and not ace_flag:
                ace_flag = True
                if deuce_flag:
                    both_flag = True
            elif turn_value == 2 and not deuce_flag:
                deuce_flag = True
                if ace_flag:
                    both_flag = True



    if len(board_cards) > 2:
        #Verifying river pairs
        river_value = extractCardValue(board_cards[2])

        #Setting river rank
        river_vector = turn_vector
        if river_value in turn_vector:
            rank_straight['river'] = rank_straight['turn']
        else:
            river_vector.append(river_value)
            river_vector.sort()
            size_river = len(river_vector)
            if size_river == 2:
                only_gap = river_vector[1] - river_vector[0]
                rank_straight['river'] = getGapScore(only_gap)

            elif size_river == 3:
                first_gap = river_vector[1] - river_vector[0]
                second_gap = river_vector[2] - river_vector[1]
                rank_straight['river'] = getGapScore(second_gap) + getGapScore(first_gap)
            
            elif size_river == 4:
                first_gap = river_vector[1] - river_vector[0]
                second_gap = river_vector[2] - river_vector[1]
                third_gap = river_vector[3] - river_vector[2]
                rank_straight['river'] = getGapScore(third_gap) + getGapScore(second_gap) + getGapScore(first_gap)

            elif size_river == 5:
                first_gap = river_vector[1] - river_vector[0]
                second_gap = river_vector[2] - river_vector[1]
                third_gap = river_vector[3] - river_vector[2]
                forth_gap = river_vector[4] - river_vector[3]
                rank_straight['river'] = getGapScore(forth_gap) + getGapScore(third_gap) + getGapScore(second_gap) + getGapScore(first_gap)

            #New ace with deuce in river treat
            if river_value == 14 and deuce_flag and not both_flag:
                rank_straight['river'] += 50
            elif river_value == 2 and deuce_flag and not both_flag:
                rank_straight['river'] += 50
            

    return rank_straight

def getGapScore(gap):
    if gap == 1:
        return 50
    if gap == 2:
        return 30
    if gap == 3:
        return 10
    if gap >= 4:
        return 0







    

