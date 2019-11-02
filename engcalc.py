import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from calc_ht import htcalc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Heat transfer calculation'
        self.icon = 'pictures/chart64.png'
        self.left = 10
        self.top = 10
        self.width = 1300
        self.height = 800
        self.initUI()
                
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setGeometry(self.left, self.top, self.width, self.height)
        
         # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
       
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Input fields to change the parameters of the calculation
        self.label1a = QtWidgets.QLabel('Gas Velocity Inside')
        self.input1 = QtWidgets.QLineEdit(self)
        self.label1b = QtWidgets.QLabel('m/s')
        
        self.label2a = QtWidgets.QLabel('Gas Velocity Outside')
        self.input2 = QtWidgets.QLineEdit(self)
        self.label2b = QtWidgets.QLabel('m/s')
        
        self.label3a = QtWidgets.QLabel('Gas Temperatur Inside')
        self.input3 = QtWidgets.QLineEdit(self)
        self.label3b = QtWidgets.QLabel('°C')
        
        self.label4a = QtWidgets.QLabel('Gas Temperature Outside')
        self.input4 = QtWidgets.QLineEdit(self)
        self.label4b = QtWidgets.QLabel('°C')
        
        self.label5a = QtWidgets.QLabel('Surface area')
        self.input5 = QtWidgets.QLineEdit(self)
        self.input5.setText('1')
        self.label5b = QtWidgets.QLabel('m²')
                
        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Calculate')
        self.button.clicked.connect(self.plot)
        
        # set the layout
        layoutParam1 = QtWidgets.QHBoxLayout()
        layoutParam1.addWidget(self.label1a, 4)
        layoutParam1.addWidget(self.input1, 2)
        layoutParam1.addWidget(self.label1b, 1)
        
        layoutParam2 = QtWidgets.QHBoxLayout()
        layoutParam2.addWidget(self.label2a, 4)
        layoutParam2.addWidget(self.input2, 2)
        layoutParam2.addWidget(self.label2b, 1)
        
        layoutParam3 = QtWidgets.QHBoxLayout()
        layoutParam3.addWidget(self.label3a, 4)
        layoutParam3.addWidget(self.input3, 2)
        layoutParam3.addWidget(self.label3b, 1)
        
        layoutParam4 = QtWidgets.QHBoxLayout()
        layoutParam4.addWidget(self.label4a, 4)
        layoutParam4.addWidget(self.input4, 2)
        layoutParam4.addWidget(self.label4b, 1)
        
        layoutParam5 = QtWidgets.QHBoxLayout()
        layoutParam5.addWidget(self.label5a, 4)
        layoutParam5.addWidget(self.input5, 2)
        layoutParam5.addWidget(self.label5b, 1)
        
        layoutInput = QtWidgets.QVBoxLayout()
        layoutInput.addLayout(layoutParam1)
        layoutInput.addLayout(layoutParam2)
        layoutInput.addLayout(layoutParam3)
        layoutInput.addLayout(layoutParam4)
        layoutInput.addLayout(layoutParam5)
        layoutInput.addWidget(self.button)
        
        layoutGraph = QtWidgets.QVBoxLayout()
        layoutGraph.addWidget(self.toolbar)
        layoutGraph.addWidget(self.canvas)
        
        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutInput, 1)
        layoutMain.addLayout(layoutGraph, 3)
        self.setLayout(layoutMain)
            
    
    def plot(self):
        gasVelIn = self.input1.text()
        gasVelOut = self.input2.text()
        gasTempIn = self.input3.text()
        gasTempOut = self.input4.text()
        surfaceArea = self.input5.text()
        gg = htcalc(int(gasVelIn), int(gasVelOut), int(gasTempIn), int(gasTempOut), int(surfaceArea), 3, [0.18, 0.07, 0.03], [1.1, 0.89, 45])
        fig = gg.draw()
        self.figure.clear()
        self.figure.tight_layout()
        self.canvas.figure = fig
        self.canvas.draw()
        plt.close(fig)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    