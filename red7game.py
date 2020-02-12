from red7 import random, os, Card, Deck, Player, current_winner_name, clear

# #Game setup ========================================================================
clear()

#Variables
deck = Deck()
playerList = []
num_players = None
turn_num = 0

#Determine the number of players in the game
while num_players not in [2,3,4]:
    try:
        num_players = int(input('How many (2-4) people are playing? '))
    except ValueError:
        print('Invalid choice')
    else:
        continue

#Give all players names
for i in range(1, num_players+1):
    playerList.append(Player(input(f"Enter player {i}'s name: ")))

#Give all players 7 cards, dealt one-by-one
for i in range(7):
    for player in playerList:
        player.draw_card(deck)
for player in playerList:
    player.setup(deck)

#Color dictionary; game always starts with red
gameColor = 'Red'
gameDict = {        
                    'Red': 'Highest card wins',
                 'Orange': 'Most of one number wins',
                 'Yellow': 'Most of one color wins',
                  'Green': 'Most even cards wins',
                   'Blue': 'Most different colors wins',
                 'Indigo': 'Most cards in a row wins',
                 'Violet': 'Most cards below 4 wins'
            }

#Determine who is winning at the beginning of the game
max_first_card = Card('Null', 0, 0)
max_id = -1
for i in range(len(playerList)):
    if playerList[i].palette[0] > max_first_card:
        max_first_card = playerList[i].palette[0]
        max_id = i

#The player right after the winning player takes the first turn
for i in range(max_id + 1):
    playerList.append(playerList.pop(0))

clear()

#Gameplay Loop ==============================================================================================
while(True):

    #p is the current player, first in the playerList
    p = playerList[0]

    #Win condition: everyone else loses
    if len(playerList) == 1:
        print(f'{p.name} has won the game!')
        break

    #Turn count
    turn_num += 1
    print(f'Turn {turn_num}')

    #If player has no cards, they lose
    if(len(p.hand)) == 0:
        print(f'{p.name} is out of cards and has lost')
        playerList.pop(0)
        continue
    
    #Some printouts for the current gamestate
    print('='*113)    
    for player in playerList:
        player.print_palette()
    print('='*113)    
    print('The color is currently', gameColor, '-', gameDict[gameColor])
    print('='*113)    
    print(f"It is {p.name}'s turn. {current_winner_name(gameColor, playerList)} is currently winning.\n")
    p.print_hand()
    print(f"{p.name} has {len(p.hand)} cards remaining.")

    #Player picks play card, change rule, both, or forfeit
    p_choice = None
    while p_choice not in [1,2,3,0,7]:
        try:
            p_choice = int(input("Enter 1 to play a card to your palette, 2 to discard a "
                                    "card and change the rule, 3 to do both, 7 for the color rules, "
                                    "or 0 to forfeit: "))
        except ValueError:
            print('Invalid choice')
        else:
            continue
    
    #All choices are handled below
    card_choice = None
    discard_choice = None

    #Player chooses to discard
    if p_choice == 1:
        while card_choice not in list(range(1, len(p.hand)+1)):
            try:
                card_choice = int(input('With card position starting at 1, pick one of '
                                       f'your {len(p.hand)} cards to play: '))
            except ValueError:
                print('Invalid choice')
            else:
                continue               
        card_choice -= 1

        p.palette.append(p.hand.pop(card_choice))

        if p.name == current_winner_name(gameColor, playerList):
            playerList.append(playerList.pop(0))
        else: 
            p.hand.append(p.palette.pop())
            turn_num -= 1
        clear()

    #Player chooses to discard to change rule
    if p_choice == 2:
        while card_choice not in list(range(1, len(p.hand)+1)):
            try:
                card_choice = int(input('With card position starting at 1, pick '
                                       f'one of your {len(p.hand)} cards to discard: '))
            except ValueError:
                print('Invalid choice')
            else:
                continue
        card_choice -= 1

        discard = p.hand.pop(card_choice)

        if p.name == current_winner_name(discard.color, playerList):
            gameColor = discard.color
            playerList.append(playerList.pop(0))
        else: 
            p.hand.append(discard)
            turn_num -= 1
        clear()

    #Player chooses to discard to change rule and play a card
    if p_choice == 3:
        while discard_choice not in list(range(1, len(p.hand)+1)):
            try:
                discard_choice = int(input('With card position starting at 1, pick '
                                          f'one of your {len(p.hand)} cards to discard: '))
            except ValueError:
                print('Invalid choice')
            else:
                continue
        discard_choice -= 1
        discard = p.hand.pop(discard_choice)
        print('='*113)
        print(f'Currently discarding a {discard.color} card')
        p.print_hand()

        while card_choice not in list(range(0, len(p.hand)+1)):
            try:
                card_choice = int(input('\nEnter 0 to abort this choice. With card position starting at 1, pick one '
                                       f'of your {len(p.hand)} cards to play: '))
            except ValueError:
                print('Invalid choice')
            else:
                continue

        #In case player wants to change their mind and not discard and play a card
        if card_choice == 0:
            turn_num -= 1
            p.hand.append(discard)
            clear()
            continue
        card_choice -= 1

        p.palette.append(p.hand.pop(card_choice))

        if p.name == current_winner_name(discard.color, playerList):
            gameColor = discard.color
            playerList.append(playerList.pop(0))
        else: 
            p.hand.append(discard)
            p.hand.append(p.palette.pop())
            turn_num -= 1
        clear()
    
    #Player forfeits
    if p_choice == 0:
        print(f'{p.name} has forfeited')
        playerList.pop(0)

        clear()

    #"Help" - prints all rules for all colors
    if p_choice == 7:
        clear()

        for color in gameDict:
            print(color, '-', gameDict[color])
        print('\n')

        turn_num -= 1

#End gameplay loop
#============================================================================================================


#To-do:

