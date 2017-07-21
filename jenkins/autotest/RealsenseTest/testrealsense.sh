#!/usr/bin/expect
set USER slamtec
set IP 192.168.11.3
set PASS slamware123
set COMD "./slamware_console depthcam --channel tcp scan"
spawn ssh "$USER@$IP" $COMD
expect {
    "yes/no"  { send "yes\r"; exp_continue }
    "password:" {send "$PASS\r"; exp_continue}
}
