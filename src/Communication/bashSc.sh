#!/bin/bash
counter = 1
while [ $counter -le 10 ]
do 
    dmesg | grep tty
    ((counter++))
    sleep 10000
done

echo All done
