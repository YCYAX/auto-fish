import pyautogui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from functools import partial
from ui.SelectUi import SelectWindow
import io
from PIL import ImageGrab

pyautogui.FAILSAFE = False


class UIIndexWindow(QWidget):
    """
    主页ui
    """

    def __init__(self):
        super().__init__()
        self.fish_count = None
        self.slide_count = None
        self.slide_pos = None
        self.fish_pos = None
        self.bar_pos = None
        self.initUI()

    def initUI(self) -> None:
        """
        主页面ui
        :return: None
        """
        # 布局
        self.main_layout = QVBoxLayout()
        self.select_area_layout = QHBoxLayout()
        self.input_area_layout = QHBoxLayout()
        self.run_area_layout = QHBoxLayout()
        # 输入
        self.slide_count_label = QLabel("左右滑动次数")
        self.input_area_layout.addWidget(self.slide_count_label)
        self.slide_count_edit = QLineEdit()
        self.slide_count_edit.textChanged.connect(partial(self.text_changed, 'slide'))
        self.input_area_layout.addWidget(self.slide_count_edit)
        self.fish_count_label = QLabel("钓鱼次数")
        self.input_area_layout.addWidget(self.fish_count_label)
        self.fish_count_edit = QLineEdit()
        self.fish_count_edit.textChanged.connect(partial(self.text_changed, 'fish'))
        self.input_area_layout.addWidget(self.fish_count_edit)
        # 按钮
        self.select_bar_button = QPushButton("选择力量条区域")
        self.select_area_layout.addWidget(self.select_bar_button)
        self.select_bar_button.clicked.connect(partial(self.select_area, 'bar'))
        self.select_bar_label = QLabel()
        self.select_area_layout.addWidget(self.select_bar_label)
        self.select_fish_button = QPushButton("选择钓鱼区域按钮")
        self.select_area_layout.addWidget(self.select_fish_button)
        self.select_fish_button.clicked.connect(partial(self.select_area, 'fish'))
        self.select_fish_label = QLabel()
        self.select_area_layout.addWidget(self.select_fish_label)
        self.select_slide_button = QPushButton("选择左滑杆区域按钮")
        self.select_area_layout.addWidget(self.select_slide_button)
        self.select_slide_button.clicked.connect(partial(self.select_area, 'slide'))
        self.select_slide_label = QLabel()
        self.select_area_layout.addWidget(self.select_slide_label)
        # 开始 结束
        self.auto_run_button = QPushButton("开始")
        self.run_area_layout.addWidget(self.auto_run_button)
        self.auto_run_button.clicked.connect(self.auto_run)
        self.auto_stop_button = QPushButton("结束")
        self.run_area_layout.addWidget(self.auto_stop_button)
        # 标题
        self.setWindowTitle('三国杀-自动钓鱼')
        self.show()
        # 设置布局
        self.main_layout.addLayout(self.input_area_layout)
        self.main_layout.addLayout(self.select_area_layout)
        self.main_layout.addLayout(self.run_area_layout)
        self.setLayout(self.main_layout)

    def screenshot(self):
        """
        截屏
        :return: buffer
        """
        # 捕获屏幕截图
        screenshot = ImageGrab.grab()
        # 创建内存缓冲区
        buffer = io.BytesIO()
        # 将截图保存到内存缓冲区（以PNG格式为例）
        screenshot.save(buffer, format="PNG")
        # 将缓冲区指针重置到开始位置，以便后续读取
        buffer.seek(0)
        return buffer

    def select_area(self, flag):
        """
        区域选择
        :param flag: 函数接口标志
        :return:
        """
        buffer = self.screenshot()
        self.select_window = SelectWindow(buffer)
        self.select_window.show()
        self.select_window.send_pos.connect(partial(self.select_show, flag))

    def select_show(self, flag, point):
        """
        坐标显示
        :param flag: 函数接口标志
        :param point: 坐标点
        :return:
        """
        match flag:
            case 'bar':
                self.bar_pos = point
                color = point[2]
                self.select_bar_label.setText(f'{point[0]},{point[1]},{color.red(), color.green(), color.blue()}')
            case 'fish':
                self.fish_pos = point
                self.select_fish_label.setText(f'{point[0]},{point[1]}')
            case 'slide':
                self.slide_pos = point
                self.select_slide_label.setText(f'{point[0]},{point[1]}')

    def auto_run(self):
        """
        开始运行
        :return:
        """
        if (self.bar_pos is None or self.slide_pos is None or self.fish_pos is None or self.slide_count is None
                or self.fish_count is None):
            return None
        select_rgb = (self.bar_pos[-1].red(), self.bar_pos[-1].green(), self.bar_pos[-1].blue())
        while True:
            pyautogui.click(x=self.fish_pos[0], y=self.fish_pos[1], clicks=self.fish_count, interval=0.1)
            try:
                buffer = self.screenshot()
            except:
                return None
            image = buffer.getvalue()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap_color = pixmap.toImage()
            rgb_color = pixmap_color.pixelColor(self.bar_pos[0], self.bar_pos[1])
            now_rgb = (rgb_color.red(), rgb_color.green(), rgb_color.blue())
            if now_rgb != select_rgb:
                for _ in range(self.slide_count):
                    # 左滑右滑两次
                    pyautogui.click(x=self.slide_pos[0], y=self.slide_pos[1])
                    pyautogui.dragTo(self.slide_pos[0] - 50, y=self.slide_pos[1], duration=0.1)
                    pyautogui.click(x=self.slide_pos[0], y=self.slide_pos[1])
                    pyautogui.dragTo(self.slide_pos[0] + 50, y=self.slide_pos[1], duration=0.1)
                    # 蓄力
                    pyautogui.click(x=self.fish_pos[0], y=self.fish_pos[1])
                    pyautogui.dragTo(x=self.fish_pos[0], y=self.fish_pos[1] - 50, duration=0.1)
            pixmap = None
            buffer = None

    def text_changed(self, flag, text):
        """
        文本变化
        :param text: 文本内容
        :param flag: 函数接口
        """
        match flag:
            case 'slide':
                try:
                    text = int(text)
                except:
                    self.slide_count_edit.setText("")
                self.slide_count = text
            case 'fish':
                try:
                    text = int(text)
                except:
                    self.fish_count_edit.setText("")
                self.fish_count = text