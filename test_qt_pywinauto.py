from pywinauto.application import Application
import time

# 1. 精准连接：我们不去启动新软件，而是让机械手在屏幕上扫描，
# 直接“附身”到那个正在运行的、标题对得上的 Qt 窗口里。
app = Application(backend="uia").connect(title="慧鱼科技-模拟上位机")

# 2. 锁定主窗口
window = app.window(title="慧鱼科技-模拟上位机")

# 3. 把窗口强行拉到最前面，假装人眼看向了它
window.set_focus()
time.sleep(1) # 停顿1秒，让你看清楚它的动作

# 4. 核心杀招：长了眼睛的精准点击！
# 让机械手在窗口里寻找那个叫这个名字的按钮，然后狠狠点下去
window.child_window(title="点击测试硬件连接", control_type="Button").click()

print("自动化验收完毕：硬件连接按钮已被成功点击！")