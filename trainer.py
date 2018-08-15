from threading import Thread
from queue import Queue
from random import shuffle, choice
from math import ceil

from board import Board
from player import NNPlayer


def trainer_thread(queue, thread_id, done_queue):
    """
    A thread tha pulls two NNPlayers from a queue and plays a game with them, updates their elo and puts them in a
    separate queue
    :param queue: a queue of bots that have not player yet
    :type queue: Queue
    :param thread_id: the thread id
    :type thread_id: int
    :param done_queue: a queue of bots that have payed
    :type done_queue: Queue
    """

    while queue.qsize() > 1:
        player_one = queue.get()
        player_two = queue.get()
        board = Board(player_one, player_two)
        winner, loser, tie = board.play()  # type: NNPlayer, NNPlayer, bool
        NNPlayer.update_elo(winner, loser, tie)
        done_queue.put(player_one)
        done_queue.put(player_two)
    #print('{} done'.format(thread_id))


def run_generation(players, threads=10):
    """
    runs one generation with each bot playing one game, removes all that tried to make and illegal move and orders the
    remaining on their elo
    :param players: an array of the current population
    :type players: NNPlayer[]
    :param threads: the number of threads to spawn
    :type threads: int
    :return:
    :rtype:
    """

    shuffle(players)
    player_queue = Queue()
    done_queue = Queue()
    for player in players:
        player_queue.put(player)
    for thread in range(threads):
        thread = Thread(target=trainer_thread, args=(player_queue, thread, done_queue))
        thread.start()
    while done_queue.qsize() < len(players):
        pass

    players.sort(reverse=True)
    return players


def train(population_size, fraction_kept, threads, generations, mutation_rate):
    """
    trains the neural nets for a given number of generations
    :param population_size: the number of bots to have in each generation
    :type population_size: int
    :param fraction_kept: proportion of bots to cull each generation
    :type fraction_kept: float
    :param threads: number of training threads to use
    :type threads: int
    :param generations: number of generations to train for
    :type generations: int
    :return: the best bot
    :rtype: NNPlayer
    """

    players = [NNPlayer() for _ in range(population_size)]

    for generation in range(generations):
        print(f"generation {generation} {players[0]}")
        players = run_generation(players, threads)[:int(len(players) * fraction_kept)]
        while len(players) < population_size:
            new_player = choice(players).copy()  # type: NNPlayer
            new_player.mutate(mutation_rate)
            players.append(new_player)
    return players[0]


if __name__ == '__main__':
    from player import HumanPlayer
    best = train(100, 0.5, 10, 100, 0.2)
    print("\n\nTraining Complete\n\n")
    print(f"best elo is {best.elo}")
    best.save()
    human = HumanPlayer()
    board = Board(human, best)
    board.play()
