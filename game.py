from threading import Thread, Lock
from random import choice

lock_console_output = Lock()


class Player:
    def __init__(self, name):
        self.name = name


class Target:
    def __init__(self):
        self.__players_hits = dict()
        self.__points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __print_hit(self, hit: int, player: Player) -> None:

        def safe_print(*string):
            """Стандартный print() не потокобезопасен, поэтому лучше использовать свой вариант печати.
            Это защищает от возможной каши в консоли."""
            with lock_console_output:
                print(*string)

        if hit == 10:
            safe_print(f"{player.name}, меткий выстрел! Количество очков: {str(hit).rjust(2, '0')}.")
        elif hit in [8, 9]:
            safe_print(f"{player.name}, неплохо! Количество очков: {str(hit).rjust(2, '0')}.")
        elif hit in [5, 6, 7]:
            safe_print(f"{player.name}, так себе выстрел. Количество очков: {str(hit).rjust(2, '0')}.")
        else:
            safe_print(f"{player.name}, мазила! Количество очков: {str(hit).rjust(2, '0')}.")

    def take_shots(self, player: Player) -> None:
        hits_counter = 0
        while hits_counter != 3:
            hit = choice(self.__points)

            if player.name not in self.__players_hits:
                self.__players_hits[player.name] = hit
            else:
                self.__players_hits[player.name] += hit if hit >= 5 else 0  # Не считаем попадания в белые зоны мишени!

            self.__print_hit(hit, player)

            hits_counter = hits_counter + 1

    def summarize(self) -> None:
        scoreboard = {v: k for k, v in sorted(self.__players_hits.items(), key=lambda x: x[1], reverse=True)}
        for score in enumerate(scoreboard, 1):
            print(f'{"Победитель!" if score[0] == 1 else str(score[0]) + "."} {scoreboard[score[1]]} (суммарное '
                  f'количество очков: {score[1]}).')


if __name__ == '__main__':
    one_player = Player("Артур")
    two_player = Player("Семён")
    three_player = Player("Данил")

    target = Target()

    print("\nИГРА НАЧИНАЕТСЯ! \n")

    first_player_hits = Thread(name='first_player', target=target.take_shots, args=(one_player,))
    second_player_hits = Thread(name='second_player', target=target.take_shots, args=(two_player,))
    third_player_hits = Thread(name='third_player', target=target.take_shots, args=(three_player,))

    first_player_hits.start(), second_player_hits.start(), third_player_hits.start()
    first_player_hits.join(), second_player_hits.join(), third_player_hits.join()

    print("\nКАЖДЫЙ ИЗ ИГРОКОВ СДЕЛАЛ ПО ТРИ ВЫСТРЕЛА. ПОДВЕДЕМ ИТОГИ ИГРЫ: \n")

    target.summarize()
