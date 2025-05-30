import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.funcaoUtil import exibir_texto_centralizado
import json
import math

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Iron Man do Marcão")
icone  = pygame.image.load("recursos/assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
craqueNeto = pygame.image.load("recursos/assets/craqueNeto.png").convert_alpha()
craqueNeto = pygame.transform.scale(craqueNeto, (112, 278))
fundoStart = pygame.image.load("recursos/assets/fundoStart.jpg")
fundoStart = pygame.transform.scale(fundoStart, (1000, 700))
fundoJogo = pygame.image.load("recursos/assets/fundoJogo.jpg")
fundoJogo = pygame.transform.scale(fundoJogo, (1000, 700))
fundoDead = pygame.image.load("recursos/assets/fundoDead.jpg")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
fundoBoasVindas = pygame.image.load("recursos/assets/fundoBoasVindas.jpg")
fundoBoasVindas = pygame.transform.scale(fundoBoasVindas, (1000, 700))
missel = pygame.image.load("recursos/assets/missile.png").convert_alpha()
missileSound = pygame.mixer.Sound("recursos/assets/missile.wav")
explosaoSound = pygame.mixer.Sound("recursos/assets/explosao.wav")
fonteMenu = pygame.font.Font("recursos/assets/Pixellari.ttf",18)
fonteMorte = pygame.font.Font("recursos/assets/Pixellari.ttf",120)
pygame.mixer.music.load("recursos/assets/ironsound.mp3")
botaoIniciar = pygame.image.load("recursos/assets/botaoIniciar.png").convert_alpha()
botaoIniciar = pygame.transform.scale(botaoIniciar, (100,68))
botaoSair = pygame.image.load("recursos/assets/botaoSair.png").convert_alpha()
botaoSair = pygame.transform.scale(botaoSair, (100,68))
botaoStart = pygame.image.load("recursos/assets/botaoStart.png").convert_alpha()
botaoStart = pygame.transform.scale(botaoStart, (100,68))
objetos_queda_imgs = [
    pygame.image.load("recursos/assets/cabeloDeBoneca.png").convert_alpha(),
    pygame.image.load("recursos/assets/cassio.png").convert_alpha(),
    pygame.image.load("recursos/assets/corinthians.png").convert_alpha(),
    pygame.image.load("recursos/assets/estudo.png").convert_alpha(),
    pygame.image.load("recursos/assets/palmeiras.png").convert_alpha(),
    pygame.image.load("recursos/assets/pao.png").convert_alpha(),
    pygame.image.load("recursos/assets/rato.png").convert_alpha(),
    pygame.image.load("recursos/assets/souza.png").convert_alpha(),
    pygame.image.load("recursos/assets/televisao.png").convert_alpha()
]
objetos_queda_imgs = [pygame.transform.scale(img, (80, 80)) for img in objetos_queda_imgs]

#Função da tela de boas vindas
def boas_vindas(nome):
    mostrando = True
    clicando = False

    x_botao, y_botao = 450, 400
    largura, altura = 100, 68
    rect_botao = pygame.Rect(x_botao, y_botao, largura, altura)

    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_botao.collidepoint(evento.pos):
                    clicando = True
            elif evento.type == pygame.MOUSEBUTTONUP:
                if clicando and rect_botao.collidepoint(evento.pos):
                    mostrando = False
                clicando = False

        tela.fill(preto)
        tela.blit(fundoBoasVindas, (0, 0))

        explicacao1 = fonteMenu.render("Você deve desviar dos mísseis que caem do céu.", True, branco)
        explicacao2 = fonteMenu.render("Use as setas do teclado para se mover.", True, branco)
        explicacao3 = fonteMenu.render("Tente alcançar a maior pontuação possível!", True, branco)

        tela.blit(explicacao1, (100, 280))
        tela.blit(explicacao2, (100, 310))
        tela.blit(explicacao3, (100, 340))

        if clicando:
            botao_menor = pygame.transform.scale(botaoStart, (int(largura * 0.95), int(altura * 0.95)))
            tela.blit(botao_menor, (x_botao + 2.5, y_botao + 2.5))
        else:
            tela.blit(botaoStart, (x_botao, y_botao))

        pygame.display.update()
        relogio.tick(60)

class ObjetoQueCai:
    def __init__(self, velocidade=1):
        self.imagem = random.choice(objetos_queda_imgs)
        self.x = random.randint(0, 950)
        self.y = -80
        self.velocidade = velocidade  # Agora controlada externamente

    def mover(self):
        self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    def colidiu_com(self, px, py, largura, altura):
        return (
            self.x < px + largura and
            self.x + 80 > px and
            self.y < py + altura and
            self.y + 80 > py
        )


def jogar():
    largura_janela = 300
    altura_janela = 80

    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    root.mainloop()

    boas_vindas(nome)

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)

    pontos = 0
    pausado = False
    larguraPersona = 112
    alturaPersona = 278

    # Cria o primeiro objeto com velocidade inicial
    objeto = ObjetoQueCai(velocidade=1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                if not pausado:
                    if evento.key == pygame.K_RIGHT:
                        movimentoXPersona = 15
                    elif evento.key == pygame.K_LEFT:
                        movimentoXPersona = -15
                    elif evento.key == pygame.K_UP:
                        movimentoYPersona = -15
                    elif evento.key == pygame.K_DOWN:
                        movimentoYPersona = 15
            elif evento.type == pygame.KEYUP:
                if not pausado:
                    if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                        movimentoXPersona = 0
                    elif evento.key in [pygame.K_UP, pygame.K_DOWN]:
                        movimentoYPersona = 0

        if pausado:
            exibir_texto_centralizado(tela, "PAUSE", fonteMorte, branco, 1000, 700)
            pygame.display.update()
            relogio.tick(60)
            continue

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > (1000 - larguraPersona):
            posicaoXPersona = 1000 - larguraPersona

        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > (700 - alturaPersona):
            posicaoYPersona = 700 - alturaPersona

        tela.fill(branco)
        tela.blit(fundoJogo, (0, 0))
        tela.blit(craqueNeto, (posicaoXPersona, posicaoYPersona))

        # Atualiza e desenha o objeto atual
        objeto.mover()
        objeto.desenhar(tela)

        # Se o objeto saiu da tela
        if objeto.y > 700:
            pontos += 1
            velocidade_nova = min(1 + int(math.sqrt(pontos)), 10)
            objeto = ObjetoQueCai(velocidade=velocidade_nova)
            pygame.mixer.Sound.play(missileSound)

        # Verifica colisão
        if objeto.colidiu_com(posicaoXPersona, posicaoYPersona, larguraPersona, alturaPersona):
            escreverDados(nome, pontos)
            dead(nome, pontos)
            return

        textoPressPause = fonteMenu.render("Press 'Space' to pause the game", True, branco)
        tela.blit(textoPressPause, (15, 35))
        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (15, 15))

        pygame.display.update()
        relogio.tick(60)



