import sys

#allows import of modules from dir windows and linux
sys.path.append('linux')
sys.path.append('windows')

#linux modules
if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import speed_test
#windows modules
if sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test




def main():
        print("Network Diagnostic Tool")
        option = input("choose option \n1.Network Information    2.Speed Test\n3.Network Interface      4.Wifi Analysis\n5.Error Reporting        6.Security Inforamtion \n7.Exit\n")

        if option == '1':
             ping_test("8.8.8.8")
             dns_lookup("www.google.com")
             trace_route("8.8.8.8")
        elif option == '2':
             speed_test()
        elif option == '3':
             pass
        elif option == '4':
             pass
        elif option == '5':
             pass
        elif option == '6':
             pass
        elif option == '7':
             exit()
        else:
            print("Invalid Option")
                                 

if __name__ == "__main__":
     main() 