#!/bin/bash

list="$(find . -name 'result*')"

for file in $list
do
  for file2 in $list; 
  do 
    if [[ $file != $file2 ]]; then
      result1=$(cat $file)
      result2=$(cat $file2)

      threshold=$(awk '{print $1/$2}' <<< "20 100")
      product=$(awk '{print $1*$2}' <<< "$result1 $threshold")

      difference1=$(awk '{print $1-$2}' <<< "$result1 $result2")

      if (( $(echo $difference1#- $product | awk '{if ($1 > $2) print 1;}') )); 
        then echo "The results provided by $file and $file2 are not the same"; 
      else echo "The results provided by $file and $file2 are the same within the threshold"; 
        fi
      fi
   done
done

