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
from time import sleep
import pandas as pd  
from prettytable import PrettyTable
import os
import sys



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
        df = self.get_work_table()
        wait = WebDriverWait(self.driver, 30)
        ## frame 内嵌页面需要切换 switch_to
        wait.until(EC.presence_of_element_located((By.ID, 'topFrameSet')))

        self.driver.switch_to.frame('leftup')
        ## 我的申请
        self.driver.find_element(By.ID, 'RightNavigationMenu_MenuSectionssb.atm.menu.myapplication_SectionHeader').click()
        ## 调休申请
        self.driver.find_element(By.ID, 'MenuSection_ssb.atm.menu.item.ajustrestapp').click()
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
        df['上班时间'] = work_time[3:8]
        for key, value in zip(df.columns.tolist(), df.iloc[0,:].to_list()): 
            ## >右对齐  < 左对齐  ,千分位,填充 ^居中 https://blog.csdn.net/chinesehuazhou2/article/details/110016578
            # print("{} : {}".format(self.algin(key, 9), value)) 
            print("{} : {}".format(self.fillempty(key, 8), value)) 
        # table2 = PrettyTable()  
        # # 添加列名  
        # table2.field_names = df.columns.tolist()
        # # 遍历 DataFrame 的每一行，添加到 PrettyTable  
        # for row in df.itertuples(index=False, name=None):
        #     table2.add_row(row)
        # # 打印表格
        # print(table2)
        # 等待
        sleep(1)
        if len(sys.argv) > 1 and sys.argv[1] == '1':
            output_excel_path = '/home/6407002602@zte.intra/Desktop/ii.xlsx'  
            sheet_name = 'Sheet3'
            if not df.empty:  
                if os.path.exists(output_excel_path):  
                    # 如果文件已存在，则追加数据  
                    with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:  
                        # 需要先读取现有的Excel文件以找到sheet，因为'a'模式不支持直接指定sheet名  
                        book = pd.ExcelFile(output_excel_path)  
                        if sheet_name in book.sheet_names:  
                            # 如果sheet存在，则读取后追加  
                            existing_df = pd.read_excel(book, sheet_name=sheet_name)  
                            combined_df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates()
                            combined_df.to_excel(writer, sheet_name=sheet_name, index=False)  
                        else:  
                            # 如果sheet不存在，则直接写入  
                            df.to_excel(writer, sheet_name=sheet_name, index=False)  
                else:  
                    # 如果文件不存在，则创建新文件并写入数据  
                    df.to_excel(output_excel_path, sheet_name=sheet_name, index=False)  
        
                print("数据已成功追加到 '~/Desktop/ii.xlsx' Excel文件的 'Sheet3' 中。")  
            else:  
                print("获取到的 我的考勤 数据为空。")

        ## todo: 异常考勤  考勤统计
    def get_work_table(self):
        """
        获取 我的考勤 表格数据
        """
        wait = WebDriverWait(self.driver, 30)
        ## frame 内嵌页面需要切换 switch_to
        wait.until(EC.presence_of_element_located((By.ID, 'topFrameSet')))
        self.driver.switch_to.frame('leftup')
        ## 我的考勤
        self.driver.find_element(By.ID, 'RightNavigationMenu_MenuSectionssb.atm.menu.mycheck_SectionHeader').click()
        ## 我的考勤统计
        self.driver.find_element(By.ID, 'MenuSection_ssb.atm.menu.item.mycheckstat').click()
        self.driver.switch_to.default_content()
        ## 调休申请 内嵌页面
        self.driver.switch_to.frame('right')
        sleep(1)
        ## 点击查询按钮
        self.driver.find_element(By.ID, 'btnSearch').click()
        table = self.driver.find_element(By.ID, 'dgrdByPerson')
        
        # 获取所有行  
        rows = table.find_elements(By.TAG_NAME, 'tr')[:2]
        keys = [header.text for header in rows[0].find_elements(By.TAG_NAME, 'td')]  # 如果是<td>标签  
        values = [value.text for value in rows[1].find_elements(By.TAG_NAME, 'td')]  # 假设第二行是<td>标签  
        df = pd.DataFrame([values], columns=keys)
        df['查询范围'] = self.driver.find_element(By.ID, 'txtBeginDate').get_attribute('value') + ' ~ ' + self.driver.find_element(By.ID, 'txtEndDate').get_attribute('value')
        # 格式化输出  
        # for key, value in zip(keys, values):  
        #     print(f"{key}: {value}") 
        # # 遍历行  
        # for row in rows:  
        #     # 获取单元格  
        #     cols = row.find_elements(By.TAG_NAME, 'td')  
        #     cols = [ele.text for ele in cols]  # 获取单元格文本  
        #     print(cols)  # 打印单元格数据列表
                # 等待
        self.driver.switch_to.default_content()
        return df

    def is_chinese(self, ch):
        return '\u4e00' <= ch <= '\u9fff'

    def algin(self, title_key, length, max_english = 2):
        '''
        中英文 由于 字节长度不同 因此格式化的时候 无法真正的对齐
        试了 全角半角 转换的方式 还是不得行
        当前实现 控制 中英文的字符数 保持一致
        '''
        # chinese_count = 0  ## 其实用不到
        english_count = 0
        for j in str(title_key):
            if self.is_chinese(j):
                # chinese_count = chinese_count + 1
                pass
            else:
                english_count = english_count + 1

        temp = max_english - english_count
        while temp > 0:
            #title_key = title_key + ' ' 在右边加 就是左对齐 使用 ljust
            title_key = '\u0020' + title_key
            temp = temp - 1
        title_key = title_key.rjust(length, '\u3000')
        #title_key = title_key.ljust(20, chr(12288))
        # print(title_key + '-')
        return title_key
    
    def fillempty(self, ustring, length):
        '''
        此方法就是 计算出所需要的 显示宽度 然后补充相应宽度的 空格 字符数是不统一的
        '''
        # 输出字符串的显示宽度为指定宽度（非域宽） 之前一直认为 中文3 英文2 后改成 中文2 英文1后 显示正常
        width = length * 2
        for uchar in ustring:
            width -= 2 if self.is_chinese(uchar) else 1
        if width <0:
            try:
                # 抛出一个异常
                raise ValueError("Error: 字符串长度 小于 需要显示长度")
            except ValueError as e:
                # 打印异常信息
                print(e)
                # 退出脚本
                sys.exit(1)
        return ' ' * width + ustring

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
    # auto_test.get_work_table()
    auto_test.gettime()
    auto_test.close_browser()
# Ended by AICoder, pid:fed84g642dc8c60146e20afdf04f658742a144cd
