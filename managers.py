# managers.py
import cv2
import numpy as np
import time

class CaptureManager(object):
    #Gestiona la captura de video y el envío de cuadros a diferentes destinos.
    #Abstrae la clase VideoCapture de OpenCV.
    def __init__(self, capture, should_mirror_preview=False):
        self._capture = capture
        self.should_mirror_preview = should_mirror_preview
        
        self.frame = None
        self._entered_frame = False
        
        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimate = None

    @property
    def frame_size(self):
        #Retorna el tamaño del cuadro (width, height).
        width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    def enterFrame(self):
        #Captura el siguiente cuadro, si existe.
        assert not self._entered_frame, 'La enterFrame() anterior no tuvo una exitFrame() coincidente.'
        
        if self._capture is not None:
            # Captura y almacena el frame
            success, frame = self._capture.read()
            if success:
                self.frame = frame
            else:
                self.frame = None

        self._entered_frame = True

    def exitFrame(self):
        #Muestra el cuadro y libera el recurso.
        if self.frame is None:
            self._entered_frame = False
            return

        # Actualizar la estimación de FPS
        if self._frames_elapsed == 0:
            self._start_time = time.time()
        else:
            time_elapsed = time.time() - self._start_time
            self._fps_estimate = self._frames_elapsed / time_elapsed
        self._frames_elapsed += 1

        # Mostrar en la ventana 
        if self.should_mirror_preview:
             self.frame = np.fliplr(self.frame).copy()

        self._entered_frame = False
        self.frame = None

class WindowManager(object):
    
    def __init__(self, window_name, keypress_callback=None):
        self.window_name = window_name
        self.keypress_callback = keypress_callback
        self.is_window_created = False

    def createWindow(self):
        cv2.namedWindow(self.window_name)
        self.is_window_created = True

    def show(self, frame):
        cv2.imshow(self.window_name, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self.window_name)
        self.is_window_created = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypress_callback is not None and keycode != -1:
            # Descartar cualquier información no ASCII codificada
            keycode &= 0xFF
            self.keypress_callback(keycode)