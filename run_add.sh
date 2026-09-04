#!/bin/bash
eval $(ssh-agent -s)
expect -c '
spawn ssh-add /Users/silversurfer/.ssh/id_ed25519
expect "Enter passphrase"
send "Cunt3344#\r"
expect eof
'
kill $SSH_AGENT_PID
