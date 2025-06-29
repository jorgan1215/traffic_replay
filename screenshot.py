'''
anthor:x30066634
date:2024/11/17
'''
import io
import time

from selenium import webdriver
import os
import datetime
import csv
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
def get_screenshot(path,pretext="",endtext=""):
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  # 隐身模式（无痕模式）
  options.add_argument('--incognito')
  # 不显示浏览器被自动化控制
  options.add_experimental_option('excludeSwitches', ['enable-automation'])
  # 添加谷歌浏览器驱动位置
  # chrome_options.binary_location = r"E:\应用\谷歌浏览器插件\chrome-win64\chrome.exe"
  # 加载启动项页面全屏效果，相当于F11。
  options.add_argument("--kiosk")
  driver = webdriver.Chrome(options=options)

  try:
    os.makedirs(path)
  except:
    pass
  # 获取地址
  with open("urls.csv","r",encoding="utf-8") as csv_file:
    csv_reader=csv.reader(csv_file,delimiter=",",skipinitialspace=True)
    # 跳过首行
    next(csv_reader)
    pre_row_url=""
    pro_row_env=""
    for row in csv_reader:
      name = str(row[0])
      url = str(row[1])
      env = str(row[2])
      sleep_time = int(row[3])
      square = str(row[4])
      file_name = f"{path}/{pretext}{name}{endtext}.png"
      if name[0]=="#":
        print(f"忽略截图：{name[1:]}")
        continue
      if env!="0" and env!=pro_row_env:
        account=env.split("_")[1]
        password=env.split("_")[2]
        if env[:4]=="PROD":
          time.sleep(1000)
        elif env[:4]=="TEST":
          time.sleep(1000)
        else:
          pass
      if not url == pre_row_url:
        driver.get(url)
        try:
          time.sleep(sleep_time)
        except:
          pass
      if square == "1":
        driver.get_screenshot_as_file(file_name)
      elif square=="2":
        # 显式等待页面加载完成
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

        # 初始化滚动截图的高度
        scroll_height = 0

        # 获取页面的总高度
        total_height = driver.execute_script("return document.body.scrollHeight;")

        # 设置每次滚动的高度
        partial_screen_height = driver.execute_script("return window.innerHeight;;")
        print(partial_screen_height)

        # 保存图片的列表
        images = []

        # 循环滚动并截图，直到滚动到页面底部
        while scroll_height < total_height:
          # 执行JavaScript滚动页面
          driver.execute_script("window.scrollTo(0, {});".format(scroll_height))

          # 等待页面加载新的内容
          wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

          # 使用Selenium获取当前视窗的截图
          image_bytes = driver.get_screenshot_as_png()

          # 将截图加入到内存中的图片对象
          image = Image.open(io.BytesIO(image_bytes))
          images.append(image)

          # 更新滚动高度
          scroll_height += partial_screen_height

        # 合并图片
        full_image = Image.new('RGB', (images[0].width, sum([img.height for img in images])))

        y_offset = 0
        for img in images:
            full_image.paste(img, (0, y_offset))
            y_offset += img.height

        # 保存最终的长截图
        full_image.save(file_name)
      elif square.find("-") != -1:
        li = square.split("-")
        x1 = int(li[0])
        y1 = int(li[1])
        x2 = int(li[2])
        y2 = int(li[3])
        full_png = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(full_png))
        result = image.crop((x1, y1, x2, y2))
        result.save(file_name)
      elif square[:2] == "//":
        element = driver.find_element(By.XPATH, square)
        element.screenshot(file_name)
      else:
        print(f"忽略截图：{name}")
        continue
      print(f"截图：{name}")
      pre_row_url = url
      pre_row_env=env
  print("截图已全部完成！")
  driver.quit()

if __name__ == '__main__':
    get_screenshot("imgs")
