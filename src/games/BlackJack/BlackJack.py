import random

import sys as system
import tkinter as tk

from src import run_main
from src.games.BlackJack.Cartes import Carte, PaquetDeCartes, Pile
from src.games.BlackJack.Joueur import Joueur
from random import shuffle
from tkinter import font as ft
from tkinter import messagebox
from src.resources.utils.Constants import clean_path, Constants, Debug


def GetPlayerPosession(player: Joueur):
    name = player.get_name()
    if name.endswith('s'):
        return name + "'"
    return name + "'s"


def g_help():
    messagebox.showinfo(title="Help & Rules", message="Blackjack rules:\n\n"
                                                      "- La mise est perdue si la maison gagne\n"
                                                      "- La mise est récupérée si il y a égalité\n"
                                                      "- La mise est récupérée plus la moitié si le joueur fait un blackjack\n")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 1.0")


class Game:

    def __init__(self, game_type: str = "european", nombreDePaquets: int = 5, start_money=100,
                 player_name=""):

        self.playerName = player_name
        if self.playerName == "":
            namesList = ["James", "Arthur", "Jean", "Juan", "Pierre", "Michel", "Thomas"]
            w = tk.Tk()
            w.title("BlackJack")
            w.protocol("WM_DELETE_WINDOW", self.exit_game)
            customFont = ft.Font(family='Source Sans Pro Black', size=17)
            name = tk.StringVar()
            name.set(namesList[random.randint(0, len(namesList)-1)])
            tk.Label(w, text="Enter your name:", font=customFont).pack(anchor="nw")
            self.PlayerNameEntry = tk.Entry(w, font=customFont, textvariable=name)
            self.PlayerNameEntry.pack(anchor="nw", fill="both")
            tk.Button(w, text="Confirm", command=lambda: self.selectPlayer(w), font=customFont).pack(anchor="n", fill="both")
            Constants.center(w)
            w.mainloop()

        self.gameType = game_type
        self.euroDraw = False
        self.aceValue = 11
        self.nombreDePaquets = nombreDePaquets
        self.paquets = self.initPaquetsTotal()
        self.cards = Pile(self.getCards())
        self.player = Joueur(self.playerName, "player")
        self.mise = 0
        self.money = {"cpu": 0, "player": start_money, "start": start_money}

        self.cpu = Joueur("House", "cpu")
        self.players = {"cpu": self.cpu, "player": self.player}
        self.imgs = {}
        self.cards_placed = []
        self.path = Constants.get_path()

        self.cardsPlaces = {"cpu": [(1, i) for i in range(1, 10)], "player": [(4, i) for i in range(1, 10)]}

        self.w = tk.Tk()
        customFont = ft.Font(family='Source Sans Pro Black', size=12)
        self.w.option_add("*font", customFont)
        self.w.title(f"BlackJack - {game_type.capitalize()}")
        self.w.protocol("WM_DELETE_WINDOW", self.exit_game)

        menubar = tk.Menu(self.w)
        self.w.config(menu=menubar)
        self.create_menu(menubar)

        sample_card = tk.PhotoImage(file=f"{clean_path(str(self.path.joinpath('resources/images/BlackJack/2_carreau.gif')))}")
        for row in [0, 2, 3]:
            self.w.rowconfigure(row, minsize=30)
        self.w.columnconfigure(0, minsize=30)
        for row in [1, 4]:
            self.w.rowconfigure(index=row, minsize=sample_card.height()+2)
        for column in range(1, 6):
            self.w.columnconfigure(index=column, minsize=sample_card.width()+2)

        self.labels = {"cpu": tk.Label(self.w, text=f"{GetPlayerPosession(self.cpu)} points: {self.cpu.get_points()}"),
                       "player": tk.Label(self.w, text=f"{GetPlayerPosession(self.player)} points: {self.player.get_points()}"),
                       "mise": tk.Label(self.w, text=f"Mise: {self.mise}"),
                       "money": tk.Label(self.w, text=f"Curr Money: {self.money['player']}"),
                       "money_lost": tk.Label(self.w, text=f"Net Profit: {self.money['start'] - self.money['player']}")}
        self.labels["cpu"].grid(row=0, column=1)
        self.labels["money_lost"].grid(row=0, column=3)
        self.labels["player"].grid(row=3, column=1)
        self.labels["mise"].grid(row=3, column=3)
        self.labels["money"].grid(row=3, column=5)

        button1 = tk.Button(self.w, text="Player draw", command=lambda: self.turn(True))
        button1.grid(row=6, column=1)
        button2 = tk.Button(self.w, text="Player rest", command=lambda: self.turn(False))
        button2.grid(row=6, column=2)
        self.buttons = [button1, button2]
        button = tk.Button(self.w, text="Restart", command=self.resetGame)
        button.grid(row=6, column=5)
        # button = tk.Button(self.w, text="Update Graphics", command=self.settings)
        # button.grid(row=6, column=6)

        Debug.out("Main Window instanciated")

        Constants.center(self.w)
        self.mise_settings()
        self.w.mainloop()

    def selectPlayer(self, w: tk.Tk):
        name = self.PlayerNameEntry.get().strip()
        if name == "":
            return
        self.playerName = name
        w.destroy()

    def mise_settings(self, additionnal_message: str = ''):
        self.UpdateGraphics()
        if additionnal_message != '':
            additionnal_message = '    /!\\' + additionnal_message + '/!\\'
        miseWindow = tk.Tk()
        customFont = ft.Font(family='Source Sans Pro Black', size=12)
        miseWindow.option_add("*font", customFont)
        miseWindow.title("Mise Select")
        miseWindow.protocol("WM_DELETE_WINDOW", self.exit_game)
        tk.Label(miseWindow, text="Rentrez la somme à miser:").grid(row=0,column=0)
        tk.Label(miseWindow, text=f"Current Money: {self.money['player']}  " + additionnal_message).grid(row=1, column=0)
        entry = tk.Entry(miseWindow)
        entry.grid(row=2, column=0)
        exitButton = tk.Button(miseWindow, text="Confirm", command=lambda: self.miser(entry, miseWindow))
        exitButton.grid(row=3, column=0)

        Constants.center(miseWindow)
        miseWindow.mainloop()

    def miser(self, widget: tk.Entry, w: tk.Tk):
        try:
            value = int(widget.get())
            if 0 < value <= self.money['player']:
                Debug.debug(str(value), "Value")
                self.mise = value
                self.money['player'] -= value
                self.UpdateGraphics()

            else:
                w.destroy()
                self.mise_settings('Wrong input')
                return
        except (IndexError, ValueError):
            w.destroy()
            self.mise_settings('Wrong input')
            return
        self.Draw("cpu")
        self.Draw("player")
        Debug.out(f"Player mise {self.mise}")
        w.destroy()

    def initPaquetsTotal(self):
        paquets = [PaquetDeCartes(self.aceValue) for _ in range(self.nombreDePaquets)]
        Debug.out("Paquets Instantiated")
        return paquets

    def getCards(self):
        cards = []
        if not self.paquets:
            self.paquets = self.initPaquetsTotal()
        for p in self.paquets:
            p_cards = p.cards
            shuffle(p_cards)
            cards += p_cards
        shuffle(cards)
        Debug.out("Cards Instantiated")
        return cards

    def resetGame(self):
        for card in self.cards_placed:
            card.destroy()
        for player in self.players.values():
            player.reset()
        self.cards = Pile(self.getCards())
        self.UpdateGraphics()
        self.buttons[0].config(command=lambda: self.turn(True))
        self.buttons[1].config(command=lambda: self.turn(False))
        Debug.out("Game Reset")
        self.mise_settings()

    def UpdateGraphics(self):
        for player in self.players:
            self.labels[player].config(text=f"{GetPlayerPosession(self.players[player])} points: {self.players[player].get_points()}")
        self.labels["mise"].config(text=f"Mise: {self.mise}")
        self.labels["money"].config(text=f"Curr Money: {self.money['player']}")
        self.labels['money_lost'].config(text=f"Net Profit: {- self.money['start'] + self.money['player']}")

    def chanceAceValue(self, val: int):
        for e in self.cards.get() + [p.hand for p in self.players.values()]:
            if e == "as":
                e.setValue(val)

    def Draw(self, player: str):
        drawn_card = self.cards.pick()
        self.players[player].draw(drawn_card)
        self.placeCard(self.cardsPlaces.get(player)[len(self.players[player].hand) - 1], drawn_card)
        self.labels[player].config(text=f"{self.players[player].name} points: {self.players[player].get_points()}")
        Debug.out(f"Player '{self.players[player].name}' has drown {str(drawn_card)}")

    def distance(self, points: int):  ## To get the distance to 21 points, closest wins (except when exceeding 21)
        return 21 - points if points <= 21 else 999

    def hasBlackjack(self, player: Joueur):
        return len(player.hand) == 2 and player.get_points() == 21

    def getClosest(self):  ## If I need to use directly the closest entity
        Debug.debug(str(self.distance(self.players["cpu"].get_points())),  "CPU dst")
        Debug.debug(str(self.distance(self.players["player"].get_points())),  "player dst")
        cpu_points = self.distance(self.players["cpu"].get_points())
        player_points = self.distance(self.players["player"].get_points())

        blackJackCount = 0
        player = self.players["player"]

        for p in self.players.values():
            if self.hasBlackjack(p):
                blackJackCount += 1
                player = p

        if cpu_points != player_points and blackJackCount == 0:
            player = self.players["cpu"] if self.distance(self.players["cpu"].get_points()) < self.distance(self.players["player"].get_points()) else self.players["player"]
        if cpu_points == player_points:
            player = self.players
        dist = self.distance(player.get_points()) if not isinstance(player, dict) else 0
        return player, dist

    def placeCard(self, place: tuple[int, int], card: Carte):
        if not self.imgs.keys().__contains__(card.get_id()):
            img = tk.PhotoImage(file=str(clean_path(str(self.path.joinpath(f'resources/images/BlackJack/{str(card.getCardTextureName())}')))))
            self.imgs[card.get_id()] = img
        else:
            img = self.imgs.get(card.get_id())
        image = tk.Label(self.w, image=img)
        self.cards_placed.append(image)
        image.grid(row=place[0], column=place[1])

    def AceMechanic(self, player: Joueur):
        ace_found = False
        for card in player.hand:
            if card.name == "as":
                if card.get_value() != 1:
                    player.hand[player.hand.index(card)].setValue(1)
                    ace_found = True
                    Debug.out(f"Player's '{player.get_name()}' ace value changed to 1")
                    Debug.debug(str([str(card) for card in player.hand]), "PlayerCards")
                    break
        if player.get_points() > 21 and ace_found:
            self.AceMechanic(player)

    def CPU_draws(self) -> bool:  #TODO: basic logic for cpu, to integrate in a better way
        return self.players["cpu"].get_points() < 17

    def CPUDraw(self):
        if self.CPU_draws():
            self.Draw("cpu")
        else:
            self.DynamicChangeAces(self.players["cpu"])

    def turn(self, player_draws: bool):

        if not player_draws:
            for b in self.buttons:
                b.config(command="")
            while self.CPU_draws():
                self.CPUDraw()
            self.End()
            return
        #
        # if self.euroDraw:
        #     if self.CPU_draws():
        #         self.Draw("cpu")
        #     else:
        #         if self.DynamicChangeAces(self.players["cpu"]):
        #             self.End()
        #             return
        if player_draws:
            self.Draw("player")

        if self.players["player"].get_points() > 21:
            if self.DynamicChangeAces(self.players["player"]):
                self.End()
                return
        if self.hasBlackjack(self.players["player"]):
            self.End()
        elif self.players["player"].get_points() == 21:
            while self.CPU_draws():
                self.CPUDraw()
            self.End()
        # elif not self.euroDraw:
        #     self.Draw("cpu")
        #     self.euroDraw = True

    def DynamicChangeAces(self, player: Joueur):
        self.AceMechanic(player)
        self.UpdateGraphics()
        return player.get_points() > 21

    def End(self):
        self.buttons[0].config(command="")
        self.buttons[1].config(command="")
        closest, dist = self.getClosest()
        if isinstance(closest, dict):
            self.EndScenario("draw", self.players)
        else:
            self.EndScenario("win", closest)

    def EndScenario(self, type: str, players):
        if type == "win":
            add_msg = ""
            mult = 1
            if self.hasBlackjack(players):
                add_msg = " With a Blackjack!"
                if players.type == "player":
                    mult = 1.5
            self.money["player"] += int(self.mise * mult) + self.mise if players.type == "player" else 0
            messagebox.showinfo("Winner", f"Player {players.name} won!{add_msg}!")
            Debug.out(f"Player {str(players)} won!")
            if self.money['player'] == 0:
                Debug.out(f"Player {self.players['player'].name} has no more money!")
                if messagebox.askyesno("You're poor!", "You are out of money... \n Restart?"):
                    self.w.destroy()
                    Launcher(base_name=self.playerName)
                else:
                    self.exit_game()

        else:
            p1 = players[list(players.keys())[0]]
            p2 = players[list(players.keys())[1]]
            self.money["player"] += self.mise
            messagebox.showinfo("Draw", f"Players {str(p1.name)} and {str(p2.name)} have draw!")
            Debug.out(f"Players {str(p1.name)} and {str(p2.name)} have draw!")

    def exit_game(self):
        Debug.out("User Exit")
        self.w.destroy()
        system.exit('User cancelation')

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        menubar.add_command(label="Restart Game", command=lambda: [self.w.destroy(), Launcher()])
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])


