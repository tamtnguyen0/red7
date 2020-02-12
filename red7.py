import random, os

clear = lambda: os.system('cls')

class Card:
    def __init__(self, color, rank, colorRank):
        self.color = color
        self.rank = rank
        self.colorRank = colorRank

    def print_card(self):
        print(f'{self.color} {self.rank}')

    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        elif self.rank == other.rank:
            return self.colorRank > other.colorRank
        else:
            return False

    def __lt__(self, other):
        return not (self > other)

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        colors = [None, 'Indigo', 'Violet', 'Blue', 'Green', 'Yellow', 'Orange', 'Red']
        
        for colorRank in range(1, len(colors)):
            for rank in list(range(1,8,1)):
                self.cards.append(Card(colors[colorRank], rank, colorRank))

    def print_deck(self):
        for card in self.cards:
            print(f'{card.color} {card.rank}')

    def deal_one_card(self):
        card_index = random.randint(0,len(self.cards)-1)
        return self.cards.pop(card_index)
        
class Player:
    def __init__(self, name='Bob'):
        self.name = name
        self.hand = []
        self.palette = []

    def print_player(self):
        self.print_hand()
        self.print_palette()

    def print_hand(self):
        card_string_list = []
        for card in self.hand:
            card_string_list.append(f'{card.color} {card.rank}')
        print(f"{self.name}'s hand: [{', '.join(card_string_list)}]")

    def print_palette(self):
        palette_list = []
        for card in self.palette:
            palette_list.append(f'{card.color} {card.rank}')
        print(f"{self.name}'s palette: [{', '.join(palette_list)}]")

    def draw_card(self, deck):
        x = deck.deal_one_card()
        self.hand.append(Card(x.color, x.rank, x.colorRank))
        return self

    def setup(self, deck):
        x = deck.deal_one_card()
        self.palette.append(Card(x.color, x.rank, x.colorRank))

def game_rule(color, palette):

    if color == 'Red':
        return 0, max(palette)

    if color == 'Orange':
        num_count = [0, 0, 0, 0, 0, 0, 0, 0]
        card_list = [[],[],[],[],[],[],[],[]]
        for card in palette:
            num_count[card.rank] += 1
            card_list[card.rank].append(card)

        highest_count = max(num_count)
        highest_list = []
        for i in range(len(num_count)):
            if num_count[i] == highest_count:
                highest_list.append(card_list[i])

        return highest_count, max(max(highest_list))

    if color == 'Yellow':
        num_count = [0, 0, 0, 0, 0, 0, 0, 0]
        card_list = [[],[],[],[],[],[],[],[]]
        for card in palette:
            num_count[card.colorRank] += 1
            card_list[card.colorRank].append(card)

        highest_count = max(num_count)
        highest_list = []
        for i in range(len(num_count)):
            if num_count[i] == highest_count:
                highest_list.append(card_list[i])

        return highest_count, max(max(highest_list))

    if color == 'Green':
        evenCount = 0
        card_list = [Card('Null', -1, -1)]

        for card in palette:
            if card.rank%2 == 0:
                evenCount += 1
                card_list.append(card)
        
        return evenCount, max(card_list)

    if color == 'Blue':
        colorSet = set()
        for card in palette:
            colorSet.add(card.color)

        return len(colorSet), max(palette)

    if color == 'Indigo':
        numSet = set()
        for card in palette:
            numSet.add(card.rank)

        card_list = [set(), set(), set(), set()]
        card_list_index = 0
        for num in numSet:
            if num + 1 in numSet:
                card_list[card_list_index].add(num)
                card_list[card_list_index].add(num+1)
            else:
                card_list[card_list_index].add(num)
                card_list_index += 1

        card_list = [val for val in card_list if val]
        max_set_len = max(len(val) for val in card_list)
        card_list = [val for val in card_list if len(val) == max_set_len]
        sequence_top = [card for card in palette if card.rank == max(max(card_list))]

        return max_set_len, max(sequence_top)

    if color == 'Violet':
        small_list = []
        for card in palette:
            if card.rank < 4:
                small_list.append(card)
        
        if len(small_list) == 0:
            return 0, Card('Null', 0, 0)

        return len(small_list), max(small_list)
        
def check_win(sub_palette1, sub_palette2):
    if sub_palette1[0] > sub_palette2[0]:
        return True
    elif sub_palette1[0] == sub_palette2[0]:
        return sub_palette1[1] > sub_palette2[1]
    else:
        return False

def current_winner_name(color, PlayerList):
    win_subpalette = (0, Card('Null', 0, 0))
    for player in PlayerList:
        player_subpalette = game_rule(color, player.palette)
        if not check_win(win_subpalette, player_subpalette):
            win_subpalette = player_subpalette
            win_name = player.name

    return win_name

    



