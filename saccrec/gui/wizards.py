from os.path import join, exists, dirname

from PySide6 import QtCore, QtWidgets

from saccrec import settings
from saccrec.gui.widgets import SubjectWidget


class SubjectWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent, workspace):
        super(SubjectWizardPage, self).__init__(parent=parent)
        self._workspace = workspace

        self.setTitle(_('Datos del sujeto'))

        self._subject_widget = SubjectWidget(workspace.subject)
        self._subject_widget.nameChanged.connect(self.on_name_changed)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._subject_widget)
        self.setLayout(self._layout)

    def reset(self):
        self._subject_widget.reset()

    def isComplete(self) -> bool:
        return self._subject_widget.subject.name.strip() != ''

    def on_name_changed(self, value: str):
        self.completeChanged.emit()


class StimulusWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent, workspace):
        super(StimulusWizardPage, self).__init__(parent)
        self._workspace = workspace
        self.setup_ui()

    def _initialize_layout(self):
        workspace = self.parent().parent()
        self._protocol = self._workspace.protocol
        self._protocol.setParent(self)
        self._layout.addWidget(self._protocol)

    def setup_ui(self):
        self.setTitle(_('Configuración del estímulo'))
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._initialize_layout()

    def reset(self):
        self._protocol.setParent(None)
        self._layout.removeWidget(self._protocol)
        self._initialize_layout()

    @property
    def json(self) -> dict:
        return self._protocol.json


class OutputWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent, workspace):
        super(OutputWizardPage, self).__init__(parent=parent)
        self._workspace = workspace
        self.setup_ui()

    def setup_ui(self):
        self.setTitle(_('Configuración de la salida'))

        layout = QtWidgets.QVBoxLayout()

        output_layout = QtWidgets.QHBoxLayout()

        self._output_path_edit = QtWidgets.QLineEdit(self)
        self._output_path_edit.textChanged.connect(self.on_output_path_changed)
        output_layout.addWidget(self._output_path_edit)

        self._output_select_button = QtWidgets.QPushButton(_('Seleccionar'), self)
        self._output_select_button.pressed.connect(self.on_output_select_clicked)
        output_layout.addWidget(self._output_select_button)

        layout.addLayout(output_layout)

        self._overview_webview = QtWidgets.QTextBrowser(self)
        # self._overview_webview.setBackgroundColor(QtCore.Qt.transparent)
        layout.addWidget(self._overview_webview)

        self.setLayout(layout)

    def reset(self):
        self._output_path_edit.setText('')

    def isComplete(self) -> bool:
        filepath = self._output_path_edit.text()
        return exists(dirname(filepath)) and filepath.lower().endswith('.rec')

    @property
    def json(self) -> str:
        return self._output_path_edit.text()

    def initializePage(self):
        self._overview_webview.setHtml(self._workspace.html_overview)

    def on_output_path_changed(self):
        self.completeChanged.emit()

    def on_output_select_clicked(self):
        subject = self._workspace.subject
        output = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _('Seleccione fichero de salida'),
            join(settings.gui.records_path, subject.code),
            filter=_('Archivo de SaccRec (*.rec)')
        )
        filepath = output[0]
        if not filepath.lower().endswith('.rec'):
            filepath += '.rec'

        self._output_path_edit.setText(filepath)
        self._workspace.filepath = filepath
        self.completeChanged.emit()


class RecordSetupWizard(QtWidgets.QWizard):
    finished = QtCore.Signal()

    def __init__(self, parent):
        super(RecordSetupWizard, self).__init__(parent)
        self._workspace = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(_('Configuración de nuevo registro'))
        self.setWizardStyle(QtWidgets.QWizard.ClassicStyle)
        self.resize(640, 480)

        self._subject_page = SubjectWizardPage(self, self._workspace)
        self._stimulus_page = StimulusWizardPage(self, self._workspace)
        self._output_page = OutputWizardPage(self, self._workspace)

        self.addPage(self._subject_page)
        self.addPage(self._stimulus_page)
        self.addPage(self._output_page)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.finish_wizard)

    def finish_wizard(self):
        self.finished.emit()

    @property
    def subject(self):
        return self.parent().subject

    @property
    def protocol(self):
        return self.parent().protocol

    def reset(self):
        self.restart()
        self._subject_page.reset()
        self._stimulus_page.reset()
        self._output_page.reset()
