#!/usr/bin/python
import sys
import random
import subprocess
from time import time, sleep
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client as cl
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

import matplotlib.pyplot as plt

# # define num of servers and requests
# NumOfServers = 5  # <- this should be read as input from sys
# NumOfRequests = 8 * NumOfServers

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
    def __init__(self, NumOfServers):
        # available cpu per server
        self.servers_avail_load = [1 for i in range(NumOfServers)]
        self.cpu_perc_used = []  # cpu used per server for all req
        self.requests = []
        self.accepted_req = 0  # count accepted requests
        self.denied_req = 0  # count denied requests from servers
        self.NumOfRequests = 8 * NumOfServers

    # Generate Random CPU demand requests
    def generate_requests(self):
        random_float_list = [
            round(random.uniform(0.05, 0.2), 2) for i in range(NumOfRequests)
        ]

        return random_float_list

    # CPU Utiliazation calculate
    def get_cpu_utilization(self):
        self.cpu_perc_used = [round(1 - x, 3) for x in self.servers_avail_load]

    # Break print from client to 2 values
    def get_client_response(self, response):
        resp_list = response.strip().split(",")
        return (resp_list[0], float(resp_list[1]))

    # get accepted count
    def count_accepted(self, acc_str):
        if acc_str == "True":
            self.accepted_req += 1

    # -----------------------| Methods For choosing a server |--------------------------
    def random_server_indx(self):
        return random.randrange(len(self.servers_avail_load))

    def first_fit_server_indx(self, cpu_req):
        return next(
            (indx for indx, x in enumerate(self.servers_avail_load) if x >= cpu_req)
        )

    def best_fit_server_indx(self, cpu_req):
        min_val = min(val for val in self.servers_avail_load if val >= cpu_req)
        return self.servers_avail_load.index(min_val)

    def worst_fit_server_idx(self):
        max_val = max(self.servers_avail_load)
        return self.servers_avail_load.index(max_val)

    # ---------------| Metrics |----------------------------------------------------
    def request_acceptance_rate(self):
        return self.accepted_req / NumOfRequests

    def cpu_utilization(self):
        return round(sum(self.cpu_perc_used) / len(self.cpu_perc_used), 3)

    def cpu_balancing(self, avg_cpu_util):
        max_val = max(self.cpu_perc_used)
        return max_val / avg_cpu_util

    # -------------| Plots | ----------------------------------------------------------
    def plot_4_methods(self, x, y1, y2, y3, y4):
        plt.plot(x, y1, label="Random")
        plt.plot(x, y2, label="FirstFit")
        plt.plot(x, y3, label="BestFit")
        plt.plot(x, y4, label="WorstFit")

    def plot_RAR(self, x, y1, y2, y3, y4):
        plot_4_methods(x, y1, y2, y3, y4)
        plt.title("Requests Acceptance Rate - (RAR)")
        plt.xlabel("Number of Total Requests")
        plt.ylabel("RAR (n)")

        plt.show()

    def plot_CPU_util(self, x, y1, y2, y3, y4):
        plot_4_methods(x, y1, y2, y3, y4)
        plt.title("CPU Utilization")
        plt.xlabel("Number of Total Requests")
        plt.ylabel("CPU_util(n)")

        plt.show()

    def plot_CPU_balance(self, x, y1, y2, y3, y4):
        plot_4_methods(x, y1, y2, y3, y4)
        plt.title("CPU load balance")
        plt.xlabel("Number of Total Requests")
        plt.ylabel("CPU_bal(n)")

        plt.show()


class Server:
    def __init__(self):
        self.cpu_avail = 1
        self.accepted = False

    def check_req(cpu_req):
        if cpu_req <= cpu_avail:
            self.cpu_avail -= cpu_req  # update new avail cpu
            self.accepted = True
        else:
            self.accepted = False

        return (self.accepted, self.cpu_avail)


# Test topology benchmarks, main
def simpleTest():
    "Create and test a simple network"
    print("Clearing old topologies....\n")
    output = subprocess.run(["sudo", "mn", "-c"])
    print(output)

    # get input from the user
    NumOfServers = sys.argv[1]

    topo = MyTopology(int(NumOfServers))
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()

    emb = net.get("embedder")
    server1 = net.get("server1")
    # server2 = net.get("server2")
    # server3 = net.get("server3")
    print(emb.IP(), server1.IP())
    p1 = server1.popen("python3 tserver.py")
    sleep(1)
    res2 = emb.cmdPrint("python3 tclient.py 10.0.0.2")

    # the_embedder = Embedder(int(NumOfServers))
    # acc_resp, cpu_load = the_embedder.get_client_response(res2)
    # print(acc_resp, cpu_load)
    # the_embedder.count_accepted(acc_resp)
    # print(the_embedder.accepted_req)

    #
    # p2 = server2.popen("python3 tserver.py")
    # sleep(5)
    #
    # res3 = server3.cmdPrint("python3 tclient.py 10.0.0.3 ")
    p1.terminate()
    # sleep(5)

    net.stop()


if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simpleTest()
