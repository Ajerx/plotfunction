import sys
import method1
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
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
        self.label_power = QLabel('Выберите степень полинома:')
        self.label_enter_k = QLabel('Введите n:')
        self.label_enter_p = QLabel('Введите p:')
        self.combon = QComboBox()
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



        self.label_power.setMaximumWidth(150)
        self.combon.setMaximumWidth(30)


        self.layout.addWidget(self.label_power)
        self.layout.addWidget(self.combon)
        self.setLayout(self.grid)
        for item in range(0, 8):
            self.combon.addItem('{}'.format(item))
        self.combon.currentIndexChanged.connect(lambda: self.combo_changed())

        self.klayout.addWidget(self.label_enter_p)
        self.klayout.addWidget(self.lineeditp)

        self.klayout.addWidget(self.label_enter_k)
        self.klayout.addWidget(self.lineeditn)

        self.grid.addWidget(self.polynomial_panel, 0, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.lineedit_whole_function, 0, 2, 1, 2, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.p_power_n_panel, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(self.visualize_button, 2, 0)

        self.visualize_button.clicked.connect(lambda: self.visualize())


        self.listforlabels = []
        self.listforlinedit = []
        self.show()

    def combo_changed(self):

        for i in self.listforlinedit:
            i.deleteLater()
        for i in self.listforlabels:
            i.deleteLater()

        self.listforlabels = []
        self.listforlinedit = []

        # if self.combon.currentText() != '0':
        for k in range(int(self.combon.currentText()), -1, -1):
            le = QLineEdit()
            # le.setAlignment(Qt.AlignTop)
            le.setObjectName('LineEdit{}'.format(k))
            le.setMaximumWidth(30)
            self.listforlinedit.append(le)
            self.layout.addWidget(le)

            if k == 0:
                lab = QLabel()
            elif k == 1:
                lab = QLabel('*x + ')
            else:
                lab = QLabel('*x^'+str(k)+' + ')
            lab.setObjectName('Label{}'.format(k))
            self.listforlabels.append(lab)
            self.layout.addWidget(lab)

    def visualize(self):
        # self.labelfirstmethod.deleteLater()
        # self.labelsecondmethod.deleteLater()

        # self.labelfirstmethod = QLabel('1-й способ:')
        # self.labelsecondmethod = QLabel('2-й способ:')

        self.scrollarea1.deleteLater()
        self.scrollarea2.deleteLater()


        if not self.RepresentsInt(self.lineeditn.text()) or int(self.lineeditn.text()) <= 0:
            msg = QMessageBox()
            msg.setText('Введите n; n >= 1')
            msg.setWindowTitle('Ошибка')
            msg.exec_()
        else:
            dictfordrawing = {}
            # if self.combon.currentText() == '0':
            #     msg = QMessageBox()
            #     msg.setText('Выберите степень полнинома больше 0')
            #     msg.setWindowTitle('Ошибка')
            #     msg.exec_()
            # else:
            if not self.is_prime(int(self.lineeditp.text())):
                msg = QMessageBox()
                msg.setText('p должно быть простым числом')
                msg.setWindowTitle('Ошибка')
                msg.exec_()
            else:
                for i in range(int(self.combon.currentText()) + 1):
                    if self.findChild(QLineEdit, "LineEdit{}".format(i)).text() == '':
                        dictfordrawing[i] = 0
                    elif not self.RepresentsInt(self.findChild(QLineEdit, "LineEdit{}".format(i)).text()):

                        msg = QMessageBox()
                        msg.setText('Введите целый коэффициент')
                        msg.setWindowTitle('Ошибка')
                        msg.exec_()
                        return None

                    else:
                        dictfordrawing[i] = int(self.findChild(QLineEdit, "LineEdit{}".format(i)).text())

                # g1 = method1.Graph(int(self.lineeditk.text()), dictfordrawing, int(self.lineeditp.text()))
                # g2 = method2.Graph(int(self.lineeditk.text()), dictfordrawing, int(self.lineeditp.text()))

                self.scrollarea1 = QScrollArea()
                label1 = QLabel()

                # pixmap1 = QPixmap(g1.path)
                # self.scrollarea1.setMinimumWidth(pixmap1.width() + 20 if pixmap1.width() + 20 < 500 else 500)
                # self.scrollarea1.setMinimumHeight(400)
                # self.scrollarea1.setMaximumWidth(pixmap1.width() + 100)
                # self.scrollarea1.setBackgroundRole(QPalette.Light)
                # label1.setPixmap(pixmap1)
                self.scrollarea1.setWidget(label1)
                self.plot_from_entered(int(self.lineeditp.text()), int(self.lineeditn.text()))
                # self.plot(int(self.lineeditp.text()), int(self.lineeditn.text()), dictfordrawing)
                # self.labelfirstmethod.setAlignment(Qt.AlignCenter)
                # self.labelfirstmethod.setFont(QFont("Times", 12, weight=QFont.Bold,  italic = True))
                # self.grid.addWidget(self.labelfirstmethod, 3, 0)
                # self.grid.addWidget(self.scrollarea1, 4, 0)


                self.scrollarea2 = QScrollArea()
                # label2 = QLabel()
                # pixmap2 = QPixmap(g2.path)
                self.scrollarea2.setMinimumWidth(400)
                self.scrollarea2.setMinimumHeight(400)

                # scrollarea2.setBackgroundRole(QPalette.Light)
                # label2.setPixmap(pixmap2)
                self.scrollarea2.setBackgroundRole(QPalette.Light)
                self.scrollarea2.setWidget(self.canvas)
                self.grid.addWidget(self.scrollarea2, 4, 0)
                #
                #
                # self.labelsecondmethod.setAlignment(Qt.AlignCenter)
                # self.labelsecondmethod.setFont(QFont("Times", 12, weight= QFont.Bold, italic = True))
                # self.grid.addWidget(self.labelsecondmethod, 3, 1)

    def plot_from_entered(self, p, n, entered_func='x + ((x**2) | (-131065))'):
        p_exp_n = p ** n
        xs = []
        fxs = []
        # current = 0
        for x in range(p_exp_n):
            xs.append(x/ p_exp_n)
            fxs.append(eval(entered_func)  % p_exp_n / p_exp_n)

            #----------
            # print(x / p_exp_n, '   ', end='')
            # print(current / p_exp_n)
            #----------
        print()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.margins(0, 0)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot(xs, fxs, 'ro', markersize=0.5)
        self.canvas.draw()

    def plot(self, p, k, coeffs):
        p_exp_k = p ** k


        xs = []
        fxs = []
        # current = 0
        for i in range(p_exp_k):
            xs.append(i/ p_exp_k)
            temp = 0
            for coefficient in range(int(self.combon.currentText()) + 1):
                temp += coeffs[coefficient] * (i ** coefficient)
            current = temp % p_exp_k
            # current = (current - 1) % p_exp_k
            # current = (2 * current ** 2 + 3 * current + 5) % a**b
            fxs.append(current/ p_exp_k)

            #----------
            print(i / p_exp_k, '   ', end='')
            print(current / p_exp_k)
            #----------
        print()
        # print(xs)
        # print(fxs)
        # xs = [element / p_exp_k for element in xs]
        # fxs = [element / p_exp_k for element in fxs]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # ax.clear()
        ax.margins(0, 0)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot(xs, fxs, 'ro', markersize=0.1)
        self.canvas.draw()

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
