from PyQt5.QtWidgets import QMessageBox
import traceback
from .constants import VERSION_STRING


def show_error_dialog(error, details=None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(error)
    if details:
        msg.setInformativeText(details)
    msg.setWindowTitle("Error")
    msg.exec_()


def show_about_dialog():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("This is One Must Fall 2097 AF file editor v{}".format(VERSION_STRING))
    msg.setWindowTitle("About AF Editor v{}".format(VERSION_STRING))
    msg.exec_()


def show_traceback_dialog(error):
    show_error_dialog(error, traceback.format_exc())
