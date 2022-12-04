from concurrent import futures
from datetime import datetime

import threading
from multiprocessing import Process, RawValue, Lock

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import socket
import time

HOSTNAME = socket.gethostname()
GRPC_PORT = '50051'

class Counter(object):
    def __init__(self, value=0):
        # RawValue because we don't need it to create a Lock:
        self.val = RawValue('i', value)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def set(self, value):
        with self.lock:
            self.val.value = value

    def value(self):
        with self.lock:
            return self.val.value

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def __init__(self, counter):
        self.counter = counter

    def SayHello(self, request, context):
        timestamp = int(request.name)
        
        new_value = calc_recv_timestamp(timestamp, self.counter)

        self.counter.set(new_value)
        print('Message received at ' + str(HOSTNAME)  + local_time(self.counter))
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

def serve(counter):
    port = GRPC_PORT
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(counter), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter.value(),
                                                     datetime.now())

def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter.value()) + 1

def event(hostname, counter):
    counter.increment()
    print('Something happened in {} !'.\
          format(hostname) + local_time(counter))

def send_message(ip, hostname, counter):
    counter.increment()

    with grpc.insecure_channel(f'{ip}:{GRPC_PORT}') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=f'{counter.value()}'))

    print('Message sent from ' + str(hostname) + local_time(counter))

if __name__ == "__main__":
    counter = Counter()
    threading.Thread(target=serve, args=(counter,)).start()
    time.sleep(1)
    send_message(f"127.0.0.1:{GRPC_PORT}", HOSTNAME, counter)