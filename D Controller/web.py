
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtCore import pyqtSignal, QUrl, Qt

class WebPage(QWebEnginePage):
    web_signal = pyqtSignal(str)
    def javaScriptConsoleMessage(self, level: 'QWebEnginePage.JavaScriptConsoleMessageLevel', message: str, lineNumber: int, sourceID: str) -> None:
        #  print("checking java console msg", level,
        #        message, lineNumber, sourceID)
         print("javascript console", message, lineNumber)
         self.web_signal.emit(message)