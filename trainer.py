def trainerThread(queue, ID, done_queue):
    while queue.qsize() > 1:
        player_one = queue.get()
        player_two = queue.get()
        playGame(player_one, player_two)
        done_queue.put(player_one)
        done_queue.put(player_two)
    print('{} done'.format(ID))
    return


def generation(players, threads=10):
    shuffle(players)
    player_queue = Queue()
    done_queue = Queue()
    for player in players:
        player_queue.put(player)
    for thread in range(threads):
        thread = Thread(target=trainerThread, args=(player_queue, thread, done_queue))
        thread.start()
    while done_queue.qsize() < len(players):
        pass
    for player in players:
        if player.fitness != 1000:
            print(player.fitness)


if __name__ == '__main__':
    players = [NNPlayer() for _ in range(100)]
    generation(players)