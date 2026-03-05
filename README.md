# 🛠️ Qt 上位机自动化测试实战与排障日志 (Pywinauto)

**作者**：张慧云
**项目定位**：Windows 桌面端 UI 自动化测试 / 独立排障实战记录

##  项目简介
基于 Python 编写的模拟 Qt 上位机软件，以及一套基于 `pywinauto` 编写的自动化验收测试脚本进行的简易自动化测试。
展示基础的 UI 自动化点击流程，记录了在 Windows 11 系统环境下，从环境搭建到脚本运行全生命周期中的排障过程。

##  技术栈
* **被测程序 (AUT)**：Python Qt 框架 (GUI 界面开发)
* **自动化测试工具**：`pywinauto` (uia / win32 后端)
* **运行与调试环境**：Visual Studio Code, Windows 11

---

##  排障记录 (Troubleshooting)

在实际推进桌面端自动化测试时，遇到了诸多底层环境与系统机制的阻碍。以下是三次复盘：

### 一：多 Python 环境冲突与 VS Code 解释器劫持
* **【现象】**：通过 `pip install pywinauto` 提示安装成功，但在 VS Code 运行脚本时立刻抛出 `ModuleNotFoundError`
* **【原因分析】**：系统内存在多套 Python 环境（包含 Windows 默认的微软商店诱饵快捷方式 `python.exe` 以及历史残留版本）。终端 CLI 安装库的路径（`D:\Lib\site-packages`）与 VS Code 工作区默认选中的 Python 解释器不匹配。
* **【解决方案】**：
  1. 排查多python所在位置：通过 CMD 运行 `where python` 抓取所有环境路径，利用 `pip show pywinauto` 定位真实工具包存放位置
  2. 清理环境：进入 Windows 系统设置，关闭“应用执行别名”中所有的 `python.exe` / `python3.exe` 伪装开关，卸载历史遗留python版本
  3. 统一环境上下文：在 VS Code 中通过 `Ctrl+Shift+P` 唤出 `Python: Select Interpreter`，强行对齐 D 盘的真实解释器路径

### 二：Windows 11 UWP 架构陷阱与输入法拦截
* **【现象】**：在尝试使用系统“记事本”作为自动化打字测试靶机时，能够成功拉起进程，但脚本无法向窗口内输入任何字符。
* **【分析】**：
  1. **系统架构改变**：Win11 新版记事本底层变更为 UWP 架构，`Application().start()` 抓取到的仅为“启动器壳子”，导致后续焦点丢失，报 `No windows for that process could be found`。
  2. **输入法劫持**：传统 `type_keys()` 模拟极速按键时，被系统默认的中文拼音输入法候选框阻碍
* **【解决方案（转换测试策略）】**：
  放弃强绑定思路，改用“盲打测试” (Blind Automation) 策略。利用 `os.system("start notepad.exe")` 强制系统调起应用，配合 `time.sleep()` 给系统缓冲期，最后调用 `pywinauto.keyboard` 模块进行最底层的物理键盘全局模拟，成功绕过系统限制完成文本输入验证

### 三：进程阻塞与终端工作目录 (CWD) 迷失
* **【现象】**：Qt 被测软件保持运行状态时，点击 VS Code 运行测试脚本无响应；强制在终端手敲命令后报错 `[Errno 2] No such file or directory`。
* **【原因分析】**：
  1. 前台运行的 Qt GUI 软件导致当前终端进程被“阻塞 (Blocked)”，无法接收新的测试执行指令
  2. 开启新终端开辟“双车道”后，新终端的默认工作目录 (CWD) 初始化在 `C:\Users\username>`，而测试脚本实际存放在 `Desktop`，导致寻址失败
* **【解决方案】**：
  明确测试执行的“双车道”规范。终端 1 挂起被测程序，开启独立的终端 2 执行测试。在终端 2 中使用 `cd Desktop` 精准切换执行目录，随后执行 `python test_qt.py`。最终实现自动化脚本对运行中 Qt 软件的高精度跨进程抓取与点击（使用 `child_window().click()` 方法）
