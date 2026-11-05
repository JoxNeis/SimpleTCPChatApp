netsh interface ip set address "Ethernet" dhcp
netsh advfirewall firewall add rule name="TCP Test 5000" dir=in action=allow protocol=TCP localport=5000