class Launcher:

    def __init__(self, base_name=""):
        self.base_name = base_name
        self.w = tk.Tk()
        self.w.title("BlackJack")
        customFont = ft.Font(family='Source Sans Pro Black', size=17)

        # self.game_type = tk.Frame(self.w, borderwidth=6, relief="solid")
        # self.type = tk.StringVar()
        # self.type.set('american')
        # tk.Label(self.game_type, text='--Game Type--', font=customFont).pack(anchor='n', padx=30)
        # radio1 = tk.Radiobutton(self.game_type, text='American', font=customFont, variable=self.type,
        #                         value='american')
        # radio1.pack(anchor='nw', padx=30)
        # radio2 = tk.Radiobutton(self.game_type, text='European', font=customFont, variable=self.type,
        #                         value='european')
        # radio2.pack(anchor='nw', padx=30)
        #
        # self.game_type.grid(row=1, column=1)

        tk.Label(self.w, text="Choose the number of decks to be used:", font=customFont).pack(anchor="nw")
        self.deckNumber = tk.Spinbox(self.w, from_=1, to=10, increment=1, font=customFont)
        self.deckNumber.pack(anchor="nw", fill="both")
        tk.Label(self.w, text="Choose your starting money:", font=customFont).pack(anchor="nw")
        mDefaultVal = tk.StringVar()
        mDefaultVal.set("150")
        self.startMoneySpin = tk.Spinbox(self.w, from_=50, to=100_000_000, textvariable=mDefaultVal, increment=50, font=customFont)
        self.startMoneySpin.pack(anchor="nw", fill="both")
        tk.Button(self.w, text="Confirm", command=self._instantiate, font=customFont).pack(anchor="n", fill="both")

        Constants.center(self.w)

        self.w.mainloop()

    def _instantiate(self):
        try:
            deckNum = round(float(self.deckNumber.get()))
            moneyAmount = round(float(self.startMoneySpin.get()))
        except ValueError or TypeError:
            return
        self.w.destroy()
        Game(nombreDePaquets=deckNum, start_money=moneyAmount, player_name=self.base_name)


if __name__ == '__main__':
    Launcher()
