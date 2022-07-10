#!/usr/bin/python

import numpy as np
from tqdm import tqdm
import itertools
import csv
import os

#np.set_printoptions(threshold=np.inf)

#~~~~~~~~~~~~~~~~~~~~~~~ Constants to Use ~~~~~~~~~~~~~~~~~~~~~~~

numberOfCards = 81

cards15 = 0
cards18 = 0
cards21 = 0

locationOfFirstCardOnTable = 0
locationOfLastCardOnTable = -1

maxCards = 21
maxLayout = 50
maxSets = 100

completedGames = 0

#~~~~~~~~~~~~~~~~~~~~~~~ Arrays ~~~~~~~~~~~~~~~~~~~~~~~

deck = np.arange(0,numberOfCards,1,dtype=int)
locationInDeck = np.arange(0,numberOfCards,1,dtype=int)

totalGames = []
gameData = []

allSets = []

#~~~~~~~~~~~~~~~~~~~~~~~ Initialize Table ~~~~~~~~~~~~~~~~~~~~~~~

# This is the table the code uses to know if three cards are a set or not.
# Since two cards uniquely determine the thrid in a set, this table calculates
# the third card at the index of the other two. Triple nested for loops are not
# ideal, but the code is only run once. 


thirdCardInSet = np.zeros((numberOfCards, numberOfCards), dtype=int)

for firstCard in range(numberOfCards):
    for secondCard in range(firstCard+1,numberOfCards):
        thirdCard = 0
        multiplier = int(27)

        for atttribute in range(4):
            firstValue = int((firstCard/multiplier))%3
            secondValue = int((secondCard/multiplier))%3
            thirdValue = int(6 - (firstValue + secondValue))%3
            thirdCard = int(thirdCard + thirdValue*multiplier)
            multiplier /= 3
            
        thirdCardInSet[firstCard][secondCard] = int(thirdCard)
        thirdCardInSet[secondCard][firstCard] = int(thirdCard)

        allSets.append([firstCard,secondCard,thirdCard])

for i in range(len(allSets)):
    allSets[i] = sorted(allSets[i])

allSets2 = []

for i in allSets:
    if i not in allSets2:
        allSets2.append(i)

cardCounts = np.zeros(numberOfCards)

for i in range(numberOfCards):
    for j in range(len(allSets2)):
        if i in allSets2[j]:
            cardCounts[i] += 1



#~~~~~~~~~~~~~~~~~~~~~~~ Read Input ~~~~~~~~~~~~~~~~~~~~~~~

# Provides user input to run the game with different choices of
# what deck to use, how sets are removed, and number of games to run.
# Inputs are the integer in front of the option.

print('')
print("What deck of cards would you like to use?")
print("1. Randomly shuffled each trial")
print("2. I would like use a fixed order deck contained in a CSV file")
deckChoice = int(input())
print('')

if deckChoice == 2:
    files = os.listdir("/Users/thomasmatthews/SET")    
    files = list(filter(lambda f: f.endswith('.csv'), files))
    print("Please input the number before the name of the file you would like to use from your options below:")
    for i in files:
        print(str(files.index(i) + 1) + ": " + i)

    fileIndex = int(input()) - 1
    csvFilename = str(files[fileIndex])

    print(".csv file selected: " + csvFilename)
    print("")
        

print("How would you like Sets to be removed?")
print("1. Take Sets Randomly")
print("2. Take Sets By SetSum")
print("3. Take Sets with most Attributes in Common - STILL TO BE WORKED ON")
print("4. Take Sets Lexicographically - STILL TO BE WORKED ON")
print("5. Take Sets By Most Remaining Options")
removeChoice = int(input())
print('')

print("Enter number of trials: ")
numberOfTrials = int(input())
print('')


#~~~~~~~~~~~~~~~~~~~~~~~ Game Class ~~~~~~~~~~~~~~~~~~~~~~~


