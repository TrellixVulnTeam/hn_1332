#!/usr/bin/expect -f

spawn ssh -p 3333 root@localhost
expect "password:"
send "password\r"
expect "#"



