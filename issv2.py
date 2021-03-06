import sys
import os
from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic
import re
from ui import *

import requests as req
import json
import geocoder
import kass

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #uic.loadUi("iss.ui", self)
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        #get_location = QAction(QIcon("bug.png"),"&Your button", self)
        #button_action.setStatusTip("This is your button")

        self.ui.get_location.clicked.connect(self.where_iss)
        self.ui.get_astrounaunts.clicked.connect(self.who_is_in_space)

        self.ui.actionGet_Astronaunts.triggered.connect(self.who_is_in_space)
        self.ui.actionGet_Location.triggered.connect(self.where_iss)


        x = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/International_Space_Station_after_undocking_of_STS-132.jpg/300px-International_Space_Station_after_undocking_of_STS-132.jpg'
        image=QImage()
        image.loadFromData(req.get(x).content)
        self.ui.iss.setPixmap(QtGui.QPixmap(image))


    def value_changed(self, i):
        print(i)

    def who_is_in_space(self):
        a=''
        URL = 'http://api.open-notify.org/astros.json'
        self.ui.astrounaunts.clear()
        r=req.get(URL)
        data = json.loads(r.text)
        kass.clearwindow()
        for dict in data['people']:
            if dict['name']:
                a=a+ dict['name']+' '+dict['craft']+'\n'
            else : continue
        self.ui.astrounaunts.setText(str(a))
   
    def where_iss(self):
        URL = 'http://api.open-notify.org/iss-now.json'
        self.ui.iss_position.clear() #clears window
        r=req.get(URL)
        data = json.loads(r.text)
        #kass.clearwindow()
        latitude =  data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        print(latitude)
        print(longitude)
        location= latitude + ',' + longitude +'\n'
        #self.iss_position.setText(location)
        
        g = geocoder.osm([latitude, longitude], method='reverse')
        #g = geocoder.osm([42.0887315,-76.0620547], method='reverse')
        c=str(g.country)
        if c == 'None':
            new_location=location + "Over Water"
            self.ui.iss_position.setText(new_location)
        else:
            b=location + "ISS is located over  " + c
            self.ui.iss_position.setText(b)
            
        location_map = 'https://maps.googleapis.com/maps/api/staticmap?center=' + latitude + ',' + longitude + '&zoom=2&maptype=hybrid&size=200x200&key=AIzaSyCtnQsWoy_AVxK7AWAHDrXOKtOr0c8GpAA'
        image_location=QImage()
        image_location.loadFromData(req.get(location_map).content)
        self.ui.location_map.setPixmap(QtGui.QPixmap(image_location))     
    
      
       
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()