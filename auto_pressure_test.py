'''
pip install apscheduler
'''
import datetime
import os
import subprocess
import shlex
import screenshot

def pressure_excute(pretext="",jmeter_location=""):
  if pretext!='' and pretext[-1]!="/":
    pretext+='/'
  if jmeter_location!='' and jmeter_location[-1]!="/":
    jmeter_location+='/'
  initial_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
  try:
    os.makedirs(f"{pretext}jtl")
    os.makedirs(f"{pretext}jmx")
    os.makedirs(f"{pretext}imgs")
  except:
    pass
  jmx_list=os.listdir(fr"{pretext}jmx")
  if not jmx_list:
    print("未找到jmx文件，程序终止")
    exit()
  for jmx in jmx_list:
    jmx_name=jmx[:-4]
    start_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    try:
      os.makedirs(f"{pretext}res/{initial_time}/{jmx_name}")
    except:
      pass
    process=subprocess.run(shlex.split(
      f"{jmeter_location}jmeter.bat -n -t {pretext}jmx/{jmx} -l {pretext}jtl/{initial_time}/{jmx_name}.jtl -e -o {pretext}res/{initial_time}/{jmx_name}"))
    end_time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    # 拍照
    screenshot.get_screenshot(f"{pretext}res/{initial_time}/{jmx_name}",f"{start_time}-{end_time}_")
    if process.returncode==0:
      print(f"报告生成成功:{jmx_name}")
    else:
      print(f"报告生成失败:{jmx_name}")
