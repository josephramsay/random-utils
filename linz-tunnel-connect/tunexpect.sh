#!/usr/bin/expect -f

set svr [lindex $argv 0];
set spasswd [lindex $argv 1];

send_user "Setting up tunnel to $svr\n"

spawn ssh $svr

expect "/.ssh/<ssh_key>':"
send "$spasswd\n"

expect "/.ssh/<ssh_key>':"
send "$spasswd\n"


#if {[fork] != 0} exit
#disconnect
interact
