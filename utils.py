# utils.py
import numpy as np
import scipy.interpolate

## --- Curvas - doblando el espacio de color ---

def createCurveFunc(points):
    """
    Retorna una función derivada de los puntos de control.
    Implementa la interpolación de spline cúbico.
    """
    if points is None or len(points) < 2:
        return None

    xs, ys = zip(*points)

    # Se necesita un mínimo de 4 puntos para la interpolación cúbica.
    # Se utiliza interpolación lineal en caso contrario.
    kind = 'linear' if len(points) < 4 else 'cubic'

    # Extrapolación (bounds_error=False) permite que la curva se extienda
    # más allá del rango definido por los puntos de control.
    return scipy.interpolate.interp1d(xs, ys, kind=kind, bounds_error=False)

def createLookupArray(func, length=256):
    """
    Retorna un array de búsqueda para entradas de números enteros a una función.
    Los valores de búsqueda se fijan a [0, length - 1].
    """
    if func is None:
        return None

    lookup_array = np.empty(length)
    for i in range(length):
        # Asegura que los valores permanezcan en el rango de 0 a 255
        lookup_array[i] = np.clip(func(i), 0, length - 1)
        
    return lookup_array

def applyLookupArray(lookup_array, src, dst):
    """Mapea una fuente a un destino usando un array de búsqueda."""
    if lookup_array is None:
        return
    # La indexación con un array (src) devuelve un nuevo array
    # donde los valores de src se usan como índices en lookup_array.
    dst[:] = lookup_array[src]

def createCompositeFunc(func0, func1):
    """Retorna una función compuesta (func0(func1(x)))."""
    if func0 is None:
        return func1
    if func1 is None:
        return func0
    return lambda x: func0(func1(x))