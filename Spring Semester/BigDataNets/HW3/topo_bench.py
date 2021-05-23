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
from alive_progress import alive_bar
import matplotlib.pyplot as plt


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


# Main Class does all the job
class Embedder:
    def __init__(self, NumOfServers):
        # available cpu per server
        self.servers_avail_load = [1 for i in range(NumOfServers)]
        self.cpu_perc_used = []  # cpu used per server for all req
        self.requests = []
        self.accepted_req = 0  # count accepted requests
        self.denied_req = 0  # count denied requests from servers
        self.NumOfRequests = 8 * NumOfServers
        self.cpu_avg_util = 0

    # Generate Random CPU demand requests
    def generate_requests(self):
        random_float_list = [
            round(random.uniform(0.05, 0.2), 2) for i in range(self.NumOfRequests)
        ]

        self.requests = random_float_list

    # CPU Utiliazation calculate
    def get_cpu_utilization(self):
        self.cpu_perc_used = [round(1 - x, 3) for x in self.servers_avail_load]

    # Break print from client to 2 values
    def get_client_response(self, response):
        resp_list = response.split(",")
        # print("-> ", resp_list[0], resp_list[1].strip())
        return (resp_list[0], float(resp_list[1].strip()))

    # get accepted count
    def count_accepted(self, acc_str):
        if acc_str == "True":
            self.accepted_req += 1

    # Update server available cpu load
    def update_server_cpu(self, server_i, val):
        self.servers_avail_load[server_i] = val

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
        return round(self.accepted_req / self.NumOfRequests, 3)

    def cpu_utilization(self):
        self.cpu_avg_util = round(sum(self.cpu_perc_used) / len(self.cpu_perc_used), 3)
        return self.cpu_avg_util

    def cpu_balancing(self):
        max_val = max(self.cpu_perc_used)
        return round(max_val / self.cpu_avg_util, 3)


# a class with method for ploting
class GraphPlots:
    def __init__(self):
        self.plot_name = "Experiment VM"

    # -------------| Plots | ----------------------------------------------------------
    def plot_4_methods(self, fig, x, y1, y2, y3, y4):
        plt.figure(fig)
        plt.plot(x, y1, label="Random")
        plt.plot(x, y2, label="FirstFit")
        plt.plot(x, y3, label="BestFit")
        plt.plot(x, y4, label="WorstFit")

    def plot_RAR(self, fig, x, y1, y2, y3, y4):
        plot_4_methods(x, fig, y1, y2, y3, y4)
        plt.title("Requests Acceptance Rate - (RAR)")
        plt.xlabel("Number of Total Requests")
        plt.ylabel("RAR (n)")

        plt.show()

    def plot_CPU_util(self, fig, x, y1, y2, y3, y4):
        plot_4_methods(x, y1, y2, y3, y4)
        plt.title("CPU Utilization")
        plt.xlabel("Number of Total Requests")
        plt.ylabel("CPU_util(n)")

        plt.show()

    def plot_CPU_balance(self, fig, x, y1, y2, y3, y4):
        plot_4_methods(x, y1, y2, y3, y4)
        plt.title("CPU load balance")
        plt.xlabel("Number of Total Requests")
        plt.ylabel("CPU_bal(n)")

        plt.show()


