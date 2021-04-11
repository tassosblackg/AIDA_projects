#!/usr/bin/env python
# coding: utf-8

# # Data Centers Traffic Analysis

# ### Big Data Networks

# #### Tassos Karageorgiadis

# In[1]:
import argparse
import os
import numpy as np
from alive_progress import alive_bar
import matplotlib.pyplot as plt
import dpkt
import datetime
import socket
from dpkt.compat import compat_ord


# In[4]:


def mac_addr(address):
    """Convert a MAC address to a readable/printable string

    Args:
        address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
    Returns:
        str: Printable/readable MAC address
    """
    return ":".join("%02x" % compat_ord(b) for b in address)


def inet_to_str(inet):
    """Convert inet object to a string

    Args:
        inet (inet struct): inet network address
    Returns:
        str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def print_packets(pcap):
    """Print out information about each packet in a pcap

    Args:
        pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    (
        tcpcounter,
        udpcounter,
        icmpcounter,
        arpcounter,
        other_ip_counter,
        other_non_ip_counter,
    ) = (0, 0, 0, 0, 0, 0)

    # Flows only for TCP or UDP packets
    #                        key                          value
    tcp_flows = {}  # {(sIP,sPort,dIP,dPort,Type) : [size,duration,last_timestamp]}
    udp_flows = {}
    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Print out the timestamp in UTC
        # print("Timestamp: ", str(datetime.datetime.utcfromtimestamp(timestamp)))

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        # print("Ethernet Frame: ", mac_addr(eth.src), mac_addr(eth.dst), eth.type)

        # # Make sure the Ethernet data contains an IP packet
        # if not isinstance(eth.data, dpkt.ip.IP):
        #     # print("Non IP Packet type not supported %s\n" % eth.data.__class__.__name__)
        #     continue
        if isinstance(eth.data, dpkt.arp.ARP):
            # print('Ignoring ARP packet %s\n' % eth.data.__class__.__name__)
            # continue
            arpcounter += 1

        elif isinstance(eth.data, dpkt.ip.IP):
            # Now unpack the data within the Ethernet frame (the IP packet)
            # Pulling out src, dst, length, fragment info, TTL, and Protocol
            ip = eth.data

            if ip.p == dpkt.ip.IP_PROTO_TCP:  # ip.p == 6:
                tcp = ip.data
                tcpcounter += 1
                tcp_key = (
                    inet_to_str(ip.src),
                    tcp.sport,
                    inet_to_str(ip.dst),
                    tcp.dport,
                    "TCP",
                )
                if tcp_key in tcp_flows:  # check if key exists in dict
                    # update duration with old_timestamp
                    duration = tcp_flows[tcp_key][1] + (
                        timestamp - tcp_flows[tcp_key][2]
                    )
                    # add new packets size to the old
                    new_size = tcp_flows[tcp_key][0] + ip.len
                    # update keys values adding packet
                    tcp_flows[tcp_key] = [new_size, duration, timestamp]
                else:  # key not in dict
                    tcp_flows[tcp_key] = [ip.len, 0, timestamp]

            elif ip.p == dpkt.ip.IP_PROTO_UDP:  # ip.p==17:
                udp = ip.data
                udpcounter += 1
                udp_key = (
                    inet_to_str(ip.src),
                    udp.sport,
                    inet_to_str(ip.dst),
                    udp.dport,
                    "UDP",
                )
                if udp_key in udp_flows:  # check if key exists in dict
                    # update duration with old_timestamp
                    duration = udp_flows[udp_key][1] + (
                        timestamp - udp_flows[udp_key][2]
                    )
                    # add new packets size to the old
                    new_size = udp_flows[udp_key][0] + ip.len
                    # update keys values adding packet
                    udp_flows[udp_key] = [new_size, duration, timestamp]
                else:  # key not in dict
                    udp_flows[udp_key] = [ip.len, 0, timestamp]

            elif ip.p == dpkt.ip.IP_PROTO_ICMP:
                icmpcounter += 1
            else:
                other_ip_counter += 1

            #         print("Test me",ip.data)
            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
        else:
            # print("Ignoring packets except ARP,TCP,UDP,ICMP \n")
            other_non_ip_counter += 1
            continue
        # Print out the info
    #         print('IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
    #               (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))
    print("Pcap file's number of arp packets :", arpcounter)
    print("Pcap file's number of tcp packets :", tcpcounter)
    print("Pcap file's number of udp packets :", udpcounter)
    print("Pcap file's number of icmp packets :", icmpcounter)
    print("Pcap file's number of Other-IP packets :", other_ip_counter)
    print("Pcap file's number of  NON-IP packets :", other_non_ip_counter)

    num_packets_per_file = [
        tcpcounter,
        udpcounter,
        arpcounter,
        icmpcounter,
        other_ip_counter,
        other_non_ip_counter,
    ]

    return num_packets_per_file, tcp_flows, udp_flows


