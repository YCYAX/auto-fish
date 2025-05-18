from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class SelectWindow(QWidget):
    send_pos = pyqtSignal(tuple)

    def __init__(self, img):
        super().__init__()
        self.img = img.getvalue()
        self.initUI()

    def initUI(self):
        # 布局
        self.main_layout = QVBoxLayout()
        self.function_layout = QHBoxLayout()
        self.main_layout.addLayout(self.function_layout)
        # 提示
        self.original_label = QLabel()
        self.function_layout.addWidget(self.original_label)
        self.info_label = QLabel("直接用鼠标在图片上左键点击选点     坐标位置----->")
        self.function_layout.addWidget(self.info_label)
        self.postion_label = QLabel()
        self.function_layout.addWidget(self.postion_label)
        self.close_button = QPushButton("确定")
        self.close_button.clicked.connect(self.return_pos)
        self.function_layout.addWidget(self.close_button)
        # 加载图片
        self.img_label = QLabel()
        self.img_label.mousePressEvent = self.get_coordinates
        self.main_layout.addWidget(self.img_label)
        pixmap = QPixmap()
        pixmap.loadFromData(self.img)
        self.pixmap_color = pixmap.toImage()
        self.original_pixmap_height = pixmap.height()
        self.original_pixmap_width = pixmap.width()
        self.original_label.setText(f"图片原尺寸：{self.original_pixmap_width},{self.original_pixmap_height}")
        # 缩小为0.5倍
        self.displayed_pixmap_height = int(self.original_pixmap_height * 0.5)
        self.displayed_pixmap_width = int(self.original_pixmap_width * 0.5)
        pixmap = pixmap.scaled(
            self.displayed_pixmap_width, self.displayed_pixmap_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_label.setPixmap(pixmap)
        # 标题
        self.setWindowTitle('选择区域')
        # 设置布局
        self.setLayout(self.main_layout)

    def get_coordinates(self, event):
        """获取鼠标点击的坐标"""
        # 获取鼠标在标签上的坐标
        pos = event.pos()
        # 计算缩放比例
        scale_x = self.original_pixmap_width / self.displayed_pixmap_width
        scale_y = self.original_pixmap_height / self.displayed_pixmap_height
        # 转换为原始图片上的坐标
        original_x = int(pos.x() * scale_x)
        original_y = int(pos.y() * scale_y)
        # 存储坐标点
        self.point = QPoint(original_x, original_y)
        self.rgb_color = self.pixmap_color.pixelColor(self.point.x(), self.point.y())
        # 显示坐标
        self.postion_label.setText(f'{self.point.x()},{self.point.y()}')

    def return_pos(self):
        self.send_pos.emit((self.point.x(), self.point.y(), self.rgb_color))
        self.close()
