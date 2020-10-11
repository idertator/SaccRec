from math import ceil
from time import time

from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import qApp, QWidget

from saccrec import settings
from saccrec.engine.stimulus import SaccadicStimuli


STIMULUS_TIMEOUT = 7    # TODO: Calculate this from the refresh rate of the monitor


class StimulusPlayerWidget(QWidget):
    started = pyqtSignal(float)
    stopped = pyqtSignal()
    finished = pyqtSignal()
    moved = pyqtSignal(int)

    def __init__(self, parent=None):
        super(StimulusPlayerWidget, self).__init__(parent=parent)

        self._sampling_step = 1000 / settings.hardware.sampling_rate

        self._stimuli = None
        self._ball_position = None
        self._initial_message = None

        self._timer = QTimer()
        self._timer.setInterval(STIMULUS_TIMEOUT)
        self._timer.timeout.connect(self.on_timeout)

        self._start_time = 0

        self._load_settings()

        self._moved = None

    def _load_settings(self):
        ball_radius = settings.stimuli.ball_radius

        if self._stimuli is None:
            self._ball_radius = ball_radius
        else:
            self._ball_radius = self._stimuli.cm_to_pixels_x(ball_radius)

        self._ball_color = settings.stimuli.ball_color
        self._background_color = settings.stimuli.back_color

    def _start_stimulus(self):
        self._ball_position = self._stimuli.screen_position(0)
        self.update()

        self._start_time = time()
        self._timer.start()
        self.started.emit(self._start_time)

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
        previous_position = self._ball_position
        self._ball_position = self._stimuli.screen_position(current_sample)

        if previous_position != self._ball_position:
            new_position = self._stimuli.position(current_sample)
            self.update()
            if new_position is not None:
                self._moved = new_position.value

        if self._ball_position is None:
            self._timer.stop()
            self.stopped.emit()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setBackground(self._background_color)
        painter.fillRect(self.rect(), self._background_color)

        if self._initial_message is not None:
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

        if self._moved is not None:
            self.moved.emit(self._moved)
            self._moved = None

    def keyPressEvent(self, event):
        if not self._timer.isActive() and event.key() == Qt.Key_Space:
            self._initial_message = None
            self._start_stimulus()
        elif self._timer.isActive() and (event.modifiers() & Qt.ControlModifier) and event.key() == Qt.Key_C:
            self._timer.stop()
            self.finished.emit()
