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
import os  
import glob  
import sys
import pandas as pd  
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  
import matplotlib.dates as mdates 
from prettytable import PrettyTable  
import matplotlib.ticker as mtk
import numpy as np



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
        # self.driver.set_window_size(1280,720) #自定义窗口大小：
        self.driver.implicitly_wait(12)  #设置隐式时间等待
        # 隐式等待：在browser.get('xxx')前 就设置，针对所有元素有效

        # 导航到指定网页
        self.driver.get(self.url)

    def getaicsvfile(self):
        """
        获取 granfana ai 昨天提交率
        """
        # 等待 查找的元素出现，最多等 N 秒
        wait = WebDriverWait(self.driver, 60)
        ## 输入框处理
        
        ## 点击 详情
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="reactRoot"]/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[4]'))).click()
        sleep(4)
        
        ## js 滚动屏幕 无效
        # self.driver.execute_script("window.scrollTo(0, window.innerHeight);")
        actions = ActionChains(self.driver)
        # 模拟按下Page Down键来滚动一个屏幕
        actions.send_keys(Keys.PAGE_DOWN).perform()
        sleep(1)
        
        ## 点击 详单
        # self.driver.find_element(By.XPATH, '//*[@id="reactRoot"]/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[6]/div/section/div[1]/header/div[1]').click()
        self.driver.find_element(By.XPATH, '//*[@id="5"]/section/div[1]/header/div').click()
        sleep(2)
        
        ## 点击 inspect
        # self.driver.find_element(By.XPATH, '//*[@id="reactRoot"]/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[6]/div/section/div[1]/header/div/div[2]/div/ul/li[3]/a/span[1]').click()
        self.driver.find_element(By.XPATH, '//*[@id="5"]/section/div[1]/header/div/div[2]/div/ul/li[3]/a/span[1]').click()
        sleep(2)
        
        ## 点击 data options
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div/div[1]/div').click()
        sleep(2)
        
        ## 点击 表头字段转换为中文
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/label').click()
        sleep(2)
       
        ## 点击 提交人排序
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/div[2]/button/div[2]').click()
        sleep(randint(1,2))
        
        ## 点击 下载
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/button/span').click()
        sleep(randint(1,2))
        
        ## 文件弹出框 处理  获取网页下载按钮背后的真实下载地址（获取不到）   Python 给定一个URL链接，读取文本文件内容

    def close_browser(self):
        """
        关闭Edge浏览器
        """
        if self.driver:
            self.driver.quit()


    def write_xlsx(self):
        """将下载的csv文件中的昨天的提交信息 写入到xlsx文件中"""
        # 设置路径  
        base_path = '/home/6407002602@zte.intra/下载'  
        output_excel_path = '/home/6407002602@zte.intra/Desktop/ii.xlsx'  
        sheet_name = 'Sheet2'  
        
        # 获取昨天的日期  
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        # print(yesterday,type(yesterday)) 
        
        # 查找最新的CSV文件  
        csv_files = glob.glob(os.path.join(base_path, '详单-data-*.csv'))
        
        if csv_files:  
            latest_csv = max(csv_files, key=os.path.getctime)  
            for file in csv_files:
                if file != latest_csv:
                    os.remove(file)
                    print("已删除文件:", file)
            print(f"正在处理文件: {latest_csv}")  
            ## todo: 1. 对比 csv 与 xlsx 文件，重复的数据不在写入  2. 周期支持定义
            # 读取CSV文件  
            df = pd.read_csv(latest_csv)

            # 筛选数据   
            filtered_df = df[(df.iloc[:, 0].str.slice(0, 10) == yesterday) & (df.iloc[:, 1] == '刘宇6407002602')]  
            # filtered_df = df[df.iloc[:, 1] == '刘宇6407002602']
            # print(filtered_df.to_csv(index=False, header=False, sep=','))
            # 如果找到符合条件的数据
            if not filtered_df.empty:  
                # 读取或创建Excel文件  
                print(filtered_df.to_string(header=False, index=False))
                if os.path.exists(output_excel_path):  
                    # 如果文件已存在，则追加数据  
                    with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:  
                        # 需要先读取现有的Excel文件以找到sheet，因为'a'模式不支持直接指定sheet名  
                        book = pd.ExcelFile(output_excel_path)  
                        if sheet_name in book.sheet_names:  
                            # 如果sheet存在，则读取后追加  
                            existing_df = pd.read_excel(book, sheet_name=sheet_name)  
                            combined_df = pd.concat([existing_df, filtered_df], ignore_index=True)  
                            combined_df.to_excel(writer, sheet_name=sheet_name, index=False)  
                        else:  
                            # 如果sheet不存在，则直接写入  
                            filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)  
                else:  
                    # 如果文件不存在，则创建新文件并写入数据  
                    filtered_df.to_excel(output_excel_path, sheet_name=sheet_name, index=False)  
        
                print("数据已成功追加到 '~/Desktop/ii.xlsx' Excel文件中。")  
            else:  
                print("csv 中没有找到符合条件 'liuyu 昨天' 的数据。")
        else:  
            print("没有找到 详单-data-*.csv 文件。")


    def process_data(self, path):
        """  
        读取CSV文件，处理数据，并返回处理后的DataFrame。  

        Returns:  
            pd.DataFrame: 包含处理后的数据（合入日期、AI生成代码行、提交代码行和比率）的DataFrame。  
        """  
        # 读取CSV文件  
        book = pd.ExcelFile(path)
        sheet_name = 'Sheet2'
        ## todo: 1. 按照最近的30天 或者 自然月展示  2. 不显示周六 周日？
        df = pd.read_excel(book, sheet_name=sheet_name)  
        # df = pd.read_csv(path, parse_dates=['合入日期'], date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'))  

        # 选择需要的列  
        # filter_df = df[df.iloc[:, 1] == '刘宇6407002602']
        df['合入日期'] = pd.to_datetime(df['合入日期'],format='%Y-%m-%d %H:%M:%S')
        df = df[['合入日期', 'AI生成代码行', '提交代码行']]
        ## 筛选出30天之内的数据
        # days30ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        # df = df.loc[df['合入日期'] >= days30ago]
        df = df.tail(30)
        # 创建一个 PrettyTable 对象
        # table = PrettyTable()  
        # # 添加列名  
        # table.field_names = df.columns.tolist()  
        # # 遍历 DataFrame 的每一行，添加到 PrettyTable  
        # for row in df.itertuples(index=False, name=None):
        #     table.add_row(row)
        # # 打印表格  
        # print(table)
        # 转换为date类型（如果parse_dates在read_csv中已处理则不需要）  
        df.loc[:, '合入日期'] = pd.to_datetime(df['合入日期'], format='%Y-%m-%d %H:%M:%S').dt.date  
        # print(df)
        # print('========================================================================')
        # 计算比率并添加到DataFrame  
        grouped_df = df.groupby('合入日期', as_index=False).sum()
        # grouped_df = df.groupby('合入日期').sum().reset_index()
        grouped_df['比率'] = (grouped_df['AI生成代码行'] / grouped_df['提交代码行']).apply(lambda x: round(x * 100, 1))  
        grouped_df.loc[:, '合入日期'] = grouped_df['合入日期'].dt.strftime('%m-%d') 
        # grouped_df.loc[:, '合入日期'] = grouped_df['合入日期'].astype(str)
        # print(grouped_df)
        # print('========================================================================')
        return grouped_df  
  
    def plot_data(self):  
        """  
        使用matplotlib绘制数据图表。  
        """  
        # 处理数据  
        df = self.process_data('/home/6407002602@zte.intra/Desktop/ii.xlsx')
        # 创建一个 PrettyTable 对象  
        table2 = PrettyTable()  
        # 添加列名  
        table2.field_names = df.columns.tolist()  
        # 遍历 DataFrame 的每一行，添加到 PrettyTable  
        for row in df.itertuples(index=False, name=None):
            table2.add_row(row)
        # 打印表格
        print(table2)
        # 创建图形和轴 
        fig, ax1 = plt.subplots(1, 1, figsize=(12, 6))

        # 绘制主坐标系（比率）
        color = 'tab:red'
        ax1.set_xlabel('Date')  
        ax1.set_ylabel('ai-rate(%)', color=color)  
        ax1.plot(df['合入日期'], df['比率'], color=color)  
        ax1.tick_params(axis='y', labelcolor=color)  
        ## 格式化成 %Y-%m-%d 就会自动补上 缺失的日期
        # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  
        # ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))  
  
        # 绘制次坐标系（AI生成代码行和提交代码行）
        ax2 = ax1.twinx()  
        color = 'tab:blue'  
        ax2.set_ylabel('code-line', color=color)  
        ax2.plot(df['合入日期'], df['AI生成代码行'], color=color, linestyle='--', label='AI-line')  
        ax2.plot(df['合入日期'], df['提交代码行'], color='tab:green', linestyle='-.', label='add-line')  
        ax2.tick_params(axis='y', labelcolor=color)  
        ax2.legend(loc='upper left')
  
        # 显示图表  
        plt.title('AI-liuyu-Analyze')  
        # 自动旋转日期标记以避免重叠
        plt.gcf().autofmt_xdate()
        plt.grid(True)  
        plt.show()  


# 使用示例
if __name__ == "__main__":
    url = "https://zdsp.zx.zte.com.cn/grafana/d/GUJ_95oSk/aidai-ma-bu-men-kan-ban?orgId=1&var-department=视频研发五部"
    
    auto_test = EdgeAutoTest(url)
    if sys.argv[1] == '1':
        print('only draw')
    else:
        auto_test.open_browser()
        auto_test.getaicsvfile()
        sleep(1)
        auto_test.close_browser()
        sleep(1)
        auto_test.write_xlsx()
        sleep(1)
    auto_test.plot_data()
