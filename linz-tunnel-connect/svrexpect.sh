#!/usr/bin/expect -f

set svr [lindex $argv 0];
set spasswd [lindex $argv 1];
set passwd [lindex $argv 2];

send_user "Setting up ssh session on $svr\n"

spawn ssh $svr

send_user "P1 rndgw\n"
expect "/.ssh/<ssh_key>':"
send "$spasswd\n"

send_user "P2 liexp\n"
expect "/.ssh/<ssh_key>':"
send "$spasswd\n"

if { $passwd != "" } {
	send_user "P3 $svr\n"
    expect "'s password:"
    send "$passwd\n"
}

interact

