from math import ceil
from time import time

from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import qApp, QWidget

from saccrec.core import Settings
from saccrec.engine.stimulus import SaccadicStimuli


STIMULUS_TIMEOUT = 7    # TODO: Calculate this from the refresh rate of the monitor


class StimulusPlayerWidget(QWidget):
    started = pyqtSignal(float)
    stopped = pyqtSignal()
    finished = pyqtSignal()
    
    def __init__(self, settings: Settings, parent=None):
        super(StimulusPlayerWidget, self).__init__(parent=parent)
        self._settings = settings
        
        self._sampling_step = 1000 / self._settings.openbci_sample_rate

        self._stimuli = None
        self._ball_position = None
        self._initial_message = None

        self._timer = QTimer()
        self._timer.setInterval(STIMULUS_TIMEOUT)
        self._timer.timeout.connect(self.on_timeout)

        self._start_time = 0

        self._load_settings()

    def _load_settings(self):
        if self._stimuli is None:
            self._ball_radius = self._settings.stimulus_saccadic_ball_radius
        else:
            self._ball_radius = self._stimuli.cm_to_pixels_x(self._settings.stimulus_saccadic_ball_radius)
        self._ball_color = self._settings.stimulus_saccadic_ball_color
        self._background_color = self._settings.stimulus_saccadic_background_color

    def _start_stimulus(self):
        self._ball_position = self._stimuli.screen_position(0)
        self.update()
        self._start_time = time()
        self.started.emit(self._start_time)
        self._timer.start()

    def run_stimulus(
        self, 
        stimuli: SaccadicStimuli, 
        initial_message: str = None
    ):
        self._stimuli = stimuli
        self._load_settings()
        self._initial_message = initial_message
    
        if initial_message is None:
            self._start_stimulus()
        else:
            self.update()

    def close_player(self):
        self.setParent(qApp.topLevelWidgets()[0])
        self.close()
        self.setParent(None)

    def on_timeout(self):
        elapsed = (time() - self._start_time) * 1000.0
        current_sample = ceil(elapsed / self._sampling_step)
        self._ball_position = self._stimuli.screen_position(current_sample)
        self.update()

        if self._ball_position is None:
            self._timer.stop()
            self.finished.emit()
            
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setBackground(self._background_color)
        painter.fillRect(self.rect(), self._background_color)

        if self._start_stimulus is not None:
            painter.save()
            painter.setPen(self._ball_color)
            
            font = painter.font()
            font.setPixelSize(48)
            painter.setFont(font)

            painter.drawText(
                self.rect(),
                Qt.AlignHCenter | Qt.AlignVCenter,
                self._initial_message
            )
            painter.restore()

        if self._ball_position is not None:
            painter.setPen(self._ball_color)
            painter.setBrush(self._ball_color)
            painter.drawEllipse(self._ball_position, self._ball_radius, self._ball_radius)

        painter.end()

    def keyPressEvent(self, event):
        if not self._timer.isActive() and event.key() == Qt.Key_Space:
            self._initial_message = None
            self._start_stimulus()
        elif self._timer.isActive() and (event.modifiers() & Qt.ControlModifier) and event.key() == Qt.Key_C:
            self._timer.stop()
            self.stopped.emit()


# class StimulusPlayerWidget1(QWidget):
    
#     def __init__(self, tipo=None, parent=None):
#         super(StimulusPlayerWidget1, self).__init__()

#         self.padre = parent

#         self.tipo = tipo

#         self.contador = 0
#         self.isRight = True

#         self.initUI()

#         self._stimulator = Stimulator(self)
#         self._ballposition = BallPosition(self.padre.test.test_duration, self.padre.test.mean_duration, self.padre.test.variation)
#         self._stimulatorTimer = QTimer()
#         self._stimulatorTimer.setInterval(16)
#         self._stimulatorTimer.timeout.connect(self.onTimerTimeout)

#         layout = QVBoxLayout()
#         layout.addWidget(self._stimulator)
        
#         self.setLayout(layout)
    
#     @property
#     def screenpixels(self):
#         app = QGuiApplication.instance()
#         size = app.primaryScreen().size()
#         return size.width(), size.height()

#     def initUI(self):
#         self.resize(self.screenpixels[0], self.screenpixels[1])

#     def runStimulator(self):
#         self.show()
#         self.initialTimeStamp = datetime.now()
#         print('Initial timestamp: '+str(self.initialTimeStamp))
#         self._stimulatorTimer.start()

#     @property
#     def stimulator(self):
#         return self._stimulator

#     @property
#     def screensize(self):
#         return self.padre.settings.screensize

#     @property
#     def distancePoints(self):
#         return float(self.padre.settings.distanceBetweenPoints)

    
#     @property
#     def distanceFromPatient(self):
#         if self.padre.test.stimulation_angle > 30:
#             angulo_maximo = self.padre.test.stimulation_angle
#         else:
#             angulo_maximo = 30
#         distance_from_mid = self.distancePoints / 2

#         distance_from_patient = distance_from_mid * (math.sin(math.radians(90 - angulo_maximo)) / math.sin(math.radians(angulo_maximo)))

#         return distance_from_patient


#     @property
#     def distanceFromCenter(self):
#         if(self.tipo == '1' or self.tipo == '3'):
#             angulo_vision = 30
#         else:
#             angulo_vision = self.padre.test.stimulation_angle 

#         pantalla_horizontal = self.screensize[0]

#         densidad_pixeles = self.screenpixels[0] / self.screensize[0]

#         distance_from_mid = self.distanceFromPatient * (math.sin(math.radians(angulo_vision)) / math.sin(math.radians(90 - angulo_vision)))

#         return math.floor(distance_from_mid * densidad_pixeles)


#     @property
#     def deltatime(self):
#         difference = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(str(self.initialTimeStamp), "%Y-%m-%d %H:%M:%S.%f")
#         delta = difference.seconds * 1000 + int(difference.microseconds/1000)
#         return delta

    
#     def onTimerTimeout(self, *args):
#         left = self.rect().center().x() - self.distanceFromCenter
#         right = self.rect().center().x() + self.distanceFromCenter


#         if self._ballposition.isRight(self.deltatime):
#             self._stimulator.position = right, self.rect().center().y()
#             if self.isRight == False:
#                 self.isRight = True
#                 self.contador = self.contador + 1
#         else:
#             self._stimulator.position = left, self.rect().center().y()
#             if self.isRight:
#                 self.isRight = False
#                 self.contador = self.contador + 1

#         if(self.tipo == '1' or self.tipo == '3'):
#             if(self.contador == 10):
#                 self._stimulatorTimer.stop()
#                 self.hide()
#                 if(self.tipo == '1'):
#                     QMessageBox.question(self,'Aviso','A continuación será el test. Presione Ok para continuar.',QMessageBox.Ok)
#                     self.padre._testStimulator.runStimulator()
#                 else:
#                     QMessageBox.question(self,'Aviso','Ha terminado la calibración. Presione Ok para finalizar.',QMessageBox.Ok)
        
#         if(self.deltatime / 1000 > self.padre.test._test_duration and self.tipo == '2'):
#             self._stimulatorTimer.stop()
#             self.hide()
#             QMessageBox.question(self,'Aviso','A continuación será la calibración. Presione Ok para continuar.',QMessageBox.Ok)
#             self.padre._calibrationWindow2.runStimulator()
