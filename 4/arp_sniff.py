from scapy.all import *
 
def arp_monitor_callback(pkt):
    pkt.show()
 
sniff(prn=arp_monitor_callback, filter="arp", count=1)