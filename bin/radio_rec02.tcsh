#!/usr/bin/env tcsh
if ($#argv < 5) then
	echo "usage: $0 channel n_minutes directory prefix quality [dateformat]"
	echo "legal choices for channel are: "
	echo " p1"
	echo " p2"
	echo " p3"
	echo " p3_radioresepsjonen"
	echo " p13"
	echo " mpetre"
	echo " gull"
	echo " jazz"
	echo " oslofjord"
	echo " super"
	echo " urort"
	echo " nyheter"
	echo " klassisk"
	echo " folkemusikk"
	echo " stortinget"
	echo " sami-radio"
	echo " sport"
	echo ' OR p4 !!'
	echo " "
	echo " and quality is either l, m or h (low, medium, high). not applicable for p4"
   echo " datefmt is like %Y%m%d_%H%M"

	exit 1
endif

set channel   = $1;
set n_minutes = $2;
set directory = $3;
set prefix    = $4;
set quality   = $5;
if ($#argv >= 6) then
   set datefmt = $6;
else
   #set datefmt = %Y%m%d_%H%M;  very detailed...
   set datefmt = %Y%m%d;
endif

#set log    = /dev/null;
set log    = /tmp/wget.log;

# arithmetics is tricky ...
set n_secs = 0;
@ n_secs = $n_minutes * 60;

echo "channel= $channel n_secs= $n_secs directory= $directory prefix= $prefix"

set filename=$directory/$prefix-`date +$datefmt`.mp3
echo "Recording to '$filename'"
hostname -f

# p1 must be treated specially
if ($channel == "p1") then
   set channel = {$channel}_ostlandssendingen
endif

# here is the main action
if ($channel == "p4") then
	wget -O $filename http://mms-live.online.no/p4_norge >& $log &
else
	wget -O $filename http://lyd.nrk.no/nrk_radio_{$channel}_mp3_{$quality} &
endif

set wgetpid=$!
echo wgetpid = $wgetpid

sleep $n_secs

kill $wgetpid

echo "Done"
