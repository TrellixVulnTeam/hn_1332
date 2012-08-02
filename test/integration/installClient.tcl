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

send "gpg --gen-key\r"
expect -re "$.*Your selection?"
send "1\r"
expect -re "$.*What keysize do you want?"
send "2048\r"
expect -re "$.*Key is valid for?"
send "0\r"
expect -re "$.*Is this correct?"

expect -re  $prompt


send "gpg --export email@addr > client.pub\r"
expect -re  $prompt

send "gpg --export-secret-keys email@addr > client\r"
expect -re  $prompt


send "exit\r"





