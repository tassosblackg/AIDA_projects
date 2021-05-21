import random
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

# global variables
NumOfServers = 5
NumOfRequests = 8 * NumOfServers

# mininet topology
class MyTopology(Topo):
    def build(self, n=2):
        switch = self.addSwitch("s1")
        embedder = self.addHost("embedder")
        self.addLink(embedder, switch)
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost("server%s" % (h + 1))
            self.addLink(host, switch)


class MyEmbedderClient:
    def __init__(self):
        self.servers_load = [0 for i in range(NumOfServers)]
        self.requests = []

    # Generate Random CPU demand requests
    def generate_requests():
        random_float_list = [
            round(random.uniform(0.05, 0.2), 2) for i in range(NumOfRequests)
        ]
        print(random_float_list)

        return random_float_list

    def checkAvailability():
        pass


class MyServer:
    def __init__(self):
        self.available_cpu_load = 1  # normalized between 0-1 instead of 100

    def reply2client():
        pass


# vm_cpu_requests = generate_requests()


def simpleTest():
    "Create and test a simple network"
    topo = MyTopology(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Ifconfig h1\n")
    h1 = net.get("embedder")
    result = h1.cmd("ifconfig")
    print("IP = ", h1.IP())
    print(result)
    # print(net.hosts)
    # hostss = net.hosts
    # for hh in hostss:
    #     print("IPee = ", hh.IP())
    net.stop()


if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simpleTest()
