#!/usr/bin/env python
# coding: utf-8

# # Data Centers Traffic Analysis

# ### Big Data Networks

# #### Tassos Karageorgiadis

# In[1]:

from alive_progress import alive_bar
import dpkt
import datetime
import socket
from dpkt.compat import compat_ord


# In[2]:


from os import walk

path = "Data/"
filenames = []
(_, _, filenames) = next(walk(path))


# In[4]:


print(filenames[0])


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
                tcpcounter += 1
            elif ip.p == dpkt.ip.IP_PROTO_UDP:  # ip.p==17:
                udpcounter += 1
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

    return (
        arpcounter,
        tcpcounter,
        udpcounter,
        icmpcounter,
        other_ip_counter,
        other_non_ip_counter,
    )


# In[ ]:
total_arp, total_tcp, total_udp, total_icmp, total_ipother, total_nonip_other = (
    0,
    0,
    0,
    0,
    0,
    0,
)
pcap_files = []
with alive_bar(len(filenames)) as bar:
    for pcapf in filenames:
        print("Pcap file reading...==> ", str(pcapf), "\n")
        with open(path + str(pcapf), "rb") as f:
            file = dpkt.pcap.Reader(f)
            n_arp, n_tcp, n_udp, n_icmp, n_otherip, n_noipother = print_packets(file)
            total_arp += n_arp
            total_tcp += n_tcp
            total_udp += n_udp
            total_icmp += n_icmp
            total_ipother += n_otherip
            total_nonip_other += n_noipother
# total packets
total_packets = (
    total_arp + total_tcp + total_udp + total_icmp + total_ipother + total_nonip_other
)

# Print Packets number per protocol type
print(
    "Total ARPs: {} Total TCPs: {} Total UDPs: {} Total ICMPs: {}, Other IP :{}, Other NON-IP :{} / Out Of {} total packets captured".format(
        total_arp,
        total_tcp,
        total_udp,
        total_icmp,
        total_ipother,
        total_nonip_other,
        total_packets,
    )
)
