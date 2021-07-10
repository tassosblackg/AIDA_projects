from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    def build(self, n=2):
        switch = self.addSwitch("s1")
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost("h%s" % (h + 1))
            self.addLink(host, switch)


def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Ifconfig h1\n")
    h1 = net.get("h1")
    s = net.hosts
    for i in s:
        print(i.IP(), i.name)
    result = h1.cmd("ping -c 3 10.0.0.3")
    print(result)
    print("TYPEEE hos -", type(net.hosts))  # is a list
    net.stop()


if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simpleTest()
