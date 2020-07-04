

def changePotRaiseMetrics(linearizedData):
    """
    Change metric for pot raise, from chips to BigBlinds
    """
    finalData = {
        'Position' : [],
        'Situation' : [],
        'Turn' : [],
        'Pot' : [],
        'Hand' : [],
        'Action' : [],
        'Raise' : []
    }
    for row in linearizedData:
        finalData['Position'].append(row[0])
        finalData['Situation'].append(row[1])
        finalData['Turn'].append(row[2])


        potInBBs = (row[3] / 0.01)
        finalData['Pot'].append(round(potInBBs, 1))


        finalData['Hand'].append(row[4])
        finalData['Action'].append(row[5])

        raisesInBBs = (row[6] / 0.01)
        finalData['Raise'].append(round(raisesInBBs, 1))

    return finalData


def raiseAsPotPercentage(data):

    for i in range(len(data['Pot'])):
        if i != 0:
            data['Raise'][i] = round(data['Raise'][i]/data['Pot'][i], 2)

    return data


def raiseAsPotPercentageAfterPreFlop(data):
    for i in range(len(data['Pot'])):
        if i != 0 and data['Situation'][i] != 0: #SmallBlind
            data['Raise'][i] = round(data['Raise'][i]/data['Pot'][i], 2)

    return data

def categorizeRaises(data):
    for i in range(len(data['Raise'])):
        if data['Action'][i] == 'r':
            value = data['Raise'][i]
            #PreFlop
            if data['Situation'][i] == 0:
                if value <= 0.03:  #PREFLOP Less than 3 bigBlinds
                    data['Action'][i] = 'rm'
                else:
                    data['Action'][i] = 'rb'
            #FlopTurnRiver
            else:
                if value <= 0.4: #PosFLOP less than 40% of the flop
                    data['Action'][i] = 'rs'
                elif value <= 0.8:
                    data['Action'][i] = 'rm'
                else:
                    data['Action'][i] = 'rb'
    
    del data['Raise'] #Delete the delte, since will not be use anymore
    return data

