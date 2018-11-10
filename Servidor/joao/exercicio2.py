import threading
import time

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        nome= str(self.name)
        #nome= threading.current_thread()
        print("Rodandao: "+str(nome))
        for i in range(1,1001):
            print(str(nome)+': '+str(i))
            time.sleep(0.05)
    
        print(str(nome)+'Fim')
        #currentTreadname = threading.currentThread()
        #print( "running in", currentTreadname  )
        #print( 'threading.main_thread()', threading.main_thread())


start = threading.Event()
thread = myThread(1,"mythrd1",1)
thread2 = myThread(1,"mythrd2",1)

thread.start()
thread2.start()
start.set()