def start():
    x_start, y_start = 450, 440
    x_quit, y_quit = 450, 525
    largura, altura = 100, 68

    rect_start = pygame.Rect(x_start, y_start, largura, altura)
    rect_quit = pygame.Rect(x_quit, y_quit, largura, altura)

    clicando_start = False
    clicando_quit = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_start.collidepoint(evento.pos):
                    clicando_start = True
                elif rect_quit.collidepoint(evento.pos):
                    clicando_quit = True

            elif evento.type == pygame.MOUSEBUTTONUP:
                if clicando_start and rect_start.collidepoint(evento.pos):
                    jogar()
                elif clicando_quit and rect_quit.collidepoint(evento.pos):
                    quit()
                clicando_start = False
                clicando_quit = False

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        if clicando_start:
            botao_menor = pygame.transform.scale(botaoStart, (int(largura * 0.95), int(altura * 0.95)))
            tela.blit(botao_menor, (x_start + 2.5, y_start + 2.5))  
        else:
            tela.blit(botaoStart, (x_start, y_start))

        if clicando_quit:
            botao_menor = pygame.transform.scale(botaoSair, (int(largura * 0.95), int(altura * 0.95)))
            tela.blit(botao_menor, (x_quit + 2.5, y_quit + 2.5))  
        else:
            tela.blit(botaoSair, (x_quit, y_quit))

        pygame.display.update()
        relogio.tick(60)


def ler_ultimos_registros(caminho_arquivo="dados.json", quantidade=5):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            # Pega os últimos 'quantidade' registros
            return dados[-quantidade:]
    except (FileNotFoundError, json.JSONDecodeError):
        # Caso o arquivo não exista ou esteja vazio/corrompido
        return []

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    with open("log.dat", "r") as arquivo:
        log_partidas = json.load(arquivo)
    
    data = log_partidas[nome][1]
    hora = log_partidas[nome][2]

    fonte_grande = pygame.font.SysFont("Arial", 64)
    fonte_media = pygame.font.SysFont("Arial", 20)
    fonte_pequena = pygame.font.SysFont("Arial", 28)
    
    ultimos_logs = list(log_partidas.items())[-5:]
    
    dead_screen = True
    while dead_screen:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    dead_screen = False  # Sai da tela de morte e volta para start() / jogar()

        tela.fill(preto)
        tela.blit(fundoDead, (0,0))
        
        exibir_texto_centralizado(tela, f"Nome: {nome}", fonteMenu, branco, 1000, 380)
        exibir_texto_centralizado(tela, f"Pontos: {pontos}", fonteMenu, branco, 1000, 430)
        exibir_texto_centralizado(tela, "Pressione ENTER para jogar novamente", fonteMenu , branco, 1000, 860)
        
        
        y_base = 480
        tela.blit(fonteMenu.render("Últimos 5 registros:", True, (255, 0, 0)), (50, y_base))
        for i, (nick, dados) in enumerate(ultimos_logs):
            pontos_registro, data_registro, hora_registro = dados
            texto_log = f"{nick} - {pontos_registro} pts em {data_registro} às {hora_registro}"
            texto_render = fonteMenu.render(texto_log, True, (255, 255, 255))
            tela.blit(texto_render, (50, y_base + 30 + i * 30))

        pygame.display.update()
        relogio.tick(60)


if __name__ == "__main__":
    start()


