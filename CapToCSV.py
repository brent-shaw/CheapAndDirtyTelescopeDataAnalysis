#!/usr/bin/env python

"""CapToCSV.py: Build CSV from initial telescope data"""

"""
Currently the data is not publically avaialble. Contact for access.
"""

__author__ = "Brent Shaw"
__copyright__ = "Copyright 2018"
__credits__ = ["Brent Shaw"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Brent Shaw"
__email__ = "shaw@live.co.za"
__status__ = "Development"

import dpkt
import datetime
from dpkt.compat import compat_ord
import socket
from geolite2 import geolite2

def mac_addr(address):
    """Convert a MAC address to a readable/printable string
       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)

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

    data = {}

    # header = "time_stamp,ip.source,ip.destination,port.source, port.destination, ip.protocol, length.packet, iso.country"

    # for row in reader:
    #     data[row['time_stamp']] = [row["ip.length"],row["ip.identification"],row["ip.offset"],row["ip.ttl"],row["ip.checksum"],row["ip.source"],row["ip.destination"],row["tcp.sequence"],row["tcp.acknowledge"],row["tcp.offset"],row["tcp.flags_x"],row["tcp.checksum"],row["tcp.urgent_point"],row["tcp_flags_binary_string_x"],row["traffic_status_x"],row["threat_type"],row["time_index"],row["seconds_in_day"],row["sin_time"],row["cos_time"],row["well_known_src_port"],row["well_known_dst_port"],row["registered_src_port"],row["registered_dst_port"],row["ephemeral_src_port"],row["ephemeral_dst_port"],row["tcp.flags_y"],row["tcp_flags_binary_string_y"],row["traffic_status_y"],row["country"],row["country_iso"],row["alpha_2_code"],row["same_source"],row["same_destination_portion"],row["diff_port_portion"],row["same_port_portion"],row["same_dest_same_port_portion"],row["same_dest_diff_port_portion"],row["diff_dest_same_port_portion"]]

    reader = geolite2.reader()

    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        #print('Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            #print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
            continue

        # Print out the timestamp in UTC
        #print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
        print('Timestamp: ', str(timestamp))

        # Now unpack the data within the Ethernet frame (the IP packet)
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        sourceip = inet_to_str(ip.src)
        destip = inet_to_str(ip.dst)

        sourcematch = reader.get(sourceip)
        destmatch = reader.get(sourceip)

        # Print out the info
        print('Protocol %d: %s (%d) -> %s (%d) \n%s -> %s \nMisc: len=%d ttl=%d DF=%d MF=%d offset=%d' % \
              (ip.p, sourceip, ip.data.sport, destip, ip.data.dport, sourcematch['country']['iso_code'], destmatch['country']['iso_code'], ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))

        print('')

    geolite2.close()

def test():
    """Open up a test pcap file and print out the packets"""
    with open('test.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        print_packets(pcap)

if __name__ == '__main__':
    test()
