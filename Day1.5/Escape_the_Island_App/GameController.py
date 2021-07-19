import numpy as np
from islandTiles.beach import tile as beach
from islandTiles.temple import tile as temple
from islandTiles.spring import tile as spring
from islandTiles.ravine import tile as ravine
from islandTiles.camp import tile as camp
from islandTiles.cave import tile as cave


class GameController:

    #I've used a dictionary here to access the classes above by their names. This is called a map, and common in coding.
    island_map = {"temple": temple, 
                "spring": spring, 
                "beach": beach, 
                "ravine": ravine, 
                "camp": camp,
                "cave": cave}

    def __init__(self):
        self.alive = True
        self.days = 0
        self.inventory = []
        self.hunger = 4
        self.thirst = 4

    def play(self):
        while(self.alive):
            if self.days == 0:
                print("You have washed up on a Deserted Island! You must search the island for Food and Water to survive until rescue. Watch out for the monsters!")
            print("Days on the deserted island: "+str(self.days))

            #Monsters choice
            while True:
                roshambooMonsterChoice = np.random.randint(5)
                guessingNumbersMonsterChoice = np.random.randint(5)
                if roshambooMonsterChoice == guessingNumbersMonsterChoice:
                    continue
                else:
                    break

            #Player choice
            print("Where would you like to search today? (temple, spring, beach, ravine, camp, cave):")
            while True:
                try:
                    playerChoice = input()
                    tile = self.island_map[playerChoice]
                except:
                    print("Can you repeat where you want to go?")
                    continue
                break
            
            #Check if player encounter monster
            if playerChoice == 'temple':
                playerChoiceNum = 0
            elif playerChoice == 'spring':
                playerChoiceNum = 1
            elif playerChoice == 'beach':
                playerChoiceNum = 2
            elif playerChoice == 'ravine':
                playerChoiceNum = 3
            elif playerChoice == 'cave':
                playerChoiceNum = 4
            
            if playerChoiceNum == roshambooMonsterChoice:
                result = self.roshambooMonsterEncounter()
                #Check if player win
                if result == 'win' or result == 'tie':
                    pass
                else:
                    self.alive = False
                    print("You are eaten by the monster")
                    continue
            elif playerChoiceNum == guessingNumbersMonsterChoice:
                result = self.guessingNumbersMonsterEncounter()
                #Check if player win
                if result == 'win' or result == 'tie':
                    pass
                else:
                    self.alive = False
                    print("You are eaten by the monster")
                    continue

            #Our code to search the Island goes here
            tile.enterTile()
            loot, encounter = tile.search()

            if encounter == "Crocodile":
                self.alive = False
                print("You are eaten by a Crocodile")
                continue
            elif encounter == "Crumbling Cliffs":
                self.alive = False
                print("The cliffs below you crumble and you fall to your death")
                continue
            
            if encounter == None:
                print("Your search yields nothing...")
            else:
                if loot != None:
                    print("You encounter "+str(encounter)+" and find "+str(loot))
                    self.inventory.append(loot)
                else:
                    print("You encounter "+str(encounter)+" but find nothing...")
                
            tile.leaveTile()
                
            #Hunger and thist
            if (self.days+1) % 2 == 0:
                randnum = np.random.randint(2)
                if randnum == 0:
                    self.hunger -=1
                else:
                    self.thirst -=1
            if self.hunger >= 4:
                self.hunger = 4
                print("You are not hungry at all")
            elif self.hunger == 3:
                print("You are a bit hungry")
            elif self.hunger == 2:
                print("You are very hungry")
            elif self.hunger == 1:
                print("You are extremely hungry! Go get some food!")
            elif self.hunger == 0:
                self.alive = False
                print("You starved to death")
                continue
            if self.thirst >= 4:
                self.thirst = 4
                print("You are not thirsty at all")
            elif self.thirst == 3:
                print("You are a bit thirsty")
            elif self.thirst == 2:
                print("You are very thirsty")
            elif self.thirst == 1:
                print("You are extremely thirsty! Go get some water!")
            elif self.thirst == 0:
                self.alive = False
                print("You died of dehydration")
                continue

            #This is the start of our player input section. We'll modify this code to make the gameplay fun.
            #Check inventory
            print("Check your inventory? (Y/N)")
            while True:
                checkInventory = input()
                if checkInventory == 'Y':
                    print("Your inventory contains:")
                    for i in range(len(self.inventory)):
                        print(str(i+1)+ ". " + self.inventory[i])
                    #Use item
                    print("Use/check an item in your inventory? (Y/N)")
                    while True:
                        useItem = input()
                        if useItem == 'Y':
                            self.useItemFunc()
                        elif useItem == 'N':
                            pass
                        else:
                            print("I didn't understand... Can you repeat that?")
                            continue
                        break
                elif checkInventory == 'N':
                    pass
                else:
                    print('Can you repeat if you want to check your inventory?')
                    continue
                break

            #Keep searching
            print("Keep searching the Deserted Island? (Y/N/Quit)")
            while True:
                keepSearching = input()
                if keepSearching == 'Quit':
                    self.alive = False
                elif keepSearching == 'Y':
                    print("Good choice, maybe you'll survive another day.")
                elif keepSearching == 'N':
                    print("Too bad! You're stuck here... Gotta keep searching.")
                else:
                    print("I didn't understand. Maybe you've been stuck on this Island for too long... Can you repeat that?")
                    continue
                break

            self.days += 1
        else:
            print("Game over. You survived for "+str(self.days)+" days.")
            tile.discovered = False
            tile.lootedItems = []
            tile.pastEncounters = []

    def useItemFunc(self):
        print("Which item do you want to use/check? (Enter the index of the item)")
        while True:
            try:
                indexOfItemToUse = int(input())-1
            except:
                print('The input is not valid!')
                continue
            break
        if indexOfItemToUse >= len(self.inventory):
            print("The item does not exist")
        else:
            itemToUse = self.inventory[indexOfItemToUse]
            if itemToUse == "Sand" or itemToUse == "More Sand" or itemToUse == "Even More Sand":
                self.inventory.remove(indexOfItemToUse)
                print("You threw the sand into the air... That was pointless, but it might be the only fun you can get on this island")
            elif itemToUse == "Golden Monkey Statuette":
                print("You looked closely at the statue. It glitters under the sun")
            elif itemToUse == "the number 817":
                print("You are not sure what the number is for")
            elif itemToUse == "a Safe":
                print("You looked closely at the safe and see that it requires a 3 digit password.\nWhat is it?")
                while True:
                    try:
                        password = int(input())
                    except:
                        print('The password you entered is not valid! Please retry...')
                        continue
                    break
                if password == 817:
                    print('Congratulations, you got it right! The safe opened and you got an easter egg!')
                    self.inventory.remove("a Safe")
                    self.inventory.append('an Easter Egg')
                    pass
                else:
                    print('The password is wrong!')
            elif itemToUse == 'an Easter Egg':
                print("This is the easter egg you got from that safe in the cave. You wonder who put the safe there...")
            elif itemToUse == "Food (Chicken)" or itemToUse == "Food (Beef)" or itemToUse == "Food (Pork)":
                self.inventory.remove(self.inventory[indexOfItemToUse])
                self.hunger += 1
                print("You ate the roasted chicken, it tastes very good")
            else:
                self.inventory.remove(self.inventory[indexOfItemToUse])
                self.thirst += 1
                print("You drank the water as you stared into the ocean. Funny how you are surrounded by water but have nothing to drink, you thought to yourself.")
        print("Do you want to use/check another item? (Y/N)")
        useAgain = input()
        if useAgain == 'Y':
            print("Your inventory now contains:")
            for i in range(len(self.inventory)):
                print(str(i+1)+ ". " + self.inventory[i])
            self.useItemFunc()
        else:
            pass

    def roshambooMonsterEncounter(self):
        print('You encountered the ro sham bo monster!!\nWhat is your choice? (rock/paper/scissors)')

        while True:
            player_choice = input()
            if player_choice == 'rock' or player_choice == 'paper' or player_choice == 'scissors':
                break
            else:
                print("Can you repeat your choice?")
                continue

        all_choices = ['rock', 'paper', 'scissors']
        ai_choice = all_choices[np.random.randint(3)]

        print('The ro sham bo monster chose ' + ai_choice)

        if player_choice == 'rock':
            if ai_choice == 'scissors':
                print('You won!')
                return 'win'
            elif ai_choice == 'rock':
                print('Tied!')
                return 'tie'
            else:
                print('You loss!')
                return 'loss'
        elif player_choice == 'scissors':
            if ai_choice == 'scissors':
                print('Tied!')
                return 'tie'
            elif ai_choice == 'rock':
                print('You loss!')
                return 'loss'
            else:
                print('You won!')
                return 'win'
        else:
            if ai_choice == 'scissors':
                print('You loss!')
                return 'loss'
            elif ai_choice == 'rock':
                print('You won!')
                return 'win'
            else:
                print('Tied!')
                return 'tie'
                
    def guessingNumbersMonsterEncounter(self):
        print('You encountered the guessing numbers monster!!\nWhat is your choice? (within the range of 0-100 inclusive)')
        while True:
            try:
                playerNumber = int(input())
            except:
                print("Invalid Input! Please enter another number")
                continue
            else:
                if type(playerNumber) == int and playerNumber >= 0 and playerNumber <= 100:
                    break
                else:
                    print("Invalid Input! Please enter another number")
                    continue
                
        aiNumber = np.random.randint(101)
        chosenNumber = np.random.randint(101)

        playerDifference = abs(chosenNumber - playerNumber)
        aiDifference = abs(chosenNumber - aiNumber)

        if playerDifference < aiDifference:
            print('You won!')
            return 'win'
        elif playerDifference == aiDifference:
            print('Tied!')
            return 'tie'
        else:
            print('You loss!')
            return 'loss'


#Food and water funcion
#Use item function
#Ro sham boo monster and guessing number monster
#Number 817 easter egg