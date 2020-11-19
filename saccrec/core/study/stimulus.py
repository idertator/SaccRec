from PyQt5 import QtCore, QtWidgets


class Stimulus(QtWidgets.QGroupBox):
    addPressed = QtCore.pyqtSignal(int)
    removePressed = QtCore.pyqtSignal(int)

    def __init__(
        self,
        index: int,
        name: str,
        angle: int,
        fixation_duration: float,
        fixation_variability: float,
        saccades_count: int,
        can_add: bool = False,
        can_remove: bool = False,
        enabled: bool = True,
        parent=None
    ):
        super(Stimulus, self).__init__(parent=parent)

        self._index = index
        self._name = name
        self._can_add = can_add
        self._can_remove = can_remove
        self._enabled = enabled

        self.setup_ui()

        self.angle = angle
        self.fixation_duration = fixation_duration
        self.fixation_variability = fixation_variability
        self.saccades_count = saccades_count

    def setup_ui(self):
        self.setTitle(self._name)
        self.setFlat(True)
        self.setMinimumHeight(90)
        self.setFixedHeight(90)

        layout = QtWidgets.QHBoxLayout(self)

        self._angle_edit = QtWidgets.QSpinBox(self)
        self._angle_edit.setMinimum(10)
        self._angle_edit.setMaximum(60)
        self._angle_edit.setSingleStep(1)
        self._angle_edit.setSuffix(' \u00B0')
        self._angle_edit.setFixedWidth(60)
        self._angle_edit.setToolTip(_('Ángulo'))
        self._angle_edit.setEnabled(self._enabled)
        self._angle_edit.valueChanged.connect(self._on_angle_value_changed)
        element_layout = QtWidgets.QVBoxLayout()
        element_layout.addWidget(QtWidgets.QLabel(_('Ángulo')))
        element_layout.addWidget(self._angle_edit)
        layout.addLayout(element_layout)

        self._fixation_mean_duration_edit = QtWidgets.QDoubleSpinBox(self)
        self._fixation_mean_duration_edit.setSingleStep(0.01)
        self._fixation_mean_duration_edit.setSuffix(_(' seg'))
        self._fixation_mean_duration_edit.setFixedWidth(80)
        self._fixation_mean_duration_edit.setToolTip(_('Duración de fijaciones'))
        self._fixation_mean_duration_edit.setEnabled(self._enabled)
        element_layout = QtWidgets.QVBoxLayout()
        element_layout.addWidget(QtWidgets.QLabel(_('T. Fijación')))
        element_layout.addWidget(self._fixation_mean_duration_edit)
        layout.addLayout(element_layout)

        self._fixation_variability_edit = QtWidgets.QDoubleSpinBox(self)
        self._fixation_variability_edit.setMinimum(0)
        self._fixation_variability_edit.setSingleStep(0.01)
        self._fixation_variability_edit.setSuffix(' %')
        self._fixation_variability_edit.setFixedWidth(80)
        self._fixation_variability_edit.setToolTip(_('Variabilidad de fijaciones'))
        self._fixation_variability_edit.setEnabled(self._enabled)
        element_layout = QtWidgets.QVBoxLayout()
        element_layout.addWidget(QtWidgets.QLabel(_('Variabilidad')))
        element_layout.addWidget(self._fixation_variability_edit)
        layout.addLayout(element_layout)

        self._saccades_count = QtWidgets.QSpinBox(self)
        self._saccades_count.setMinimum(5)
        self._saccades_count.setMaximum(100)
        self._saccades_count.setSingleStep(1)
        self._saccades_count.setFixedWidth(60)
        self._saccades_count.setToolTip(_('Cantidad de sácadas'))
        self._saccades_count.setEnabled(self._enabled)
        element_layout = QtWidgets.QVBoxLayout()
        element_layout.addWidget(QtWidgets.QLabel(_('Cantidad')))
        element_layout.addWidget(self._saccades_count)

        layout.addLayout(element_layout)
        layout.addStretch()

        if self._can_remove:
            self.cancel_widget_button = QtWidgets.QPushButton('-')
            self.cancel_widget_button.setFixedWidth(20)
            self.cancel_widget_button.setFixedHeight(20)
            self.cancel_widget_button.pressed.connect(self._on_remove_pressed)
            layout.addWidget(self.cancel_widget_button)

        if self._can_add:
            self._add_widget_button = QtWidgets.QPushButton('+')
            self._add_widget_button.setFixedWidth(20)
            self._add_widget_button.setFixedHeight(20)
            self._add_widget_button.pressed.connect(self._on_add_pressed)
            layout.addWidget(self._add_widget_button)

        self.setAlignment(QtCore.Qt.AlignBottom)
        self.setLayout(layout)

    def _on_remove_pressed(self):
        self.removePressed.emit(self._index)

    def _on_add_pressed(self):
        self.addPressed.emit(self._index)

    def _on_angle_value_changed(self, value: int):
        self.angle = value

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def angle(self) -> int:
        return self._angle_edit.value()

    @angle.setter
    def angle(self, value: int):
        if self._enabled:
            self._name = _('Prueba sacádica a {angle}\u00B0').format(angle=value)
        self.setTitle(self._name)
        self._angle_edit.setValue(value)

    @property
    def fixation_duration(self) -> float:
        return self._fixation_mean_duration_edit.value()

    @fixation_duration.setter
    def fixation_duration(self, value: float):
        self._fixation_mean_duration_edit.setValue(value)

    @property
    def fixation_variability(self) -> float:
        return self._fixation_variability_edit.value()

    @fixation_variability.setter
    def fixation_variability(self, value: float):
        self._fixation_variability_edit.setValue(value)

    @property
    def saccades_count(self) -> int:
        return self._saccades_count.value()

    @saccades_count.setter
    def saccades_count(self, value: int):
        self._saccades_count.setValue(value)

    @property
    def can_add(self) -> bool:
        return self._can_add

    @property
    def can_remove(self) -> bool:
        return self._can_remove

    @property
    def json(self) -> dict:
        return {
            'name': self._name,
            'angle': self.angle,
            'fixation_duration': self.fixation_duration,
            'fixation_variability': self.fixation_variability,
            'saccades_count': self.saccades_count,
        }
