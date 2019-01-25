count=118

for filename in /home/panasonic-da-ai/Dataset/helmetV2/train/xmls/*.xml; do
        
        name=${filename##*/}
        base=${name%.xml}        
        echo $name
        echo "###############"
        #echo $base        
        newval=$(($base + $count))
        #echo $newval
        #count=$(($count + 1))
        #echo $count
        #echo "$newval".xml
	echo $base
	newname="$newval".xml
        mv $name $newname 
done
