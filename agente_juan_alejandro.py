def traducir_posicion(i, j):
  return i*5+j+1

def traducir_posicion(num):
  num -= 1
  j = (num%5)
  i = num//5
  return (i,j)


class AgenteJ_A(object):
  """Agente realizado por Juan Daniel Morales y Alejandro Ochoa"""
  def __init__(self, jugador):
    super(AgenteJ_A, self).__init__()
    self.jugador = jugador
    self.ownBoard = [[" " for x in range(5)] for y in range (5)]
    self.oponentBoard = [[1/25 for x in range(5)] for y in range(5)]
    self.lastAction = None

  def jugar(self):
    pass

if __name__ == '__main__':
  pass