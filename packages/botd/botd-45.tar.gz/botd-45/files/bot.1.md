% BOT(1) BOT(1)
% Bart Thate
% April 2021

# NAME
BOT - client version of botd

# SYNOPSIS
| bot \<cmd>\ 
| bot cfg server=irc.freenode.net channel=\\#botd
| bot mods=csl,irc

# DESCRIPTION
BOT is the user client version of BOTD, it can be used in development of bot
commands. Uses ~/.bot as the work directory and ./mod as the modules
directory.

Programming commands is easy, just edit mod/hlo.py and add this piece of
code:

    def hlo(event):
        event.reply("hello")

The hlo command is now available:

    $ bot hlo
    hello

# EXAMPLES

| $ bot
| $ 

| $ bot cmd
| cfg,cmd,dlt,ech,exc,flt,fnd,krn,met,sve,thr,upt,ver

| $ bot cfg
| cc=@ channel=#botd nick=botd port=6667 server=localhost

| bot krn
| $ cmd=krn name=bot txt=krn users=True version=1 wd=/home/bart/.bot

| $ bot thr
| CLI.handler 0s | CLI.input 0s

| $ bot mods=csl,irc
| >

# SEE ALSO
| botd
| botctl
| ~/.bot
| ./mod

# COPYRIGHT
BOT is placed in the Public Domain.
