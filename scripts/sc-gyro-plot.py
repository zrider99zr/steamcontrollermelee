#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015 Stany MARCEL <stanypub@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Steam Controller gyro data plot"""

from steamcontroller import SteamController
import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
import struct

def _main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle('Input Display')
    textbox = QLineEdit(w)
    textbox.move(20,20)
    textbox.resize(280,160)

    w.resize(320, 200)
    imu = {
        'gpitch' : [],
        'groll'  : [],
        'gyaw'   : [],
        'q1'     : [],
        'q2'     : [],
        'q3'     : [],
        'q4'     : [],
    }

    def update(sc, sci):
        if sci.status != 15361:
            return
        
        s = ""
        for name in imu.keys():
            s += name + " = " + sci._asdict()[name] + "\n"

    app.processEvents()
    sc = SteamController(callback=update)
    sc.handleEvents()
    sc._sendControl(struct.pack('>' + 'I' * 6,
                                0x87153284,
                                0x03180000,
                                0x31020008,
                                0x07000707,
                                0x00301400,
                                0x2f010000))
    def closeEvent(event):
        global run
        run = False
        event.accept()

    win.closeEvent = closeEvent
    app.processEvents()

    try:
        i = 0
        while run:
            i = i + 1
            sc.handleEvents()
            app.processEvents()
    except KeyboardInterrupt:
        print("Bye")


if __name__ == '__main__':
    _main()
