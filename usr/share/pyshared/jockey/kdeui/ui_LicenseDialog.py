#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from kde/LicenseDialog.ui on Wed Jul 15 15:57:05 2009
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

class Ui_dialog_licensetext(object):
    def setupUi(self, dialog_licensetext):
        dialog_licensetext.setObjectName("dialog_licensetext")
        dialog_licensetext.setEnabled(True)
        dialog_licensetext.resize(427, 383)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_licensetext.sizePolicy().hasHeightForWidth())
        dialog_licensetext.setSizePolicy(sizePolicy)
        dialog_licensetext.setMinimumSize(QtCore.QSize(322, 272))
        dialog_licensetext.setMaximumSize(QtCore.QSize(160000, 160000))
        self.gridLayout = QtGui.QGridLayout(dialog_licensetext)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_license_drivername = QtGui.QLabel(dialog_licensetext)
        self.label_license_drivername.setObjectName("label_license_drivername")
        self.horizontalLayout.addWidget(self.label_license_drivername)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.textview_license_text = QtGui.QTextBrowser(dialog_licensetext)
        self.textview_license_text.setEnabled(True)
        self.textview_license_text.setObjectName("textview_license_text")
        self.gridLayout.addWidget(self.textview_license_text, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(dialog_licensetext)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(dialog_licensetext)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton*)"), dialog_licensetext.accept)
        QtCore.QMetaObject.connectSlotsByName(dialog_licensetext)

    def retranslateUi(self, dialog_licensetext):
        dialog_licensetext.setWindowTitle(kdecore.i18n("Dialog"))
        self.label_license_drivername.setText(kdecore.i18n("(driver name)"))
        self.textview_license_text.setHtml(kdecore.i18n("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\">Jockey is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\">Jockey is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\">You should have received a copy of the GNU General Public License along with Jockey; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"></p></body></html>"))
