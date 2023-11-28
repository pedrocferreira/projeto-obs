from tkinter import *
from tkinter import ttk
import time

# Configurações de Estilo
# Configurações de Estilo
COR_FUNDO = "#1C1C1C"
COR_FUNDO_TIME = "#800080"
COR_FUNDO_PONTOS = "#993399"
COR_TEXTO = "#FFFFFF"
FONT_NOME = ("Arial", 14, "bold")
FONT_PLACAR = ("Arial", 24, "bold")
FONT_CRONOMETRO = ("Arial", 20, "bold")

# Variáveis globais
pontos = {'home': 0, 'away': 0}
games = {'home': 0, 'away': 0}
nomes = {'home': "", 'away': ""}
pontos_tenis = [0, 15, 30, 40, "Game"]

# Variáveis do cronômetro
cronometro_ativo = False
tempo_inicial = 0
sacando = 'home'

def resetar_placar():
    global pontos, games, cronometro_ativo, tempo_inicial
    pontos = {'home': 0, 'away': 0}
    games = {'home': 0, 'away': 0}
    cronometro_ativo = False
    tempo_inicial = 0
    label_cronometro.config(text="00:00:00")
    atualizar_pontuacao()  # Atualiza o placar
def alternar_saque():
    global sacando
    sacando = 'away' if sacando == 'home' else 'home'
    atualizar_pontuacao()
# Função para atualizar o placar
def atualizar_pontuacao():
    global cronometro_ativo
    if games['home'] < 6 and games['away'] < 6:
        pontuacao_home = pontos_tenis[pontos['home']]
        pontuacao_away = pontos_tenis[pontos['away']]

        if pontos['home'] > 3 and pontos['away'] > 3:
            if pontos['home'] == pontos['away']:
                pontuacao_home = pontuacao_away = "Deuce"
            elif pontos['home'] == pontos['away'] + 1:
                pontuacao_home = "Vantagem"
            elif pontos['away'] == pontos['home'] + 1:
                pontuacao_away = "Vantagem"

        # Adiciona a indicação de saque ao placar
        indicador_saque_home = " •" if sacando == 'home' else ""
        indicador_saque_away = " •" if sacando == 'away' else ""

        label_games_home.config(text=f"Games: {games['home']}")
        label_pontos_home.config(text=f"{pontuacao_home}{indicador_saque_home}")

        label_games_away.config(text=f"Games: {games['away']}")
        label_pontos_away.config(text=f"{pontuacao_away}{indicador_saque_away}")
    else:
        vencedor = 'home' if games['home'] == 6 else 'away'
        if vencedor == 'home':
            label_games_home.config(text="Vencedor")
            label_pontos_home.config(text=nomes['home'])
            label_games_away.config(text="")
            label_pontos_away.config(text="")
        else:
            label_games_away.config(text="Vencedor")
            label_pontos_away.config(text=nomes['away'])
            label_games_home.config(text="")
            label_pontos_home.config(text="")

# Função para adicionar ponto
def adicionar_ponto(time):
    if games['home'] < 6 and games['away'] < 6:
        pontos[time] += 1
        if pontos[time] > 4:
            pontos[time] = 0
            games[time] += 1

        atualizar_pontuacao()

# Função para atualizar nomes e iniciar o cronômetro
def atualizar_nomes_e_iniciar():
    global cronometro_ativo, tempo_inicial
    nomes['home'] = entry_nome_home.get()
    nomes['away'] = entry_nome_away.get()
    if not cronometro_ativo:
        cronometro_ativo = True
        tempo_inicial = time.time()
        atualizar_cronometro()
    atualizar_pontuacao()

# Função para atualizar o cronômetro
def atualizar_cronometro():
    if cronometro_ativo:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        horas = int(tempo_decorrido // 3600)
        minutos = int((tempo_decorrido % 3600) // 60)
        segundos = int(tempo_decorrido % 60)
        label_cronometro.config(text=f"{horas:02d}:{minutos:02d}:{segundos:02d}")
        label_cronometro.after(1000, atualizar_cronometro)

# Criação da janela do placar
def criar_janela_placar():
    janela_placar = Tk()
    janela_placar.title("Beach Tennis Scoreboard")

    # Define as cores e estilos dos labels
    janela_placar.configure(bg='green')  # A cor de fundo deve ser a mesma em todos os widgets para alinhamento visual
    estilo = ttk.Style()
    estilo.configure("TLabel", background='green', foreground='white', font=('Arial', 12))
    estilo.configure("TEntry", font=('Arial', 12))
    estilo.configure("TButton", font=('Arial', 12))

    # Organização dos labels e entries com o gerenciador de layout 'grid'
    ttk.Label(janela_placar, text="Jogador Casa", style="TLabel").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    label_nome_home = ttk.Label(janela_placar, style="TLabel", width=20)
    label_nome_home.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(janela_placar, text="Jogador Visitante", style="TLabel").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    label_nome_away = ttk.Label(janela_placar, style="TLabel", width=20)
    label_nome_away.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # ... (adicionar outros labels e widgets conforme necessário)

    # Configuração de redimensionamento
    janela_placar.grid_columnconfigure(0, weight=1)
    janela_placar.grid_columnconfigure(1, weight=1)
    for i in range(4):  # Ajuste o alcance de acordo com o número de linhas que você tem
        janela_placar.grid_rowconfigure(i, weight=1)

    return janela_placar

# Criação da janela de controle
def criar_janela_controle():
    janela_controle = Tk()
    janela_controle.title("Controles do Placar")
    janela_controle.configure(bg=COR_FUNDO)

    # Criação de Labels para identificar os campos
    label_nome_home = Label(janela_controle, text="Nome Jogador Casa:", font=FONT_NOME, fg=COR_TEXTO, bg=COR_FUNDO)
    label_nome_home.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    global entry_nome_home
    entry_nome_home = ttk.Entry(janela_controle, font=FONT_NOME)
    entry_nome_home.insert(0, nomes['home'])
    entry_nome_home.grid(row=0, column=1, sticky="ew", padx=10)

    label_nome_away = Label(janela_controle, text="Nome Jogador Visitante:", font=FONT_NOME, fg=COR_TEXTO, bg=COR_FUNDO)
    label_nome_away.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    global entry_nome_away
    entry_nome_away = ttk.Entry(janela_controle, font=FONT_NOME)
    entry_nome_away.insert(0, nomes['away'])
    entry_nome_away.grid(row=1, column=1, sticky="ew", padx=10)

    # Botão para atualizar os nomes e iniciar o jogo
    botao_iniciar_jogo = ttk.Button(janela_controle, text="Iniciar Jogo", command=atualizar_nomes_e_iniciar)
    botao_iniciar_jogo.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

    # Botões para adicionar pontos
    botao_ponto_home = ttk.Button(janela_controle, text="Ponto para Casa", command=lambda: adicionar_ponto('home'))
    botao_ponto_home.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

    botao_ponto_away = ttk.Button(janela_controle, text="Ponto para Visitante", command=lambda: adicionar_ponto('away'))
    botao_ponto_away.grid(row=3, column=1, pady=5, padx=10, sticky="ew")

    # Botão para alternar o saque
    botao_alternar_saque = ttk.Button(janela_controle, text="Alternar Saque", command=alternar_saque)
    botao_alternar_saque.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

    # Configurações para que os widgets se expandam com a janela
    janela_controle.grid_columnconfigure(1, weight=1)

    return janela_controle

# Inicialização das janelas
janela_placar = criar_janela_placar()
janela_controle = criar_janela_controle()

# Executar ambas as janelas
janela_placar.mainloop()
janela_controle.mainloop()
