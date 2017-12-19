import numpy as np
import math

def subset_sum(numbers, target, partial=[]):
    s = sum(partial)

    # check if the partial sum is equals to target
    if s == target: 
        global count_15s
        count_15s += 1
    if s >= target:
        return # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, partial + [n]) 


def ConvertToHeirarchy(row):
    new_row = []

    for i in range(0, len(row)):
        val = 0
        if (row[i] != 0):
            val = (row[i]-1)%13 + 1
        new_row += [val]
        
    return new_row


def ConvertToValue(row):
    new_row = []

    for i in range(0, len(row)):
        val = ((row[i]-1)%13 + 1)
        if (row[i] == 0):
            val = 0
        elif val > 10:
            val = 10
        new_row += [val]
        
    return new_row


def ConvertMatToRow(matrix, row_idx):
    return np.squeeze(np.asarray(matrix[row_idx])).tolist()


def HistogramRow(row):
    histogram = {}
    row = sorted(row)
    
    for i in range(0, len(row)):
        if not row[i] in histogram:
            histogram[row[i]] = 1
        else:
            histogram[row[i]] += 1

    return histogram


def Score15s(row):
    row = ConvertToValue(row)
    new_row = []
    
    # strip out the zeros
    for i in range(0, len(row)):
        if (row[i] != 0):
            new_row += [row[i]]

    global count_15s
    count_15s = 0
    subset_sum(new_row, 15)
    return count_15s*2


def ScoreRuns(row):
    row = ConvertToHeirarchy(row)
    histogram = HistogramRow(row)
    
    prev_key = -1
    run_keys = []
    max_histo_val = 0
    found_run = False

    for key, val in histogram.items():
        if (((key - prev_key) == 1) and (prev_key != 0)):
            if (len(run_keys) == 0):
                run_keys += [prev_key]
            run_keys += [key]
        else:
            run_len = 1
            if (len(run_keys) < 3):
                run_keys = []
            
        prev_key = key

    if (len(run_keys) >= 3):
        for key in run_keys:
            if (histogram[key] > max_histo_val):
                max_histo_val = histogram[key]
        
    return max_histo_val * len(run_keys)


def ScorePairs(row):
    row = ConvertToHeirarchy(row)
    histogram = HistogramRow(row)
    pair_score = 0
    
    for key, val in histogram.items():
        if ((val > 1) and (key != 0)):
            # val choose 2 (count the number of pairs)
            pair_score += math.factorial(val) / (math.factorial(2) * math.factorial(val-2))
            
    return int(pair_score)*2


def ScoreFlush(row):
    spade_count = 0
    diamond_count = 0
    heart_count = 0
    club_count = 0
    unplaced_count = 0
    
    for i in range(0, len(row)):
        if ((row[i] <= 13) and (row[i] >= 1)):
            spade_count += 1
        elif ((row[i] <= 26) and (row[i] >= 14)):
            club_count += 1
        elif ((row[i] <= 39) and (row[i] >= 27)):
            heart_count += 1
        elif ((row[i] <= 52) and (row[i] >= 40)):
            diamond_count += 1
        else:
            unplaced_count += 1

    score = 0
    if (spade_count >= 5) or (club_count >= 5) or (heart_count >= 5) or (diamond_count >= 5):
        score = 5

    return score


def ScoreRow(matrix, row_idx):
    row = ConvertMatToRow(matrix, row_idx)
    score = Score15s(row) + ScoreRuns(row) + ScorePairs(row) + ScoreFlush(row)
    return score


def ScoreCrib(crib):
    crib = np.squeeze(crib).tolist()
    score = Score15s(crib) + ScoreRuns(crib) + ScorePairs(crib) + ScoreFlush(crib)
    return score


def ScoreGame(matrix):
    player0_score = 0
    player1_score = 0
    
    for i in range(0, len(matrix)):
        player0_score += ScoreRow(matrix, i)
        player1_score += ScoreRow(matrix.T, i)

    return (player0_score, player1_score)

        

"""
cribbage_board = np.matrix([[5, 5, 5, 5, 5],
                            [8, 8, 8, 8, 8],
                            [11, 11, 11, 11, 11],
                            [6, 6, 6, 6, 6],
                            [12, 12, 12, 12, 12]])

a = 0

a += ScoreRow(cribbage_board, 0)
a += ScoreRow(cribbage_board, 1)
a += ScoreRow(cribbage_board, 2)
a += ScoreRow(cribbage_board, 3)
a += ScoreRow(cribbage_board, 4)

b = 0
new_board = cribbage_board.T
b += ScoreRow(new_board, 0)
b += ScoreRow(new_board, 1)
b += ScoreRow(new_board, 2)
b += ScoreRow(new_board, 3)
b += ScoreRow(new_board, 4)

print("player 1 score " + str(a))
print("player 2 score " + str(b))
"""

    

"""
cribbage_board = np.matrix([[8, 8, 7, 7, 7],
                            [5, 5, 10, 10, 10],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0]])


occurances = Count15s(cribbage_board[0])
print(occurances)

occurances = Count15s(cribbage_board[1])
print(occurances)
"""
