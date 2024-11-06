import sys

#allows import of modules from dir windows and linux
sys.path.append('linux')
sys.path.append('windows')

#linux modules
if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import speed_test
    from linux.network_interface import network_interfaces_info
#windows modules
if sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test
    from windows.network_interface import network_interfaces_info




def main():
    print("Network Diagnostic Tool")
    
    while True:
        
        print("choose option \n1.Network Information    2.Speed Test\n3.Network Interface      4.Wifi Analysis\n5.Error Reporting        6.Security Inforamtion \n7.Exit\n")
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
             pass
        elif option == '5':
             pass
        elif option == '6':
             pass
        elif option == '7':
             print("Exiting")
             break
        else:
            print("Invalid Option")
                                 

if __name__ == "__main__":
     main() 