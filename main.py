import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.funcaoUtil import exibir_texto_centralizado
import json

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
craqueNeto = pygame.image.load("recursos/assets/craqueNeto.png")
craqueNeto = pygame.transform.scale(craqueNeto, (256, 384))
fundoStart = pygame.image.load("recursos/assets/fundoStart.jpg")
fundoStart = pygame.transform.scale(fundoStart, (1000, 700))
fundoJogo = pygame.image.load("recursos/assets/fundoJogo.jpg")
fundoJogo = pygame.transform.scale(fundoJogo, (1000, 700))
fundoDead = pygame.image.load("recursos/assets/fundoDead.jpg")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
fundoBoasVindas = pygame.image.load("recursos/assets/fundoBoasVindas.jpg")
fundoBoasVindas = pygame.transform.scale(fundoBoasVindas, (1000, 700))
missel = pygame.image.load("recursos/assets/missile.png")
missileSound = pygame.mixer.Sound("recursos/assets/missile.wav")
explosaoSound = pygame.mixer.Sound("recursos/assets/explosao.wav")
fonteMenu = pygame.font.Font("recursos/assets/Pixellari.ttf",18)
fonteMorte = pygame.font.Font("recursos/assets/Pixellari.ttf",120)
pygame.mixer.music.load("recursos/assets/ironsound.mp3")

#Função da tela de boas vindas
def boas_vindas(nome):
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    mostrando = False

        tela.fill(preto)
        tela.blit(fundoBoasVindas, (0,0))

        explicacao1 = fonteMenu.render("Você deve desviar dos mísseis que caem do céu.", True, branco)
        explicacao2 = fonteMenu.render("Use as setas do teclado para se mover.", True, branco)
        explicacao3 = fonteMenu.render("Tente alcançar a maior pontuação possível!", True, branco)

        tela.blit(explicacao1, (100, 280))
        tela.blit(explicacao2, (100, 310))
        tela.blit(explicacao3, (100, 340))

        botao_jogar = pygame.draw.rect(tela, branco, (350, 400, 300, 50), border_radius=15)
        texto_botao = fonteMenu.render("Começar o Jogo", True, preto)
        tela.blit(texto_botao, (450, 415))

        pygame.display.update()
        relogio.tick(60)

def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida

    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    # Inicia o loop da interface gráfica
    root.mainloop()

    boas_vindas(nome)
    

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    pausado = False
    larguraPersona = 250
    alturaPersona = 127
    larguaMissel  = 50
    alturaMissel  = 250
    dificuldade  = 30
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado  # Alterna entre pausado e não pausado

                if not pausado:  # Só permite movimento se não estiver pausado
                    if evento.key == pygame.K_RIGHT:
                        movimentoXPersona = 15
                    elif evento.key == pygame.K_LEFT:
                        movimentoXPersona = -15
                    elif evento.key == pygame.K_UP:
                        movimentoYPersona = -15
                    elif evento.key == pygame.K_DOWN:
                        movimentoYPersona = 15

            elif evento.type == pygame.KEYUP:
                if not pausado:  # Impede travamento de movimento durante o pause
                    if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                        movimentoXPersona = 0
                    elif evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                        movimentoYPersona = 0

        if pausado:
            exibir_texto_centralizado(tela, "PAUSE", fonteMorte, branco, 1000, 700)
            pygame.display.update()
            relogio.tick(60)
            continue

                
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 15
        elif posicaoXPersona >750:
            posicaoXPersona = 740
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 15
        elif posicaoYPersona > 573:
            posicaoYPersona = 563
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( craqueNeto, (posicaoXPersona, posicaoYPersona) )
        
        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,800)
            pygame.mixer.Sound.play(missileSound)
            
            
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        
        textoPressPause = fonteMenu.render("Press 'Space' to pause the game", True, branco)
        tela.blit(textoPressPause, (15,35))
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        
        os.system("cls")
        # print( len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead(nome, pontos)
                return
            
       
        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,20))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,70))
        
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
        exibir_texto_centralizado(tela, "Pressione ENTER para jogar novamente", fonteMenu , branco, 1000, 516)
        
        
        y_base = 480
        tela.blit(fonte_pequena.render("Últimos 5 registros:", True, (255, 255, 0)), (50, y_base))
        for i, (nick, dados) in enumerate(ultimos_logs):
            pontos_registro, data_registro, hora_registro = dados
            texto_log = f"{nick} - {pontos_registro} pts em {data_registro} às {hora_registro}"
            texto_render = fonte_media.render(texto_log, True, (255, 255, 255))
            tela.blit(texto_render, (50, y_base + 30 + i * 30))

        pygame.display.update()
        relogio.tick(60)


if __name__ == "__main__":
    start()


