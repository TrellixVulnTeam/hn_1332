#!/usr/bin/expect -f

spawn ssh -p 3333 hnbuild@localhost
expect ' ~]$'
send "sudo rpm -i hypernova/x86_64/*.rpm\r"
expect ' ~]$'




