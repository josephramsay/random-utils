#!/usr/bin/expect -f

set svr [lindex $argv 0];
set spasswd [lindex $argv 1];

send_user "Setting up tunnel to $svr\n"

spawn ssh $svr

send_user "P1 rndgw\n"
expect "/.ssh/<ssh_key>':"
send "$spasswd\n"

send_user "P2 liexp\n"
expect "/.ssh/<ssh_key>':"
send "$spasswd\n"


#if {[fork] != 0} exit
#disconnect
interact
