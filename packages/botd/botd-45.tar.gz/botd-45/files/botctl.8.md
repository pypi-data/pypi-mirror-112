% BOTCTL(8)  BOTCTL(8)
% Bart Thate
% April 2021

# NAME
BOTCTL - control the bot daemon

# SYNOPSIS
sudo botctl \<cmd\>

# DESCRIPTION
BOTCTL executes botcmd under the systemd-exec wrapper, this to make commands run
under systemd. Uses /var/lib/botd as the work directory and
/vae/lib/botd/mod as the modules directory.

# EXAMPLES
| sudo botctl cmd
| sudo botctl cfg server=irc.freenode.net channel=\#dunkbots nick=botje
| sudo botctl met ~botfather@jsonbot/daddy
| sudo botctl rss https://github.com/bthate/botd/commits/master.atom
| sudo botctl krn mods=rss

# AUTHOR
Bart Thate \<bthate@dds.nl\>

# COPYRIGHT
BOTCTL is placed in the Public Domain. 

# SEE ALSO
| bot
| botd
| /var/lib/botd
| /var/lib/botd/mod
| /usr/local/share/botd/botd.service
