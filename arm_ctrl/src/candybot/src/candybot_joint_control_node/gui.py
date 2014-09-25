
from PyQt4 import QtGui, QtCore


class KukaGUI(QtGui.QWidget):
    
	def __init__(self):
		super(KukaGUI, self).__init__()
        
		self.initUI()
        
	def initUI(self):               
        
		self.setGeometry(300, 300, 300, 350)        
		self.setWindowTitle('Kuka GUI')   

		hbox = QtGui.QHBoxLayout()
		
		for i in range(1,4):
			sld = QtGui.QSlider(QtCore.Qt.Vertical, self)
			sld.setGeometry(40*i,10, 30, 200);
			sld.setRange(0,1000)
			sld.setObjectName(str(i))
			#QtCore.QObject.connect(sld, QtCore.SIGNAL('valueChanged(int)'), KukaGUI.onSliderMove)
			if i==1:
				sld.setRange(0,1000)
				sld.setValue(500)
				sld.setSingleStep(1);
			if i==2:
				sld.setRange(0,1000)
				sld.setValue(500)
				sld.setSingleStep(1);	

			if (i == 3):
				sld.setRange(0,10)
				sld.setValue(5)
			sld.valueChanged.connect(self.onSliderMove)
			hbox.addWidget(sld)

		btn = QtGui.QPushButton("Stahp!",self)
		btn.setGeometry(40,250, 200, 40);
		hbox.addWidget(btn)
		btn.clicked.connect(self.claw)
        #btn.move(30, 250)
		self._sliderPositions = [0,0,0,True]
        


	def onSliderMove(self, value):

		handle = self.sender()
		ind = int(handle.objectName())
		
		self._sliderPositions[ind-1] = float(value)/1000.0 - 0.5

		if ind == 3:
			self._sliderPositions[ind-1] = float(value)/10.0 - 0.5
			print "dz", self._sliderPositions[ind-1]
		#if ind == 1:
			#_joint_positions[ind-1] = float(value)/1000.0 - 0.5
			#print "dx", self._sliderPositions[ind-1]
		#elif ind == 2:
			#_joint_positions[ind-1] = float(value)/1000.0 - 0.5
			#print "dy", self._sliderPositions[ind-1]


	def claw(self):
		print "STAHP!"
		global _joint_positions;
		self._sliderPositions[-1] = False;


		
        
	def closeEvent(self, event):
		global _ex
		reply = QtGui.QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			_ex = True
			event.accept()
		else:
			event.ignore()     

	def getSliderPositions(self):

		return self._sliderPositions;