import random
from copy import deepcopy

colores = {
  "verde" : 0,
  "amarillo" : 1,
  "anaranjado" : 2,
  "rojo" : 3
}

pastel =  [[0.70, 0.15, 0.1, 0.05],
           [0.17, 0.6, 0.17, 0.06],
           [0.06, 0.17, 0.6, 0.17],
           [0.05, 0.12, 0.23, 0.6],
           [0.03, 0.07, 0.1, 0.8]]

DISPARAR  = 1
OBSERVAR  = 2
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

def traducir_posicion(i, j):
  return i*5+j+1

def traducir_posicion(num):
  num -= 1
  j = (num%5)
  i = num//5
  return (i,j)

def imprimir_matriz(matriz):
  for x in matriz:
    for y in x:
      print(y, end=" ")
    print("")


class AgenteJ_A(object):
  """Agente realizado por Juan Daniel Morales y Alejandro Ochoa"""
  def __init__(self):
    super(AgenteJ_A, self).__init__()
    self.jugador        = 0
    self.estrellita     = 0 # Donde esta mi estrella
    self.infoOpSobreMi  = [[1/25 for x in range(5)] for y in range(5)] # La mia como el la ve
    self.infoSobreOp    = [[1/25 for x in range(5)] for y in range(5)] #La de el
    self.ultimaAccion   = OBSERVAR
    self.ultimaPosicion = (0,0)


  def jugar(self, jugador, resultado_accion, accion_oponente, estrellita):
    self.jugador = jugador
    self.estrellita = estrellita
    self.actualizar_datos(resultado_accion)
    self.actualizar_oponente(accion_oponente)

    #Revisar si las probabilidades del oponente, luego de saber qué acción realizaron en este momento,
    #son más peligrosas que las de nosotros luego de haber recibido los datos del sensor.
    #Esto con lo de la info perfecta.

    # if mayorProbabilidad < 0.7:
    #   posicionASensar = posicionConMayorProbabilidad
    #   self.ultimaAccion = OBSERVAR
    #   self.ultimaPosicion = posicionASensar

    # else:
    #   self.ultimaAccion = DISPARAR
    #   self.ultimaPosicion = posicionADisparar

  def actualizar_oponente(self, accion_oponente):
    tipoAccion, parametroAccion, resultado = accion_oponente
    if tipoAccion == DISPARAR:
      pass
    elif tipoAccion == OBSERVAR:
      self.actualizarProbabilidadesSobreMi(parametroAccion, resultado)
    elif tipoAccion == MOVER:
      self.moverProbabilidadesSobreEnemigo()
      pass

  def actualizar_datos(self, resultado_accion):
    if self.ultimaAccion == DISPARAR:
      if resultado_accion == ACIERTO: # Se reestablecen las probabilidades
        # self.infoSobreOp = [[1/25 for x in range(5)] for y in range(5)]
        i,j = self.ultimaPosicion
        self.infoSobreOp[i][j] = 1
      elif resultado_accion == FALLO: #Bajar las probabilidades a cero
        i,j = self.ultimaPosicion
        self.infoSobreOp[i][j] = 0
      self.infoSobreOp = self.normalizar(self.InfoSobreOp)

    elif self.ultimaAccion == OBSERVAR:
      self.actualizar_probabilidades(resultado_accion)

    elif self.ultimaAccion == MOVER:
      self.moverProbabilidadesSobreMi()

  def actualizar_probabilidades(self, color):
      s = 0.0
      for x in range(len(self.infoSobreOp)):
        for y in range(len(self.infoSobreOp[x])):
          distancia_cells = getDistancia((x, y), self.ultimaPosicion)
          self.infoSobreOp[x][y] = self.infoSobreOp[x][y] * pastel[distancia_cells][colores[color]]
          # s+= self.infoSobreOp[x][y]
      self.infoSobreOp = self.normalizar(self.infoSobreOp)

  def normalizar(self, matriz):
    s = 0.0

    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        s += matriz[i][j]

    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
          matriz[i][j] = matriz[i][j] / s

    return matriz

  def movimientoPermitido(self, movimiento):
    return movimiento[0] >= 0 and movimiento[0] <= 4 and movimiento[1] >= 0 and movimiento[1] <= 4

  def getMovimientosPosibles(self, celda):
    movimientos = [(-1,0),(1,0),(0,-1),(0,1)]
    celdasPosibles = []
    for i in range(len(movimientos)):
      movimientoNuevo = (celda[0] + movimientos[i][0], celda[1] + movimientos[i][1])
      if(self.movimientoPermitido(movimientoNuevo)):
        celdasPosibles.append(movimientoNuevo)
    return celdasPosibles

  def moverProbabilidadesSobreEnemigo(self):
    matriz = self.infoSobreOp
    matrizMovida = [[0 for x in range(5)] for y in range(5)]
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        movimientosPosibles = self.getMovimientosPosibles((i,j))
        for movimiento in movimientosPosibles:
          matrizMovida[movimiento[0]][movimiento[1]] += matriz[i][j]/len(movimientosPosibles)
    matrizMovida = self.normalizar(matrizMovida)
    return matrizMovida


  def moverProbabilidadesSobreMi(self):
    matriz = self.infoOpSobreMi
    matrizMovida = [[0 for x in range(5)] for y in range(5)]
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        movimientosPosibles = self.getMovimientosPosibles((i,j))
        for movimiento in movimientosPosibles:
          matrizMovida[movimiento[0]][movimiento[1]] += matriz[i][j]/len(movimientosPosibles)
    return matrizMovida


  def actualizarProbabilidadesSobreMi(self, posicionSensada, color):
    matriz = self.infoOpSobreMi
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        distancia = getDistancia((i,j), traducir_posicion(posicionSensada))
        matriz[i][j] *= pastel[distancia][colores[color]]
        #le tengo la fe
        
    self.infoOpSobreMi = self.normalizar(matriz)

        


if __name__ == '__main__':
  a = AgenteJ_A()
  a.jugar(1, "amarillo", [OBSERVAR, 24, "verde"], 24)
  print("información del oponente")
  imprimir_matriz(a.infoOpSobreMi)
  print("información sobre oponente")
  imprimir_matriz(a.infoSobreOp)
  a.ultimaAccion = MOVER
  a.jugar(1, None, [MOVER, None, None], 24)
  print("información del oponente")
  imprimir_matriz(a.infoOpSobreMi)
  print("información sobre oponente")
  imprimir_matriz(a.infoSobreOp)
