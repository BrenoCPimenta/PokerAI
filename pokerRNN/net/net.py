# -*- coding: utf-8 -*-
"""
PokerRNN.ipynb
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch import optim

import sys, random, os
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

"""## Parameters """

args = {
    #----DATA------
    'num_classes' : 5,    #Based on personal studies
    'input_size'  : 44,   #Based on personal studies
    'hidden_size' : 500,  #Based on DeepStack paper

    #----GPU-----
    'batch_size'  : 1,
    'num_workers' : 1,
    
    #----NET------
    'num_layers'  : 20,   #Based on DOTANET paper
    'dropout'     : 0.35, #Based on DOTANET paper

    #----OPTIMIZER------
    'lr'          : 6e-4, #Based on DOTANET paper
    'weight_decay': 1e-4  #Based on FilterNet paper
}

if torch.cuda.is_available():
  args['device'] = torch.device('cuda')
else:
  args['device'] = torch.device('cpu')

"""## Data:"""

from google.colab import files
uploaded = files.upload()

test_np = np.load('/test.npy', allow_pickle=True)
train_np = np.load('/train.npy', allow_pickle=True)


class RecurrenntDataSetLoader():
  def __init__(self, listOfLists):
    self.listOfLists = listOfLists
    self.inputs = []
    self.answers = []
    self.size = len(listOfLists)
    self.__turnIntoTensor()

  def __turnIntoTensor(self):
    for data_list in self.listOfLists:

      temp_input = []
      for data_input in data_list[0]:
        tensor = torch.FloatTensor(data_input)
        temp_input.append(tensor)

      temp_answers = []
      for data_answers in data_list[1]:
        tensor = torch.FloatTensor(data_answers)
        temp_answers.append(tensor)

      self.inputs.append(temp_input)
      self.answers.append(temp_answers)


  def __len__(self):
    return self.size
  
  def __getitem__(self, index):
    data_val = self.inputs[index]
    target = self.answers[index]
    return data_val,target

train_set = RecurrenntDataSetLoader(train_np)

train_loader = DataLoader(train_set,
                          args['batch_size'],
                          num_workers=args['num_workers'],
                          shuffle=True)

test_set = RecurrenntDataSetLoader(test_np)

test_loader = DataLoader(test_set,
                          args['batch_size'],
                          num_workers=args['num_workers'],
                          shuffle=True)

"""## NET:"""

class Rede(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers, dropout):
        super(Rede, self).__init__()
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.dropout = dropout 

        self.gru = nn.GRU(self.input_size, self.hidden_size, num_layers=self.num_layers, batch_first=True, dropout=self.dropout)
        self.out = nn.Linear(self.hidden_size, self.output_size)
        self.activation = nn.Sigmoid()

    def forward(self, targets):
        sequence_size = len(targets)
        hidden = torch.zeros(self.num_layers, targets[0].size(0), self.hidden_size).to(args['device'])
        
        output_vector = []
        for i in sequence_size:
          output_gru, hidden = self.gru(targets[i], hidden)
          output_net = self.activation(self.out(output_gru))
          output_vector.append(outpu_net)
        
        return output_vector


pokerRNN = Rede(args['input_size'],
                args['hidden_size'],
                args['num_classes'],
                args['num_layers'],
                args['dropout'] ).to(args['device'])

"""## [Loss Function:](https://discuss.pytorch.org/t/rnn-for-many-to-many-classification-task/15457/3)"""

class CrossEntropyS2SLoss(nn.Module):
    """
    Custom Loss Function
    """
    def __init__(self):
        super(CrossEntropyS2SLoss, self).__init__()

    def forward(self, output, result):
        sequence_size = len(result)
        loss_func = nn.CrossEntropyLoss()

        # Loss from one sequence
        loss = loss_func(output[0], result[0]) 
        for i in range(1, sequence_size):
            loss += loss_func(output[i], result[i])

        return loss

criterion = CrossEntropyS2SLoss().to(args['device'])

"""## Optimizer:"""

optimizer = optim.Adam(pokerRNN.parameters(), lr=args['lr'], weight_decay=args['weight_decay'])