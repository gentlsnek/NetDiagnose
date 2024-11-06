import sys

#allows import of modules from dir windows and linux
sys.path.append('linux')
sys.path.append('windows')

#linux modules
if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import speed_test
    from linux.network_interface import network_interfaces_info
    from linux.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info_nmcli
    from linux.portscan import port_scan
#windows modules
if sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test
    from windows.network_interface import network_interfaces_info
    from windows.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info_nmcli
    from windows.portscan import port_scan




def main():
    print("Network Diagnostic Tool")
    
    while True:
        
        print("choose option \n1.Network Information    2.Speed Test\n3.Network Interface      4.Wifi Analysis\n5.Port Scan              6.Error Reporting\n7.Security Inforamtion   8.Exit\n")
        option = input("Enter Option: ")

        if option == '1':
             ping_test("8.8.8.8")
             dns_lookup("www.google.com")
             trace_route("8.8.8.8")
        elif option == '2':
             speed_test()
        elif option == '3':
             network_interfaces_info()
        elif option == '4':
             get_iw_info()
             get_wireless_interface()
             get_wifi_signal_strength()
             get_wifi_info_nmcli()
        elif option == '5':
             port_scan()
        elif option == '6':
             pass
        elif option == '7':
             pass
        elif option == '8':
             print("Exiting")
             break
        else:
            print("Invalid Option")
                                 

if __name__ == "__main__":
     main() 