import random, time, os

import numpy

from funcoes_auxiliares import gerarAnaliseIndividual, gerarAnaliseIndividualSA, gerarAnaliseGeral, funcaoX2, funcaoEggholder, funcaoParedaoEspinhento, np, truncar, verificaIntervaloX, verificaIntervaloXY, geraParametroControle, criterioMetropolis, geraRandomicoMetropolis, ajustaParametroControle, geraPerturbacaoX, geraPerturbacaoY

class MetaHeuristicas:

#    def __init__(self, name, salary):
#         self.name = name
#         self.salary = salary
#         Employee.empCount += 1

    def hillClimbingX2(self, qtdIteracoes, intervaloX, limiteTempo):

        xMinimo, xMaximo = intervaloX[0], intervaloX[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-x2-intervalo-[%d, %d]" % (xMinimo, xMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i in range(qtdIteracoes):

            valorPartida = xMaximo - ((xMaximo - xMinimo) * random.random()) # Gerando valores entre [xMinimo,xMaximo]
            solucao = valorPartida

            qtdIteracoesSolucao = 0
            listaPerturbacao = [10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):

                solucaoAtual = solucao

                listaX.append(solucao)
                listaY.append(funcaoX2(solucao))

                for valorPerturbacao in listaPerturbacao:
                    if((not verificaIntervaloX(solucao + valorPerturbacao, xMinimo, xMaximo)) or (not verificaIntervaloX(solucao - valorPerturbacao, xMinimo, xMaximo))):                        
                        continue
                    if(funcaoX2(solucao + valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao + valorPerturbacao
                        break
                    elif(funcaoX2(solucao - valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao - valorPerturbacao
                        break                    

                qtdIteracoesSolucao += 1
                
                if(solucao == solucaoAtual):
                    break

            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoX2(solucao))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x): " + str(truncar(valorPartida, 5))
            solucaoValorPartidaStr = "Função objetivo inicial f(x²): " + str(truncar(funcaoX2(valorPartida), 5))
            valorFinalStr = "Solução final (x): " + str(np.format_float_scientific(np.float32(solucao), precision=5))
            solucaoValorFinalStr = "Função objetivo final f(x²): " + str(np.format_float_scientific(np.float32(funcaoX2(solucao)), precision=5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de X² usando Hill-Climbing", "Solução", "Resultado", "x2", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de X² usando Hill-Climbing (Análise)", "x2", diretorio)

    def hillClimbingX2PassandoValorPartida(self, intervaloX, listaValoresPartida, limiteTempo):

        xMinimo, xMaximo = intervaloX[0], intervaloX[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-x2-valor-partida-intervalo-[%d, %d]" % (xMinimo, xMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i, valorPartida in enumerate(listaValoresPartida):

            solucao = float(valorPartida)

            qtdIteracoesSolucao = 0
            listaPerturbacao = [10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):

                solucaoAtual = solucao

                listaX.append(solucao)
                listaY.append(funcaoX2(solucao))

                for valorPerturbacao in listaPerturbacao:
                    if((not verificaIntervaloX(solucao + valorPerturbacao, xMinimo, xMaximo)) or (not verificaIntervaloX(solucao - valorPerturbacao, xMinimo, xMaximo))):                        
                        continue
                    if(funcaoX2(solucao + valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao + valorPerturbacao
                        break
                    elif(funcaoX2(solucao - valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao - valorPerturbacao
                        break                    

                qtdIteracoesSolucao += 1
                
                if(solucao == solucaoAtual):
                    break

            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoX2(solucao))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x): " + str(truncar(valorPartida, 5))
            solucaoValorPartidaStr = "Função objetivo inicial f(x²): " + str(truncar(funcaoX2(valorPartida), 5))
            valorFinalStr = "Solução final (x): " + str(np.format_float_scientific(np.float32(solucao), precision=5))
            solucaoValorFinalStr = "Função objetivo final f(x²): " + str(np.format_float_scientific(np.float32(funcaoX2(solucao)), precision=5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de X² usando Hill-Climbing", "Solução", "Resultado", "x2", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de X² usando Hill-Climbing (Análise)", "x2", diretorio)

    def hillClimbingSteepestAscentX2(self, qtdIteracoes, intervaloX, limiteTempo):
        
        xMinimo, xMaximo = intervaloX[0], intervaloX[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-steepest-ascent-x2-intervalo-[%d, %d]" % (xMinimo, xMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i in range(qtdIteracoes):

            valorPartida = xMaximo - ((xMaximo - xMinimo) * random.random()) # Gerando valores entre [xMinimo,xMaximo]
            solucao = valorPartida

            qtdIteracoesSolucao = 0
            listaPerturbacao = [10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):
                
                solucaoAtual = solucao

                listaX.append(solucao)
                listaY.append(funcaoX2(solucao))

                for valorPerturbacao in listaPerturbacao:
                    if((not verificaIntervaloX(solucao + valorPerturbacao, xMinimo, xMaximo)) or (not verificaIntervaloX(solucao - valorPerturbacao, xMinimo, xMaximo))):                        
                        continue
                    if(funcaoX2(solucao + valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao + valorPerturbacao
                    if(funcaoX2(solucao - valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao - valorPerturbacao

                qtdIteracoesSolucao += 1

                if(solucaoAtual == solucao):
                    break

            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoX2(solucao))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x): " + str(truncar(valorPartida, 5))
            solucaoValorPartidaStr = "Função objetivo inicial f(x²): " + str(truncar(funcaoX2(valorPartida), 5))
            valorFinalStr = "Solução final (x): " + str(np.format_float_scientific(np.float32(solucao), precision=5))
            solucaoValorFinalStr = "Função objetivo final f(x²): " + str(np.format_float_scientific(np.float32(funcaoX2(solucao)), precision=5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de X² usando Hill-Climbing", "Solução", "Resultado", "x2", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de X² usando Hill-Climbing Steepest Ascent (Análise)", "x2", diretorio)

    def hillClimbingSteepestAscentX2PassandoValorPartida(self, intervaloX, listaValoresPartida, limiteTempo):

        xMinimo, xMaximo = intervaloX[0], intervaloX[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-steepest-ascent-x2-valor-partida-intervalo-[%d, %d]" % (xMinimo, xMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i, valorPartida in enumerate(listaValoresPartida):

            solucao = float(valorPartida)

            qtdIteracoesSolucao = 0
            listaPerturbacao = [10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):
                
                solucaoAtual = solucao

                listaX.append(solucao)
                listaY.append(funcaoX2(solucao))

                for valorPerturbacao in listaPerturbacao:
                    if((not verificaIntervaloX(solucao + valorPerturbacao, xMinimo, xMaximo)) or (not verificaIntervaloX(solucao - valorPerturbacao, xMinimo, xMaximo))):                        
                        continue
                    if(funcaoX2(solucao + valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao + valorPerturbacao
                    if(funcaoX2(solucao - valorPerturbacao) < funcaoX2(solucao)):
                        solucao = solucao - valorPerturbacao

                qtdIteracoesSolucao += 1

                if(solucaoAtual == solucao):
                    break

            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoX2(solucao))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x): " + str(truncar(valorPartida, 5))
            solucaoValorPartidaStr = "Função objetivo inicial f(x²): " + str(truncar(funcaoX2(valorPartida), 5))
            valorFinalStr = "Solução final (x): " + str(np.format_float_scientific(np.float32(solucao), precision=5))
            solucaoValorFinalStr = "Função objetivo final f(x²): " + str(np.format_float_scientific(np.float32(funcaoX2(solucao)), precision=5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de X² usando Hill-Climbing", "Solução", "Resultado", "x2", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de X² usando Hill-Climbing Steepest Ascent (Análise)", "x2", diretorio)

    def hillClimbingEggholder(self, qtdIteracoes, intervaloX, intervaloY, limiteTempo):

        xMinimo, xMaximo = intervaloX[0], intervaloX[1]
        yMinimo, yMaximo = intervaloY[0], intervaloY[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-eggholder-intervalo-x-[%d, %d]-y-[%d, %d]" % (xMinimo, xMaximo, yMinimo, yMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i in range(qtdIteracoes):

            valorPartida = [xMaximo - ((xMaximo - xMinimo) * random.random()), yMaximo - ((yMaximo - yMinimo) * random.random())] # Gerando valores entre [xMinimo,xMaximo] e [yMinimo, yMaximo]
            solucao = valorPartida[:] # Copiar lista ignorando a referência (cópia real)

            qtdIteracoesSolucao = 0
            listaPerturbacao = [100, 50, 20, 10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):

                solucaoAtual = solucao[:]

                listaX.append(solucao[0])
                listaY.append(solucao[1])

                solucaoEncontrada = False

                for valorPerturbacao in listaPerturbacao:
                    
                    if(verificaIntervaloXY(solucao[0] + valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] + valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] + valorPerturbacao
                            solucaoEncontrada = True
                    
                    if(verificaIntervaloXY(solucao[0] - valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] - valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] - valorPerturbacao
                            solucaoEncontrada = True

                    if(verificaIntervaloXY(solucao[0], solucao[1] + valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] + valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] + valorPerturbacao
                            solucaoEncontrada = True
                    
                    if(verificaIntervaloXY(solucao[0], solucao[1] - valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] - valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] - valorPerturbacao
                            solucaoEncontrada = True

                    if(solucaoEncontrada):
                        break                    

                qtdIteracoesSolucao += 1
                
                if(solucao == solucaoAtual):
                    break
                
            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoEggholder(solucao[0], solucao[1]))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x, y): (" + str(truncar(valorPartida[0], 5)) + ", " + str(truncar(valorPartida[1], 5)) + ")"
            solucaoValorPartidaStr = "Função objetivo inicial f(x, y): " + str(truncar(funcaoEggholder(valorPartida[0], valorPartida[1]), 5))
            valorFinalStr = "Solução final (x, y): (" + str(truncar(solucao[0], 5)) + ", " + str(truncar(solucao[1], 5)) + ")"
            solucaoValorFinalStr = "Função objetivo final f(x, y): " + str(truncar(funcaoEggholder(solucao[0], solucao[1]), 5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de Eggholder usando Hill-Climbing", "X", "Y", "eggholder", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de Eggholder usando Hill-Climbing (Análise)", "eggholder", diretorio)

    def hillClimbingEggholderPassandoValorPartida(self, intervaloX, intervaloY, listaValoresPartida, limiteTempo):
        
        xMinimo, xMaximo = intervaloX[0], intervaloX[1]
        yMinimo, yMaximo = intervaloY[0], intervaloY[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-eggholder-valor-partida-intervalo-x-[%d, %d]-y-[%d, %d]" % (xMinimo, xMaximo, yMinimo, yMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i, valorPartida in enumerate(listaValoresPartida):

            valorPartida = [float(valorPartida[0]), float(valorPartida[1])]
            solucao = valorPartida[:] # Copiar lista ignorando a referência (cópia real)

            qtdIteracoesSolucao = 0
            listaPerturbacao = [100, 50, 20, 10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):

                solucaoAtual = solucao[:]

                listaX.append(solucao[0])
                listaY.append(solucao[1])

                solucaoEncontrada = False

                for valorPerturbacao in listaPerturbacao:
                    
                    if(verificaIntervaloXY(solucao[0] + valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] + valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] + valorPerturbacao
                            solucaoEncontrada = True
                    
                    if(verificaIntervaloXY(solucao[0] - valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] - valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] - valorPerturbacao
                            solucaoEncontrada = True

                    if(verificaIntervaloXY(solucao[0], solucao[1] + valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] + valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] + valorPerturbacao
                            solucaoEncontrada = True
                    
                    if(verificaIntervaloXY(solucao[0], solucao[1] - valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] - valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] - valorPerturbacao
                            solucaoEncontrada = True

                    if(solucaoEncontrada):
                        break                    

                qtdIteracoesSolucao += 1
                
                if(solucao == solucaoAtual):
                    break
                
            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoEggholder(solucao[0], solucao[1]))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x, y): (" + str(truncar(valorPartida[0], 5)) + ", " + str(truncar(valorPartida[1], 5)) + ")"
            solucaoValorPartidaStr = "Função objetivo inicial f(x, y): " + str(truncar(funcaoEggholder(valorPartida[0], valorPartida[1]), 5))
            valorFinalStr = "Solução final (x, y): (" + str(truncar(solucao[0], 5)) + ", " + str(truncar(solucao[1], 5)) + ")"
            solucaoValorFinalStr = "Função objetivo final f(x, y): " + str(truncar(funcaoEggholder(solucao[0], solucao[1]), 5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de Eggholder usando Hill-Climbing", "X", "Y", "eggholder", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de Eggholder usando Hill-Climbing (Análise)", "eggholder", diretorio)

    def hillClimbingSpeedestAscentEggholder(self, qtdIteracoes, intervaloX, intervaloY, limiteTempo):
        
        xMinimo, xMaximo = intervaloX[0], intervaloX[1]
        yMinimo, yMaximo = intervaloY[0], intervaloY[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-speedest-ascent-eggholder-intervalo-x-[%d, %d]-y-[%d, %d]" % (xMinimo, xMaximo, yMinimo, yMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i in range(qtdIteracoes):

            valorPartida = [xMaximo - ((xMaximo - xMinimo) * random.random()), yMaximo - ((yMaximo - yMinimo) * random.random())] # Gerando valores entre [xMinimo,xMaximo] e [yMinimo, yMaximo]
            solucao = valorPartida[:] # Copiar lista ignorando a referência (cópia real)

            qtdIteracoesSolucao = 0
            listaPerturbacao = [100, 50, 20, 10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):
                
                solucaoAtual = solucao[:]

                listaX.append(solucao[0])
                listaY.append(solucao[1])

                for valorPerturbacao in listaPerturbacao:
                    
                    if(verificaIntervaloXY(solucao[0] + valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] + valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] + valorPerturbacao                            
                    
                    if(verificaIntervaloXY(solucao[0] - valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] - valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] - valorPerturbacao                            

                    if(verificaIntervaloXY(solucao[0], solucao[1] + valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] + valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] + valorPerturbacao                            
                    
                    if(verificaIntervaloXY(solucao[0], solucao[1] - valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] - valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] - valorPerturbacao                                               

                qtdIteracoesSolucao += 1
                
                if(solucao == solucaoAtual):
                    break
                
            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoEggholder(solucao[0], solucao[1]))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x, y): (" + str(truncar(valorPartida[0], 5)) + ", " + str(truncar(valorPartida[1], 5)) + ")"
            solucaoValorPartidaStr = "Função objetivo inicial f(x, y): " + str(truncar(funcaoEggholder(valorPartida[0], valorPartida[1]), 5))
            valorFinalStr = "Solução final (x, y): (" + str(truncar(solucao[0], 5)) + ", " + str(truncar(solucao[1], 5)) + ")"
            solucaoValorFinalStr = "Função objetivo final f(x, y): " + str(truncar(funcaoEggholder(solucao[0], solucao[1]), 5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de Eggholder usando Hill-Climbing Speedest Ascent", "X", "Y", "eggholder", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de Eggholder usando Hill-Climbing Speedest Ascent (Análise)", "eggholder", diretorio)

    def hillClimbingSpeedestAscentEggholderPassandoValorPartida(self, intervaloX, intervaloY, listaValoresPartida, limiteTempo):

        xMinimo, xMaximo = intervaloX[0], intervaloX[1]
        yMinimo, yMaximo = intervaloY[0], intervaloY[1]

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/hill-climbing-speedest-ascent-eggholder-valor-partida-intervalo-x-[%d, %d]-y-[%d, %d]" % (xMinimo, xMaximo, yMinimo, yMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for i, valorPartida in enumerate(listaValoresPartida):

            valorPartida = [float(valorPartida[0]), float(valorPartida[1])]
            solucao = valorPartida[:] # Copiar lista ignorando a referência (cópia real)

            qtdIteracoesSolucao = 0
            listaPerturbacao = [100, 50, 20, 10, 7.5, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001]
            listaX = []; listaY = []

            tempoInicial = time.time()

            while((time.time()-tempoInicial) < limiteTempo):

                solucaoAtual = solucao[:]

                listaX.append(solucao[0])
                listaY.append(solucao[1])

                for valorPerturbacao in listaPerturbacao:
                    
                    if(verificaIntervaloXY(solucao[0] + valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] + valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] + valorPerturbacao                            
                    
                    if(verificaIntervaloXY(solucao[0] - valorPerturbacao, solucao[1], xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0] - valorPerturbacao, solucao[1]) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[0] = solucao[0] - valorPerturbacao                            

                    if(verificaIntervaloXY(solucao[0], solucao[1] + valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] + valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] + valorPerturbacao                            
                    
                    if(verificaIntervaloXY(solucao[0], solucao[1] - valorPerturbacao, xMinimo, xMaximo, yMinimo, yMaximo)):
                        if(funcaoEggholder(solucao[0], solucao[1] - valorPerturbacao) < funcaoEggholder(solucao[0], solucao[1])):
                            solucao[1] = solucao[1] - valorPerturbacao                    

                qtdIteracoesSolucao += 1
                
                if(solucao == solucaoAtual):
                    break
                
            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(qtdIteracoesSolucao)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoEggholder(solucao[0], solucao[1]))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x, y): (" + str(truncar(valorPartida[0], 5)) + ", " + str(truncar(valorPartida[1], 5)) + ")"
            solucaoValorPartidaStr = "Função objetivo inicial f(x, y): " + str(truncar(funcaoEggholder(valorPartida[0], valorPartida[1]), 5))
            valorFinalStr = "Solução final (x, y): (" + str(truncar(solucao[0], 5)) + ", " + str(truncar(solucao[1], 5)) + ")"
            solucaoValorFinalStr = "Função objetivo final f(x, y): " + str(truncar(funcaoEggholder(solucao[0], solucao[1]), 5))

            gerarAnaliseIndividual(listaX, listaY, i, valorPartidaStr, solucaoValorPartidaStr, valorFinalStr, solucaoValorFinalStr, qtdIteracoesSolucao, tempoExecucao, "Minimização de Eggholder usando Hill-Climbing Speedest Ascent", "X", "Y", "eggholder", diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de Eggholder usando Hill-Climbing Speedest Ascent (Análise)", "eggholder", diretorio)

    def simmulatedAnnealing(self, intervaloX, intervaloY, qtdIteracoes, limiteTempo, funcaoObjetivo):

        xMinimo, xMaximo = intervaloX[0], intervaloX[1]
        yMinimo, yMaximo = intervaloY[0], intervaloY[1]

        nomeFuncaoObjetivo = str(funcaoObjetivo.__name__).replace("funcao", "")

        diretorioRaiz = "resultados"
        diretorio = diretorioRaiz + "/simulated-annealing-%s-x-[%d, %d]-y-[%d, %d]" % (nomeFuncaoObjetivo, xMinimo, xMaximo, yMinimo, yMaximo)
        diretorioGraficos = diretorio + "/graficos"

        # Criar diretório para gráficos
        if not os.path.exists(diretorio):
            os.mkdir(diretorio)
            os.mkdir(diretorioGraficos)

        listaQtdIteracoesSolucao = []
        listaTempoGasto = []
        listaSolucoes = []

        for iteracao in range(qtdIteracoes):

            valorPartida = [xMaximo - ((xMaximo - xMinimo) * random.random()), yMaximo - ((yMaximo - yMinimo) * random.random())] # Gerando valores entre [xMinimo,xMaximo] e [yMinimo, yMaximo]

            listaX = []; listaY = []

            tempoInicial = time.time()
    
            numeroPerturbacoes = qtdIteracoes
            c0 = geraParametroControle(numeroPerturbacoes, intervaloX, intervaloY, funcaoObjetivo)
            alfa = 0.99 - ((0.99 - 0.8) * random.random())
            # L0 = 0 # Número de transições iniciais

            k = 0
            i = valorPartida[:] # Copiar lista ignorando a referência (cópia real)

            melhorXY = i[:]
            qtdQuedasPermitidas = 10
            quedasTemperatura = qtdQuedasPermitidas

            ck = c0

            tempoInicial = time.time()

            while(ck > 0.001 and (time.time()-tempoInicial) < limiteTempo):

                # solucaoAtual = i[:]

                listaX.append(i[0])
                listaY.append(i[1])
                

                j = i[:]

                # Gerando uma perturbação pequena para x
                valorPerturbacaoX = geraPerturbacaoX(i, xMinimo, xMaximo, yMinimo, yMaximo)
                j[0] = j[0] + valorPerturbacaoX

                # Gerando uma perturbação pequena para y
                valorPerturbacaoY = geraPerturbacaoY(i, xMinimo, xMaximo, yMinimo, yMaximo)
                j[1] = j[1] + valorPerturbacaoY

                if(i == j):
                    if(quedasTemperatura > 0):
                        quedasTemperatura -= 1
                        continue
                    else:
                        break

                fSolucaoAtual = funcaoObjetivo(i[0], i[1])
                fSolucaoNova = funcaoObjetivo(j[0], j[1])

                if(fSolucaoNova <= fSolucaoAtual):
                    i = j
                    melhorXY = j[:]
                    quedasTemperatura = qtdQuedasPermitidas
                elif(criterioMetropolis(fSolucaoNova, fSolucaoAtual, ck) > geraRandomicoMetropolis()):
                    i = j
                    quedasTemperatura = qtdQuedasPermitidas
                else:
                    quedasTemperatura -= 1

                if(quedasTemperatura == 0):
                    break

                k += 1

                # Calcula tamanho Lk
                ck = ajustaParametroControle(ck, alfa)

            tempoExecucao = time.time() - tempoInicial

            listaQtdIteracoesSolucao.append(k)
            listaTempoGasto.append(tempoExecucao)
            listaSolucoes.append(funcaoObjetivo(melhorXY[0], melhorXY[1]))

            # Análise individual das soluções encontradas
            valorPartidaStr = "Solução inicial (x, y): (" + str(truncar(valorPartida[0], 5)) + ", " + str(truncar(valorPartida[1], 5)) + ")"
            solucaoValorPartidaStr = "Função objetivo inicial f(x, y): " + str(truncar(funcaoObjetivo(valorPartida[0], valorPartida[1]), 5))
            melhorXYStr = "Melhor solução (x, y): (" + str(truncar(melhorXY[0], 5)) + ", " + str(truncar(melhorXY[1], 5)) + ")"
            solucaoMelhorXYStr = "Melhor valor da função objetivo f(x, y): " + str(truncar(funcaoObjetivo(melhorXY[0], melhorXY[1]), 5))
            valorFinalStr = "Solução final (x, y): (" + str(truncar(i[0], 5)) + ", " + str(truncar(i[1], 5)) + ")"
            solucaoValorFinalStr = "Função objetivo final f(x, y): " + str(truncar(funcaoObjetivo(i[0], i[1]), 5))

            gerarAnaliseIndividualSA(listaX, listaY, iteracao, valorPartidaStr, solucaoValorPartidaStr,
                                   melhorXY, melhorXYStr, solucaoMelhorXYStr,
                                   valorFinalStr, solucaoValorFinalStr, k, tempoExecucao, 
                                   "Minimização de %s usando Simulated Annealing (SA)" % nomeFuncaoObjetivo, 
                                   "X", "Y",
                                   nomeFuncaoObjetivo, diretorioGraficos)

        # Análise pós execução das múltiplas soluções encontradas, partindo de diferentes valores iniciais.
        gerarAnaliseGeral(listaQtdIteracoesSolucao, listaTempoGasto, listaSolucoes, "Minimização de %s usando Simulated Annealing (SA) (Análise)" % nomeFuncaoObjetivo, nomeFuncaoObjetivo, diretorio)