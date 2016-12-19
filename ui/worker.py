import grpc
from worker_pb2 import *
import threading

def init():
    global worker
    channel = grpc.insecure_channel('localhost:' + str(__worker_port))
    worker = WorkerStub(channel)

# we start this on a thread as a deadlock workaround
# because calling this method goes C++ -> Python -> C++ -> Python
# and that doesn't play nice with the locks we have to prevent data races.
# we should perhaps find some other way to prevent the deadlock.
def silence():
    threading.Thread(target=worker.Silence, args=(Empty(),)).start()

def setNumInputs(num):
    worker.SetNumInputs(NumChannels(num=num))
def setNumOutputs(num):
    worker.SetNumOutputs(NumChannels(num=num))