# Test topology benchmarks, main
def simpleTest():
    "Create and test a simple network"

    # # get input from the user
    # NumOfServers = sys.argv[1]
    exp_num_servers = [10, 20, 30, 40, 50]
    rar_val_method1, rar_val_method2, rar_val_method3, rar_val_method4 = [], [], [], []
    cpu_util_method1, cpu_util_method2, cpu_util_method3, cpu_util_method4 = (
        [],
        [],
        [],
        [],
    )
    cpu_bal_method1, cpu_bal_method2, cpu_bal_method3, cpu_bal_method4 = [], [], [], []
    with alive_bar(len(exp_num_servers)) as bar1:

        for ns in exp_num_servers:
            print("\nClearing old topologies....\n")
            output = subprocess.run(["sudo", "mn", "-c"])
            print(output)

            topo = MyTopology(ns)
            net = Mininet(topo)

            net.start()
            print("Dumping host connections")
            dumpNodeConnections(net.hosts)
            print("Testing network connectivity")
            net.pingAll()

            # split Hosts
            host_emb = net.get("embedder")
            servers = net.hosts
            servers = servers[1:]  # drop embedder from list

            # -------------------- | Random Method | ---------------------------------------------
            # create objects
            the_embedder = Embedder(ns)
            # ----| Start handling requests |-------
            the_embedder.generate_requests()

            for new_req in the_embedder.requests:
                server_index = the_embedder.random_server_indx()  # random index
                pipeI = servers[server_index].popen(
                    "python3 tserver.py"
                )  # start server xmlrpc
                sleep(1)
                result_response = host_emb.cmdPrint(
                    "python3 tclient.py "
                    + (servers[server_index].IP())
                    + " "
                    + str(the_embedder.servers_avail_load[server_index])
                    + " "
                    + str(new_req)
                )
                acc_resp, new_cpu_load = the_embedder.get_client_response(
                    result_response
                )
                the_embedder.count_accepted(acc_resp)  # count accepted req
                # assign new cpu load value for a specific server
                the_embedder.update_server_cpu(server_index, new_cpu_load)
                pipeI.terminate()  # terminate server

            the_embedder.get_cpu_utilization()  # create utilization list
            # print("Servers' percent used per server ", the_embedder.cpu_perc_used)
            rar_val_method1.append(the_embedder.request_acceptance_rate())
            cpu_util_method1.append(the_embedder.cpu_utilization())
            cpu_bal_method1.append(the_embedder.cpu_balancing())
            # print("Stats ", rar_val_method1, cpu_util_method1, cpu_bal_method1)

            # ---------------------------| FirstFit | ----------------------------------------------------------
            the_embedder2 = Embedder(ns)
            # ----| Start handling requests |-------
            the_embedder2.generate_requests()

            for new_req in the_embedder2.requests:
                server_index = the_embedder2.random_server_indx()  # random index
                pipeI = servers[server_index].popen(
                    "python3 tserver.py"
                )  # start server xmlrpc
                sleep(1)
                result_response = host_emb.cmdPrint(
                    "python3 tclient.py "
                    + (servers[server_index].IP())
                    + " "
                    + str(the_embedder2.servers_avail_load[server_index])
                    + " "
                    + str(new_req)
                )
                acc_resp, new_cpu_load = the_embedder2.get_client_response(
                    result_response
                )
                the_embedder2.count_accepted(acc_resp)  # count accepted req
                # assign new cpu load value for a specific server
                the_embedder2.update_server_cpu(server_index, new_cpu_load)

            the_embedder2.get_cpu_utilization()  # create utilization list
            rar_val_method2.append(the_embedder2.request_acceptance_rate())
            cpu_util_method2.append(the_embedder2.cpu_utilization())
            cpu_bal_method2.append(the_embedder2.cpu_balancing())
            #
            # ------------------------------| BestFit | ----------------------------------------------------------
            the_embedder3 = Embedder(ns)
            # ----| Start handling requests |-------
            the_embedder3.generate_requests()

            for new_req in the_embedder3.requests:
                server_index = the_embedder3.random_server_indx()  # random index
                pipeI = servers[server_index].popen(
                    "python3 tserver.py"
                )  # start server xmlrpc
                sleep(1)
                result_response = host_emb.cmdPrint(
                    "python3 tclient.py "
                    + (servers[server_index].IP())
                    + " "
                    + str(the_embedder3.servers_avail_load[server_index])
                    + " "
                    + str(new_req)
                )
                acc_resp, new_cpu_load = the_embedder3.get_client_response(
                    result_response
                )
                the_embedder3.count_accepted(acc_resp)  # count accepted req
                # assign new cpu load value for a specific server
                the_embedder3.update_server_cpu(server_index, new_cpu_load)

            the_embedder3.get_cpu_utilization()  # create utilization list
            rar_val_method3.append(the_embedder3.request_acceptance_rate())
            cpu_util_method3.append(the_embedder3.cpu_utilization())
            cpu_bal_method3.append(the_embedder3.cpu_balancing())
            #
            # -------------------------- | WorstFit | ------------------------------------------------
            the_embedder4 = Embedder(ns)
            # ----| Start handling requests |-------
            the_embedder4.generate_requests()

            for new_req in the_embedder4.requests:
                server_index = the_embedder4.random_server_indx()  # random index
                pipeI = servers[server_index].popen(
                    "python3 tserver.py"
                )  # start server xmlrpc
                sleep(1)
                result_response = host_emb.cmdPrint(
                    "python3 tclient.py "
                    + (servers[server_index].IP())
                    + " "
                    + str(the_embedder4.servers_avail_load[server_index])
                    + " "
                    + str(new_req)
                )
                acc_resp, new_cpu_load = the_embedder4.get_client_response(
                    result_response
                )
                the_embedder4.count_accepted(acc_resp)  # count accepted req
                # assign new cpu load value for a specific server
                the_embedder4.update_server_cpu(server_index, new_cpu_load)

            the_embedder4.get_cpu_utilization()  # create utilization list
            rar_val_method4.append(the_embedder4.request_acceptance_rate())
            cpu_util_method4.append(the_embedder4.cpu_utilization())
            cpu_bal_method4.append(the_embedder4.cpu_balancing())

            bar1()  # update
    print("\nStats1 ", rar_val_method1, cpu_util_method1, cpu_bal_method1)
    print("\nStats2 ", rar_val_method2, cpu_util_method2, cpu_bal_method2)
    print("\nStats3 ", rar_val_method3, cpu_util_method3, cpu_bal_method3)
    print("\nStats4 ", rar_val_method4, cpu_util_method4, cpu_bal_method4)

    # ------------------------------| Ploting | ----------------------------------------
    my_plots = GraphPlots()
    my_plots.plot_RAR(
        1,  # figure number
        exp_num_servers,
        rar_val_method1,
        rar_val_method2,
        rar_val_method3,
        rar_val_method4,
    )
    my_plots.plot_CPU_util(
        2,  # figure number
        exp_num_servers,
        cpu_util_method1,
        cpu_util_method2,
        cpu_util_method3,
        cpu_util_method4,
    )
    my_plots.plot_CPU_balance(
        3,  # figure number
        exp_num_servers,
        cpu_bal_method1,
        cpu_bal_method2,
        cpu_bal_method3,
        cpu_bal_method4,
    )

    # print(result_response)
    #
    # print(servers)
    # server1 = net.get("server1")
    # server2 = net.get("server2")
    # server3 = net.get("server3")
    # emb = net.get("embedder")
    # print(emb.IP(), servers[0].IP())
    # p1 = servers[0].popen("python3 tserver.py")
    # sleep(1)
    # res2 = emb.cmdPrint("python3 tclient.py 10.0.0.2 " + str(0.8) + " " + str(0.2))
    #
    # the_embedder = Embedder(int(NumOfServers))
    # acc_resp, cpu_load = the_embedder.get_client_response(res2)
    # print(acc_resp, cpu_load)
    # the_embedder.count_accepted(acc_resp)
    # print(the_embedder.accepted_req)

    # p1.terminate()

    net.stop()


if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel("info")
    simpleTest()
