import re

def extractRaises(plays):
  
  joinPlays = ''.join(map(str, plays))
  numbers = re.findall("[-\d]+", joinPlays)  

  
  cleanPlays = []
  for play in plays:
    cleanPlays.append(''.join([i for i in play if not i.isdigit()]))

  if len(numbers) != 0:
    #Treating raises to be percentages and be a part from the game
    #Other raises:
    for x in range(len(numbers)-1, 0, -1):
      raise_value = int(numbers[x]) - int(numbers[x-1])
      percentage = float(raise_value)/float(10000)
      round_percentage = round(0.025 * round(percentage/0.025) , 3)#rounding for 2.5% to abstract results
      numbers[x] = round_percentage
    
    #the first raise:
    percentage_firstNumber = float(numbers[0])/float(10000)
    round_firstNumber =round( 0.025 * round(percentage_firstNumber/0.025) , 3)
    numbers[0] = round_firstNumber

  return (numbers,cleanPlays)