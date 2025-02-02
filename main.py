
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt5.QtGui import QPixmap # оптимізована для показу на екрані картинка
 
from PIL import Image, ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
 
styles = """
QWidget {
    background-color: rgb(9, 18, 44); 
}
QPushButton{
    color: rgb(135, 35, 65);
    padding: 10;
QLabel {
    font-weight: bold;
}
QListWidget {
    font-size: 20px;
} 

"""
styles2 = """
QWidget {
    background-color: rgb(24, 50, 129); 
}
QPushButton#bw {
    color: rgb(19, 230, 65);
    background-color: rgb(125, 1, 1);
}
QPushButton#rizkist {
    color: rgb(19, 230, 65);
    background-color: rgb(125, 1, 1);
}
QPushButton#vidzerkal {
    color: rgb(19, 230, 65);
    background-color: rgb(125, 1, 1);
}
QPushButton#right {
    color: rgb(19, 230, 65);
    background-color: rgb(125, 1, 1);
}
QPushButton#left {
    color: rgb(19, 230, 65);
    background-color: rgb(125, 1, 1);
}
QPushButton#dir {
    color: rgb(19, 230, 65);
    background-color: rgb(125, 1, 1);
}
QLabel#image {
    color: rgb(19, 230, 65);
    background-color: rgb(6, 5, 5);
}
QPushButton{
    color: rgb(208, 187, 193);
    padding: 15;
QLabel {
    font-weight: bold;
}
QListWidget {
    font-size: 15px;
} 

"""

app = QApplication([])
app.setStyleSheet(styles2)
win = QWidget()      
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Картинка")
lb_image.setObjectName("image")
btn_dir = QPushButton("Папка")
btn_dir.setObjectName("dir")
lw_files = QListWidget()
 
btn_left = QPushButton("Вліво")
btn_left.setObjectName("left")
btn_right = QPushButton("Вправо")
btn_right.setObjectName("right")
btn_flip = QPushButton("Відзеркалити")
btn_flip.setObjectName("vidzerkal")
btn_sharp = QPushButton("Різкість")
btn_sharp.setObjectName("rizkist")
btn_bw = QPushButton("Ч/Б")
btn_bw.setObjectName("bw")
 
row = QHBoxLayout()          # Головна лінія
col1 = QVBoxLayout()         # ділиться на два стовпці
col2 = QVBoxLayout()
col1.addWidget(btn_dir)      # в першому - кнопка вибору каталогу
col1.addWidget(lw_files)     # і список файлов
col2.addWidget(lb_image, 95) # в другому - картинка
row_tools = QHBoxLayout()    # і ряд кнопок
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
 
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
 
win.show()
 
workdir = ''
 
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
 
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()
 
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
 
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)
 
btn_dir.clicked.connect(showFilenamesList)
 
class ImageProcessor():
   def __init__(self):
       self.image = None
       self.dir = None
       self.filename = None
       self.save_dir = "Modified/"
 
   def loadImage(self, filename):
       ''' під час завантаження запам'ятовуємо шлях та ім'я файлу '''
       self.filename = filename
       fullname = os.path.join(workdir, filename)
       self.image = Image.open(fullname)
 
   def saveImage(self):
       ''' зберігає копію файлу у підпапці '''
       path = os.path.join(workdir, self.save_dir)
       if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
       fullname = os.path.join(path, self.filename)
 
       self.image.save(fullname)
 
   def do_bw(self):
       self.image = self.image.convert("L")
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_left(self):
       self.image = self.image.transpose(Image.ROTATE_90)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def do_right(self):
       self.image = self.image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def do_flip(self):
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def showImage(self, path):
       lb_image.hide()
       pixmapimage = QPixmap(path)
       w, h = lb_image.width(), lb_image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       lb_image.setPixmap(pixmapimage)
       lb_image.show()
 
def showChosenImage():
   if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(filename)
       workimage.showImage(os.path.join(workdir, workimage.filename))
 
workimage = ImageProcessor() #поточне робоче зображення для роботи
lw_files.currentRowChanged.connect(showChosenImage)
 
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
 
app.exec()



