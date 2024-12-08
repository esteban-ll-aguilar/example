arreglo = [8,1,5,14,4,15,12,6,2,11,10,7,9]
def metodo_binario(arreglo: list):                                        
    for i in range(len(arreglo)):                                        
        for j in range(i+1, len(arreglo)):
            if arreglo[i] > arreglo[j]:
                arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
    return arreglo


"""
Cálculo de valores de la función de T(n) obtenida:
  T(n) = 12n^2 + 10n + 7
"""

print(metodo_binario(arreglo))