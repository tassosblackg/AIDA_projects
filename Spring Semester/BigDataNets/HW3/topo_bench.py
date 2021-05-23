import random
import subprocess
from time import time, sleep
from signal import SIGINT
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client as cl
from mininet.util import pmonitor
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI

# define num of servers and requests
NumfOfServers = 5  # <- this should be read as input from sys
NumOfRequests = 8 * NumfOfServers

# mininet topology
class MyTopology(Topo):
    def build(self, n=2):
        switch = self.addSwitch("sw1")
        embedder = self.addHost("embedder")
        self.addLink(embedder, switch)
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost("server%s" % (h + 1))
            self.addLink(host, switch)


class Embedder:
    def __init__(self):
        self.servers_load = [1 for i in range(NumOfServers)]
        self.requests = []
        self.accepted_req = 0  # count accepted requests
        self.denied_req = 0  # count denied requests from servers

    # Generate Random CPU demand requests
    def generate_requests():
        random_float_list = [
            round(random.uniform(0.05, 0.2), 2) for i in range(NumOfRequests)
        ]

        return random_float_list

    # Methods For choosing a server
    def random_server_indx():
        return random.randrange(len(self.servers_load))

    def first_fit_server_indx(cpu_req):
        return next((indx for indx, x in enumerate(self.servers_load) if x >= cpu_req))

    def best_fit_server_indx(cpu_req):
        min_val = min(val for val in self.servers_load if val >= cpu_req)
        return self.servers_load.index(min_val)

    def worst_fit_server_idx():
        max_val = max(self.servers_load)
        return self.servers_load.index(max_val)


class Server:
    pass


# Test topology benchmarks, main
def simpleTest():
    "Create and test a simple network"
    print("Clearing old topologies....\n")
    output = subprocess.run(["sudo", "mn", "-c"])
    print(output)

    # seconds = 10
    topo = MyTopology(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()

    # emb = net.get("embedder")
    # server1 = net.get("server1")
    # server2 = net.get("server2")
    # server3 = net.get("server3")
    # print(emb.IP(), server1.IP())
    # p1 = server1.popen("python3 tserver.py")
    # sleep(10)
    # res2 = emb.cmdPrint("python3 tclient.py 10.0.0.2")
    #
    # p2 = server2.popen("python3 tserver.py")
    # sleep(5)
    #
    # res3 = server3.cmdPrint("python3 tclient.py 10.0.0.3 ")
    # p1.terminate()
    # sleep(5)

    net.stop()


if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simpleTest()