class VersionSET(object):
    
                         
    def __init__(self, deckChoice):
        self.deckChoice = deckChoice



    def swap_cards(self, firstLocation, secondLocation):
        firstCard = int(deck[firstLocation])
        secondCard = int(deck[secondLocation])
        deck[firstLocation] = secondCard
        locationInDeck[firstCard] = secondLocation
        deck[secondLocation] = firstCard
        locationInDeck[secondCard] = firstLocation

    def number_of_cards_left_in_deck(self):
        return numberOfCards - (locationOfLastCardOnTable+1)

    def number_of_cards_on_table(self):
        return locationOfLastCardOnTable - locationOfFirstCardOnTable + 1

    def is_on_table(self, card):
        cardLocation = locationInDeck[card]
        return np.logical_and(locationOfFirstCardOnTable <= cardLocation, cardLocation <= locationOfLastCardOnTable)
        

    def take_card(self, card):
        global locationOfFirstCardOnTable
 
        if self.is_on_table(card):
            self.swap_cards(locationOfFirstCardOnTable, int(locationInDeck[card]))
            locationOfFirstCardOnTable += 1
            return True
        else:
            return False


    def deal(self, amount):
        global locationOfLastCardOnTable
        
        if self.number_of_cards_left_in_deck() < amount:
            return False
        else:
            locationOfLastCardOnTable += amount
            return True
    

    def setup_game(self):

        global csvFilename
        global deck
        global locationInDeck

        # random
        if deckChoice == 1:
            for location in range(numberOfCards):
                newLocation = np.random.randint(location, numberOfCards)
                self.swap_cards(int(location), int(newLocation))
        
        #from CSV
        if deckChoice == 2:
            with open(csvFilename) as c:
                csv_reader = csv.reader(c)
                rows = list(csv_reader)

                r = np.random.randint(0,len(rows))

                deck = rows[r]

                deck = list(map(int, deck))

                deck = np.array(deck)

                for i in range(81):
                    card = int(deck[i])
                    locationInDeck[card] = int(i)





#~~~~~~~~~~~~~~~~~~~~~~~ Switching Between Cards and Vectors ~~~~~~~~~~~~~~~~~~~~~~~


# there is a conceivable use for this, although I haven't yet ran across it.
# 'Vector' refers to 4-tuple modular atrithmetic form, 'Card' is integer form.


#~~~~~~~~~~~~~~~~~~~~~~~ Taking Sets ~~~~~~~~~~~~~~~~~~~~~~~

# original, more brute force method

    def find_sets(self):
        setsOnTable = []
        for firstLocation in range(locationOfFirstCardOnTable,locationOfLastCardOnTable):
            firstCard = int(deck[firstLocation])
        
            for secondLocation in range(firstLocation + 1,locationOfLastCardOnTable+1):
                secondCard = int(deck[secondLocation])
            
                thirdCard = int(thirdCardInSet[firstCard][secondCard])
            
                if self.is_on_table(thirdCard):
                    tempSet = [firstCard, secondCard, thirdCard]
                    setsOnTable.append(tempSet)
               
        return setsOnTable

    
# method without for loops for speed. This version if hard-coded default.

    def find_sets2(self):
        setsOnTable2 = []
        
        cardsToCheck = deck[np.arange(locationOfFirstCardOnTable,locationOfLastCardOnTable+1)]
        twos = itertools.combinations(cardsToCheck,2)

        twos = np.array(list(twos))

        if self.number_of_cards_on_table() == 0:

            return []

        firstCard = twos[:,0]
        secondCard = twos[:,1]

        thirdCard = thirdCardInSet[firstCard,secondCard]

        thirdCardLocations = locationInDeck[thirdCard]

        mask = self.is_on_table(thirdCard)

        setsOnTable2 = np.array([firstCard[mask],secondCard[mask],thirdCard[mask]])

        return setsOnTable2.T


# each set is counted three times

    def number_of_sets_on_table(self, sets):
        return len(sets)/3


    def take_set(self, choice, setsOnTable):
        outputSet = []

        if choice == 1:
            outputSet = self.take_random_set(setsOnTable)
        elif choice == 2:
            outputSet = self.take_setsum_set(setsOnTable)
        elif choice == 3:
            outputSet = self.take_random_set(setsOnTable)
            print('Does not work')
        elif choice == 4:
            outputSet = self.take_random_set(setsOnTable)
            print('Does not work')
        elif choice == 5:
            outputSet = self.take_mostoptions_set(setsOnTable)
        
        return outputSet

    def take_random_set(self, sets):
        choice = np.random.randint(0,len(sets))
        removedSet = sets[choice]

        self.take_card(removedSet[0])
        self.take_card(removedSet[1])
        self.take_card(removedSet[2])

        return removedSet

    def take_setsum_set(self, sets):
        sumScores = np.zeros(len(sets))
        
        for i in range(len(sets)):
            c1 = sets[i][0]
            c2 = sets[i][1]
            c3 = sets[i][2]
            setSum = c1 + c2 + c3
            sumScores[i] = setSum

        inds = np.where(sumScores == min(sumScores))
        remInd = np.random.choice(inds[0])

        removedSet = sets[remInd]

        self.take_card(removedSet[0])
        self.take_card(removedSet[1])
        self.take_card(removedSet[2])

        return removedSet

    def take_mostoptions_set(self, sets):
        global allSets2
        global cardCounts

        for i in range(len(sets)):
            sets[i] = sorted(sets[i])

        sets2 = np.unique(sets,axis=0)

        srs = []
        
        for i in sets2:
            srs.append(cardCounts[i[0]] + cardCounts[i[1]] + cardCounts[i[2]])

        remSet = sets2[srs.index(min(srs))]

        #print(sets2,srs,remSet)

        for i in remSet:
            allSets2[:] = (value for value in allSets2 if i not in value)

        cardCounts = np.zeros(numberOfCards)

        for i in range(numberOfCards):
            for j in range(len(allSets2)):
                if i in allSets2[j]:
                    cardCounts[i] += 1

        self.take_card(remSet[0])
        self.take_card(remSet[1])
        self.take_card(remSet[2])

        return remSet


