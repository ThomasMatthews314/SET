#!/usr/bin/python

import numpy as np
from tqdm import tqdm
#np.set_printoptions(threshold=np.inf)

maxCards = 21
maxLayout = 50
maxSets = 100


frequency = np.zeros((maxLayout + 1, maxCards + 1, maxSets + 1))
count = np.zeros(maxLayout+1)
count2 = np.zeros((maxLayout + 1, maxCards + 1))







with open('totalGames.npy','rb') as a:
    totalGames = np.load(a, allow_pickle = True)





def combine_games():
    
    for i in range(len(totalGames)):

        for j in range(len(totalGames[i])):
            numOfCards = int(totalGames[i][j][0])
            numOfSets = int(totalGames[i][j][1])
            
            count[j] += 1
            count2[j][numOfCards] += 1
            frequency[j][numOfCards][numOfSets] += 1

        
combine_games()


def print_data():

    average = np.zeros(maxLayout + 1)

    total = 0

    for i in range(maxLayout):
        print('SETS' + ' in layout #' + str(i))
        print(str(count[i]) + ' trials')
        total = 0

        for j in range(maxCards+1):
            if (j%3 ==0 and count2[i][j] > 0):
                print('Sets in ' + str(j) + ' cards')
                print('')

            for k in range(maxSets + 1):

                if(frequency[i][j][k] > 0):
                    total += k*frequency[i][j][k]
                    print(str(k) + ' : ' + str(frequency[i][j][k]))

        average[i] = total/count[i]
        print('average = ' + str(average[i]))

    print('')
    print('SETS', str(count[0]) + ' trials')
    print('')
    print('Averages:')
    for i in range(maxLayout):
        print(average[i])

    print('')
    #print('15 cards:', cards15, '18 cards:', cards18, '21 cards:', cards21)

def averages_of_12():
        
    average12 = np.zeros(maxLayout + 1)

    total12 = 0
        
    for i in range(maxLayout):
        print('SETS' + ' in layout #' + str(i))
        print(str(count[i]) + ' trials')
        total12 = 0

        for k in range(maxSets + 1):

            if(frequency[i][12][k] > 0):
                total12 += k*frequency[i][12][k]
                print(str(k) + ' : ' + str(frequency[i][12][k]))

        average12[i] = total12/count2[i][12]

    print('Averages of 12 cards only:')
        
    for i in range(maxLayout):
        print(average12[i])

def after_no_sets():

    data = np.zeros((50,100))
    countNone = np.zeros(50)

    for i in tqdm(range(len(totalGames))):
        

        index_pos_list = []
        index_pos = 0
        while True:
            try:
                # Search for item in list from indexPos to the end of list
                index_pos = totalGames[i].index((12,0), index_pos)
                # Add the index position in list
                index_pos_list.append(index_pos)
                index_pos += 1

            except ValueError as e:
                break
        
        index_pos_last = 0
    
        for q in range(len(totalGames[i])):
        
            if totalGames[i][q][0] > 9:
                index_pos_last = q
        
        index_pos_list.append(index_pos_last)
    

        for p in range(len(index_pos_list)-1):
            temp = totalGames[i][index_pos_list[p]:index_pos_list[p+1]]
            for x in range(len(temp)):
                data[x][int(temp[x][1])] += 1
                countNone[x] += 1

    averagesNone = np.zeros(50)
    totalNone = 0



    for i in range(50):
        totalNone = 0

        for j in range(100):

            if data[i][j] > 0:
                totalNone += j*data[i][j]

        averagesNone[i] = totalNone/countNone[i]

    for i in range(50):
        print(averagesNone[i])
        
        


#print_data()

after_no_sets()


