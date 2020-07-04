def setValueToRaise(orderPlays, gamepotRaiseData):
    gamepotRaiseData['Receive'] = []
    for situation in orderPlays:
        raisedAlready = [0, 0, 0, 0, 0, 0]
        raiseComing = 0
        for hand in situation:
            if hand[2] == 'sb' or hand[2] == 'bb':
                if hand[2] == 'sb':
                    gamepotRaiseData['Receive'].append(0)
                    raisedAlready[0] = 0.005
                if hand[2] == 'bb':
                    gamepotRaiseData['Receive'].append(0.005)
                    raisedAlready[1] = 0.01
                    raiseComing = 0.01

            elif raiseComing > raisedAlready[hand[0]]:
                gamepotRaiseData['Receive'].append(round(raiseComing - raisedAlready[hand[0]], 3))
                raisedAlready[hand[0]] = raiseComing
            else:
                gamepotRaiseData['Receive'].append(0)

            if hand[2] == 'r':
                raiseComing = hand[3]
            
            
    #Transform in BB's metric
    for i, coming_value in enumerate(gamepotRaiseData['Receive']):
        comingInBBs = (coming_value / 0.01)
        gamepotRaiseData['Receive'][i] = (round(comingInBBs, 1))
         


    return gamepotRaiseData


def getPotOdds(gamepotRaiseData):
    gamepotRaiseData['PotOdds'] = []
    for i in range(len(gamepotRaiseData['Receive'])):
        future_pot = gamepotRaiseData['Receive'][i] + gamepotRaiseData['Pot'][i]
        if future_pot != 0 :
            raw_pot_odd = round((gamepotRaiseData['Receive'][i] / future_pot), 2)
            pot_odd = (raw_pot_odd / 0.05) * 0.05
        else:
            pot_odd = 0
        gamepotRaiseData['PotOdds'].append(pot_odd)
    
    del gamepotRaiseData['Receive']
    return gamepotRaiseData

    
