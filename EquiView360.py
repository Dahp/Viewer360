import os
import sys
import cv2
import platform
import logging
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QDesktopWidget, QFileDialog, QProgressBar, QMessageBox, QAction, QMenuBar, QVBoxLayout

import Equirec2Perspec as E2P
import CubeProjection as CP
import convert360 as convert

# Linux systems need this env var
if platform.system() == 'Linux':
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

class Window(QDialog):
    def __init__(self):
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        super().__init__()
        self.title = "Equirectangular 360° Viewer"
        self.pos = QPoint(0, 0)
        self.fov = 100
        self.width = 1080
        self.height = 720
        self.setFixedSize(self.width, self.height)
        self.equ = None  # Initialize equ attribute as None
        self.equ = None
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("./sources/icon.png"))
        self.centerWindow()

        layout = QVBoxLayout(self)  # Create a layout for the dialog
        self.setLayout(layout)

        self.labelImage = QLabel(self)
        layout.addWidget(self.labelImage)  # Add the label to the layout

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(10, self.height - 30, self.width - 20, 20)  # Set progress bar position and size
        self.progressBar.setHidden(True)  # Hide the progress bar initially
        layout.addWidget(self.progressBar)  # Add the progress bar to the layout

        self.createMenu()

        self.show()

        # self.selectImage()
        
        if self.equ is None:
            self.selectEquirectProjection()  # Automatically select Equirectangular projection on first launch


    def centerWindow(self):
        frameRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameRect.moveCenter(centerPoint)
        self.move(frameRect.topLeft())



    def createMenu(self):
        menubar = QMenuBar(self)
        MenuFile = menubar.addMenu('Файл')
        MenuProjection = menubar.addMenu('Проекции')
        
        
        selectImageAction = QAction('Выбрать другое изображение', self)
        selectImageAction.triggered.connect(self.selectImage)
        MenuFile.addAction(selectImageAction)
        
        # ------------------ MenuConvertTOformat
        MenuConvertTOformat = MenuFile.addMenu('Перевести в формат')

        equirectAction = QAction('Из эквидистантной  в кубическую', self)
        equirectAction.triggered.connect(self.SaveEquiToCubic)
        MenuConvertTOformat.addAction(equirectAction)

        cubeAction = QAction('Из кубической в эквидистантную', self)
        cubeAction.triggered.connect(self.SaveCubicToEqui)
        MenuConvertTOformat.addAction(cubeAction)
        
        # ------------------

        resetAction = QAction('Начальный вид', self)
        resetAction.triggered.connect(self.resetView)
        menubar.addAction(resetAction)
        
        # ----------------- MenuProjection
        equirectAction = QAction('Эквидистантная', self)
        equirectAction.triggered.connect(self.selectEquirectProjection)
        MenuProjection.addAction(equirectAction)

        cubeAction = QAction('Кубическая', self)
        cubeAction.triggered.connect(self.selectCubeProjection)
        MenuProjection.addAction(cubeAction)
        
        # ------------------

        helpAction = QAction('Помощь', self)
        helpAction.triggered.connect(self.showHelp)
        MenuFile.addAction(helpAction)

        aboutAction = QAction('О программе', self)
        aboutAction.triggered.connect(self.showAbout)
        MenuFile.addAction(aboutAction)


        layout = self.layout()  # Get the dialog layout
        layout.setMenuBar(menubar)  # Set the menu bar in the layout
    
    
    def SaveEquiToCubic(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        
        # height = self.height
        height = 1440
        new_name_file = "results/" + os.path.basename(file_path)
        
        logging.info(f'new_name_file = {new_name_file}')
        logging.info(f'hight = {height}')
        logging.info(f'file_path = {file_path}')
        
        convert.SaveEquiToCubic_convert(height=height, file_path=file_path, new_name_file=new_name_file)
        
    def SaveCubicToEqui(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        
        new_name_file = "results/" + os.path.basename(file_path)
        # width = self.width 
        # height = self.height
        width = 2160
        height = 1440
        logging.info(f'new_name_file = {new_name_file}')
        logging.info(f'hight = {height}')
        logging.info(f'width = {width}')
        logging.info(f'file_path = {file_path}')
        
        convert.SaveCubicToEqui_convert(file_path, new_name_file, width, height)

        
        

        
        
    
    def resetView(self):
        self.fov = 100
        self.pos = QPoint(0, 0)
        self.updateLabelImage()

    def selectImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_path:
            self.loadImage(file_path)
        else:
            self.showErrorDialog("Image selection canceled.")

    def loadImage(self, file_path):
        self.progressBar.setValue(0)  # Reset progress bar
        self.progressBar.setHidden(False)  # Show the progress bar
        try:
            self.imgPath = cv2.imread(file_path, cv2.IMREAD_COLOR)
            self.progressBar.setValue(50)  # Update progress bar
            
            if self.projectionType == "Equirectangular":
                self.equ = E2P.Equirectangular(self.imgPath)
            elif self.projectionType == "Cube":
                self.cube = CP.CubeProjection(self.imgPath)
            
            self.updateLabelImage()
            self.progressBar.setValue(100)  # Update progress bar to indicate completion
            
            self.progressBar.setHidden(True)
    
        except Exception as e:
            self.showErrorDialog(f"Error loading image: {str(e)}")

    def selectEquirectProjection(self):
        self.projectionType = "Equirectangular"
        self.selectImage()
        
    def selectCubeProjection(self):
        self.projectionType = "Cube"
        self.selectImage()
        

    def updateLabelImage(self):
        pixmap = self.getPixmap()
        self.labelImage.setPixmap(pixmap)
        
    def getPixmap(self):
        if self.projectionType == "Equirectangular":
            if self.equ is None:
                return QPixmap()  # Return empty pixmap if equ is not initialized
            img = self.equ.GetPerspective(self.fov, self.pos.x(), self.pos.y(), self.height, self.width)
        elif self.projectionType == "Cube":
            if self.cube is None:
                return QPixmap()  # Return empty pixmap if cube is not initialized
            img = self.cube.GetPerspective()

        qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
        return QPixmap.fromImage(qimg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.pos.setY(self.pos.y() - 30)
        elif event.key() == Qt.Key_Up:
            self.pos.setY(self.pos.y() + 30)
        elif event.key() == Qt.Key_Left:
            self.pos.setX(self.pos.x() - 30)
        elif event.key() == Qt.Key_Right:
            self.pos.setX(self.pos.x() + 30)

        self.updateLabelImage()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = (event.pos() - self.mousePos) * 0.1
            self.pos += delta
            self.updateLabelImage()
            self.mousePos = event.pos()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.fov *= 1.25
        else:
            self.fov /= 1.25

        self.updateLabelImage()

    def showErrorDialog(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

    def showHelp(self):
        QMessageBox.information(self, "Help", "Put your help instructions here.")

    def showAbout(self):
        QMessageBox.about(self, "About", "Your application description here.")
    
# Launch the application
if __name__ =='__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())