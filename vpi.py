import copy
from agente_juan_alejandro import traducir_a_posicion, getDistancia, pastel

def vpi(matriz):
  pos             = (0,0)
  probCondicional = parte1(matriz, pos) # Solo par una posicion
  print(probCondicional)
  probConjunta    = parte2(probCondicional)
  print(probConjunta)
  probColor       = parte3(probConjunta)
  print(probColor)
  # simular()
  # sacarUtilidades()
  return probColor

def parte1(matriz, pos):
  probDistancia = {}

  # for i in range(len(matriz)):
  #   for j in range(len(matriz)):
  #     pos = traducir_a_posicion(i,j)
  #     probDistancia[pos] = {
  #       0: 0,
  #       1: 0,
  #       2: 0,
  #       3: 0,
  #       4: 0
  #     }

      # probDistancia[pos][0]     = matriz[i][j]
      # probDistancia[pos][1] += getProbsAXPosiciones(matriz, (i,j), 1)
      # probDistancia[pos][2]  += getProbsAXPosiciones(matriz, (i,j), 2)
      # probDistancia[pos][3]    += getProbsAXPosiciones(matriz, (i,j), 3)
      # probDistancia[pos][4]    += getProbsAXPosiciones(matriz, (i,j), 4)
  probDistancia[0] = matriz[pos[0]][pos[1]]
  probDistancia[1] = getProbsAXPosiciones(matriz, pos, 1)
  probDistancia[2] = getProbsAXPosiciones(matriz, pos, 2)
  probDistancia[3] = getProbsAXPosiciones(matriz, pos, 3)
  probDistancia[4] = getProbsAXPosiciones(matriz, pos, 4)

  # Hay que normalizar?
  return probDistancia

def parte2(probDistancia):
  probConjunta = {
    "verde": {
      0: pastel[0][0] * probDistancia[0],
      1: pastel[1][0] * probDistancia[1],
      2: pastel[2][0] * probDistancia[2],
      3: pastel[3][0] * probDistancia[3]
    },
    "amarillo": {
      0: pastel[0][1] * probDistancia[0],
      1: pastel[1][1] * probDistancia[1],
      2: pastel[2][1] * probDistancia[2],
      3: pastel[3][1] * probDistancia[3]
    },
    "naranja": {
      0: pastel[0][2] * probDistancia[0],
      1: pastel[1][2] * probDistancia[1],
      2: pastel[2][2] * probDistancia[2],
      3: pastel[3][2] * probDistancia[3]
    },
    "rojo": {
      0: pastel[0][3] * probDistancia[0],
      1: pastel[1][3] * probDistancia[1],
      2: pastel[2][3] * probDistancia[2],
      3: pastel[3][3] * probDistancia[3]
    }
  }

  return probConjunta

def parte3(probConjunta):
  probs = {
    "verde" : sum(probConjunta["verde"].values()),
    "amarillo" : sum(probConjunta["amarillo"].values()),
    "naranja" : sum(probConjunta["naranja"].values()),
    "rojo" : sum(probConjunta["rojo"].values())
  }
  return probs

def getProbsAXPosiciones(matriz, pos, x):
  prob = 0.0
  for casilla in getCasillasAXPosiciones(matriz, pos, x):
    prob += matriz[pos[0]][pos[1]]
  return prob

def getCasillasAXPosiciones(matriz, pos, x):
  celdas = []
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if getDistancia((i,j), pos) == x:
        celdas.append((i,j))
  return celdas

(vpi([[1/25 for x in range(5)] for y in range(5)]))