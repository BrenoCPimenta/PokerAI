# Time Series Poker AI Bot using RNN
#### (AI algorithm that plays Texas hold 'em poker)
This project aims to create a neural network capable of playing poker, more specifically No Limit 6 players texas hold 'em, NLHE. 
It was built a supervised time series model, that was trained using pluribus modified data.
Although it is well known that reinforcement learning is a more appropriate approach to this problem, this project aimed to verify the limit of a supervised time series on accomplish this task. 
The main goal is to see if the net could learn part of the pattern, known as GTO poker, that resides on the pros and bot strategies.

# Architecture:
* **Net:** A block of GRU layers, followed by a linear layer and last for a sigmoid activation function.
* **Loss:** A simple custom loss function based on CrossEntropyLoss.
* **Optimizer:** Adam.
* **Hyperparameters:** Are a variance of values used by the following projects:
   * [DeepStack](https://science.sciencemag.org/content/356/6337/508)
   * [DotaNet](https://ieeexplore.ieee.org/document/8499076)
   * [FilterNet](https://www.preprints.org/manuscript/202002.0318/v1)

# Data
The raw data is from Pluribus (state of the art to this present day) bot, who played against professional players and made a significant amount of the hands public on their [paper in science](https://science.sciencemag.org/content/365/6456/885).

Example of a hand by the pluribus paper:
> STATE:0:fffr225fc/cc/cc/cr475f:3cKc|Kh5d|3h4s|8c4d|7h5c|TcTh/7dAcJh/2d/Td:-50|-225|0|0|0|275:MrOrange|MrWhite|MrBlonde|Eddie|Bill|Pluribus

The biggest challenge was the data treatment, so that could be consumed by the NN losing as least valuable information as possible.<br>
And the plays were separated by player, so the loss could be calculated as if the net was playing the game. 

### Abstraction:
Since the game complexity is enormous, abstraction was needed.
* **Actions:** The actions were separated in 5 categories F-fold; C-check/call; RS-small-raise; RM-medium-rase; RB-big-raise. Inside the project there is a study that explains why.
* **Hand Cards**: This [algorithm](https://github.com/ihendley/treys) was used to only be computed the hand strength.
* **Table Cards**: When the table cards are shown the hand strength is recalculated, but there is more information. It was calculated by custom functions, part of those information, known as **Board Texture**, represented by BoardStraight, BoardColor and BoardPair columns.
* **Pot**: PotOdds are calculated by every decision.
<br>
After the abstraction was applied, with other fundamental information, the same data presented above looked like this:
  
  
![Image](https://github.com/BrenoCPimenta/PokerRNN/blob/master/img/data_table.jpg?raw=true)
Afterwards normalization was applied, and the data was separated in train 80% and test 20%, both of which obey a distribution of turns of the plays.
