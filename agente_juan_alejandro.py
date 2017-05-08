from vpi import *

from copy import deepcopy
import random

colores = {
  "verde"     : 0,
  "amarillo"  : 1,
  "anaranjado": 2,
  "rojo"      : 3
}

sensor =  [[0.70, 0.15, 0.1, 0.05],
           [0.17, 0.6, 0.17, 0.06],
           [0.06, 0.17, 0.6, 0.17],
           [0.05, 0.12, 0.23, 0.6],
           [0.03, 0.07, 0.1, 0.8]]

DISPARAR  = 1
SENSAR    = 2
MOVER     = 3

ARRIBA    = 1
DERECHA   = 2
ABAJO     = 3
IZQUIERDA = 4

ACIERTO   = 1
FALLO     = 0

def getDistancia(cell1, cell2):
    distancia_x = abs(cell2[0] - cell1[0])
    distancia_y = abs(cell2[1] - cell1[1])
    distancia_total = distancia_x + distancia_y
    if(distancia_total<=4):
        return distancia_total
    else:
        return 4

def traducir_posicion(num):
  if type(num) is tuple:
    i,j = num
    return i*5+j+1
  else:
    num -= 1
    j = (num%5)
    i = num//5
    return (i,j)


def normalizar(matriz):
  s = 0.0
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      s += matriz[i][j]

  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        matriz[i][j] = matriz[i][j] / s

  return matriz

def imprimir_matriz(matriz):
  for x in matriz:
    for y in x:
      print(y, end=" ")
    print("")

def actualizar_probabilidades(matriz, posicionSensada, color):
  nuevaMatriz = deepcopy(matriz)
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      distancia = getDistancia((i,j), traducir_posicion(posicionSensada))
      nuevaMatriz[i][j] *= sensor[distancia][colores[color]]
  return normalizar(nuevaMatriz)

