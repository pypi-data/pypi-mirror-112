import beanstalkc
import threading
import errno


class Pusher(threading.Thread):
    beans = None
    connected = False
    running = True
    tube = None

    def __init__(self, tube, host="localhost"):
        threading.Thread.__init__(self)
        self.beans = beanstalkc.Connection(host)
        self.connect()
        self.beans.use(tube)
        self.tube = tube

    def connect(self):
        if self.connected is not True:
            self.beans.connect()
            self.connected = True

    def getBuriedJob(self):
        job = self.beans.peek_buried()
        return job

    def kick(self, n=None):
        if n:
            return self.beans.kick(n)
        return self.beans.kick()

    def getStat(self):
        return self.beans.stats_tube(self.tube)

    def releaseJob(self, job, priority=None, delay=0):
        if priority:
            job.release(priority, delay)
        else:
            job.release(delay=delay)

    def buriedJob(self, job):
        job.bury()

    def setJob(self, job_message, priority=None, delay=0, ttr=3600):
        if priority:
            self.beans.put(str(job_message), priority, delay, ttr)
        else:
            self.beans.put(str(job_message), delay=delay, ttr=ttr)

    # sleep(1)

    def deleteJob(self, job):
        job.delete()

    def close(self):
        self.beans.close()


class Worker(threading.Thread):
    beanstalk = None
    running = True
    reserve_timeout = 1

    def __init__(self, tube, host="localhost", port=11300, reserve_timeout=1):
        threading.Thread.__init__(self)
        self.beanstalk = beanstalkc.Connection(host=host, port=port)
        self.beanstalk.connect()
        self.tube = tube
        # self.beanstalk.watch(tube)
        self.watchTube(tube)
        self.reserve_timeout = reserve_timeout

    def isWaiting(self):
        stat = self.beanstalk.stats_tube(self.tube)
        if stat['current-waiting'] > 0:
            return True
        return False

    def getTubes(self):
        tubes = self.beanstalk.tubes()
        #        print tubes
        return tubes

    def watchTube(self, tube):
        self.beanstalk.watch(tube)
        self.ignoreTubes(tube)

    def ignoreTubes(self, tube):
        tubes = self.getTubes()
        for t in tubes:
            if t != tube:
                self.beanstalk.ignore(t)

    def getJob(self, timeout=None):
        try:
            job = self.beanstalk.reserve(self.reserve_timeout)
        except IOError as e:
            if e.errno == errno.EPIPE:
                self.beanstalk.connect()
                job = self.beanstalk.reserve(timeout)
            else:
                raise IOError(e)
        return job

    def releaseJob(self, job, priority=None, delay=0):
        if priority:
            job.release(priority, delay)
        else:
            job.release(delay=delay)

    def deleteJob(self, job):
        job.delete()

    def buriedJob(self, job):
        job.bury()

    def getStat(self):
        return self.beanstalk.stats_tube(self.tube)

    def stop(self):
        self.running = False
        print("Worker stopped")

    def run(self):
        self.running = True
        print("Worker running")
        i = 1
        while self.running:
            job = self.beanstalk.reserve()
            #            print "Worker "+self.worker_id+" get message "+job.body
            job.delete()
            i += 1

    def close(self):
        self.beanstalk.close()
