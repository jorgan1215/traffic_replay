import json
from selenium import webdriver
import os
import datetime
from browsermobproxy import  Server
import keyboard

try:
  server = Server(r"C:\Users\xingq\Desktop\AJS\autotest\temp\common_test\browsermob-proxy-2.1.4\bin\browsermob-proxy")
  server.start()
  print(f"服务已启动，监听端口：{server.port}")
  proxy = server.create_proxy()
  options = webdriver.ChromeOptions()
  options.add_argument(f"--proxy-server={proxy.proxy}")
  options.add_argument(f"--ignore-certificate-errors")
  driver = webdriver.Chrome(options=options)
  while True:
    print("---按下ESC键以开始捕获---")
    keyboard.wait("esc")
    start_time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    proxy.new_har("network", options={'captureHeaders':True,'captureContent': True,'captureBinaryContent':True})
    print("正在捕获中...\n---按下ESC键以结束捕获---")
    keyboard.wait("esc")
    end_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    har=proxy.har
    try:
      os.makedirs(r"hars")
    except:
      pass
    path=f"hars/{start_time}-{end_time}.txt"
    with open(path,"w",encoding="utf-8") as file:
      json.dump(har,file)
      print(f"HAR文件保存成功：{path}")
except Exception as e:
  print(e)
  exit()
