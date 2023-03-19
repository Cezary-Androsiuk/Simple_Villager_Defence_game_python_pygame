import random
import time
import numpy
import pygame
import copy
import datetime
from pygame.locals import *

from GlobalFunctions import *

from Coin import Coin
from Villager import Villager
from Enemy import Enemy
from Player import Player

class Game:
    game_running = True
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    window_width = 1200
    window_height = 720
    screen = pygame.display.set_mode((window_width, window_height))

    font = pygame.font.SysFont('ubuntumono', 30)
    font2 = pygame.font.SysFont('ubuntumono', 50)
    money_text = font.render("TEXT", False, (170, 170, 170))
    score_text = font.render("TEXT", False, (170, 170, 170))

    player = Player()

    enemy_array = []
    enemy_spawn_count = 1
    enemy_spawn_timer_delay = 30
    enemy_spawn_timer = enemy_spawn_timer_delay

    improve_difficulty_timer_delay = 30 * 5
    improve_difficulty_timer = improve_difficulty_timer_delay



    villagers_array = []
    villagers_array.append(Villager([window_width/2, window_height/2], 300))

    buy_villager_text = font.render("Buy Villager 50K", False, (30, 30, 30))
    buy_villager_button = pygame.Rect(
                                pygame.Vector2(
                                    window_width - 10 - buy_villager_text.get_width()  - 20,
                                    window_height - 45),
                                pygame.Vector2(buy_villager_text.get_width() + 20, 40)
                            )
    exit_game_text = font.render("Exit Game", False, (30, 30, 30))
    exit_game_button = pygame.Rect(
                                pygame.Vector2(
                                    window_width / 2 - (exit_game_text.get_width() + 20) / 2,
                                    window_height - 45),
                                pygame.Vector2(exit_game_text.get_width() + 20, 40)
                            )
    clear_score_history_text = font.render("Clear Score History", False, (30, 30, 30))
    clear_score_history_button = pygame.Rect(
                                pygame.Vector2(
                                    window_width / 2 - (clear_score_history_text.get_width() + 20) / 2,
                                    window_height - 90),
                                pygame.Vector2(clear_score_history_text.get_width() + 20, 40)
                            )

    coins_array = []

    pause_text = font2.render("TEXT", False, (170, 170, 170))

    pause = False
    lose = False

    score_saved = False
    leaderboard_loaded = False
    leaderboard_scores_array = []

    def __int__(self):
        pass

    def pollEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_running = False
                self.save_current_score()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause:
                        # to niżej usunąć
                        # self.game_running = False
                        if self.lose:
                            self.game_running = False
                            self.save_current_score()
                        self.pause = False
                    else:
                        self.pause = True
            # left button down
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.pause:
                    if self.buy_villager_button.collidepoint(pygame.mouse.get_pos()):
                        if self.player.money >= 50000:
                            self.villagers_array.append(
                                Villager(
                                    [
                                        random.randint(
                                            self.window_width/2 - (self.window_width * 0.1),
                                            self.window_width/2 + (self.window_width * 0.1)
                                        ),
                                        random.randint(
                                            self.window_height / 2 - (self.window_height * 0.1),
                                            self.window_height / 2 + (self.window_height * 0.1)
                                        )
                                     ],
                                    200,
                                    15,
                                    750
                                )
                            )
                            self.player.villagers_count_as_score_const += 1
                            self.player.money -= 50000
                        else:
                            print("you need $50k")
                    else:
                        self.player.gunStartFire()
                else:
                    if self.exit_game_button.collidepoint(pygame.mouse.get_pos()):
                        self.game_running = False
                        self.save_current_score()
                    if self.clear_score_history_button.collidepoint(pygame.mouse.get_pos()):
                        self.clear_score_history()
                        self.pause = False

            # left button up
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.player.gunStopFire()
            # # right button down
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #     self.player.gunStartFire()
            # # right button up
            # if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            #     self.player.gunStopFire()

        # key = pygame.key.get_pressed()
        # if key[pygame.K_w]:
        #     self.player.movePlayer([0,-1])


    def computeGassCollision(self,enemy):
        gas_array = self.player.getGas()
        for gas in gas_array:
            if vectorLength(buildVector(gas.position, enemy.position)) < gas.size + enemy.size:
                enemy.poison()

    def enemySpawnPosition(self, enemy_size):
        x, y = pygame.display.get_surface().get_size()
        rnd_side = random.randint(0,3)
        match rnd_side:
            case 0: # left
                return [0, random.randint(enemy_size, y - enemy_size)]
            case 1: # right
                return [x, random.randint(enemy_size, y - enemy_size)]
            case 2: # top
                return [random.randint(enemy_size, x - enemy_size), 0]
            case 3: # bottom
                return [random.randint(enemy_size, x - enemy_size), y]

    def closestVillager(self, enemy_position):
        distance = 100000
        villager_position = [0, 0]
        for villager in self.villagers_array:
            each_distance = vectorLength(buildVector(villager.position, enemy_position))
            if each_distance < distance:
                distance = each_distance
                villager_position = villager.position
        return villager_position


    def updateEnemy(self):
        if self.enemy_spawn_timer == 0:
            self.enemy_spawn_timer = self.enemy_spawn_timer_delay
            enemy_size = 20
            for i in range(0, self.enemy_spawn_count):
                self.enemy_array.append(Enemy(self.enemySpawnPosition(enemy_size), enemy_size, 80))
        else:
            self.enemy_spawn_timer -= 1

        # if self.enemy_spawn_timer_delay > 2:
        #     # there is possibility to decrease spawn time
        #     if self.improve_difficulty_timer == 0:
        #         self.improve_difficulty_timer_delay += 30
        #         self.improve_difficulty_timer = self.improve_difficulty_timer_delay
        #         self.enemy_spawn_timer_delay -= 1
        #     else:
        #         self.improve_difficulty_timer -= 1
        # else:
        #     # there is NO possibility to decrease spawn time,
        #     # so increase enemy spawn count
        #     if self.improve_difficulty_timer == 0:
        #         self.improve_difficulty_timer_delay += 30
        #         self.improve_difficulty_timer = self.improve_difficulty_timer_delay
        #         self.enemy_spawn_count += 1
        #     else:
        #         self.improve_difficulty_timer -= 1


        if self.improve_difficulty_timer == 0:
            self.improve_difficulty_timer_delay += 30
            self.improve_difficulty_timer = self.improve_difficulty_timer_delay
            if self.enemy_spawn_timer_delay > 2:
                self.enemy_spawn_timer_delay -= 1
            else:
                self.enemy_spawn_count += 1
            print("current enemy spawn time delay: " + str(self.enemy_spawn_timer_delay) +
                  "   current enemy spawn count: " + str(self.enemy_spawn_count))
        else:
            self.improve_difficulty_timer -= 1

        for enemy in self.enemy_array:
            self.computeGassCollision(enemy)
            enemy.update(self.closestVillager(enemy.position))
            if not enemy.alive:
                for i in range(0, 3):
                    self.coins_array.append(
                        Coin(
                            (enemy.position[0] + random.randint(-enemy.size, enemy.size),
                             (enemy.position[1] + random.randint(-enemy.size, enemy.size))),
                            1000
                        )
                    )
                self.enemy_array.remove(enemy)

    def updateCoin(self):
        for coin in self.coins_array:
            coin.update(pygame.mouse.get_pos())
            gainedCoins = coin.isCollected()
            if gainedCoins != 0:
                self.coins_array.remove(coin)
                self.player.money += gainedCoins

    def closestEnemy(self, villager_position):
        distance = 100000
        enemy_position = [0, 0]
        for enemy in self.enemy_array:
            each_distance = vectorLength(buildVector(enemy.position, villager_position))
            if each_distance < distance:
                distance = each_distance
                enemy_position = enemy.position
        return enemy_position

    def detectVillagerAndEnemyCollision(self,villager):
        for enemy in self.enemy_array:
            if vectorLength(buildVector(villager.position, enemy.position)) < enemy.size + villager.size:
                villager.dealDamage(1)


    def updateVillager(self):
        for villager in self.villagers_array:
            villager.update(self.closestEnemy(villager.position))
            self.detectVillagerAndEnemyCollision(villager)
            if not villager.alive:
                self.villagers_array.remove(villager)
                self.player.villagers_count_as_score_const -= 1

    def save_current_score(self):
        with open("leaderboard.txt", 'r') as f:
            prev_file = f.read().split('\n')
        with open("leaderboard.txt", 'w') as f:
            # f.write("Score: " + str(self.player.score) + " Villagers: " + str(len(self.villagers_array)) +
            #         " Date: " +  datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S') + "\n")
            f.write("Score(" + str(self.player.score) + ") Villagers(" + str(len(self.villagers_array)) +
                    ") Date(" +  datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S') + ")\n")
            for line in prev_file:
                f.write(line + "\n")

    def load_leaderboard(self):
        self.leaderboard_scores_array.append(self.font.render("Last 15 Scores", False, (170, 170, 170)))
        # last 15 and
        with open("leaderboard.txt", 'r') as f:
            temp = f.read().split('\n')
        i = 0
        for line in temp:
            value = line.split(' ')
            # self.leaderboard_scores_array.append([map(int, value[0]), value[1]])
            self.leaderboard_scores_array.append(self.font.render(line, False, (170, 170, 170)))
            i += 1
            if i == 15:
                break
        # records = list(map(int, temp))
        # records.sort(reverse=True)

    def renderLeaderboard(self):
        top_margin = 120
        i = 0
        for single_text in self.leaderboard_scores_array:
            self.screen.blit(single_text, [self.window_width/2 - single_text.get_width()/2, top_margin + 30 * i])
            i += 1

    def clear_score_history(self):
        with open("leaderboard.txt", 'w') as f:
            f.write("")

    def update(self):
        self.clock.tick(30)
        self.pollEvent()

        if len(self.villagers_array) == 0:
            self.pause = True
            self.lose = True

        if not self.pause:
            self.leaderboard_loaded = False
            self.leaderboard_scores_array.clear()

            self.player.updateGun(pygame.mouse.get_pos())
            self.player.update()

            self.updateEnemy()
            self.updateCoin()
            self.updateVillager()


        else:
            if self.lose:
                # save score
                if not self.score_saved:
                    self.save_current_score()
                    self.score_saved = True
            # load score
            if not self.leaderboard_loaded:
                self.load_leaderboard()
                self.leaderboard_loaded = True

        m_str = "  $" + str((int)(self.player.money / 1000)) + ","
        if self.player.money % 1000 < 1:
            m_str += "000"
        elif self.player.money % 1000 < 10:
            m_str += "00" + str(self.player.money % 1000)
        elif self.player.money % 1000 < 100:
            m_str += "0" + str(self.player.money % 1000)
        else:
            m_str += str(self.player.money % 1000)
        self.money_text = self.font.render(m_str, False, (170, 170, 170))

        self.score_text = self.font.render(
            "Score: " + str(self.player.score) + "   Villagers: " +
            str(self.player.villagers_count_as_score_const) + "", False, (170, 170, 170))

    def render(self):
        self.screen.fill((30, 30, 30))
        if not self.pause:
            for enemy in self.enemy_array:
                enemy.render(self.screen)

            for coin in self.coins_array:
                coin.render(self.screen)

            for villager in self.villagers_array:
                villager.render(self.screen)

            self.player.render(self.screen)

            self.screen.blit(self.money_text, (0, 0))

            pygame.draw.rect(self.screen, (170, 170 ,170), self.buy_villager_button)
            self.screen.blit(self.buy_villager_text, (
                self.window_width - self.buy_villager_text.get_width() - 20, self.window_height - 40)
            )

        else:
            if self.lose:
                self.pause_text = self.font2.render("YOU LOSE", False, (255, 65, 65))
            else:
                self.pause_text = self.font2.render("GAME PAUSED", False, (170, 170, 170))

            self.screen.blit(self.pause_text, (self.window_width / 2 - self.pause_text.get_width() / 2, 50))

            self.renderLeaderboard()

            pygame.draw.rect(self.screen, (170, 170 ,170), self.exit_game_button)
            self.screen.blit(self.exit_game_text, (
                self.window_width/2 - self.exit_game_text.get_width()/2 , self.window_height - 40)
            )
            pygame.draw.rect(self.screen, (170, 170 ,170), self.clear_score_history_button)
            self.screen.blit(self.clear_score_history_text, (
                self.window_width/2 - self.clear_score_history_text.get_width()/2 , self.window_height - 85)
            )
        self.screen.blit(self.score_text, (self.window_width / 2 - self.score_text.get_width() / 2, 0))

        pygame.display.update()

    def running(self):
        return self.game_running

        # with open('records/leaderboard', 'r') as f:
        #     temp = f.read().strip().split('\n')
        #
        # records = list(map(int, temp))
        # records.sort(reverse=True)

    # if self.score_record:
    #     with open('records/leaderboard', 'a') as f:
    #         f.write(str(self.score)+'\n')

