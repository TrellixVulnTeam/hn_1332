#!/usr/bin/expect -f

spawn ssh -p 3333 root@localhost
expect "password:"
send "password\r"
expect "#"
send "find /usr/ &>/dev/null" # Generates entropy
send "gpg --gen-key\r"
expect "Your selection?"
send "1\r"
expect "What keysize do you want? (2048)"
send "2048\r"
expect "Key is valid for? (0)"
send "0\r"
expect "Is this correct? (y/N)"
send "y\r"
expect "Real name:"
send "server\r"
expect "Email address:"
send "server@domain.com\r"
expect "Comment:"
send "\r"
expect "Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit?"
send "O\r"
interact


