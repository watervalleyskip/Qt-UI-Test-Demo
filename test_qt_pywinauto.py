from pywinauto.application import Application
import time

# 1. 让机械手扫描并选中正在运行的Qt 窗口里
app = Application(backend="uia").connect(title="慧鱼科技-模拟上位机")

# 2. 锁定主窗口
window = app.window(title="慧鱼科技-模拟上位机")

# 3. 把窗口强行拉到最前面
window.set_focus()
time.sleep(1) # 停顿1秒，留缓冲时间

# 4. 让机械手寻找对应名字按钮，点击
window.child_window(title="点击测试硬件连接", control_type="Button").click()


print("自动化验收完毕：硬件连接按钮已被成功点击！")
