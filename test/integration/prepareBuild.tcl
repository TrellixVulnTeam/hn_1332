#!/usr/bin/expect -f

spawn ssh -p 2222 root@localhost
expect "password:"
send "password\r"
expect "#"



