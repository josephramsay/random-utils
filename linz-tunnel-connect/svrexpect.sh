#!/usr/bin/expect -f

set svr [lindex $argv 0];
set spasswd [lindex $argv 1];
set passwd [lindex $argv 2];

send_user "Setting up ssh session on $svr\n"

spawn ssh $svr

expect "/.ssh/<ssh_key>':"
send "$spasswd\n"

expect "/.ssh/<ssh_key>':"
send "$spasswd\n"

if { $passwd != "" } {
    expect "'s password:"
    send "$passwd\n"
}

interact

