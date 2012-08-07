#!/usr/bin/expect -f  
#
# HyperNova server management framework
#
# Client installation script
#
# Copyright (c) 2012 TDM Ltd
#                     Laurent David<laurent@tdm.info>
#


set timeout 100
set prompt "\^.*\]\\\$ "

spawn ssh -p 3333 hnbuild@localhost
expect -re  $prompt

send "hn-client-setup --email user@tdm.info -n user\r"
expect -re  $prompt

send "sudo /usr/local/hypernova/bin/hn-agent-add-client  --key-file client.pub --email user@tdm.info"
expect -re  $prompt

send "hn-client config node add host1 127.0.0.1 server.pub"
expect -re  $prompt

send "exit\r"