#~~~~~~~~~~~~~~~~~~~~~~~ Play Game ~~~~~~~~~~~~~~~~~~~~~~~

# this function is the entire game logic for SET. Includes
# commented print statements for debugging

    def play_game(self, removeChoice):
        global locationOfFirstCardOnTable
        global locationOfLastCardOnTable
        global gameData

        locationOfFirstCardOnTable = 0
        locationOfLastCardOnTable = -1

        
        self.deal(12)


        layout = 0
        done = False
    
        index = 0

        while(not(done)):
            numberOfSets = 0
            setsInPlay = []
            #print('layout',layout,'cards on table',locationOfFirstCardOnTable,locationOfLastCardOnTable,'('+str(self.number_of_cards_on_table())+')')


            if (self.number_of_cards_on_table()<12):
                done = True

            if (self.number_of_cards_on_table()==12 and index < 23):
                setsInPlay = self.find_sets2()
                numberOfSets = self.number_of_sets_on_table(setsInPlay)
                gameData.append((self.number_of_cards_on_table(), numberOfSets))

                if numberOfSets > 0:
                    self.take_set(removeChoice, setsInPlay)
                    #print('took a set from 12')
            
                    if self.number_of_cards_left_in_deck() >= 3:
                        self.deal(3)
                        layout += 1
                        index += 1

                elif numberOfSets==0:
                    global cards15
                    self.deal(3)
                    layout += 1
                    index += 1
                    cards15 += 1
                    #print("couldn't take a set")

                numberOfSets = 0

            if self.number_of_cards_on_table()>12 and index < 23:
                setsInPlay = self.find_sets2()
                numberOfSets = self.number_of_sets_on_table(setsInPlay)
                #print('layout',layout,'cards on table',locationOfFirstCardOnTable,locationOfLastCardOnTable,'('+str(self.number_of_cards_on_table())+')')

                gameData.append((self.number_of_cards_on_table(), numberOfSets))
 

                if numberOfSets > 0:
                    self.take_set(removeChoice, setsInPlay)
                    layout += 1
                    #print('took a set from 15')

                elif numberOfSets==0:
                    self.deal(3)
                    layout += 1
                    index += 1

                    if self.number_of_cards_on_table() == 18:
                        global cards18
                        cards18 += 1

                    if self.number_of_cards_on_table() == 21:
                        global cards21
                        cards21 += 1
                    #print('now 18 cards')

            while(index >= 23):
                #print("we're in the end game now")
                #print('cards left in deck',self.number_of_cards_left_in_deck())
                #print('layout',layout,'cards on table',locationOfFirstCardOnTable,locationOfLastCardOnTable)
                setsInPlay = self.find_sets2()
                numberOfSets = self.number_of_sets_on_table(setsInPlay)
                gameData.append((self.number_of_cards_on_table(), numberOfSets))


                if numberOfSets == 0:
                    done = True
                    layout = 0
                    index = 0

                else:
                    self.take_set(removeChoice, setsInPlay)
                    #print("took a set")
                    layout += 1
                    index += 1

        totalGames.append(gameData)
        

    def reset_game(self):
        global locationOfFirstCardOnTable
        global locationOfLastCardOnTable
        global deck
        global locationInDeck

        global gameData

        
        locationOfFirstCardOnTable = 0
        locationOfLastCardOnTable = -1
        
        deck = np.arange(0,numberOfCards,1,dtype=int)
        locationInDeck = np.arange(0,numberOfCards,1,dtype=int)

        gameData = []



#~~~~~~~~~~~~~~~~~~~~~~~ Execute Games ~~~~~~~~~~~~~~~~~~~~~~~

game = VersionSET(deckChoice)

for i in tqdm(range(numberOfTrials)):
    game.setup_game()
    game.play_game(removeChoice)
    game.reset_game()

with open('totalGames.npy','wb') as a:
    np.save(a, totalGames)

print('Game Data saved to: totalGames.npy\\')
