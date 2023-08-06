#!/usr/bin/bash
filename="file_test.fa"
while read -r line
do
	if [[ "$line" == [A-Z]* ]] || [[ "$line" == [A-Z]$ ]] ; then 
	    echo "$line" | sed 's/.\{80\}/&\n/g'
	else
    	    echo "$line" 
	fi
	
done < "$filename"