class AgenteJ_A(object):
  """Agente realizado por Juan Daniel Morales y Alejandro Ochoa"""
  def __init__(self):
    super(AgenteJ_A, self).__init__()
    self.jugador        = 0
    self.estrellita     = 0 # Donde esta mi estrella
    self.infoOpSobreMi  = [[1/25 for x in range(5)] for y in range(5)] # La mia como el la ve
    self.infoSobreOp    = [[1/25 for x in range(5)] for y in range(5)] # La de el
    self.ultimaAccion   = None
    self.ultimaPosicion = 0
    self.primera_jugada = False


  def jugar(self, jugador, resultado_accion, accion_oponente, estrellita):
    # if self.primera_jugada:
    #   self.primera_jugada = False
    #   if accion_oponente is not None and accion_oponente[0] is not None:
    #     self.actualizar_oponente(accion_oponente)
    #   self.ultimaPosicion = traducir_posicion((1,1))
    #   self.ultimaAccion = SENSAR
    #   return [SENSAR, traducir_posicion((1,1))]
    
    self.jugador = jugador
    self.estrellita = estrellita
    self.actualizar_datos(resultado_accion)
    self.actualizar_oponente(accion_oponente)

    maxVal, posMax = getMax(self.infoOpSobreMi)
    if maxVal >= 0.33 and posMax == traducir_posicion(self.estrellita):
      direccion = self.dondeMover()
      self.ultimaAccion = MOVER
      #print("mover a ", direccion)
      return [MOVER, direccion]
      

    maxVal, posMax = getMax(self.infoSobreOp)
    if(maxVal >= 0.25):
      self.ultimaPosicion = traducir_posicion(posMax)
      self.ultimaAccion = DISPARAR
      return [DISPARAR, traducir_posicion(posMax)]

    utilidadActual = getUtilidad(self.infoSobreOp)
    posASensar, utilidad = vpi(self.infoSobreOp)
    # print("Utilidad actual ", utilidadActual)
    
    if utilidad - utilidadActual <= 8:
      # print("Disparar en ", posMax)
      self.ultimaPosicion = traducir_posicion(posMax)
      self.ultimaAccion = DISPARAR
      return [DISPARAR, traducir_posicion(posMax)]
    else:
      #print("Sensar en ", posASensar)
      self.ultimaPosicion = posASensar
      self.ultimaAccion = SENSAR
      return [SENSAR, posASensar]

  def dondeMover(self):
    estrella = traducir_posicion(self.estrellita)
    posMovs = self.get_movimientos_posibles(estrella)
    if (estrella in posMovs):
       posMovs.remove(estrella)
    
    probs_movs = [(self.infoOpSobreMi[mov[0]][mov[1]], mov) for mov in posMovs]
    nuevaCelda = random.choice(sorted(probs_movs)[:2])
    nuevaCelda = nuevaCelda[1]
    movimientos = [(-1,0), (0,1), (1,0), (0,-1)]
    
    for mov in movimientos:
      candidato = estrella[0] + mov[0], estrella[1] + mov[1]
      if candidato == nuevaCelda:
        return movimientos.index(mov)+1

        

  def actualizar_datos(self, resultado_accion):
    if self.ultimaAccion == DISPARAR:
      if resultado_accion == ACIERTO: # Se reestablecen las probabilidades
        i,j = traducir_posicion(self.ultimaPosicion)
        self.infoSobreOp = [[0 for x in range(5)] for y in range(5)]
        self.infoSobreOp[i][j] = 1
      elif resultado_accion == FALLO: #Bajar las probabilidades a cero
        i,j = traducir_posicion(self.ultimaPosicion)
        self.infoSobreOp[i][j] = 0
      self.infoSobreOp = normalizar(self.infoSobreOp)

    elif self.ultimaAccion == SENSAR:
      self.infoSobreOp = actualizar_probabilidades(self.infoSobreOp, self.ultimaPosicion, resultado_accion)

    elif self.ultimaAccion == MOVER:
      self.infoOpSobreMi =  self.mover_probabilidades(self.infoOpSobreMi)

  def actualizar_oponente(self, accion_oponente):
    tipoAccion, parametroAccion, resultado = accion_oponente
    if tipoAccion == DISPARAR:
      if resultado == ACIERTO: # Se reestablecen las probabilidades
        i,j = traducir_posicion(parametroAccion)
        self.infoOpSobreMi = [[0 for x in range(5)] for y in range(5)]
        self.infoOpSobreMi[i][j] = 1
      elif resultado == FALLO: #Bajar las probabilidades a cero
        i,j = traducir_posicion(parametroAccion)
        self.infoOpSobreMi[i][j] = 0
      self.infoOpSobreMi = normalizar(self.infoOpSobreMi)
    elif tipoAccion == SENSAR:
      self.infoOpSobreMi = actualizar_probabilidades(self.infoOpSobreMi, parametroAccion, resultado)
    elif tipoAccion == MOVER:
      self.infoSobreOp = self.mover_probabilidades(self.infoSobreOp)


  def movimientoPermitido(self, movimiento):
    return movimiento[0] >= 0 and movimiento[0] <= 4 and movimiento[1] >= 0 and movimiento[1] <= 4

  def get_movimientos_posibles(self, celda):
    movimientos = [(-1,0),(1,0),(0,-1),(0,1)]
    celdasPosibles = []

    if celda[0] == 0 or celda[0] == 4 or celda[1] == 0 or celda[1] == 4:
      celdasPosibles.append(celda)

    for i in range(len(movimientos)):
      movimientoNuevo = (celda[0] + movimientos[i][0], celda[1] + movimientos[i][1])
      if(self.movimientoPermitido(movimientoNuevo)):
        celdasPosibles.append(movimientoNuevo)
    return celdasPosibles

  def mover_probabilidades(self, matriz):
    matrizMovida = [[0 for x in range(5)] for y in range(5)]
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        movimientosPosibles = self.get_movimientos_posibles((i,j))
        for movimiento in movimientosPosibles:
          matrizMovida[movimiento[0]][movimiento[1]] += matriz[i][j]/len(movimientosPosibles)
    matrizMovida = normalizar(matrizMovida)
    return matrizMovida



if __name__ == '__main__':
  pass
  # color = getColor(a.ultimaPosicion)
  # print("Te salio color ", color, " en la posicion ", a.ultimaPosicion)
  # imprimir_matriz(a.infoSobreOp)
  # [accion, parametroAccion] = a.jugar(1, color, [SENSAR, 24, "verde"], 24)
  # numerito = int(input("Ingrese accion: "))
  # while(numerito >= 0):
  #   if(accion == DISPARAR):
  #     if(parametroAccion == traducir_posicion(estrellita)):
  #       print("Le diste ppeeeerrroooo")
  #       [accion, parametroAccion] = a.jugar(1, ACIERTO, [MOVER, None, None], 24)
  #       estrellita = random.choice(a.get_movimientos_posibles((estrellita)))
  #     else:
  #       print("Fallaste perrroooo")
  #       [accion, parametroAccion] = a.jugar(1, FALLO, [SENSAR, 24, "verde"], 24)
  #   elif(accion == SENSAR):
  #       color = getColor(a.ultimaPosicion)
  #       print("Te salio color ", color, " en la posicion ", a.ultimaPosicion)
  #       [accion, parametroAccion] = a.jugar(1, color, [SENSAR, 24, "verde"], 24)
  #   imprimir_matriz(a.infoSobreOp)
  #   numerito = int(input("Ingrese accion: "))
    
  # print(np.array(a.infoSobreOp))