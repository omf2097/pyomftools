from PyQt5.QtWidgets import QMainWindow, qApp, QFileDialog
from .ui.mainwindow import Ui_MainWindow
from .state import load_file, save_to, new_file, get_current_file, get_current_file_name
from .utils import show_traceback_dialog, show_about_dialog


class AFUiApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(AFUiApp, self).__init__()
        self.setupUi(self)

        self.actionQuit.triggered.connect(qApp.quit)
        self.actionOpen.triggered.connect(self.open_file_action)
        self.actionSave.triggered.connect(self.save_file_action)
        self.actionSave_As.triggered.connect(self.save_file_to_action)
        self.actionNew.triggered.connect(self.new_file_action)
        self.actionAbout.triggered.connect(show_about_dialog)

    def refresh_title(self):
        filename = get_current_file_name()
        if filename:
            self.setWindowTitle("AF Editor ({})".format(filename))
        else:
            self.setWindowTitle("AF Editor")

    def open_file_action(self):
        dialog = QFileDialog()
        filename, _ = dialog.getOpenFileName(
            parent=self,
            caption="Open AF file",
            filter="AF Files (*.AF)",
            options=QFileDialog.Options()
        )
        if filename:
            try:
                load_file(filename)
                self.refresh_title()
            except Exception as e:
                show_traceback_dialog(
                    "Error while attempting to load file '{}': Caught exception '{}'".format(filename, str(e)))

    def save_file_action(self):
        filename = get_current_file_name()
        if filename:
            try:
                save_to(filename)
                self.refresh_title()
            except Exception as e:
                show_traceback_dialog(
                    "Error while attempting to save file '{}': Caught exception '{}'".format(filename, str(e)))

    def save_file_to_action(self):
        dialog = QFileDialog()
        filename, _ = dialog.getSaveFileName(
            parent=self,
            caption="Save AF file",
            filter="AF Files (*.AF)",
            options=QFileDialog.Options()
        )
        if filename:
            try:
                save_to(filename)
                self.refresh_title()
            except Exception as e:
                show_traceback_dialog(
                    "Error while attempting to save file '{}': Caught exception '{}'".format(filename, str(e)))

    def new_file_action(self):
        new_file()
        self.refresh_title()

