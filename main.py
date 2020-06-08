import sys
import re
import datetime
import math
import numpy as np
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, \
    QPushButton, QApplication, QHBoxLayout, \
    QLineEdit, QMessageBox, QLabel, QSlider, QScrollArea, QFileDialog


class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(700)
        self.setMinimumHeight(610)
        self.grid = QGridLayout()
        self.enter_function_label = QLabel('Введите функцию: f(x) =')
        self.label_enter_n = QLabel('Введите n:')
        self.label_enter_p = QLabel('Введите p:')
        self.lineedit_whole_function = QLineEdit()
        self.lineeditn = QLineEdit()
        self.lineeditp = QLineEdit()
        self.visualize_button = QPushButton('Построить')
        self.save_button = QPushButton('Сохранить')
        self.save_button.setDisabled(True)
        self.labelfirstmethod = QLabel()
        self.labelsecondmethod = QLabel()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.scrollarea = QScrollArea()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setDisabled(True)
        self.slider_label = QLabel('Выберите размер точки:')
        self.slider.setMinimum(0)
        self.slider.setMaximum(10000)
        self.slider.setValue(5000)
        self.function_panel = QWidget()
        self.function_layout = QHBoxLayout()
        self.p_power_n_panel = QWidget()
        self.klayout = QHBoxLayout()
        self.buttons_panel = QWidget()
        self.buttons_layout = QHBoxLayout()

        self.initui()

    def initui(self):
        self.setWindowTitle('Интерфейс')
        self.lineeditn.setMaximumWidth(30)
        self.lineeditp.setMaximumWidth(30)
        self.visualize_button.setMaximumWidth(100)
        self.save_button.setMaximumWidth(100)

        self.function_layout.addStretch()
        self.function_layout.setContentsMargins(0, 0, 0, 0)
        self.function_panel.setLayout(self.function_layout)

        self.klayout.addStretch()
        self.klayout.setContentsMargins(0, 0, 0, 0)
        self.p_power_n_panel.setLayout(self.klayout)

        self.buttons_layout.addStretch()
        self.buttons_layout.setSpacing(100)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_panel.setLayout(self.buttons_layout)

        self.slider.setMinimumWidth(250)

        self.setLayout(self.grid)
        self.grid.setAlignment(Qt.AlignTop)

        self.function_layout.addWidget(self.enter_function_label)
        self.function_layout.addWidget(self.lineedit_whole_function)

        self.buttons_layout.addWidget(self.visualize_button)
        self.buttons_layout.addWidget(self.save_button)

        self.klayout.addWidget(self.label_enter_p)
        self.klayout.addWidget(self.lineeditp)

        self.klayout.addWidget(self.label_enter_n)
        self.klayout.addWidget(self.lineeditn)

        self.grid.addWidget(self.function_panel, 0, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.p_power_n_panel, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.slider_label, 2, 0, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.slider, 3, 0, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.buttons_panel, 4, 0, Qt.AlignLeft | Qt.AlignTop)

        self.slider.sliderReleased.connect(lambda:
                                           self.plot_from_entered(int(self.lineeditp.text()),
                                                                  int(self.lineeditn.text()),
                                                                  self.lineedit_whole_function.text()))
        self.visualize_button.clicked.connect(lambda: self.visualize())
        self.save_button.clicked.connect(lambda: self.save_figure())

        # self.show()

    def visualize(self):
        if not self.represents_int(self.lineeditn.text()) or int(self.lineeditn.text()) <= 0:
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
                self.scrollarea.deleteLater()
                self.plot_from_entered(int(self.lineeditp.text()), int(self.lineeditn.text()),
                                       self.lineedit_whole_function.text())

                self.scrollarea = QScrollArea()

                self.scrollarea.setMinimumWidth(400)
                self.scrollarea.setMinimumHeight(400)

                self.scrollarea.setBackgroundRole(QPalette.Light)
                self.scrollarea.setWidget(self.canvas)
                self.grid.addWidget(self.scrollarea, 5, 0, 1, 2)

    def plot_from_entered(self, p, n, entered_func='x + ((x**2) | (-131065))'):
        p_exp_n = p ** n
        self.slider.setDisabled(False)
        self.save_button.setDisabled(False)
        a = datetime.datetime.now()
        entered_func = entered_func.lower()
        entered_func = self.replace_in_entered_func(p, n, entered_func)
        try:
            entered_func_as_lambda = eval('lambda x: ' + entered_func)
        except SyntaxError:
            msg = QMessageBox()
            msg.setText('Введена неверная функция')
            msg.setWindowTitle('Ошибка')
            msg.exec_()
            return
        xs = [x / p_exp_n for x in np.arange(0, p_exp_n, 1)]
        fxs = [entered_func_as_lambda(x) % p_exp_n / p_exp_n for x in np.arange(0, p_exp_n, 1)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.margins(0, 0)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot(xs, fxs, 'bo', markersize=self.slider.value() / (5000 + p_exp_n/4))
        self.canvas.draw()
        b = datetime.datetime.now()
        print(b - a)

    def save_figure_without_dialog(self, save_path):
        self.figure.savefig(save_path)

    def save_figure(self):
        filename = QFileDialog.getSaveFileName(None, 'Please choose your File.',
                                               self.lineedit_whole_function.text()
                                               + '; p = ' + self.lineeditp.text() +
                                               '; n = ' + self.lineeditn.text(),
                                               "Images (*.png)")
        if filename[0]:
            self.figure.savefig(filename[0])

    def find_divisions(self, text_func, p):
        overall_division = 0
        base = p #int(self.lineeditp.text())
        all_divisions = re.findall('/{1}\d+', text_func)
        for division in all_divisions:
            overall_division += math.ceil(math.log(int(division[1:]), base))
        return overall_division

    def replace_in_entered_func(self, p, n, text_func):
        repls = [['^', '**'], ['xor', '^'], ['and', '&'], ['or', '|'], ['not', '~']]

        text_func = self.divison_expression_to_number(text_func)

        n_power = n
        n_power += self.find_divisions(text_func, p)

        for operation in repls:
            text_func = text_func.replace(operation[0], operation[1])

        rational_numbers = re.findall("r{1}\({1}\d+,{1}\d+\){1}", text_func)

        for rational in rational_numbers:
            prefix, period = rational.split(',')
            text_func = text_func.replace(rational,
                                          self.rational_to_integer(prefix[2:], period[:-1], n_power, p))
        return text_func

    def divison_expression_to_number(self, expression):
        all_division_expressions_in_brackets = re.findall('/\((.*?)\)', expression)
        for expr in all_division_expressions_in_brackets:
            expression = expression.replace('/(' + expr + ')', '/' + str(eval(expr)))
        return expression

    def rational_to_integer(self, prefix, period, n, p):
        s = prefix
        while len(s) < n:
            s = period + s
        return str(int(s[-n:], p))

    def is_prime(self, n):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False
        for divisor in range(3, int(n ** 0.5) + 1, 2):
            if n % divisor == 0:
                return False
        return True

    def represents_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def check_transitivity(self, text_func):

        entered_func_as_lambda = eval('lambda x: (' + text_func + ') % 8')

        l = list(range(0, 8))

        result = entered_func_as_lambda(l[0])
        while len(l) > 0:
            if result in l:
                l.remove(result)
            else:
                return False
            result = entered_func_as_lambda(result)
        return True


    def draw_quadratic_polynomials_plots(self, min_a, max_a, min_b, max_b, min_c, max_c, ns):
        """
        Draw plots for quadratic polynomials. Draw only for ergodic ones. ns is a list of different n.
        """

        latex = ""

        p = 2
        ergodic = 0
        non_ergodic = 0
        for a in range(min_a, max_a):
            if a == 0:
                continue
            for b in range(min_b, max_b):
                for c in range(min_c, max_c):
                    text_func = "{a}*x^2 + {b}*x + {c}".format(a=a if a >= 0 else f"({a})",
                                                               b=b if b >= 0 else f"({b})",
                                                               c=c if c >= 0 else f"({c})")

                    replaced_func = self.replace_in_entered_func(p, ns[0], text_func)

                    transitivity = self.check_transitivity(replaced_func)
                    if transitivity:
                        ergodic += 1
                        latex += f"""
                        \\begin{{figure}}[H]
                            \centering
                            \caption{{$f(x) = {text_func.replace("*", "")}$}}
                        """


                        for n in ns:
                            self.plot_from_entered(p, n, entered_func=replaced_func)
                            self.save_figure_without_dialog(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                         "plots",
                                                                         text_func.replace("*", "") +
                                                                         f", p={p}, n={n}.png"))
                            latex += f"""
                                \subfigure[$p=2, n={n}$]{{\includegraphics[width=0.32\\textwidth]{{{text_func.replace("*", "")}, p=2, n={n}.png}}}}"""

                        latex += """
                        \end{figure}

                        \par\\noindent\\rule{\\textwidth}{0.4pt}

                        """

                    else:
                        non_ergodic += 1
                    print("Original Function: {o}. Replaced Function: {f}. Transitivity: {t}".format(o=text_func,
                                                                                                     f=replaced_func,
                                                                                                     t=transitivity))

        print(f"Ergodic: {ergodic}")
        print(f"Non-Ergodic: {non_ergodic}")

        with open('latex.txt', 'w') as latex_file:
            latex_file.write(latex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    interface = Interface()
    # sys.exit(app.exec_())

    interface.draw_quadratic_polynomials_plots(min_a=-10,
                                               max_a=11,
                                               min_b=-10,
                                               max_b=11,
                                               min_c=-10,
                                               max_c=11,
                                               ns=[13, 16, 19])