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
        self.icon = '~/Insync/jan.k.peters@gmail.com/Google Drive/CODE/python/Eng_calc/Eng_calc/pictures/chart64.png'
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
        nametext = ['Gas Velocity Inside', 'Gas Velocity Outside', 'Gas Temperature Inside', 'Gas Temperature Outside', 'Surface Area']
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
        
        self.maxlayer = 5
        self.ltname = {}
        self.ltinputs = {}
        self.ltunit = {}
        self.lcname = {}
        self.lcinputs = {}
        self.lcunit = {}
        for i in range(self.maxlayer+1):
            self.ltname[i] = QtWidgets.QLabel('Thickness')
            self.ltinputs[i] = QtWidgets.QLineEdit(self)
            self.ltunit[i] = QtWidgets.QLabel('m')
            self.lcname[i] = QtWidgets.QLabel('Therm. cond.')
            self.lcinputs[i] = QtWidgets.QLineEdit(self)
            self.lcunit[i] = QtWidgets.QLabel('W/m°K')
            
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
        
        layoutlayerParam = {}
        for i in range(self.maxlayer+1):
            layoutlayerParam[i] = QtWidgets.QHBoxLayout()
            layoutlayerParam[i].addWidget(self.ltname[i], 2)
            layoutlayerParam[i].addWidget(self.ltinputs[i], 1)
            layoutlayerParam[i].addWidget(self.ltunit[i], 1)
            layoutlayerParam[i].addWidget(self.lcname[i], 2)
            layoutlayerParam[i].addWidget(self.lcinputs[i], 1)
            layoutlayerParam[i].addWidget(self.lcunit[i], 1)      
                
        layoutInput = QtWidgets.QVBoxLayout()
        for i in range(len(layoutParam)):
            layoutInput.addLayout(layoutParam[i])
        for i in range(self.maxlayer+1):
            layoutInput.addLayout(layoutlayerParam[i])
        layoutInput.addWidget(self.button)
        
        layoutGraph = QtWidgets.QVBoxLayout()
        layoutGraph.addWidget(self.toolbar)
        layoutGraph.addWidget(self.canvas)
        
        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutInput, 1)
        layoutMain.addLayout(layoutGraph, 3)
        self.setLayout(layoutMain)
            
    
    def add_layer(self):
        if self.layerbtn[0].isChecked():
            number = 1
        else:
            number = 0 
        print(number)
    
    
    def plot(self):
        self.figure.clf() # Not clearing previous plot it seems???
        gasVelIn = self.inputs[0].text()
        gasVelOut = self.inputs[1].text()
        gasTempIn = self.inputs[2].text()
        gasTempOut = self.inputs[3].text()
        surfaceArea = self.inputs[4].text()
        
        layerth = []
        for i in range(self.maxlayer+1):
            if self.ltinputs[i].text() != "" and self.ltinputs[i].text() != '0':
                layerth.append(float(self.ltinputs[i].text()))
        
        thermo = []
        for i in range(len(layerth)):
            thermo.append(float(self.lcinputs[i].text()))
        
        layernr = len(layerth)
        
        gg = htcalc(float(gasVelIn), float(gasVelOut), float(gasTempIn), float(gasTempOut), float(surfaceArea), layernr, layerth, thermo)
        fig = gg.draw()
        self.canvas.figure = fig
        self.canvas.draw()
        plt.close(fig)
        
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    