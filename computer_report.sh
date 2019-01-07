#!/bin/bash

now=$(date +"%d.%m.%Y_%H:%M:%S")
#exec &> computer_report_$now.txt # Redirect to file

echo "                                                          "
echo "**************     Computer Report  $now   *****************"
echo "                                                          "

#This function writes lines of CPU info
getcpuinfo(){
grep "$regex" /proc/cpuinfo | sed "s/$regex/$item/g"
echo ""
return
}

#This function return Memory value according to memoryindex
getmemoryinfo(){
dataline=$(free --mega | grep "Mem:\s*")
read -a dataarray <<< $dataline # Read line into an array
retmemoryval=${dataarray[$memoryindex]}
echo -e $TitleMemory$retmemoryval
echo ""
}

echo HARDWARE:
echo ""

#CPU type
item="CPU Type\t\t:\t"
regex="model name\s*:\s*"
getcpuinfo $item $regex

#Number of Cores
item="Number of Cores\t\t:\t"
regex="cpu cores\s*:\s*"
getcpuinfo $item $regex

#Speed
item="Speed (MHz)\t\t:\t"
regex="cpu MHz\s*:\s*"
getcpuinfo $item $regex

#Total Memory
memoryindex=1
TitleMemory="Total Memory (MB)\t:\t"
getmemoryinfo $memoryindex $TitleMemory

#Used Memory
memoryindex=2
TitleMemory="Used Memory (MB)\t:\t"
getmemoryinfo $memoryindex $TitleMemory

#Available Memory
memoryindex=6
TitleMemory="Available Memory (MB)\t:\t"
getmemoryinfo $memoryindex $TitleMemory

echo ""
echo USERS:
echo ""

#Number of registered users
TitleRegUsers="Registered Users\t:\t"
RegisteredUsers=$(who | wc -l)
echo -e $TitleRegUsers$RegisteredUsers
echo ""

#Logged in users
TitleLoggedinUsers="Logged in Users\t\t:\t"
LoggedinUsers=$(users | xargs -n1 | sort -u | xargs) # remove doubles
echo -e $TitleLoggedinUsers$LoggedinUsers
echo ""

#Users Home Directory
echo -e "Users Home Directories\t:"
echo ""
echo -e "User\t\tHome Directory"
read -a LoggedinUsersarray <<< $LoggedinUsers # Read line into an array
COUNTER=0
while [ $COUNTER -lt $RegisteredUsers ]; do
    User=${LoggedinUsersarray[i]}
    HomeDir=$(eval echo ~$User) # puts out $User's home dir.
    echo -e $User"\t\t"$HomeDir
    let COUNTER=COUNTER+1
done
echo ""

#Detailed List of Users
echo -e "Detailed List of Users\t:"
echo ""
w | sed '1d' #finger # if not available use: w | sed '1d'
echo ""

echo "*************   End Computer Report $now  *****************"
echo "                                                           "

#EOF
