# Data Centers Traffic Analysis

### HW2 Big Data Networks

### AID21002
------------------------------------------------------

### A) Introduction:

-----------------
In this project I had to read a set of *.pcap* files and create a program that analyzes traffic statistics per protocol type or per flow for each protocol. The types of protocols that were taken into account was *TCP, UDP, ARP, ICMP*. All other types just ignored or simple count them as a percentage of the total traffic of packets across all data. The program was developed using Python while familiarized with the format of data per packet using Wireshark.

### B) Count packets per protocol:
------------------------------


![Protocol Type percentage out of total number of packets](Images/ProtocolPerc.png "percentage of packets per protocol")

### C) CDF flow analysis per protocol:
----------------------------------



### D) Extra Figures :

In the next figure we see the flows for *'univ1_pt1'*.pcap file analyzed inside the *Wireshark* environment using wireshark statistics and flows. This figures show the flows from IP to IP showing details about source and destination ports while at the comment section we can see the extra info for each flow e.g. protocol,ACK,SYN signals, etc.

![Wireshark Flows For All Packets Example](Images/WiresharkFlows.png "Wireshark Flows ")

### References:
-----------------

1. | [CDF Packets sizes examples][1]


2. | [ARP packet sizes ][2]

3. | [Flow-based TCP Connection Analysis][3]

4. | [ICMP packets][4]

5. | [ARP packets][5]

6. | [TCP packet][6]

7. | [Wireshark packets filtering][7]

8. | [TCP Timestamps][8]

[1]:https://www.researchgate.net/figure/Packet-size-CDF-per-protocol-in-downlink-left-and-uplink-right-traffic_fig2_228395666
[2]:https://community.cisco.com/t5/switching/arp-packet-size/td-p/1551467
[3]:https://www2.tkn.tu-berlin.de/bib/limmer2009flowbased/limmer2009flowbased.pdf
[4]:https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
[5]:https://en.wikipedia.org/wiki/Address_Resolution_Protocol
[6]:https://el.wikipedia.org/wiki/%CE%A0%CF%81%CF%89%CF%84%CF%8C%CE%BA%CE%BF%CE%BB%CE%BB%CE%BF_%CE%95%CE%BB%CE%AD%CE%B3%CF%87%CE%BF%CF%85_%CE%9C%CE%B5%CF%84%CE%B1%CF%86%CE%BF%CF%81%CE%AC%CF%82
[7]:https://linoxide.com/wireshark-filters/
[8]:https://cloudshark.io/articles/tcp-timestamp-option/

### Author

Tassos Karageorgiadis April,2021
