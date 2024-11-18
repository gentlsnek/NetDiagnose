import psutil
import socket


def network_interfaces_info():

    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    interf = []
    addr = []
    
    for interface_name, addresses in interfaces.items():
        #print(f"\nInterface: {interface_name}")
        
 
        if interface_name in stats:
            iface_stats = stats[interface_name]
            interf.append(f" Interface: {interface_name} \n")
            interf.append(f" Status: {'Up' if iface_stats.isup else 'Down'} \n")
            interf.append(f" Duplex: {iface_stats.duplex} \n")
            interf.append(f" Speed: {iface_stats.speed} Mbps \n")
            interf.append(f" MTU: {iface_stats.mtu} \n\n")

        for address in addresses:
            if address.family == socket.AF_NETLINK:
                
                addr.append(f" MAC Address: {address.address}\n\n")
            elif address.family == socket.AF_INET:
                addr.append(f" IPv4 Address: {address.address}\n")
                addr.append(f" Netmask: {address.netmask}\n")
                addr.append(f" Broadcast IP: {address.broadcast}\n\n")
            elif address.family == socket.AF_INET6:
                pass
               # addr.append(f" IPv6 Address: {address.address}\n\n")
               # addr.append(f"  Netmask: {address.netmask}\n\n")

    return [interf,addr]