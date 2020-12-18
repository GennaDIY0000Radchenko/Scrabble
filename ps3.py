# Name          : Radchenko Gennadiy
# Collaborators : Obolonskiy Denis (student of Sumy SU) - help in testing
# Time spent    : 1.5 hours to make secondary functions and from 3 to 4 hours to make play-functions

import math
import random
from copy import deepcopy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCORE = 0

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file. Please, wait a few seconds...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print(" ", len(wordlist), "words loaded\nGood luck :)\n\n")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word1 = word.lower()
    first = 0
    for i in word1:
        first += SCRABBLE_LETTER_VALUES.get(i, 0)
    second = HAND_SIZE * len(word) - 3 * (n - len(word))
    if second < 1:
        second = 1
    return first * second


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        letter_up = letter.upper()
        for j in range(hand[letter]):
            print(letter_up, end=' ')  # print all on the same line
    print()  # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    list_hand = [letter for letter in hand.keys()]
    number = random.randint(0, len(list_hand) - 1)

    if hand[list_hand[number]] == 1:
        del hand[list_hand[number]]
    else:
        hand[list_hand[number]] = hand[list_hand[number]] - 1
    hand["*"] = 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = {}
    word1 = word.lower()
    for letter_in_hand in hand.keys():
        counter = 0
        if letter_in_hand in word1:
            for letter_in_word in word1:
                if letter_in_word == letter_in_hand:
                    counter += 1
        if hand[letter_in_hand] == counter:
            pass
        else:
            new_hand[letter_in_hand] = hand[letter_in_hand] - counter

    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    test = True
    word1 = word.lower()
    checked_letters = []
    hand_letters = [letter for letter in hand.keys()]

    if "*" in word1:
        position = []
        for letter in range(len(word1)):
            if word1[letter] == "*":
                position.append(letter)
        if len(position) >= 2:
            test = False
        else:
            pos = position[0]
            test = False
            for var_vow in VOWELS:
                word2 = word1[:pos] + var_vow + word1[pos + 1:]
                hand1 = deepcopy(hand)
                hand1[var_vow] = hand1.get(var_vow, 0) + 1
                if is_valid_word(word2, hand1, word_list):
                    return True

    if word1 not in word_list:
        test = False

    if test:
        for letter_in_word in word1:
            if letter_in_word not in checked_letters:
                if letter_in_word in hand_letters:
                    counter = 0
                    for letter in word1:
                        if letter == letter_in_word:
                            counter += 1
                    if hand[letter_in_word] - counter < 0:
                        test = False
                    checked_letters.append(letter_in_word)
                else:
                    test = False
            if not test:
                break
    return test


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum([hand[letter] for letter in hand.keys()])


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    global SCORE
    score = 0
    while True:
        print("\nCurrent Hand:", end=" ")
        display_hand(hand)
        word = str(input('Enter word, or “!!” to indicate that you are finished: '))
        valid = is_valid_word(word, hand, word_list)
        if word == "!!":
            break

        elif valid:
            word_up = word.upper()
            score_plus = get_word_score(word, calculate_handlen(hand))
            score += score_plus
            print(f'"{word_up}" earned {score_plus} points. Total: {score}')

        hand = update_hand(hand, word)

        if not valid:
            print('This is not a valid word.', end=' ')
            if calculate_handlen(hand) != 0:
                print('Please choose another word.')
            else:
                print('')

        if calculate_handlen(hand) == 0:
            print('Ran out of letters')
            break

    print(f'\nTotal score for this hand: {score} points'
          f'\n--------------------------------------')
    return score


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_letter = letter
    while new_letter in [letters for letters in hand.keys()]:
        new_letter = random.choice(VOWELS + CONSONANTS)
    hand[new_letter] = hand[letter]
    del hand[letter]
    return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    global SCORE
    while True:
        try:
            HANDS = input('\nEnter total number of hands: ')
            HANDS = int(HANDS)
            assert 1 <= HANDS
            break
        except ValueError:
            print('Input error! Be careful')
        except AssertionError:
            print('You must enter the number of games(natural number)!')

    hand = deal_hand(HAND_SIZE)
    set_hand = [letter for letter in hand.keys()]

    while HANDS != 0:

        print("\nCurrent Hand:", end=" ")
        display_hand(hand)

        while True:
            choose = str(input('Would you like to substitute a letter(yes/no)? '))
            if choose == 'yes':
                while True:
                    substitute_letter = str(input('Which letter would you like to replace, or “!!” to go back: '))
                    if substitute_letter == '!!':
                        choose = '!!'
                        break
                    elif substitute_letter in set_hand and substitute_letter != "*":
                        substitute_hand(hand, substitute_letter)
                        break
                    else:
                        print("There`s no such letter in the current hand!")

            elif choose == 'no':
                break
            else:
                print('Please, enter "yes" or "no"!')
                continue
            if choose == '!!':
                continue
            break

        score = play_hand(hand, word_list)
        while True:
            choice_3 = str(input('Would you like to replay the hand(yes/no)? '))
            if choice_3 == 'yes':
                score += play_hand(hand, word_list)
            elif choice_3 == 'no':
                break
            else:
                print('Please, enter "yes" or "no"!')
                continue
            break
        SCORE += score
        hand = deal_hand(HAND_SIZE)
        set_hand = [letter for letter in hand.keys()]
        HANDS -= 1

    print(f'\nYou played with this number of letters in hand:   {HAND_SIZE}')
    print(f'You played with this number of hands in one game: {HANDS}')
    print(f'TOTAl SCORE over all hands :                      {SCORE}\n')

    if SCORE / HAND_SIZE <= 200:
        print('You can do better')
    elif SCORE / HAND_SIZE <= 400:
        print('It`s good result')
    else:
        print('You played like pro. Keep it up')

    while True:
        choice_2 = str(input('\nBritney: Hit me baby one more time! Yes/no?: '))
        if choice_2.lower() == 'yes':
            print('\n')
            play_game(word_list)
        elif choice_2.lower() == 'no':
            break
        else:
            print('Britney loves accurate men, so enter "yes" or "no"')


if __name__ == '__main__':
    word_list = load_words()

    print("\n'*' can replace one of these letters : ", end="")
    for letter in VOWELS:
        letter_up = letter.upper()
        print(letter_up, end=" ")
    print('\nKeep in mind !\n\n')

    while True:
        choice_1 = str(input('\n__PLAY__'
                             '\nSETTINGS'
                             '\n__QUIT__'
                             '\n--------'
                             '\nSelect->'))
        if choice_1.lower() in ['play', '__play__']:
            play_game(word_list)
            continue
        elif choice_1.lower() in ['settings', '__settings__']:
            while True:
                try:
                    arg = input('How many letters do you want to start the game witg(5->30), or "!!" to  go back: ')
                    if arg == "!!":
                        break
                    arg = int(arg)
                    assert 5 <= arg <= 30
                    HAND_SIZE = arg
                    print('Okay, settings saved')
                    break
                except ValueError:
                    print('Please, enter a number')
                except AssertionError:
                    print('The number of letters should range from 5 to 30')
            continue
        elif choice_1.lower() in ['quit', '__quit__']:
            print('Bye! Have a nice day! :)')
            break
        else:
            print('Hey, dude choose one of the following (play, settings or quit)(try enter without "__")')
