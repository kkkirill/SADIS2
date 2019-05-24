from decimal import Decimal

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
import sys


class CalculatorConfig:
    def __init__(self):
        self.amount_of_blocks = 6
        self.spin_box_defaults = (0.6, 0.18, 0.19, 0.2, 0.7, 0.12)
        self.spin_box_qualification_defaults = [6, 9]
        self.edit_line_default = ''


class Calculator(QDialog):
    def __init__(self):
        super(Calculator, self).__init__()

        self.config = CalculatorConfig()
        self.ui = uic.loadUi('main.ui', self)
        self.setFixedSize(783, 574)
        self.spin_values = [value for value in self.config.spin_box_defaults]
        self.spin_values_qualification = self.config.spin_box_qualification_defaults
        self.__reset(False)
        self.__bind()

    def __reset(self, flag: bool = True):
        for i, spin_box_value in enumerate(self.config.spin_box_defaults if flag else self.spin_values, start=1):
            getattr(self, f'doubleSpinBox{i}').setValue(spin_box_value)
        for i in range(int(self.config.amount_of_blocks / 2)):
            getattr(self, f'lineEdit{i+1}').setText(self.config.edit_line_default)
        for i, value in enumerate(
                self.config.spin_box_qualification_defaults if flag else self.spin_values_qualification, start=1):
            getattr(self, f'spinBox{i+6}').setValue(value)
        self.__update()

    def __bind(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.okButton.clicked.connect(self.__calculate)
        self.resetButton.clicked.connect(self.__reset)
        self.exitButton.clicked.connect(self.close)

    def __update(self):
        for i in range(self.config.amount_of_blocks):
            self.spin_values[i] = getattr(self, f'doubleSpinBox{i+1}').value()
        for i, _ in enumerate(self.spin_values_qualification):
            self.spin_values_qualification[i] = getattr(self, f'spinBox{i+7}').value()

    def __calculate(self):
        self.__update()
        self.weights = [value / sum(self.spin_values_qualification) for value in self.spin_values_qualification]
        for i in range(1, 3):
            getattr(self, f'lineEdit{i}').setText(str(round(self.weights[i - 1], 2)))
        result = [round(self.weights[0] * self.spin_values[i] + self.weights[1] * self.spin_values[i + 3], 3) for i in
                  range(int(len(self.spin_values) / 2))]
        self.output(result)

    def output(self, result: list):
        getattr(self, f'lineEdit3').setText(str(result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()

    sys.exit(app.exec_())
