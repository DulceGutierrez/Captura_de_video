# filters.py
import cv2
import numpy as np
from utils import createCurveFunc, createLookupArray, applyLookupArray, createCompositeFunc

## --- Filtro de Detección de Bordes (strokeEdges) ---

def strokeEdges(src, dst, blur_ksize=7, edge_ksize=5):
    """Detecta y resalta los bordes en la imagen (efecto cómic)."""
    if blur_ksize >= 3:
        # Desenfoque mediano para reducir el ruido
        blurred_src = cv2.medianBlur(src, blur_ksize)
        gray_src = cv2.cvtColor(blurred_src, cv2.COLOR_BGR2GRAY)
    else:
        gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro Laplaciano para la detección de bordes
    # CV_8U es un tipo de dato sin signo de 8 bits
    edges = cv2.Laplacian(gray_src, cv2.CV_8U, ksize=edge_ksize)

    # Invertir los bordes (bordes oscuros sobre fondo claro)
    inverse_edges = 255 - edges

    # Normalizar los bordes y multiplicarlos por la imagen original (oscurece los bordes)
    # Convertir a flotante para la operación de normalización
    inverse_edges_norm = inverse_edges / 255.0

    # Dividir la imagen fuente en canales para aplicar la máscara
    b, g, r = cv2.split(src)

    # Multiplicar cada canal por los bordes normalizados
    b[:] = b * inverse_edges_norm
    g[:] = g * inverse_edges_norm
    r[:] = r * inverse_edges_norm

    cv2.merge([b.astype(np.uint8), g.astype(np.uint8), r.astype(np.uint8)], dst)


## --- Filtros de Curvas BGR (BGRCurveFilter) ---

class BGRCurveFilter(object):
    """Filtro que aplica diferentes curvas a cada canal BGR."""
    
    def __init__(self, v_points=None, b_points=None, g_points=None, r_points=None, dtype=np.uint8):
        # Crear la tabla de consulta (LUT) para cada canal.
        # Si se proporciona un filtro de valor (v_points), se compone con los filtros de color.
        
        length = np.iinfo(dtype).max + 1
        
        v_func = createCurveFunc(v_points)
        b_func = createCurveFunc(b_points)
        g_func = createCurveFunc(g_points)
        r_func = createCurveFunc(r_points)

        self._b_lookup_array = createLookupArray(createCompositeFunc(b_func, v_func), length)
        self._g_lookup_array = createLookupArray(createCompositeFunc(g_func, v_func), length)
        self._r_lookup_array = createLookupArray(createCompositeFunc(r_func, v_func), length)

    def apply(self, src, dst):
        """Aplica el filtro con una fuente/destino BGR."""
        b, g, r = cv2.split(src)

        # Aplicar la tabla de búsqueda a cada canal
        applyLookupArray(self._b_lookup_array, b, b)
        applyLookupArray(self._g_lookup_array, g, g)
        applyLookupArray(self._r_lookup_array, r, r)

        cv2.merge([b, g, r], dst)

class BGRPortraCurveFilter(BGRCurveFilter):
    """Un filtro que aplica curvas similares a Kodak Portra a BGR."""

    def __init__(self, dtype=np.uint8):
        # Puntos de control basados en la emulación de película Portra
        # Aumenta el rojo, reduce el azul en las sombras
        BGRCurveFilter.__init__(
            self,
            v_points=[(0, 0), (23, 20), (157, 173), (255, 255)],
            b_points=[(0, 0), (41, 46), (231, 228), (255, 255)],
            g_points=[(0, 0), (52, 47), (189, 196), (255, 255)],
            r_points=[(0, 0), (69, 69), (213, 218), (255, 255)],
            dtype=dtype
        )