from multiprocessing import Process, Lock, Queue,JoinableQueue
from random import random, choice
import random
import  os, time, json
from hashlib import md5


def consumer(q,name):
    while True:
        res = q.get()
        time.sleep(random.randint(1,3))
        print("%s eat %s" % (name, res))
        q.task_done()

def producer(q, name, food):
    for i in range(3):
        time.sleep(random.randint(1,3))
        res = "%s %s" % (food, i)
        q.put(res)
        print("%s produces %s" % (name, res))
    q.join()

if __name__=="__main__":
    q =JoinableQueue()
    p1 = Process(target=producer, args=(q,'james','apple'))
    c1 = Process(target=consumer, args=(q,'dog'))
    c1.daemon =  True
    p1.start()
    c1.start()
    p1.join()


    print('end!')


