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
           [0.05, 0.1, 0.15, 0.8]]

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
  def __init__(self, jugador):
    super(AgenteJ_A, self).__init__()
    self.jugador        = jugador
    self.estrellita     = 0 # Donde esta mi estrella
    self.infoOpSobreMi  = [[1/25 for x in range(5)] for y in range(5)] # La mia como el la ve
    self.infoSobreOp    = [[1/25 for x in range(5)] for y in range(5)] #La de el
    self.ultimaAccion   = None
    self.ultimaPosicion = (0,0)


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
    self.estrellita = estrellita

  def actualizar_oponente(accion_oponente):
    tipoAccion, parametroAccion, resultado = accion_oponente
    if tipoAccion == DISPARAR:
      pass
    elif tipoAccion == OBSERVAR:
      self.actualizarProbabilidadesSobreMi(parametroAccion, resultado)
    elif tipoAccion == MOVER:
      pass

  def actualizar_datos(self.resultado_accion):
    if self.ultimaAccion == DISPARAR:
      if resultado_accion == ACIERTO: # Se reestablecen las probabilidades
        # self.infoSobreOp = [[1/25 for x in range(5)] for y in range(5)]
        i,j = self.ultimaPosicion
        self.infoSobreOp[i][j] = 1
      elif resultado_accion == FALLO: #Bajar las probabilidades a cero
        i,j = self.ultimaPosicion
        self.opponentBoard[i][j] = 0
      self.normalizar()

    elif self.ultimaAccion == OBSERVAR:
      self.actualizar_probabilidades(resultado_accion)

    elif self.ultimaAccion == MOVER:
      pass

  def actualizar_probabilidades(self, color):
      # TODO: ARREGLAR ESTO

      s = 0.0
      for x in range(len(self.infoSobreOp)):
        for y in range(len(self.infoSobreOp[x])):
          distancia_cells = getDistancia((x, y), ultimaPosicion)
          self.infoSobreOp[x][y] = self.infoSobreOp[x][y] * colores[distancia_cells][color]
          s+= self.infoSobreOp[x][y]

      self.normalizar()

  def normalizar(self, matriz):
    s = 0.0

    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        s += matriz[i][j]

    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
          matriz[i][j] = matriz[i][j] / s

    return matriz


  def actualizarProbabilidadesSobreMi(self, posicionSensada, color):
    matriz = self.infoOpSobreMi
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        distancia = getDistancia((i,j), traducir_posicion(posicionSensada))
        matriz[i][j] *= pastel[distancia][colores[color]]
        #no le tengo la fe
        
    self.infoOpSobreMi = self.normalizar(matriz)

        


if __name__ == '__main__':
  a = AgenteJ_A(1)
  a.jugar(None,[1,24,3],12)
  imprimir_matriz(a.infoOpSobreMi)