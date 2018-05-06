import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap, QPalette, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout,\
    QPushButton, QApplication, QHBoxLayout,\
    QLineEdit, QMessageBox, QLabel, QComboBox, QScrollArea

class Interface(QWidget):

    def __init__(self):
        super(Interface, self).__init__()
        self.grid = QGridLayout()
        self.enter_function_label = QLabel('Введите функцию: y=')
        self.label_enter_k = QLabel('Введите n:')
        self.label_enter_p = QLabel('Введите p:')
        self.lineedit_whole_function = QLineEdit()
        self.lineeditn = QLineEdit()
        self.lineeditp = QLineEdit()
        self.visualize_button = QPushButton('Построить')
        self.labelfirstmethod = QLabel()
        self.labelsecondmethod = QLabel()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.scrollarea1 = QScrollArea()
        self.scrollarea2 = QScrollArea()

        self.initui()

    def initui(self):
        self.setWindowTitle('Интерфейс')
        self.lineeditn.setMaximumWidth(30)
        self.lineeditp.setMaximumWidth(30)
        self.visualize_button.setMaximumWidth(100)



        self.polynomial_panel = QWidget()
        self.layout = QHBoxLayout()
        self.layout.addStretch()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.polynomial_panel.setLayout(self.layout)


        self.p_power_n_panel = QWidget()
        self.klayout = QHBoxLayout()
        self.klayout.addStretch()
        self.klayout.setContentsMargins(0, 0, 0, 0)
        self.p_power_n_panel.setLayout(self.klayout)

        self.enter_function_label.setMinimumWidth(100)

        self.layout.addWidget(self.enter_function_label)
        self.setLayout(self.grid)

        self.klayout.addWidget(self.label_enter_p)
        self.klayout.addWidget(self.lineeditp)

        self.klayout.addWidget(self.label_enter_k)
        self.klayout.addWidget(self.lineeditn)

        self.grid.addWidget(self.polynomial_panel, 0, 0, 1, 1, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.lineedit_whole_function, 0, 1, 1, 1, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.p_power_n_panel, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.visualize_button, 2, 0)

        self.visualize_button.clicked.connect(lambda: self.visualize())


        self.listforlabels = []
        self.listforlinedit = []
        self.show()

    def visualize(self):
        self.scrollarea2.deleteLater()
        if not self.RepresentsInt(self.lineeditn.text()) or int(self.lineeditn.text()) <= 0:
            msg = QMessageBox()
            msg.setText('Введите n; n >= 1')
            msg.setWindowTitle('Ошибка')
            msg.exec_()
        else:

            if not self.is_prime(int(self.lineeditp.text())):
                msg = QMessageBox()
                msg.setText('p должно быть простым числом')
                msg.setWindowTitle('Ошибка')
                msg.exec_()
            else:

                self.plot_from_entered(int(self.lineeditp.text()), int(self.lineeditn.text()),
                                       self.lineedit_whole_function.text())

                self.scrollarea2 = QScrollArea()

                self.scrollarea2.setMinimumWidth(400)
                self.scrollarea2.setMinimumHeight(400)

                self.scrollarea2.setBackgroundRole(QPalette.Light)
                self.scrollarea2.setWidget(self.canvas)
                self.grid.addWidget(self.scrollarea2, 4, 0, 1, 2)

    def plot_from_entered(self, p, n, entered_func):
        entered_func = self.replace_in_entered_func(entered_func)

        try:
            x = 0
            eval(entered_func)
        except:
            msg = QMessageBox()
            msg.setText('Введена неверная функция')
            msg.setWindowTitle('Ошибка')
            msg.exec_()
            exit()

        p_exp_n = p ** n
        xs = [x/ p_exp_n for x in range(p_exp_n)]
        fxs = [eval(entered_func) % p_exp_n / p_exp_n for x in range(p_exp_n)]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.margins(0, 0)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot(xs, fxs, 'ro', markersize=0.3)
        self.canvas.draw()

    def replace_in_entered_func(self, text_func):
        repls = {'^':'**','AND':'&','OR':'|'}
        for original_operation, python_operation in repls:
            text_func = text_func.replace(original_operation, python_operation)
        return text_func

    def is_prime(self, n):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False
        for divisor in range(3, int(n ** 0.5) + 1, 2):
            if n % divisor == 0:
                return False
        return True

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

if __name__ == '__main__':

    app = QApplication(sys.argv)
    interface = Interface()
    sys.exit(app.exec_())
