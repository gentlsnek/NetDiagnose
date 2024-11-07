import sys

#allows import of modules from dir windows and linux
sys.path.append('linux')
sys.path.append('windows')

#linux modules
if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import speed_test
    from linux.network_interface import network_interfaces_info
    from linux.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info
    from linux.portscan import port_scan
    from linux.security import NetworkSecurityCheck
#windows modules
if sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test
    from windows.network_interface import network_interfaces_info
    from windows.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info_nmcli
    from windows.portscan import port_scan
    from windows.security import  NetworkSecurityCheck




def main():
    print("Network Diagnostic Tool")
    
    while True:
        
        print("choose option \n1.Network Information    2.Speed Test\n3.Network Interface      4.Wifi Analysis\n5.Port Scan              6.Security Inforamtion\n7.Error Reporting        8.Exit\n")
        option = input("Enter Option: ")

        if option == '1':
             input_ip = input("Enter IP: ")
             input_dns = input("Enter DNS: ")
             input_route = input("Enter Route: ")
             if input_ip == "": 
                    input_ip = "8.8.8.8"
             if input_dns == "":
                    input_dns = "www.google.com"
             if input_route == "":
                    input_route = "8.8.8.8"
             ping_test(input_ip)
             dns_lookup(input_dns)
             trace_route(input_route)
        elif option == '2':
             speed_test()
        elif option == '3':
             network_interfaces_info()
        elif option == '4':
             get_iw_info()
             get_wireless_interface()
             get_wifi_signal_strength()
             get_wifi_info()
        elif option == '5':
             port_scan()
        elif option == '6':
             
             target_ip = input("Enter Target IP: ")
             port = input("Enter Port: ")
             hostname = input("Enter Hostname: ")

             if target_ip == "":
                  target_ip = '8.8.8.8'
             if port == "":
                  port = 300    
             if hostname == "":
                  hostname = 'www.google.com'
             NetworkSecurityCheck.nmap_scan(target_ip, port)
             NetworkSecurityCheck.firewall_detection(target_ip, port)
             NetworkSecurityCheck.ssl_tls_inspection(hostname)
             
        elif option == '7':
             pass
        elif option == '8':
             print("Exiting")
             break
        else:
            print("Invalid Option")
                                 

if __name__ == "__main__":
     main() 