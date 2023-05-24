from PyQt5.QtCore               import QUrl
from PyQt5.QtWidgets            import QMainWindow
from PyQt5.QtWebEngineWidgets   import QWebEngineView

from dcontroller.modules        import dkit
from dcontroller.modules.web    import WebPage
from dcontroller.resource.ui.ui import Ui_MainWindow

import math
import os

class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.showMaximized()
        self.vehicle = False
        self.initialize_bttns()
        self.map()

    def initialize_bttns(self):
        self.label.hide()
        self.connectBttn.clicked.connect(self.connectDrone)

    def get_connectionInfo(self):
        connection_str = ''
        if self.comboBox.currentIndex() == 0:
            connection_str =  self.comboBox_3.currentText()
        elif self.comboBox.currentIndex() == 1:
            connection_str = f'tcp:{self.lineEdit.text()}:{self.lineEdit_2.text()}'
            print(connection_str)
        return connection_str
    
    def connectDrone(self):
        if self.connectBttn.text() == "Connect":
            connection_str = self.get_connectionInfo()
            self.vehicle = dkit.connect_to_vehicle(connection_str)
            if self.vehicle:
                self.comboBox.hide()
                self.stackedWidget.hide()
                self.label.show()
                self.label.setText(f'Type: {self.vehicle._vehicle_type}')
                self.telemetry_listener(True)

            self.connectBttn.setText("Disconnect")

        elif self.connectBttn.text() == "Disconnect":
            self.vehicle.close()
            self.telemetry_listener(False)
            self.connectBttn.setText("Connect")
            self.comboBox.show()
            self.stackedWidget.show()
            self.lable.setText(" ")
            self.label.hide()
            

    def telemetry_listener(self, off):
        
        def attitude_callback(object,attr_name, value):
            roll = math.degrees(value.roll)
            pitch = math.degrees(value.pitch)
            yaw = (math.degrees(value.yaw) + 360 ) % 360

            self.yawlbl.setText(f"{yaw:.2f} deg")
            self.pitchlbl.setText(f"{pitch:.2f} deg")
            self.rolllbl.setText(f"{roll:.2f} deg")
            
        def groundspeed_callback(object,attr_name, value):
            groundspeed = value
            self.gslbl.setText(f"{groundspeed:.2f} m/s")

        def mode_callback(self,object,attr_name, value):
            pass
            
        def altitude_callback(object,attr_name, value):
            altitude = self.vehicle.location.global_relative_frame.alt
            self.altlbl.setText(f'{altitude:.2f} m')

        def GPS_Hdop(object,attr_name, value):
            pass  
            
        def dis_to_home(object,attr_name, value):
            dist_to_home = 0
            # self..setText(f"DTH: {dist_to_home:.2f} m")

        def update_drone_on_map(object,attr_name, value):
            if self.var:
                lat = value._lat
                lon = value._lon
                js_code = f"updateDroneMarker({lat}, {lon})"
                self.webView.page().runJavaScript(js_code)   

        def arming_callback(object,attr_name, value):
            pass
            
        def airspeed_callback(object,attr_name, value):
            airspeed = value
            self.aslbl.setText(f"{airspeed:.2f} m/s")

        if not off:
            self.vehicle.add_attribute_listener('attitude', attitude_callback) 
            self.vehicle.add_attribute_listener('groundspeed', groundspeed_callback)
            self.vehicle.add_attribute_listener('mode', mode_callback)
            self.vehicle.add_attribute_listener('location', altitude_callback)
            self.vehicle.add_attribute_listener('gps_0', GPS_Hdop)      
            self.vehicle.add_attribute_listener('location',update_drone_on_map)
            self.vehicle.add_attribute_listener('battery', arming_callback)
            self.vehicle.add_attribute_listener('airspeed', airspeed_callback)

        elif off:
            self.vehicle.add_attribute_listener('attitude', attitude_callback) 
            self.vehicle.add_attribute_listener('groundspeed', groundspeed_callback)
            self.vehicle.add_attribute_listener('mode', mode_callback)
            self.vehicle.add_attribute_listener('location', altitude_callback)
            self.vehicle.add_attribute_listener('gps_0', GPS_Hdop)      
            self.vehicle.add_attribute_listener('location', update_drone_on_map)
            self.vehicle.add_attribute_listener('battery', arming_callback)
            self.vehicle.add_attribute_listener('airspeed', airspeed_callback)
        
    def map(self):
        self.var = False
        
        self.map1_obj = WebPage()
        self.webView = QWebEngineView()
        self.webView.setPage(self.map1_obj)
        
        map_path = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), "map.html"))
        
        map1_url = QUrl.fromLocalFile(map_path)
        self.webView.load(QUrl(map1_url))
        
        self.gridLayout_6.addWidget(self.webView)
        
            

        def onLoadFinished_map1(map_obj):
            if map_obj:
                self.var = True
                js_code = f"updateDroneMarker({0}, {0})"
                self.webView.page().runJavaScript(js_code)
               

        self.webView.loadFinished.connect(onLoadFinished_map1)


    
