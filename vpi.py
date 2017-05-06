import copy
import numpy as np
from agente_juan_alejandro import *

def vpi(matriz):
  
  print(np.array(matriz))
  utilidades = []
  for x in range(1, 26):
    i,j = traducir_posicion(x)
    probCondicional = parte1(matriz, (i,j)) # Solo para una posicion
    probConjunta    = parte2(probCondicional)
    probColor       = parte3(probConjunta)
    utilidades.append(simular(matriz, (i,j), probColor))

  print_utilidades(utilidades)
  mejorUtilidad = max(utilidades)
  print("La mejor utilidad la tiene la posicion ", utilidades.index(mejorUtilidad)+1, "con: ", mejorUtilidad)
  return utilidades.index(mejorUtilidad)+1, mejorUtilidad

def parte1(matriz, pos):
  probDistancia = {}

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
      0: sensor[0][0] * probDistancia[0],
      1: sensor[1][0] * probDistancia[1],
      2: sensor[2][0] * probDistancia[2],
      3: sensor[3][0] * probDistancia[3],
      4: sensor[4][0] * probDistancia[4]
    },
    "amarillo": {
      0: sensor[0][1] * probDistancia[0],
      1: sensor[1][1] * probDistancia[1],
      2: sensor[2][1] * probDistancia[2],
      3: sensor[3][1] * probDistancia[3],
      4: sensor[4][0] * probDistancia[4]
    },
    "anaranjado": {
      0: sensor[0][2] * probDistancia[0],
      1: sensor[1][2] * probDistancia[1],
      2: sensor[2][2] * probDistancia[2],
      3: sensor[3][2] * probDistancia[3],
      4: sensor[4][0] * probDistancia[4]
    },
    "rojo": {
      0: sensor[0][3] * probDistancia[0],
      1: sensor[1][3] * probDistancia[1],
      2: sensor[2][3] * probDistancia[2],
      3: sensor[3][3] * probDistancia[3],
      4: sensor[4][0] * probDistancia[4]
    }
  }

  return probConjunta

def parte3(probConjunta):
  probs = {
    "verde" : sum(probConjunta["verde"].values()),
    "amarillo" : sum(probConjunta["amarillo"].values()),
    "anaranjado" : sum(probConjunta["anaranjado"].values()),
    "rojo" : sum(probConjunta["rojo"].values())
  }

  s = sum(probs.values())

  probs = {
    "verde" : probs["verde"]/s,
    "amarillo" : probs["amarillo"]/s,
    "anaranjado" : probs["anaranjado"]/s,
    "rojo" : probs["rojo"]/s
  }

  return probs

def simular(matriz, pos, probColor):
  utilidadTotal = 0
  i,j = pos

  for color in probColor.keys():
    matrizSimulada = actualizar_probabilidades(matriz, traducir_a_posicion(i,j), color)
    utilidadTotal += getUtilidad(matrizSimulada)*probColor[color]

  return utilidadTotal


def getUtilidad(matriz):
  desvEst = np.std(matriz)

  if 0 <= desvEst < 0.025:
    # print("1")
    return 12.5
  elif 0.025 <= desvEst < 0.05:
    # print("2")
    return 25
  elif 0.05 <= desvEst < 0.075:
    # print("3")
    return 37.5
  elif 0.075 <= desvEst < 0.1:
    # print("4")
    return 50
  elif 0.1 <= desvEst < 0.125:
    # print("5")
    return 62.5
  elif 0.125 <= desvEst < 0.15:
    # print("6")
    return 75
  elif 0.15 <= desvEst < 0.175:
    # print("7")
    return 87.5
  elif 0.175 <= desvEst < 0.2:
    # print("8")
    return 100
  else:
    return 125

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

def print_utilidades(utilidades):
  for x in range(len(utilidades)):
    print(x+1, ": ", utilidades[x])

if __name__ == '__main__':
  a = AgenteJ_A()
  pos = vpi(a.infoSobreOp)
  a.ultimaPosicion = pos[0]
  a.jugar(1, "rojo", [SENSAR, 24, "verde"], 24)
  pos = vpi(a.infoSobreOp)
  a.ultimaPosicion = pos[0]
  a.jugar(1, "amarillo", [SENSAR, 24, "rojo"], 24)
  pos = vpi(a.infoSobreOp)
  a.ultimaPosicion = pos[0]
  a.jugar(1, "verde", [SENSAR, 24, "rojo"], 24)
  print(np.array(a.infoSobreOp))
