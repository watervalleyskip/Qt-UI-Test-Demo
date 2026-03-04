import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

def on_button_click():
    # 这就是一个“槽”：按钮被点击后要发生的事
    msg = QMessageBox()
    msg.setWindowTitle("测试提醒")
    msg.setText("你好！这是一个用 Qt 做的软件窗口！")
    msg.exec_()

# 1. 创建 Qt 应用程序的环境
app = QApplication(sys.argv)

# 2. 创建一个主窗口（乐高底板）
window = QWidget()
window.setWindowTitle("慧鱼科技-模拟上位机")
window.resize(300, 200)

# 3. 创建一个按钮控件（乐高积木）
btn = QPushButton("点击测试硬件连接")
# 将按钮的“点击信号”连接到上面的“槽”函数
btn.clicked.connect(on_button_click) 

# 4. 把按钮放到窗口里排好
layout = QVBoxLayout()
layout.addWidget(btn)
window.setLayout(layout)

# 5. 显示窗口，并让程序一直运行
window.show()
sys.exit(app.exec_())