from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
import subprocess


class GeneratedTopo(Topo):
    "Internet Topology Zoo Specimen."

    def __init__(self, **opts):
        "Create a topology."

        # Initialize Topology
        Topo.__init__(self, **opts)

        # add nodes, switches first...
        NewYork = self.addSwitch("s0")
        Chicago = self.addSwitch("s1")
        WashingtonDC = self.addSwitch("s2")
        Seattle = self.addSwitch("s3")
        Sunnyvale = self.addSwitch("s4")
        LosAngeles = self.addSwitch("s5")
        Denver = self.addSwitch("s6")
        KansasCity = self.addSwitch("s7")
        Houston = self.addSwitch("s8")
        Atlanta = self.addSwitch("s9")
        Indianapolis = self.addSwitch("s10")

        # ... and now hosts
        NewYork_host = self.addHost("h0")
        Chicago_host = self.addHost("h1")
        WashingtonDC_host = self.addHost("h2")
        Seattle_host = self.addHost("h3")
        Sunnyvale_host = self.addHost("h4")
        LosAngeles_host = self.addHost("h5")
        Denver_host = self.addHost("h6")
        KansasCity_host = self.addHost("h7")
        Houston_host = self.addHost("h8")
        Atlanta_host = self.addHost("h9")
        Indianapolis_host = self.addHost("h10")

        # add edges between switch and corresponding host
        self.addLink(NewYork, NewYork_host)
        self.addLink(Chicago, Chicago_host)
        self.addLink(WashingtonDC, WashingtonDC_host)
        self.addLink(Seattle, Seattle_host)
        self.addLink(Sunnyvale, Sunnyvale_host)
        self.addLink(LosAngeles, LosAngeles_host)
        self.addLink(Denver, Denver_host)
        self.addLink(KansasCity, KansasCity_host)
        self.addLink(Houston, Houston_host)
        self.addLink(Atlanta, Atlanta_host)
        self.addLink(Indianapolis, Indianapolis_host)

        # add edges between switches
        self.addLink(NewYork, Chicago, bw=1, delay="0.806374975652ms")
        self.addLink(NewYork, WashingtonDC, bw=1, delay="0.605826192092ms")
        self.addLink(Chicago, Indianapolis, bw=1, delay="1.34462717203ms")
        self.addLink(WashingtonDC, Atlanta, bw=1, delay="0.557636936322ms")
        self.addLink(Seattle, Sunnyvale, bw=1, delay="1.28837123738ms")
        self.addLink(Seattle, Denver, bw=1, delay="1.11169346865ms")
        self.addLink(Sunnyvale, LosAngeles, bw=1, delay="0.590813628707ms")
        self.addLink(Sunnyvale, Denver, bw=1, delay="0.997327682281ms")
        self.addLink(LosAngeles, Houston, bw=1, delay="1.20160833263ms")
        self.addLink(Denver, KansasCity, bw=1, delay="0.223328790403ms")
        self.addLink(KansasCity, Houston, bw=1, delay="1.71325092726ms")
        self.addLink(KansasCity, Indianapolis, bw=1, delay="0.240899959477ms")
        self.addLink(Houston, Atlanta, bw=1, delay="1.34344500256ms")
        self.addLink(Atlanta, Indianapolis, bw=1, delay="0.544962634977ms")


def simpleTest():

    print("\nClearing old topologies....\n")
    output = subprocess.run(["sudo", "mn", "-c"])
    print(output)

    topo = MyTopology()
    net = Mininet(topo)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    # net.stop()


if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simpleTest()
