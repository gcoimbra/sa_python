import matplotlib.pyplot as plt
import numpy as np
import os, math, random
from PIL import Image, ImageFont, ImageDraw

def funcaoX2(x):
    return x**2 # Ou pow(x, 2)

def funcaoEggholder(x, y):
    resultado = -((y+47) * math.sin(math.sqrt(abs((x/2)+(y+47))))) - (x*math.sin(math.sqrt(abs(x-(y+47)))))
    return resultado

def funcaoParedaoEspinhento(x,y):
    return -0.0001*(abs(math.sin(x)*math.sin(y)*math.exp(abs(100 - math.sqrt(x**2 + y**2)/math.pi)))+1)**0.1

def criterioMetropolis(solucaoNova, solucaoAnterior, parametroControle):
    if solucaoNova <= solucaoAnterior:
        return 1
    else:
        return math.exp((solucaoAnterior - solucaoNova) / parametroControle)

def geraRandomicoMetropolis():
    return (0.99999 - ((0.99999 - 0) * random.random())) # - 0 é só simbólico

def geraPerturbacaoX(i, xMinimo, xMaximo, yMinimo, yMaximo):

    limiteTentativas = 10
    while(limiteTentativas > 0):
        valorPerturbacaoX = np.random.uniform(-0.1, 0.1)
        if(verificaIntervaloXY(i[0] + valorPerturbacaoX, i[1], xMinimo, xMaximo, yMinimo, yMaximo)):
            break
        limiteTentativas -= 1
    
    # Significa que não encontrou nenhuma solução para esse intervalo, logo retorna 0 para contribuir para o critério de parada
    if(limiteTentativas == 0):
        return 0

    return valorPerturbacaoX

def geraPerturbacaoY(i, xMinimo, xMaximo, yMinimo, yMaximo):

    limiteTentativas = 10
    while(limiteTentativas > 0):
        valorPerturbacaoY = np.random.uniform(-0.1, 0.1)
        if(verificaIntervaloXY(i[0], i[1] + valorPerturbacaoY, xMinimo, xMaximo, yMinimo, yMaximo)):
            break
        limiteTentativas -= 1
    
    # Significa que não encontrou nenhuma solução para esse intervalo, logo retorna 0 para contribuir para o critério de parada
    if(limiteTentativas == 0):
        return 0

    return valorPerturbacaoY

def truncar(valor, qtdCasas):
    valorTruncado = str(valor).split(".")
    valorTruncado = valorTruncado[0] + "." + valorTruncado[1][:qtdCasas]
    return valorTruncado

def verificaIntervaloX(x, xMinimo, xMaximo):
    if(x >= xMinimo and x <= xMaximo):
        return True
    return False

def verificaIntervaloXY(x, y, xMinimo, xMaximo, yMinimo, yMaximo):
    if((x >= xMinimo and x <= xMaximo) and (y >= yMinimo and y <= yMaximo)):
        return True
    return False

def escreverNaImagem(draw, posicaoX, posicaoY, texto, cor, fonte):
    draw.text((posicaoX, posicaoY), texto, cor, font=fonte)

def gerarAnaliseIndividual(listaXAnaliseIndividual, listaYAnaliseIndividual, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoes, tempoExecucao, tituloGrafico, eixoX, eixoY, nomeFuncao, diretorio):
    
    # Transformando lista em array Numpy
    np_listaX = np.array(listaXAnaliseIndividual)
    np_listaY = np.array(listaYAnaliseIndividual)
    
    # Criando um gráfico
    plt.plot(np_listaX, np_listaY)
    
    # Atribuindo um título ao gráfico
    plt.title(tituloGrafico)
    plt.xlabel(eixoX)
    plt.ylabel(eixoY)

    lista_cores = ['#ebc634']

    if(len(np_listaX) > 1):
        for index in range(len(np_listaX) - 2):
            lista_cores.append('#346eeb')
        lista_cores.append('#eb4034')

    # Atribuindo uma legenda
    plt.scatter(np_listaX, np_listaY, label='Solução inicial', color=lista_cores)
    plt.legend()

    plt.savefig(diretorio + "/" + nomeFuncao + "_%s.png" % (i+1))
    plt.clf()

    ladoAdiocionarTexto = 85
    try:
        if((listaXAnaliseIndividual[0] < listaXAnaliseIndividual[-1]) and (listaYAnaliseIndividual[0] > listaYAnaliseIndividual[-1])):
            ladoAdiocionarTexto = 380
    except:
        pass

    img = Image.open(diretorio + "/" + nomeFuncao + "_%s.png" % (i+1))
    draw = ImageDraw.Draw(img)

    # Para adicionar fontes: "/usr/share/fonts/truetype/freefont/arial.ttf"
    fontTitulo = ImageFont.truetype("FreeSans.ttf", 12, encoding="unic")
    corTitulo = (0, 127, 0)

    escreverNaImagem(draw, ladoAdiocionarTexto, 100, "Análise de execução:", corTitulo, fontTitulo)

    # Para adicionar fontes: "/usr/share/fonts/truetype/freefont/arial.ttf"
    font = ImageFont.truetype("FreeSans.ttf", 10, encoding="unic")
    cor = (0, 0, 0)

    escreverNaImagem(draw, ladoAdiocionarTexto, 115, valorPartidaStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 130, solucaoValorPartidaStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 145, valorFinalStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 160, solucaoValorFinalStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 175, "Quantidade de iterações: " + str(qtdIteracoes), cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 190, "Tempo de execução: " + str(np.format_float_scientific(np.float32(tempoExecucao), precision=3)) + " seg", cor, font)

    img.save(diretorio + "/" + nomeFuncao + "_%s.png" % (i+1))

