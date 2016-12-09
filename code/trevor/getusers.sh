#!/bin/bash

for d in * ; do
	echo "username,position,posts,ppd,up,down,registered" > $d/userdat.csv
	
	find $d -name "*action=profile*" | while read profile; do
		NAMEDAT="$(grep -h "<div class=\"username\">" $profile | sed "s/^[ \t]*//g; s/<div class=\"username\"><h4>*/\"/g; s/ <span class=\"position\">*/\",\"/g; s/<\/span><\/h4><\/div>*/\"/g;")"
		POSTS="$(grep -A1 'Posts:' $profile | grep -v 'Posts:' | sed -e "s/^[ \t]*//g; s/<dd>//g; s/<\/dd>//g; s/ (/,/g; s/ per day)//g")"
		KARMA="$(grep -A1 'Karma:' $profile | grep -v 'Karma:' | sed "s/^[ \t]*//g; s/<dd>//g; s/<\/dd>//g; s/\+//g; s/\//,/g; s/-//g;")"
		REGISTERED="$(grep -A1 'Date Registered:' $profile | grep -v 'Date Registered:' | sed "s/^[ \t]*//g; s/<dd>/\"/g; s/<\/dd>/\"/g")"
		echo $NAMEDAT,$POSTS,$KARMA,$REGISTERED >> $d/userdat.csv 
	done 
done
