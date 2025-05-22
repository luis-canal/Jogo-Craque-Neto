def exibir_texto_centralizado(tela, texto, fonte, cor, largura_tela, altura_tela):
    renderizado = fonte.render(texto, True, cor)
    ret_texto = renderizado.get_rect(center=(largura_tela // 2, altura_tela // 2))
    tela.blit(renderizado, ret_texto)
