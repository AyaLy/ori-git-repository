# Started by AICoder, pid:fed84g642dc8c60146e20afdf04f658742a144cd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from random import randint
import tkinter as tk  
from tkinter import messagebox  
import threading



def auto_close_window():
    # 等待n秒
    sleep(2)
    # 注意：不能直接在这里关闭窗口，因为这会导致程序崩溃
    # 相反，我们设置一个标志位来通知主线程关闭窗口
    window.after(0, window.destroy)  # 使用after(0, ...)来在主线程中调用destroy
  
def on_close():
    # 这里可以添加一些清理代码，如果需要的话
    print("Window is closing...")


class EdgeAutoTest:
    """
    使用Edge浏览器进行自动化测试的类
    """

    def __init__(self, url):
        """
        初始化Edge浏览器并打开指定网页
        
        :param url: 要打开的网页URL
        :type url: str
        """
        self.url = url
        self.driver = None

    def open_browser(self):
        """
        打开Edge浏览器并导航到指定网页
        """
        # 尝试传参
        s = Service("/usr/bin/msedgedriver")
        # 设置Edge浏览器选项
        options = webdriver.EdgeOptions()
        # options.add_experimental_option("detach", True)
        # options.use_chromium = True
        options.add_argument("--start-maximized")  # 启动时最大化窗口
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        # options.add_argument("--incognito")  # 启动无痕模式
        # options.add_argument('--headless') #浏览器不提供可视化页面
        # options.add_argument('--no-sandbox') # 关闭沙盒模式（提高性能）
        # options.add_argument("--disable-infobars")  # 隐藏信息栏
        options.add_argument("--disable-extensions")  # 禁用所有扩展程序
        # options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截
        options.add_argument('--disable-dev-shm-usage') # 使用/dev/shm分区以避免共享内存问题
        options.add_argument('--disable-gpu') # 禁用GPU硬件加速
        # options.add_argument('--remote-debugging-port=9222') # 启用远程调试端口
        options.add_argument('--single-process')
        options.binary_location = r'/usr/bin/microsoft-edge-stable' #手动指定使用的 浏览器 位置

        # 创建Edge浏览器实例
        self.driver = webdriver.Edge(service=s, options=options)
        # self.driver.maximize_window()  #最大化浏览器窗口
        #self.driver.set_window_size(1280,720) #自定义窗口大小：
        self.driver.implicitly_wait(12)  #设置隐式时间等待
        #隐式等待：在browser.get('xxx')前 就设置，针对所有元素有效

        # 导航到指定网页
        self.driver.get(self.url)
        sleep(3)

    def gettime(self):
        """
        获取 调休申请 中 上下班时间 的文本
        """
        # 等待 查找的元素出现，最多等 N 秒
        wait = WebDriverWait(self.driver, 60)
        ## frame 内嵌页面需要切换 switch_to
        wait.until(EC.presence_of_element_located((By.ID, 'topFrameSet')))

        self.driver.switch_to.frame('leftup')
        ## 我的申请
        self.driver.find_element(By.ID, 'RightNavigationMenu_MenuSectionssb.atm.menu.myapplication_SectionHeader').click()
        sleep(2)
        ## 调休申请
        self.driver.find_element(By.ID, 'MenuSection_ssb.atm.menu.item.ajustrestapp').click()
        sleep(2)
        self.driver.switch_to.default_content()
        ## 调休申请 内嵌页面
        self.driver.switch_to.frame('right')
        sleep(1)
        ## 使用 js 方法输入文本
        js = "var element=document.getElementById('txtMemo'); element.value='调休十分钟';"
        self.driver.execute_script(js)
        #<textarea name="txtMemo" rows="2" cols="20" id="txtMemo" mlm="true" ...textarea>
        ## 使用 send_keys 方法输入文本
        # self.driver.find_element(By.ID, 'txtMemo').clear().send_keys("调休十分钟")
        # sleep(1)
        sel = self.driver.find_element(By.ID, 'GetApproveInfo1_ddlApprove')
        #Select(sel).select_by_value("471432")
        Select(sel).select_by_visible_text("钱晨00125315")
        sleep(1)
        #<option value="471432">钱晨00125315</option>
        # 获取调休页面的上下班时间
        work_time=self.driver.find_element(By.XPATH, '//*[@id="lblWorkDate"]').text
        print('text: ['+work_time+'], start: ['+work_time[3:8]+']')
        self.driver.switch_to.default_content()
        # 等待
        sleep(1)

        ## todo: 异常考勤  考勤统计
    def get_work_table(self):
        """
        获取 我的考勤 表格数据
        """
        wait = WebDriverWait(self.driver, 60)
        ## frame 内嵌页面需要切换 switch_to
        wait.until(EC.presence_of_element_located((By.ID, 'topFrameSet')))
        self.driver.switch_to.frame('leftup')
        ## 我的考勤
        self.driver.find_element(By.ID, 'RightNavigationMenu_MenuSectionssb.atm.menu.mycheck_SectionHeader').click()
        sleep(2)
        ## 我的考勤统计
        self.driver.find_element(By.ID, 'MenuSection_ssb.atm.menu.item.mycheckstat').click()
        sleep(2)
        self.driver.switch_to.default_content()
        ## 调休申请 内嵌页面
        self.driver.switch_to.frame('right')
        sleep(1)
        ## 点击查询按钮
        self.driver.find_element(By.ID, 'btnSearch').click()
        sleep(2)
        table = self.driver.find_element(By.ID, 'dgrdByPerson')  
        
        # 获取所有行  
        rows = table.find_elements(By.TAG_NAME, 'tr')[:2]
        keys = [header.text for header in rows[0].find_elements(By.TAG_NAME, 'td')]  # 如果是<td>标签  
        values = [value.text for value in rows[1].find_elements(By.TAG_NAME, 'td')]  # 假设第二行是<td>标签  
        
        # 格式化输出  
        for key, value in zip(keys, values):  
            print(f"{key}: {value}") 
        # # 遍历行  
        # for row in rows:  
        #     # 获取单元格  
        #     cols = row.find_elements(By.TAG_NAME, 'td')  
        #     cols = [ele.text for ele in cols]  # 获取单元格文本  
        #     print(cols)  # 打印单元格数据列表
                # 等待
        sleep(1)


    def close_browser(self):
        """
        关闭Edge浏览器
        """
        if self.driver:
            self.driver.quit()

# 使用示例
if __name__ == "__main__":
    url = "https://atm.zte.com.cn/ATM/UILoader/Index_Internal.aspx"
    
    auto_test = EdgeAutoTest(url)
    # 创建主窗口  
    window = tk.Tk()
    window.title("提示")
    
    # 设置窗口关闭时的回调函数  
    window.protocol("WM_DELETE_WINDOW", on_close)

    # 显示一个标签来提示用户扫码
    label = tk.Label(window, text="请在 60s 内扫码登录！", font=("Arial", 15))
    # pack(): 将小部件添加到窗口中   padx pady n个像素的水平x 垂直y填充
    label.pack(pady=20)

    # 启动一个线程来计时
    threading.Thread(target=auto_close_window).start()

    # 进入主事件循环
    window.mainloop()
    auto_test.open_browser()
    auto_test.gettime()
    auto_test.get_work_table()
    auto_test.close_browser()
# Ended by AICoder, pid:fed84g642dc8c60146e20afdf04f658742a144cd
