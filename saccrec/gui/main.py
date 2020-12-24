from os.path import join

from PySide6 import QtWidgets, QtGui

from saccrec import settings

import saccrec.gui.icons  # noqa: F401

from .about import AboutDialog
from .runner import Runner
from .settings import SettingsDialog


class MainWindow(
    Runner,
    QtWidgets.QMainWindow
):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Runner.__init__(self)

        self._new_record_wizard = None

        self._about_dialog = AboutDialog()
        self._settings_dialog = SettingsDialog(self)

        # self._runner.stopped.connect(self.on_runner_stopped)
        # self._runner.finished.connect(self.on_runner_finished)

        self.setup_ui()

    def setup_ui(self):
        # Setting up top level menus
        menubar = self.menuBar()

        file_menu = menubar.addMenu(_('&Study'))
        help_menu = menubar.addMenu(_('&Help'))

        # Setting up actions
        self._new_action = QtGui.QAction(QtGui.QIcon(':document.svg'), _('&New Recording'), self)
        self._new_action.triggered.connect(self.on_new_test_wizard_clicked)

        self._exit_action = QtGui.QAction(QtGui.QIcon(':exit.svg'), _('&Exit'), self)
        self._exit_action.setShortcut('Ctrl+Q')
        self._exit_action.setStatusTip(_('Exit the app'))
        self._exit_action.triggered.connect(QtWidgets.QApplication.instance().quit)

        self._settings_action = QtGui.QAction(QtGui.QIcon(':settings.svg'), _('&Settings'), self)
        self._settings_action.setShortcut('Ctrl+P')
        self._settings_action.setStatusTip(_('Configure the application'))
        self._settings_action.triggered.connect(self.open_settings_dialog)

        self._stop_action = QtGui.QAction(QtGui.QIcon(':stop-solid.svg'), _('&Stop'), self)
        self._stop_action.setShortcut('Ctrl+D')
        self._stop_action.setStatusTip(_('Stop recording'))
        self._stop_action.triggered.connect(self._on_stop_clicked)

        self._about_action = QtGui.QAction(QtGui.QIcon(':help.svg'), _('&About ...'), self)
        self._about_action.triggered.connect(self.on_about_dialog_clicked)

        help_menu.addAction(self._about_action)

        # Setting up top menu
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._settings_action)

        file_menu.addSeparator()

        file_menu.addAction(self._exit_action)

        # Setting up top toolbar
        main_toolbar = self.addToolBar('Main Toolbar')
        main_toolbar.addAction(self._new_action)
        main_toolbar.addAction(self._settings_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self._stop_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(self._exit_action)

        # Setting up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('SaccRec')
        self.setWindowIcon(QtGui.QIcon(':app.png'))

        self._setup_gui_for_non_recording()

        self.show()

    def _setup_gui_for_recording(self):
        self._new_action.setEnabled(False)
        self._exit_action.setEnabled(False)
        self._settings_action.setEnabled(False)
        self._about_action.setEnabled(False)

        self._stop_action.setEnabled(True)

    def _setup_gui_for_non_recording(self):
        self._new_action.setEnabled(True)
        self._exit_action.setEnabled(True)
        self._settings_action.setEnabled(True)
        self._about_action.setEnabled(True)

        self._stop_action.setEnabled(False)

    def on_new_test_wizard_clicked(self):
        if self._new_record_wizard is None:
            from .wizards import RecordSetupWizard

            self._new_record_wizard = RecordSetupWizard(parent=self)
            self._new_record_wizard.finished.connect(self.on_new_test_wizard_finished)

        self._new_record_wizard.show()

    def on_new_test_wizard_finished(self):
        self._new_action.setEnabled(False)
        self._settings_action.setEnabled(False)

        self.start()

    def open_settings_dialog(self):
        self._settings_dialog.open()

    def on_about_dialog_clicked(self):
        self._about_dialog.open()

    def _on_stop_clicked(self):
        answer = QtWidgets.QMessageBox.critical(
            self,
            _('Test Interruption Confirmation'),
            _('Are you sure to interrupt the test?'),
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No
        )
        if answer == QtWidgets.QMessageBox.Ok:
            self.stop()
