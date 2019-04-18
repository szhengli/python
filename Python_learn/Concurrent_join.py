from multiprocessing import Process
import time
import random

def task(name):
    print("%s is piaoing " % name)
    time.sleep(10)
    print("%s is end " % name)


if __name__== "__main__":
    p = Process(target=task, args=('egon',))
    p.daemon =  True

    p.start()
    time.sleep(1)
   # p.join()

    print("zhu end")



