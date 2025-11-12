# cameo.py
import cv2
import sys
import numpy as np

# Importar módulos locales
from managers import WindowManager, CaptureManager
from filters import strokeEdges, BGRPortraCurveFilter

class Cameo(object):
    """
    Clase principal de la aplicación Cameo.
    Implementa el enfoque orientado a objetos para la captura y filtrado.
    """
    def __init__(self):
        # Inicialización del gestor de ventana y captura
        self._window_manager = WindowManager('Cameo', self.onKeypress)
        
        # Uso de la cámara por defecto (0). 
        # Si tienes problemas, prueba con 1, 2, etc. o verifica permisos.
        self._capture_manager = CaptureManager(
            cv2.VideoCapture(0),
            should_mirror_preview=True
        )

        # Inicialización de los filtros a aplicar
        self._curve_filter = BGRPortraCurveFilter()

        # Configuración de FPS para un flujo más suave (opcional)
        self._capture_manager._capture.set(cv2.CAP_PROP_FPS, 30)
        self._capture_manager._capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self._capture_manager._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def run(self):
        """Bucle principal de la aplicación."""
        print("Iniciando Cameo. Presiona 'Esc' para salir.")
        
        self._window_manager.createWindow()

        while self._window_manager.is_window_created:
            self._capture_manager.enterFrame()
            frame = self._capture_manager.frame

            if frame is not None:
                # --- Aplicación de Filtros (Capítulo 3) ---

                # 1. Aplicar el filtro de bordes (efecto cómic/tinta)
                # Modificamos el frame in-place, lo que se refleja en la siguiente línea
                strokeEdges(frame, frame) 

                # 2. Aplicar el filtro de curvas (emulación de película Portra)
                self._curve_filter.apply(frame, frame)
                
                # Mostrar el cuadro filtrado
                self._window_manager.show(frame)

            self._capture_manager.exitFrame()
            self._window_manager.processEvents()

    def onKeypress(self, keycode):
        """
        Maneja las pulsaciones de teclas.
        'Esc' (27) para salir.
        """
        if keycode == 27:  # Código ASCII para 'Esc'
            self._window_manager.destroyWindow()
        
        # Opcional: Implementar captura de pantalla, grabación de video, etc.

if __name__ == '__main__':
    try:
        Cameo().run()
    except Exception as e:
        print(f"Ocurrió un error al ejecutar Cameo: {e}")
        # Cierra las ventanas de OpenCV en caso de excepción
        cv2.destroyAllWindows()
    finally:
        # Asegúrate de cerrar todas las ventanas al finalizar
        cv2.destroyAllWindows()