import sys
import matlab.engine as matlab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from scipy.integrate import simps
from scipy.signal import find_peaks
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog,QApplication,QVBoxLayout
from PyQt5 import QtCore,QtGui



class MatlabBaglanti():
    
    def __init__(self,zaman,aci):
        self.motor = matlab.start_matlab()
        self.zaman=zaman
        self.aci=aci
        

    
    def ModelYukle(self):
        self.motor.eval("model = 'ModelModelModel'",nargout=0)
        self.motor.eval("load_system(model)",nargout=0)
    
    def Simule(self):
        
        #self.metin='Simülasyon Başlıyor...'
        self.motor.eval("set_param(model,'StopTime','"+str(self.zaman)+"')",nargout=0)
        self.motor.set_param('ModelModelModel/Glider1/aci','value',str(self.aci),nargout=0)
        self.motor.eval("sim(model)",nargout=0)
        #self.metin='Simülasyon Tamamlandı'
        self.zaman = np.array(self.motor.workspace['tout'])
        self.hiz = np.matrix(self.motor.workspace['Velocity'])
        self.results= np.matrix(self.motor.workspace['results'])
        self.soc = self.results[:,0]
        self.guc = self.results[:,4]
        self.tork = self.results[:,13]
        
    def SonucGoster(self):
        
        fig = plt.figure(figsize=(30,20))
        plt.suptitle('Zamana Göre Simülasyon Çıktıları',fontsize=30)


        plt.subplot(2, 2, 1)
        plt.plot(self.zaman,self.hiz,color='green')
        plt.ylabel('Hız (Mil/Saat)', fontsize=20)
        plt.xlabel('Zaman (s)', fontsize=20)

        plt.subplot(2, 2, 2)
        plt.plot(self.zaman,self.soc,color='green')
        plt.ylabel('State of Charge (%)', fontsize=20)
        plt.xlabel('Zaman (s)', fontsize=20)

        plt.subplot(2, 2, 3)
        plt.scatter(np.array(self.hiz),np.array(self.guc),marker='o',color='gray')
        plt.ylabel('Batarya Gücü', fontsize=20)
        plt.xlabel('Hız', fontsize=20)

        plt.subplot(2, 2, 4)
        plt.scatter(np.array(self.hiz),np.array(self.tork),marker='v',color='gray')
        plt.ylabel('Tork', fontsize=20)
        plt.xlabel('Hız', fontsize=20)
        plt.show()


 
    
        
    def PeakGoster(self):
    
        metin="Hızın Peak Yaptığı Saniyeler :\n"
        x = np.array(self.zaman).reshape(-1,)
        y = np.array(self.hiz).reshape(-1,)
        self.peaks, _ = find_peaks(y)
        self.peaknokta = [x /10 for x in self.peaks]
        for i in range (0,len(self.peaknokta)):
            metin+=str(i+1)+". --> "+str(self.peaknokta[i])+"\n"
        plt.plot(y)
        plt.plot(self.peaks, y[self.peaks], "x")
        plt.text(50, 30, metin, fontsize=10)
        plt.grid(True)
        plt.show()
        
    


class Pencere(QDialog):
    
    def __init__(self):
        super(Pencere,self).__init__()
        loadUi("C:\\Users\\Public\\interface.ui",self)

        self.pushButton.clicked.connect(self.Baglan)
        self.pushButton_2.clicked.connect(self.SimulasyonCikti)
        self.pushButton_3.clicked.connect(self.PeakCikti)

    def Baglan(self):
        self.simulasyonzaman=int(self.sure.value())
        self.egimaci=int(self.dial.value())
        self.progressBar.setValue(25)
        self.label_2.setText('MATLAB Başlatılıyor...')
        self.motor=MatlabBaglanti(self.simulasyonzaman,self.egimaci)
        self.label_2.setText('MATLAB Başlatıldı')
        self.progressBar.setValue(50)
        self.label_3.setText('Model Yükleniyor...')
        self.motor.ModelYukle()
        self.label_3.setText('Model Yüklendi')
        self.progressBar.setValue(75)
        self.label_4.setText('Simülasyon Başlıyor...')
        self.motor.Simule()
        self.label_4.setText('Simülasyon Tamamlandı')
        self.progressBar.setValue(100)
        self.MesafeGoster()
        
    def MesafeGoster(self):
        x=list(np.array(self.motor.hiz).reshape(-1,))
        y=list(np.array(self.motor.zaman).reshape(-1,))
        y1 = [x * saniyetosaat for x in y]
        alan=simps(x,y1)
    
        fig, ax = plt.subplots()
        ax.set_title('Alınan mesafe :{} mil / {} kilometre'.format(round(alan,2),round(1.609344*alan,2)))
        ax.fill_between(y,x, 0,
                         color='red',      
                         alpha=0.2);

        self.plotWidget = FigureCanvas(fig)
        lay = QVBoxLayout(self.content_plot)  
        lay.setContentsMargins(0, 0, 0, 0)      
        lay.addWidget(self.plotWidget)
        plt.close(fig)
    def PeakCikti(self):
        self.motor.PeakGoster()
        
        
    def SimulasyonCikti(self):
        self.motor.SonucGoster()
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    widget=Pencere()
    widget.show()

    app.exit(app.exec())
