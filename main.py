import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from win32api import GetSystemMetrics
import os
from pynput.keyboard import Key, Listener
#pyinstaller -F --noconsole main.py #py to exe

count = 0
keys = []
attr = "\n"
url = ''
refference = ''

def root():
    def game_browser():
        app = QApplication(sys.argv)
        browser = QWebEngineView()

        title = "Nirvana Conquer"
        width = int((GetSystemMetrics(0) / 4) + 100)
        height = int((GetSystemMetrics(1) / 2) + 150)

        browser.setFixedWidth(width)
        browser.setFixedHeight(height)
        qtRectangle = browser.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        browser.setWindowTitle(title)

        browser.load(QUrl(url))
        browser.setWindowModality(Qt.ApplicationModal) #Block window to be resized
        browser.setWindowFlags(Qt.WindowStaysOnTopHint) #Over all apps
        browser.show()
        app.exec_()

    def write_file(keys):
        with open("log.txt", "a") as f:
            for key in keys:
                try:
                    k = key.char
                    f.write(k)
                except AttributeError:
                    if key == Key.enter:
                        f.write('\n')

    def read_file():
        with open("log.txt", "+r") as f:
            read = f.readline()
            f.truncate(0)
            global command
            command = read
        f.close()

    def read_command():
        with open("readme.txt", "+r") as f:
            readc = f.readline()
            global refference
            refference = readc
        f.close()

    def read_url():
        with open("url.txt", "+r") as f:
            readu = f.readline()
            global url
            url = readu
        f.close()

    def on_release(key):
        if key == Key.esc:
            return

    def on_press(key):
        global keys, count
        keys.append(key)
        count += 1
        #print("{0} pressed".format(key))

        if count >= 10 or key == Key.enter:
            count = 0
            write_file(keys)
            read_file()
            read_command()
            read_url()
            keys = []
            if command == refference + attr:
                os.startfile('.\\TimeDelay.exe') #comment ptr debug
                game_browser()
                sys.exit(1)

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    root()