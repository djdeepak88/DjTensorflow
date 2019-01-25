for i in `seq 5 1 183`; do echo $i;  sed -i 's#/home/deepak-kumar-jha/Single_Image_object_detection_Model/Helmet_Pics/Gray_Resized_Images#/home/panasonic-da-ai/Dataset/Helmet/images#g' "$i".xml  ; done 

grep -Ril "text-to-find-here" /

grep -rnw '/path/to/somewhere/' -e 'tf.ConfigProto(allow_soft_placement=True)'

for f in *.jpeg; do
    mv -- "$f" "$(basename -- "$f" .jpeg).jpg"
done


<path>C:/Users/krish.naik/Downloads/jeans _ Google Search/61PStgbt2EL._UY606_.jpg</path>

^[a-zA-Z]:\\[\\\S|*\S]?.*$

for i in `seq 5 1 183`; do echo $i;  sed -i 's#^C:/Users#/home/panasonic-da-ai/Dataset/Jeans_Tshirt/images/"$($i)".jpg"#g' "$i".xml  ; done



grep -Po '^[a-zA-Z]:\\[\\\S|*\S]?.*$' 1.xml


grep -oh "^(?:[\w]\:|\\)(\\[a-z_\-\s0-9\.]+)+\.(jpeg|jpg)$"


// File Path Extension.

^(?:[\w]\:|\\)(\\[a-z_\-\s0-9\.]+)+\.(txt|gif|pdf|doc|docx|xls|xlsx)$


^(?:[\w]\:|\\|\)(\\[a-z_\-\s0-9\.]+)+\.(jpeg|jpg)$


^(?:[\w]\:|\\) -- Begin with x:\ or \\
 
[a-z_\-\s0-9\.] -- valid characters are a-z| 0-9|-|.|_ (you can add more)
 
(txt|gif|pdf|doc|docx|xls|xlsx) -- Valid extension (you can add more)



egrep -i  "^\(?:[\w]\:|\\|\\\)(\\[a-z_\-\s0-9\.]+)+\.\(jpeg|jpg\)"



for i in `seq 1 1 47`; do echo $i; grep path "$i".xml   ; done

grep -R -E --include="*.xml"  "^\(?:[\w]\:|\\|\\\)(\\[a-z_\-\s0-9\.]+)+\.\(jpeg|jpg\)" 1.xml



sed -i -e '/<annotation>/,/<\/annotation>/ s|<path>[0-9a-z._-A-Z:]\{1,\}</path>|<path>/home/panasonic-da-ai/Dataset/Jeans_Tshirt/images/1.jpg<path>|g' 1.xml

xmlstarlet ed -u //annotation/path -v '/home/panasonic-da-ai/Dataset/Jeans_Tshirt/images/1.jpg' 1.xml > 

xmlstarlet ed -u //annotation/folder -v 'Jeans_Tshirt' 1.xml

for i in `seq 1 1 47`; do echo $i;    ; done


for i in `seq 1 1 47`; do echo $i;

xmlstarlet ed -u //annotation/path -v /home/panasonic-da-ai/Dataset/Jeans_Tshirt/images/"$i".jpg "$i".xml > temp.txt.$$  && mv temp.txt.$$  "$i".xml;

xmlstarlet ed -u //annotation/folder -v 'Jeans_Tshirt' "$i".xml > temp.txt.$$  && mv temp.txt.$$  "$i".xml;

xmlstarlet ed -u //annotation/filename -v "$i".jpg "$i".xml > temp.txt.$$  && mv temp.txt.$$  "$i".xml;

done


 