def gerarAnaliseIndividualSA(listaXAnaliseIndividual, listaYAnaliseIndividual, i, valorPartidaStr, solucaoValorPartidaStr, melhorXY, melhorXYStr, solucaoMelhorXYStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoes, tempoExecucao, tituloGrafico, eixoX, eixoY, nomeFuncao, diretorio):
    
    # Transformando lista em array Numpy
    np_listaX = np.array(listaXAnaliseIndividual)
    np_listaY = np.array(listaYAnaliseIndividual)
    
    # Criando um gráfico
    plt.plot(np_listaX, np_listaY)
    
    # Atribuindo um título ao gráfico
    plt.title(tituloGrafico)
    plt.xlabel(eixoX)
    plt.ylabel(eixoY)

    lista_cores = ['#ebc634']

    if(len(np_listaX) > 1):

        for index in range(len(np_listaX) - 2):
            lista_cores.append('#346eeb')
        lista_cores.append('#eb4034')

        for indice in range(len(np_listaX)):
            if(np_listaX[indice] == melhorXY[0] and np_listaY[indice] == melhorXY[1]):
                lista_cores[indice] = '#22dd22'
                break

    # Atribuindo uma legenda
    plt.scatter(np_listaX, np_listaY, label='Solução inicial', color=lista_cores)
    plt.legend()

    plt.savefig(diretorio + "/" + nomeFuncao + "_%s.png" % (i+1))
    plt.clf()

    ladoAdiocionarTexto = 85
    try:
        if((listaXAnaliseIndividual[0] < listaXAnaliseIndividual[-1]) and (listaYAnaliseIndividual[0] > listaYAnaliseIndividual[-1])):
            ladoAdiocionarTexto = 380
    except:
        pass

    img = Image.open(diretorio + "/" + nomeFuncao + "_%s.png" % (i+1))
    draw = ImageDraw.Draw(img)

    # Para adicionar fontes: "/usr/share/fonts/truetype/freefont/arial.ttf"
    fontTitulo = ImageFont.truetype("FreeSans.ttf", 12, encoding="unic")
    corTitulo = (0, 127, 0)

    escreverNaImagem(draw, ladoAdiocionarTexto, 100, "Análise de execução:", corTitulo, fontTitulo)

    # Para adicionar fontes: "/usr/share/fonts/truetype/freefont/arial.ttf"
    font = ImageFont.truetype("FreeSans.ttf", 10, encoding="unic")
    cor = (0, 0, 0)

    escreverNaImagem(draw, ladoAdiocionarTexto, 115, valorPartidaStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 130, solucaoValorPartidaStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 145, melhorXYStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 160, solucaoMelhorXYStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 175, valorFinalStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 190, solucaoValorFinalStr, cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 205, "Quantidade de iterações: " + str(qtdIteracoes), cor, font)
    escreverNaImagem(draw, ladoAdiocionarTexto, 220, "Tempo de execução: " + str(np.format_float_scientific(np.float32(tempoExecucao), precision=3)) + " seg", cor, font)

    img.save(diretorio + "/" + nomeFuncao + "_%s.png" % (i+1))

def gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, tituloGrafico, nomeFuncao, diretorio):

    # Transformando lista em array Numpy
    np_listaXAnaliseGeral = np.array(listaQtdIteracoesSolucao)
    np_listaYAnaliseGeral = np.array(listaTempoGasto)
    np_listaZAnaliseGeral = np.array(listaSolucoes)

    # Criando um gráfico
    plt.bar(np_listaXAnaliseGeral, np_listaYAnaliseGeral)
    # plt.xticks(np_listaXAnaliseGeral)

    # Atribuindo um título ao gráfico
    plt.title(tituloGrafico)
    plt.xlabel('Iterações')
    plt.ylabel('Tempo')

    # Exibindo o gráfico gerado
    # plt.show()

    plt.savefig(diretorio + "/analise_" + nomeFuncao + ".png", dpi=300)
    plt.close()

    img = Image.open(diretorio + "/analise_" + nomeFuncao + ".png")
    draw = ImageDraw.Draw(img)

    # Para adicionar fontes: "/usr/share/fonts/truetype/freefont/arial.ttf"
    fontTitulo = ImageFont.truetype("FreeSans.ttf", 30, encoding="unic")
    corTitulo = (0, 127, 0)

    escreverNaImagem(draw, 250, 180, "Análise de execução:", corTitulo, fontTitulo)

    # Para adicionar fontes: "/usr/share/fonts/truetype/freefont/arial.ttf"
    font = ImageFont.truetype("FreeSans.ttf", 26, encoding="unic")
    cor = (0, 0, 0)

    if(np.min(np_listaZAnaliseGeral) >= -1 and np.min(np_listaZAnaliseGeral) <= 1):
        escreverNaImagem(draw, 250, 220, "Menor solução: " + str(np.format_float_scientific(np.float32(np.min(np_listaZAnaliseGeral)), precision=5)), cor, font)
    else:
        escreverNaImagem(draw, 250, 220, "Menor solução: " + str(truncar(np.min(np_listaZAnaliseGeral), 5)), cor, font)
    
    if(np.max(np_listaZAnaliseGeral) >= -1 and np.max(np_listaZAnaliseGeral) <= 1):
        escreverNaImagem(draw, 250, 245, "Maior solução: " + str(np.format_float_scientific(np.float32(np.max(np_listaZAnaliseGeral)), precision=5)), cor, font)
    else:
        escreverNaImagem(draw, 250, 245, "Maior solução: " + str(truncar(np.max(np_listaZAnaliseGeral), 5)), cor, font)
    
    if(np.mean(np_listaZAnaliseGeral) >= -1 and np.mean(np_listaZAnaliseGeral) <= 1):
        escreverNaImagem(draw, 250, 270, "Média das soluções: " + str(np.format_float_scientific(np.float32(np.mean(np_listaZAnaliseGeral)), precision=5)), cor, font)
    else:
        escreverNaImagem(draw, 250, 270, "Média das soluções: " + str(truncar(np.mean(np_listaZAnaliseGeral), 5)), cor, font)
    
    if(np.std(np_listaZAnaliseGeral) >= -1 and np.std(np_listaZAnaliseGeral) <= 1):
        escreverNaImagem(draw, 250, 295, "Desvio padrão das soluções: " + str(np.format_float_scientific(np.float32(np.std(np_listaZAnaliseGeral)), precision=5)), cor, font)
    else:
        escreverNaImagem(draw, 250, 295, "Desvio padrão das soluções: " + str(truncar(np.std(np_listaZAnaliseGeral), 5)), cor, font)

    escreverNaImagem(draw, 250, 345, "Mínimo de iterações: " + str(np.min(np_listaXAnaliseGeral)), cor, font)
    escreverNaImagem(draw, 250, 370, "Máximo de iterações: " + str(np.max(np_listaXAnaliseGeral)), cor, font)
    escreverNaImagem(draw, 250, 395, "Média de iterações: " + str(truncar(np.mean(np_listaXAnaliseGeral), 5)), cor, font)
    escreverNaImagem(draw, 250, 420, "Desvio padrão das iterações: " + str(truncar(np.std(np_listaXAnaliseGeral), 5)), cor, font)

    escreverNaImagem(draw, 250, 470, "Mínimo de tempo: " + str(np.format_float_scientific(np.float32(np.min(np_listaYAnaliseGeral)), precision=3)) + " seg", cor, font)
    escreverNaImagem(draw, 250, 495, "Máximo de tempo: " + str(np.format_float_scientific(np.float32(np.max(np_listaYAnaliseGeral)), precision=3)) + " seg", cor, font)
    escreverNaImagem(draw, 250, 520, "Média de tempo: " + str(np.format_float_scientific(np.float32(np.mean(np_listaYAnaliseGeral)), precision=3)) + " seg", cor, font)
    escreverNaImagem(draw, 250, 545, "Desvio padrão do tempo: " + str(np.format_float_scientific(np.float32(np.std(np_listaYAnaliseGeral)), precision=3)) + " seg", cor, font)

    img.save(diretorio + "/analise_" + nomeFuncao + "_texto.png")

def geraParametroControle(numeroPerturbacoes, intervaloX, intervaloY, funcao):

    xMinimo, xMaximo = intervaloX[0], intervaloX[1]
    yMinimo, yMaximo = intervaloY[0], intervaloY[1]

    lista_solucoes_aleatorias = []

    for i in range(numeroPerturbacoes):
        valorXY = [xMaximo - ((xMaximo - xMinimo) * random.random()), yMaximo - ((yMaximo - yMinimo) * random.random())] # Gerando valores entre [xMinimo,xMaximo] e [yMinimo, yMaximo]
        solucao = funcao(valorXY[0], valorXY[1])
        lista_solucoes_aleatorias.append(solucao)

    lista_variacoes_solucoes = []

    for i in range(0, numeroPerturbacoes-1):
        lista_variacoes_solucoes.append(abs(lista_solucoes_aleatorias[i] - lista_solucoes_aleatorias[i+1]))
    
    media_variacoes_solucoes = np.mean(lista_variacoes_solucoes)

    c0 = -media_variacoes_solucoes / (math.log(0.8)/math.log(math.e))

    return c0

def ajustaParametroControle(ck, alfa):
    return alfa*ck