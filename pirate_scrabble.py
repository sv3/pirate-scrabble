import random
import string

with open('twl06.txt') as twl06:
    dictionary = [word[:-1].upper() for word in twl06.readlines()[2:]]

min_word_length = 3
alphabet = string.ascii_uppercase
pool = [13,5,6,7,24,6,7,6,12,2,2,8,8,11,15,4,2,12,10,10,6,2,4,2,2,2]
pool_flipped = [0 for i in range(26)]
played_words = []


def pooltoletters(letterpool):
    letterlist = [ alphabet[i]*num for i, num in enumerate(letterpool) ]
    return ''.join(letterlist)


def letterstopool(letters):
    letterpool = [0 for i in range(26)]
    for l in letters.upper():
        letterindex = alphabet.find(l)
        print(letterindex)
        letterpool[letterindex] += 1
    return letterpool


def pickletter(letterpool):
    poolstring = ''.join([ alphabet[i]*num for i, num in enumerate(letterpool) ])
    letter = random.choice(poolstring)
    return letter


def check_fully_contained(donor, target):
    '''Check if donor is fully contained in target. Return any remaining letters from target'''
    for l in donor:
        index = target.find(l)

        # letter not in target word - abort
        if index < 0:
            return False
        else:
            # remove the letter
            target = target[:index] + target[index+1:]

    # return remaining letters from target word
    return target


def recursive(target, played_words, letterpool):
    target = target.upper()

    if played_words != []:
        for donor in played_words:
             # Check if any of the played words are fully contained in the target word
            remaining = check_fully_contained(donor, target)
            if remaining == False:
                # try the next word in played_words
                continue
            elif remaining == '':
                # found a word to steal - done
                played_words.remove(donor)
                print('stealing ' + donor + ' to make ' + target)
                return True, letterpool, played_words
            else:
                # found a word to steal for some of the letters needed - we need to go deeper
                played_words.remove(donor)
                result, newpool, new_played_words = recursive(remaining, played_words, letterpool)
                print('stealing ' + donor + ' to make ' + target)
                if result == True:
                    return True, newpool, new_played_words
                else:
                    return False, letterpool, played_words

    # take a tile from the pool for each letter in the word
    newpool = letterpool.copy()
    target_remaining = ''
    for letter in target:
        letterindex = alphabet.find(letter)
        newpool[letterindex] -= 1

        # did we run out of this letter? add it to the remaining (leftover) letters
        if newpool[letterindex] < 0:
            target_remaining = target_remaining + letter
    print('letters remaining in pool after making', target , ':', pooltoletters(newpool))


    if all(map(lambda x: x>=0, newpool)):
        return True, newpool, played_words
    else:
        return False, letterpool, played_words
    return False, letterpool, played_words

def infinite():
    while True:
        print('tiles in pool: ', end='')
        print(pooltoletters(pool_flipped))
        print('words played: ' + '  '.join(played_words) )

        word = input('enter word: ').upper()
        clear_output()

        result = False

        # is it a valid word?
        if len(word) == 0:
            pass
        elif len(word) < min_word_length:
            print('That word is too short. Minimum length is', min_word_length)
        elif word not in dictionary:
            print(word, 'is not even a word ⚆_⚆')
        else:
            result, pool_flipped, played_words = recursive(word, played_words, pool_flipped)

        if result:
            print('You claimed ' + word)
            played_words.append(word)
        else:
            letter = pickletter(pool)
            print('flipped over', letter)
            letterindex = alphabet.find(letter)
            pool[letterindex] -= 1
            pool_flipped[letterindex] += 1

