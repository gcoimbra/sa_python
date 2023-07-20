import os

import funcoes_auxiliares
from MetaHeuristicas import MetaHeuristicas

# Criar diretório para resultados
diretorio = "resultados"
if not os.path.exists(diretorio):
    os.mkdir(diretorio)
else:
    os.system("rm -r resultados/*")

metaHeuristicas = MetaHeuristicas()

metaHeuristicas.simmulatedAnnealing(qtdIteracoes=30, intervaloX=(-512, 512), intervaloY=(-512, 512),
                                    limiteTempo=1, funcaoObjetivo=funcoes_auxiliares.funcaoEggholder)

metaHeuristicas.simmulatedAnnealing(qtdIteracoes=30, intervaloX=(-10, 10), intervaloY=(-10, 10),
                                    limiteTempo=1, funcaoObjetivo=funcoes_auxiliares.funcaoParedaoEspinhento)
