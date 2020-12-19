
import threading
from queue import Queue
import sync_dl.config as cfg
import sync_dl 

class Runner:
    '''
    Used to run a single command at a time without locking up the UI
    Does not buffer Commands 

    '''
    def __init__(self):
        self.jobQueue = Queue(1)

        self.working=False

        self.t=threading.Thread(target = self.start)
        self.t.start()

    def addJob(self,job,plPath,*args):
        if self.working:
            cfg.logger.info("Command Currently Running")
        else:
            self.jobQueue.put((job,plPath,args))


    def start(self):
        while threading.main_thread().is_alive():
            try:
                package = self.jobQueue.get(timeout=3)
            except:
                continue

            self.working=True

            job,plPath,args=package
            try:
                job(plPath,*args)
                cfg.logger.info("Done!")
            except:
                sync_dl.plManagement.correctStateCorruption(plPath)
                cfg.logger.info("Cancelled")
            
            self.working=False


runner=Runner()