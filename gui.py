import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from calc_ht import htcalc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Engineering calculations'
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
        
        # Add figure instance and canvas to plot the graph on
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Input fields to change the parameters of the calculation
        nametext = ['Gas Velocity Inside', 'Gas Velocity Outside', 'Gas Temperatur Inside', 'Gas Temperature Outside', 'Surface Area']
        unittext = ['m/s', 'm/s', '°C', '°C', 'm²']
        stdvalue = ['4', '0.5', '21', '4', '1']
        
        self.name = {}
        self.inputs = {}
        self.unit = {}
        for i in range(len(nametext)):
            self.name[i] = QtWidgets.QLabel(nametext[i])
            self.inputs[i] = QtWidgets.QLineEdit(self)
            self.inputs[i].setText(stdvalue[i])
            self.unit[i] = QtWidgets.QLabel(unittext[i])
            
        # THE button to calculate the case
        self.button = QtWidgets.QPushButton('Calculate')
        self.button.clicked.connect(self.plot)
        
        # set the layout
        layoutParam = {}
        for i in range(len(nametext)):
            layoutParam[i] = QtWidgets.QHBoxLayout()
            layoutParam[i].addWidget(self.name[i], 4)
            layoutParam[i].addWidget(self.inputs[i], 2)
            layoutParam[i].addWidget(self.unit[i], 1)
              
        layoutInput = QtWidgets.QVBoxLayout()
        for i in range(len(layoutParam)):
            layoutInput.addLayout(layoutParam[i])
        layoutInput.addWidget(self.button)
        
        layoutGraph = QtWidgets.QVBoxLayout()
        layoutGraph.addWidget(self.toolbar)
        layoutGraph.addWidget(self.canvas)
        
        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutInput, 1)
        layoutMain.addLayout(layoutGraph, 3)
        self.setLayout(layoutMain)
            
    
    def plot(self):
        gasVelIn = self.inputs[0].text()
        gasVelOut = self.inputs[1].text()
        gasTempIn = self.inputs[2].text()
        gasTempOut = self.inputs[3].text()
        surfaceArea = self.inputs[4].text()
        gg = htcalc(float(gasVelIn), float(gasVelOut), float(gasTempIn), float(gasTempOut), float(surfaceArea), 3, [0.18, 0.07, 0.03], [1.1, 0.89, 45])
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
    