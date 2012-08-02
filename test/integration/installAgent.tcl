#!/usr/bin/expect -f  
#
# HyperNova server management framework
#
# Agent installation script
#
# Copyright (c) 2012 TDM Ltd
#                     Laurent David<laurent@tdm.info>
#
set timeout 100
set prompt "\^.*\]\\\$ "

spawn ssh -p 3333 hnbuild@localhost

expect -re  $prompt
send "sudo yum -y localinstall hypernova/x86_64/*.rpm\r"
expect -re  $prompt

send "sudo yum -y install rng-tools\r"
expect -re  $prompt

send "sudo rngd -r /dev/urandom -o /dev/random\r"
expect -re  $prompt


send "sudo /usr/local/hypernova/bin/hn-agent-setup\r"
expect -re  $prompt

send "sudo service hnagent start\r"
expect -re  $prompt

send "sudo yum -y install nginx-php-fpm php-{bz2,curl,devel,fpm,ftp,gd,mcrypt,mysql,mysqli,openssl,pdo,pdo-mysql,pdo-sqlite,pear,pgsql,phar,xsl,zip,zlib}\r"
expect -re  $prompt

send "exit\r"





