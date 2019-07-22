from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout, QVBoxLayout
from PyQt5.QtWidgets import QDoubleSpinBox, QComboBox, QDialogButtonBox

from saccrec.consts import SETTINGS_STIMULUS_SCREEN_WIDTH_MINIMUM
from saccrec.consts import SETTINGS_STIMULUS_SCREEN_WIDTH_MAXIMUM
from saccrec.consts import SETTINGS_STIMULUS_SCREEN_HEIGHT_MINIMUM
from saccrec.consts import SETTINGS_STIMULUS_SCREEN_HEIGHT_MAXIMUM
from saccrec.consts import SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM
from saccrec.consts import SETTINGS_STIMULUS_SACCADIC_DISTANCE_MAXIMUM

from saccrec.core.settings import Settings
from saccrec.engine.recording import list_ports

class SettingsDialog(QDialog):
    
    def __init__(self, settings: Settings, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)
        
        self._settings = settings

        layout = QVBoxLayout()

        settings_layout = QFormLayout()

        self._openbci_ports_combo = QComboBox()
        for port in list_ports():
            self._openbci_ports_combo.addItem(port, port)
        settings_layout.addRow('Puerto OpenBCI', self._openbci_ports_combo)

        stimulus_screen_size_layout = QFormLayout()

        self._stimulus_screen_width_edit = QDoubleSpinBox()
        self._stimulus_screen_width_edit.setMinimum(SETTINGS_STIMULUS_SCREEN_WIDTH_MINIMUM)
        self._stimulus_screen_width_edit.setMaximum(SETTINGS_STIMULUS_SCREEN_WIDTH_MAXIMUM)
        self._stimulus_screen_width_edit.setSuffix(' cm')
        stimulus_screen_size_layout.addRow('Ancho', self._stimulus_screen_width_edit)

        self._stimulus_screen_height_edit = QDoubleSpinBox()
        self._stimulus_screen_height_edit.setMinimum(SETTINGS_STIMULUS_SCREEN_HEIGHT_MINIMUM)
        self._stimulus_screen_height_edit.setMaximum(SETTINGS_STIMULUS_SCREEN_HEIGHT_MAXIMUM)
        self._stimulus_screen_height_edit.setSuffix(' cm')
        stimulus_screen_size_layout.addRow('Alto', self._stimulus_screen_height_edit)

        settings_layout.addRow('Pantalla de Estímulo', stimulus_screen_size_layout)

        self._stimulus_saccadic_distance_edit = QDoubleSpinBox()
        self._stimulus_saccadic_distance_edit.setMinimum(SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM)
        self._stimulus_saccadic_distance_edit.setMaximum(SETTINGS_STIMULUS_SACCADIC_DISTANCE_MAXIMUM)
        self._stimulus_saccadic_distance_edit.setSuffix(' cm')

        settings_layout.addRow('Distancia de estímulo sacádico', self._stimulus_saccadic_distance_edit)

        layout.addLayout(settings_layout)

        dialog_buttons = QDialogButtonBox()
        dialog_buttons.addButton('Aplicar', QDialogButtonBox.AcceptRole)
        dialog_buttons.addButton('Cancelar', QDialogButtonBox.RejectRole)
        dialog_buttons.accepted.connect(self.on_accepted)
        dialog_buttons.rejected.connect(self.on_rejected)

        layout.addWidget(dialog_buttons)

        self.setLayout(layout)

    def open(self):
        if self._openbci_ports_combo.count() > 0 and self._settings.openbci_port != '':
            self._openbci_ports_combo.setCurrentIndex(self._openbci_ports_combo.findText(self._settings.openbci_port))
        else:
            self._openbci_ports_combo.setCurrentIndex(0)

        self._stimulus_screen_width_edit.setValue(self._settings.stimulus_screen_width)
        self._stimulus_screen_height_edit.setValue(self._settings.stimulus_screen_height)
        self._stimulus_saccadic_distance_edit.setValue(self._settings.stimulus_saccadic_distance)

        super(SettingsDialog, self).open()

    def on_accepted(self):
        self._settings.openbci_port = self._openbci_ports_combo.currentData()
        self._settings.stimulus_screen_width = self._stimulus_screen_width_edit.value()
        self._settings.stimulus_screen_height = self._stimulus_screen_height_edit.value()
        self._settings.stimulus_saccadic_distance = self._stimulus_saccadic_distance_edit.value()
        self.accept()

    def on_rejected(self):
        self.reject()
        