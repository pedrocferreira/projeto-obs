import tkinter as tk
from tkinter import messagebox
import os


class BeachTennisGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.player1_games = 0
        self.player2_games = 0
        self.player1_points = "0"
        self.player2_points = "0"
        self.current_server = 1  # Assume player 1 starts serving
        self.update_score_files()
        self.update_server_file()

    def update_server_image(self):
        # Alternar entre saque.png e saque2.png
        if os.path.exists("saque.png"):
            os.rename("saque.png", "saque2.png")
        elif os.path.exists("saque2.png"):
            os.rename("saque2.png", "saque.png")

    def increment_point(self, player):
        if player == 1:
            self.player1_points = self.next_point(self.player1_points)
            if self.player1_points == "game":
                self.player1_games += 1
                self.player1_points, self.player2_points = "0", "0"
        else:
            self.player2_points = self.next_point(self.player2_points)
            if self.player2_points == "game":
                self.player2_games += 1
                self.player1_points, self.player2_points = "0", "0"

        self.update_score_files()
        if self.player1_games == 6 or self.player2_games == 6:
            return True
        return False

    def switch_server(self):
        if self.current_server == 1:
            self.current_server = 2
        else:
            self.current_server = 1
        self.update_server_file()
        self.update_server_image()

    def next_point(self, current_point):
        points_order = ["0", "15", "30", "40", "game"]
        return points_order[points_order.index(current_point) + 1]

    def update_score_files(self):
        print("Atualizando arquivos de pontuação...")
        try:
            with open("player1_score.txt", "w") as file1, open("player2_score.txt", "w") as file2:
                file1.write(f"{self.player1_games} {self.player1_points}\n")
                file2.write(f"{self.player2_games} {self.player2_points}\n")
            print("Arquivos de pontuação atualizados com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar arquivos de pontuação: {e}")

    def update_server_file(self):
        # Reset both files
        open("server1.txt", "w", encoding="utf-8").close()
        open("server2.txt", "w", encoding="utf-8").close()

        # Update the file of the current server
        if self.current_server == 1:
            with open("server1.txt", "w", encoding="utf-8") as file1:
                file1.write("🟡")
        else:
            with open("server2.txt", "w", encoding="utf-8") as file2:
                file2.write("🟡")


def setup_initial_window():
    initial_window = tk.Tk()
    initial_window.title("Definição dos Jogadores")

    game = BeachTennisGame()

    tk.Label(initial_window, text="Nome Jogador 1").pack()
    player1_name_entry = tk.Entry(initial_window)
    player1_name_entry.pack()

    tk.Label(initial_window, text="Nome Jogador 2").pack()
    player2_name_entry = tk.Entry(initial_window)
    player2_name_entry.pack()

    def open_score_window():
        with open("player1_name.txt", "w") as file1, open("player2_name.txt", "w") as file2:
            file1.write(f"{player1_name_entry.get()}\n")
            file2.write(f"{player2_name_entry.get()}\n")

        score_window = tk.Toplevel()
        score_window.title("Atualização de Pontos")

        def update_score(player):
            game_ended = game.increment_point(player)
            if game_ended:
                winner = "Jogador 1" if game.player1_games == 6 else "Jogador 2"
                messagebox.showinfo("Fim do Jogo", f"Vencedor: {winner}")
                score_window.destroy()
                initial_window.deiconify()
                game.reset_game()

        tk.Button(score_window, text="Pontuação Jogador 1", command=lambda: update_score(1)).pack()
        tk.Button(score_window, text="Pontuação Jogador 2", command=lambda: update_score(2)).pack()
        tk.Button(score_window, text="Trocar Sacador", command=game.switch_server).pack()

        initial_window.withdraw()

    tk.Button(initial_window, text="Iniciar Jogo", command=open_score_window).pack()

    initial_window.mainloop()


if __name__ == "__main__":
    setup_initial_window()