# ------- Main Function that performing all the steps of analysis, printing results ----------------------------------------------------------
def packet_analysis(files):
    """
    Function that reads all pcap files from a directory, and performing the analysis tasks
    """
    total_tcp_flows, total_udp_flows = {}, {}
    types_of_packets = ["TCP", "UDP", "ARP", "ICMP", "OTHERip", "OTHERnon_ip"]
    num_of_packets_per_type = [0] * len(types_of_packets)
    with alive_bar(len(files)) as bar:
        for pcapf in files:
            print("\n Next pcap file.. reading...==> ", str(pcapf), "\n")
            with open(str(pcapf), "rb") as f:
                file = dpkt.pcap.Reader(f)
                packets_per_file, f_tcp_flows, f_udp_flows = print_packets(file)
                num_of_packets_per_type[0] += packets_per_file[0]  # total tcp packets
                num_of_packets_per_type[1] += packets_per_file[1]  # total udp packets
                num_of_packets_per_type[2] += packets_per_file[2]  # total arp packets
                num_of_packets_per_type[3] += packets_per_file[3]  # total icmp packets
                num_of_packets_per_type[4] += packets_per_file[
                    4
                ]  # total other_ip  packets
                num_of_packets_per_type[5] += packets_per_file[
                    5
                ]  # total ohter_nonip packets

    # total packets read
    total_num_packets = sum(num_of_packets_per_type)
    # add dictionary records from a file
    total_tcp_flows.update(f_tcp_flows)
    total_udp_flows.update(f_udp_flows)

    # Print Packets number per protocol type
    print(
        "Total TCPs: {} Total UDPs: {},Total ARPs: {}, Total ICMPs: {}, Other IP :{}, Other NON-IP :{} / Out Of {} total packets captured".format(
            num_of_packets_per_type[0],
            num_of_packets_per_type[1],
            num_of_packets_per_type[2],
            num_of_packets_per_type[3],
            num_of_packets_per_type[4],
            num_of_packets_per_type[5],
            total_num_packets,
        )
    )

    print(
        "\nTotal TCP Flows:{} and Total UDP Flows: {}\n".format(
            len(total_tcp_flows), len(total_udp_flows)
        )
    )

    percentage_num_packets = [
        round(i / total_num_packets * 100, 2) for i in num_of_packets_per_type
    ]
    print(
        "\nPercentage of packets per type out of the total packet number :\n",
        types_of_packets,
        "\n",
        percentage_num_packets,
    )
    # ----- Plot graphs ----------------------------------------------
    print("\n...Ploting packets per protocol percentage... fig1\n")
    bar_width = 0.4
    plt.figure(1)

    plt.bar(
        types_of_packets[0],
        percentage_num_packets[0],
        bar_width,
        color="red",
        label="TCP",
    )
    plt.bar(
        types_of_packets[1],
        percentage_num_packets[1],
        bar_width,
        color="green",
        label="UDP",
    )
    plt.bar(
        types_of_packets[2],
        percentage_num_packets[2],
        bar_width,
        color="blue",
        label="ARP",
    )
    plt.bar(
        types_of_packets[3],
        percentage_num_packets[3],
        bar_width,
        color="magenta",
        label="ICMP",
    )
    plt.bar(
        types_of_packets[4],
        percentage_num_packets[4],
        bar_width,
        color="yellow",
        label="OTHERip",
    )
    plt.bar(
        types_of_packets[5],
        percentage_num_packets[5],
        bar_width,
        color="black",
        label="OTHERnon_ip",
    )
    plt.xlabel("Packets protocol")
    plt.ylabel("percentage('%')")
    plt.title("Bar diagram of perc of packets out of total")
    # plt.xticks(features_indx + bar_width / 2, types_of_packets, rotation=90)
    plt.legend(loc="best")

    # The same plot in absolute numbers
    print("\n...Ploting packets per protocol absolute numbers... fig2\n")
    plt.figure(2)
    plt.bar(
        types_of_packets[0],
        num_of_packets_per_type[0],
        bar_width,
        color="red",
        label="TCP",
    )
    plt.bar(
        types_of_packets[1],
        num_of_packets_per_type[1],
        bar_width,
        color="green",
        label="UDP",
    )
    plt.bar(
        types_of_packets[2],
        num_of_packets_per_type[2],
        bar_width,
        color="blue",
        label="ARP",
    )
    plt.bar(
        types_of_packets[3],
        num_of_packets_per_type[3],
        bar_width,
        color="magenta",
        label="ICMP",
    )
    plt.bar(
        types_of_packets[4],
        num_of_packets_per_type[4],
        bar_width,
        color="yellow",
        label="OTHERip",
    )
    plt.bar(
        types_of_packets[5],
        num_of_packets_per_type[5],
        bar_width,
        color="black",
        label="OTHERnon_ip",
    )
    plt.xlabel("Packets protocol")
    plt.ylabel("Absolute Number/Out of Total")
    plt.title("Bar diagram num of packets out of total")
    plt.legend(loc="best")

    ##----------------- Plots for Flows-------------------------------------
    tcp_flow_sizes = [s[0] for s in total_tcp_flows.values()]  # get size of each flow
    tcp_flow_duration = [d[1] for d in total_tcp_flows.values()]

    udp_flow_sizes = [s2[0] for s2 in total_udp_flows.values()]  # get size of each flow
    udp_flow_duration = [d2[1] for d2 in total_udp_flows.values()]

    # getting data of the histogram
    count_tcp_s, bins_count_tcp_s = np.histogram(tcp_flow_sizes, bins=20)
    count_tcp_d, bins_count_tcp_d = np.histogram(tcp_flow_duration, bins=20)

    count_udp_s, bins_count_udp_s = np.histogram(udp_flow_sizes, bins=20)
    count_udp_d, bins_count_udp_d = np.histogram(udp_flow_duration, bins=20)

    # finding the PDF of the histogram using count values
    pdf_tcp_s = count_tcp_s / sum(count_tcp_s)
    pdf_tcp_d = count_tcp_d / sum(count_tcp_d)

    pdf_udp_s = count_udp_s / sum(count_udp_s)
    pdf_udp_d = count_udp_d / sum(count_udp_d)

    # using numpy np.cumsum to calculate the CDF
    # We can also find using the PDF values by looping and adding
    cdf_tcp_s = np.cumsum(pdf_tcp_s)
    cdf_tcp_d = np.cumsum(pdf_tcp_d)

    cdf_udp_s = np.cumsum(pdf_udp_s)
    cdf_udp_d = np.cumsum(pdf_udp_d)

    # -- TCP and UDP Size flows CDF
    plt.figure(3)
    # plotting PDF and CDF
    plt.plot(bins_count_tcp_s[1:], cdf_tcp_s, color="green", label="TCP_S_CDF")
    plt.plot(bins_count_udp_s[1:], cdf_udp_s, label="UDP_S_CDF")

    plt.xlabel("Flows Size in Bytes (x10^7)")
    plt.ylabel("CDF")
    plt.title("TCP UDP Flows Size CDF")
    plt.legend(loc="best")

    plt.figure(4)
    plt.plot(bins_count_tcp_s[1:], pdf_tcp_s, color="green", label="TCP_D_PDF")
    plt.plot(bins_count_udp_s[1:], pdf_udp_s, label="UDP_D_PDF")
    plt.xlabel("Flows Time Size in Bytes (x10^7)")
    plt.ylabel("PDF")
    plt.title("TCP UDP Flows Size PDF")
    plt.legend(loc="best")

    # -- TCP and UDP duration plot CDF
    plt.figure(5)
    plt.plot(bins_count_tcp_d[1:], cdf_tcp_d, color="green", label="TCP_D_CDF")
    plt.plot(bins_count_udp_d[1:], cdf_udp_d, label="UDP_D_CDF")
    plt.xlabel("Flows Time Duration in Sec")
    plt.ylabel("CDF")
    plt.title("TCP UDP Flows Duration CDF")
    plt.legend(loc="best")

    plt.figure(6)
    plt.plot(bins_count_tcp_d[1:], pdf_tcp_d, color="green", label="TCP_D_PDF")
    plt.plot(bins_count_udp_d[1:], pdf_udp_d, label="UDP_D_PDF")
    plt.xlabel("Flows Time Duration in Sec")
    plt.ylabel("PDF")
    plt.title("TCP UDP Flows Duration PDF")
    plt.legend(loc="best")

    plt.show()


# read filenames from a give directory path
def get_files2read(directory):

    filenames, files = [], []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            files.append(os.path.abspath(os.path.join(dirpath, f)))
    # print(filenames[0])
    return files


# parser menu, pass argmunents
def parserMenu():

    parser = argparse.ArgumentParser(prog="traffic analysis")
    # parser.add_argument("-csr","--csr",action="store_true",help='read mps file or LP file to convert')
    parser.add_argument("input_path", type=str, help="<directory_path>")
    args = parser.parse_args()
    print(args.input_path)
    files = get_files2read(args.input_path)
    print("\n-> Files to be read .... \n", files, "\n")

    packet_analysis(files)


if __name__ == "__main__":
    # packet_analysis()
    parserMenu()
