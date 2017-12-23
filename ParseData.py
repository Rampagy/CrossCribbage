import csv
import numpy as np
import os

def GetTrainingData():
    data_list = []

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Replays', 'replay.csv'), 'rt') as fi:
        reader = csv.reader(fi)
        for row in reader:
            #skip the header
            if row[0] != 'in0':
                data_list.append(list(map(float, row)))

    return np.matrix(data_list)

"""
data = GetTrainingData().T
input_data = data[:27, :]
output_data = data[27:, :]

print(data.shape)
print(data[:, 0])
print(input_data[:, 0])
print(output_data[:, 0])
"""
