'''
https://blog.csdn.net/m0_71555731/article/details/139267914
'''
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import threading
import auto_pressure_test
def task1():
  try:
    auto_pressure_test.pressure_excute("C:/Users/xingq/Desktop","D:/'Program Files'/apache-jmeter-5.6.3/bin")
  except Exception as e:
    print(e)

def task2():
  print("22读取数据...")
  time.sleep(1)
  print("22导出数据...")

def scheduler1():
  scheduler = BlockingScheduler()
  scheduler.add_job(func=task1, trigger="interval", seconds=8)
  scheduler.start()

def scheduler2():
  scheduler = BlockingScheduler()
  scheduler.add_job(func=task2, trigger="interval", seconds=4)
  scheduler.start()



if __name__ == '__main__':
  # 实例化对象
  thread1 = threading.Thread(target=scheduler1, args=())
  thread2 = threading.Thread(target=scheduler2, args=())

  # 开始线程
  thread1.start()
  thread2.start()
