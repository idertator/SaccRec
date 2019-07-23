from PyQt5.QtCore import QObject, pyqtSignal

from saccrec.core import Settings


class Manager(QObject):
    recordingStarted = pyqtSignal()
    recordingStopped = pyqtSignal()
    recordingFinished = pyqtSignal()

    def __init__(self, settings: Settings, parent=None):
        super(Manager, self).__init__(parent=parent)

        self._settings = settings

    def start_recording(self, **parameters):
        self.recordingStarted.emit()

    def stop_recording(self):
        self.recordingStopped.emit()
    
    

