import time
import random
from multiprocessing import Process

class Piao(Process):
    def __init__(self, name):
        Process.__init__(self)
        self.name  = name
    def run(self):
        print('%s piaoing' % name)
        time.sleep(5)
        print('%s paio end' % name)




if __name__ ==  '__main__':
    print('start')
    names = ['egon', 'james', 'alex', 'sam']
    l=list(range(0,4))
    i=0
    for name in names:
        l[i]=Piao(name)
        l[i].start()
        i += 1
    l[i-1].join()

    print('end !')
