"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    i, kth_pargrph_index, empty_string = 0, 0, ''
    while(kth_pargrph_index<k+1):
        if i == len(paragraphs) and kth_pargrph_index<k+1:
            return ''
        elif select(paragraphs[i]) == True:
            kth_pargrph_index+=1
            if kth_pargrph_index == k+1:
                return paragraphs[i]
        i+=1
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    "and (paragraph[(paragraph.find(topic[i])-1)] not in 'abcdefghijklmnopqrstuvwxyz') and (paragraph[(paragraph.find(topic[i])+len(topic[i])-1)] not in 'abcdefghijklmnopqrstuvwxyz'):"

    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph):
        i=0
        paragraph = paragraph.lower()
        paragraph = paragraph.translate(paragraph.maketrans('', '', string.punctuation))
        pg_list = paragraph.split()
        while(i<len(topic)):
            k=0
            while(k<len(pg_list)):
                if topic[i] in pg_list:
                    return True
                k+=1
            i+=1
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    dividend,divisor,i=0,len(reference_words),0
    while(i<len(typed_words) and i<len(reference_words)):
        if typed_words[i] in reference_words[i]:
            dividend+=1
        i+=1
    if len(typed_words) > len(reference_words):
        divisor+=len(typed_words)-len(reference_words)
    if len(reference_words) > len(typed_words) > 0:
        divisor=len(typed_words)
    return (dividend/divisor)*100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    words=len(typed)/5
    words_per_min=words*(60/elapsed)
    return words_per_min
    # END PROBLEM 4

"""for k in len(valid_words[i]):
                valid_words[i].slice(p,q)
                k,p,q = k+1,p+1,q+1"""

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    finding_smallest_diff_function = lambda valid_words: diff_function(user_word, valid_words, limit)
    closest_word = min(valid_words, key=finding_smallest_diff_function)
    i = 0
    while(i<len(valid_words)):
        if user_word in valid_words[i] and len(user_word) == len(valid_words[i]):
            return user_word
        if diff_function(user_word, closest_word, limit) > limit:
            return user_word
        elif i+1 == len(valid_words) and diff_function(user_word, closest_word, limit) <= limit:
            return closest_word
        i+=1
    # END PROBLEM 5


def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def swap_count(start,goal,limit):
        if limit==-1:
            return limit+1
        if len(start) == 0 or len(goal) == 0:
            return max(len(start), len(goal))
        if start[0] == goal[0]:
            return swap_count(start[1:],goal[1:],limit)
        elif start[0] != goal[0]:
            return 1+swap_count(start[1:],goal[1:],limit-1)
    return swap_count(start,goal,limit)
    # END PROBLEM 6


def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    """ Base cases: """
        # BEGIN
    if limit==-1:
        return limit+1
    if (start == goal):
        return 0
    elif (len(start) == 0 or len(goal) == 0):
        return max(len(start), len(goal))
    elif start[0] == goal[0]: # Fill in the condition
        # BEGIN
        return feline_fixes(start[1:], goal[1:], limit)
    else:
        add_diff = 1+feline_fixes(goal[0] + start, goal, limit-1) # Fill in these lines
        remove_diff = 1+feline_fixes(start[1:], goal, limit-1)
        substitute_diff = 1+feline_fixes(start[1:], goal[1:], limit-1)
        return min(add_diff, remove_diff, substitute_diff)
        # END """


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    if_typed_is_longer, correct_words, i = 0,0,0
    while (i<len(prompt)) and i<len(typed):
        if typed[i] == prompt[i]:
            correct_words+=1
        else: break
        i+=1
    progress = correct_words/(len(prompt)+if_typed_is_longer)
    dict = {'id': id, 'progress': progress}
    send(dict)
    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    i,j,k=0,0,0
    times=[[]]
    while(i<len(times_per_player)-1):
        if i > 0:
            times[i].append([])
        while(k<len(times_per_player[i])-1):
            times[i].append(times_per_player[i][k+1] - times_per_player[i][k])
            k+=1
        i+=1
    return times[0][0]
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
