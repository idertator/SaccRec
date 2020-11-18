from PyQt5.QtCore import pyqtSignal, QObject

from saccrec.core import Record
from saccrec.core.study import Hardware, Subject
from saccrec.engine.recording import OpenBCIRecorder
from saccrec.engine.stimulus import SaccadicStimuli
from saccrec import settings

from .player import StimulusPlayerWidget
from .signals import SignalsWidget


class Runner(QObject):
    started = pyqtSignal()
    stopped = pyqtSignal()
    finished = pyqtSignal()

    def __init__(
        self,
        player: StimulusPlayerWidget,
        signals: SignalsWidget,
        parent=None
    ):
        super(Runner, self).__init__(parent=parent)
        self._player = player
        self._signals = signals

        self._recorder = OpenBCIRecorder(
            port=settings.hardware.port,
            sampling_rate=settings.hardware.sampling_rate
        )

        self._tests_stimuli = None
        self._current_test = None

        self._stimulus = None
        self._output = None
        self._distance_to_subject = None
        self._tests_stimuli: list[SaccadicStimuli] = None
        self._record = None

        self._player.started.connect(self.on_player_started)
        self._player.stopped.connect(self.on_player_stopped)
        self._player.finished.connect(self.on_player_finished)
        self._player.moved.connect(self.on_player_moved)

    def run(
        self,
        stimulus: dict,
        output: str,
        distance_to_subject: float,
        tests_stimuli: list[SaccadicStimuli],
        **kwargs
    ):
        self._stimulus = stimulus
        self._output = output
        self._distance_to_subject = distance_to_subject
        self._tests_stimuli = tests_stimuli

        from saccrec.core import workspace
        self._record = Record(
            subject=workspace.subject,
            hardware=Hardware(
                sample_rate=settings.hardware.sampling_rate,
                channels=settings.hardware.channels.json
            )
        )

        if not self._recorder.is_alive():
            self._recorder.start()
            self._recorder.wait_until_ready()

        if not self._signals.isVisible():
            self._signals.show()

        tests_stimuli = self._tests_stimuli
        self._current_test = 0
        self._current_sd_file = None

        self._signals.hide()
        self._start_test()

        self._player.showFullScreen()
        self.started.emit()

    def _start_test(self):
        stimuli: SaccadicStimuli = self._tests_stimuli[self._current_test]

        self._player.run_stimulus(
            stimuli,
            '\n'.join([str(stimuli), _('Presione espacio para continuar')])
        )

        self._player.move(
            settings.screen.secondary_screen_rect.left(),
            settings.screen.secondary_screen_rect.top()
        )

    def on_player_started(self):
        if not self._signals.is_rendering:
            self._signals.start(self._recorder)     # TODO: Change this to adding samples from here

        self._current_sd_file = self._recorder.start_recording()
        print(self._current_sd_file)  # TODO: Remove this later

    def on_player_stopped(self):
        self._signals.stop()
        self._recorder.stop_recording()
        self._recorder.close_recorder()

        self.stopped.emit()

    def on_player_finished(self):
        self._signals.stop()
        self._recorder.stop_recording()

        current_stimulus = self._tests_stimuli[self._current_test]
        self._record.add_test(
            filename=self._current_sd_file,
            angle=current_stimulus.angle,
            fixation_duration=current_stimulus.fixation_duration,
            fixation_variability=current_stimulus.fixation_variability,
            saccades_count=current_stimulus.saccades_count,
            test_name=current_stimulus.test_name
        )

        if self._current_test < len(self._tests_stimuli) - 1:
            stimuli = self._tests_stimuli[self._current_test]
            self._current_test += 1

            self._player.run_stimulus(
                stimuli,
                '\n'.join([str(stimuli), _('Presione espacio para continuar')])
            )
        else:
            self._player.close_player()
            self._record.save(self._output)
            self.finished.emit()

    def on_player_moved(self, position: int):
        self._recorder.put_marker(position)
