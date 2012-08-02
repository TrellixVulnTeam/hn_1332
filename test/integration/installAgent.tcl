#!/usr/bin/expect -f  

set timeout 100
set prompt "\^.*\]\\\$ "

spawn ssh -p 3333 hnbuild@localhost

expect -re  $prompt
send "sudo yum localinstall hypernova/x86_64/*.rpm\r"
expect -re ".\*is this ok .\*: "
send "y\r"
expect -re  $prompt

send "sudo yum install rng-tools\r"
expect -re ".\*is this ok .\*: "
send "y\r"
expect -re  $prompt

send "sudo rngd -r /dev/urandom -o /dev/random\r"
expect -re  $prompt


send "sudo /usr/local/hypernova/bin/hn-agent-setup\r"
expect -re  $prompt

send "sudo service hnagent start\r"
expect -re  $prompt

send "exit\r"





