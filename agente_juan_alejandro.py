import random

colores = {
  "verde" : random.choice[0,1],
  "amarillo" : random.choice[2,3],
  "anaranjado" : random.choice[3,4],
  "rojo" : random.choice[4,5]
}

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
    if(distancia_total<=5):
        return distancia_total
    else:
        return 5

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
  def __init__(self, jugador):
    super(AgenteJ_A, self).__init__()
    self.jugador = jugador
    self.ownBoard = [[0 for x in range(5)] for y in range (5)]
    self.oponentBoard = [[1/25 for x in range(5)] for y in range(5)]
    self.ultimaAccion = None
    self.ultimaPosicion = 0


  def jugar(self, resultado_accion, accion_oponente, estrellita):
    self.colocar_estrellita(estrellita)
    self.actualizar_datos(resultado_accion)
    self.actualizar_oponente(accion_oponente)

    #TODO: Esto es un borrador
    if mayorProbabilidad < 0.7:
      posicionASensar = posicionConMayorProbabilidad
      self.ultimaAccion = OBSERVAR
      self.ultimaPosicion = posicionASensar

    else mayorProbabilidad:
      self.ultimaAccion = DISPARAR
      self.ultimaPosicion = posicionADisparar


  def colocar_estrellita(self, estrellita):
    i, j = traducir_posicion(estrellita)
    self.ownBoard[i][j] = 1

  def actualizar_oponente(accion_oponente):
    tipoAccion, parametroAccion, resultado = accion_oponente
    if tipoAccion == DISPARAR:
      pass
    elif tipoAccion == OBSERVAR:
      pass
    elif tipoAccion == MOVER:
      pass

  def actualizar_datos(self.resultado_accion):
    if self.ultimaAccion == DISPARAR:
      if resultado_accion == ACIERTO: # Se reestablecen las probabilidades
        self.oponentBoard = [[1/25 for x in range(5)] for y in range(5)]
      elif resultado_accion == FALLO: #Bajar las probabilidades a cero
        i,j = self.ultimaPosicion
        self.opponentBoard[i][j] = 0

    elif self.ultimaAccion == OBSERVAR:
      self.actualizar_probabilidades(resultado_accion)

    elif self.ultimaAccion == MOVER:
      pass

  def actualizar_probabilidades(self, color):
      # TODO: ARREGLAR ESTO

      s = 0.0
      for x in range(len(self.oponentBoard)):
        for y in range(len(self.oponentBoard[x])):
          distancia_cells = getDistancia((x, y), ultimaPosicion)
          self.oponentBoard[x][y] = self.oponentBoard[x][y] * colores[distancia_cells][color]
          s+= self.oponentBoard[x][y]

      self.normalizar(s)

  def normalizar(self, s):
    for i in range(len(self.oponentBoard)):
      for j in range(len(self.oponentBoard[i])):
          self.oponentBoard[i][j] = self.oponentBoard[i][j] / s


if __name__ == '__main__':
  a = AgenteJ_A(1)
  a.jugar(None,[1,24,3],12)
  imprimir_matriz(a.ownBoard)