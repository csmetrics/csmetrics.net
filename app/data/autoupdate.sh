#!/bin/bash
instfile="inst_full_clean.csv"
contfile="country_continent.csv"
input="errorfix.txt"
while IFS= read -r line
do
  if [[ $line == *"ErrorReport"* ]]; then
    IFS=':' read -r -a array <<< "$line"
    search=$(echo ",${array[1]},")
    echo ""
    echo "** Change" ${array[1]} ${array[2]} ${array[3]}
    origline=$(grep "$search" $instfile)
    echo " Original Line: " $origline

    IFS=',' read -r -a originfo <<< "$origline"
    if [[ ${array[2]} == *"type"* ]]; then
      echo " Update type: " ${originfo[2]} "-->" ${array[3]}
      newline=$(echo "${originfo[0]},${originfo[1]},${array[3]},${originfo[3]},${originfo[4]},${originfo[5]}")
    elif [[ ${array[2]} == *"country"* ]]; then
      echo " Update type: " ${originfo[4]} "-->" ${array[3]}
      cont=$(grep "${array[3]}" $contfile)
      IFS=$',\n\r' read -r -a continfo <<< "$cont"
      echo " Found continent: " ${continfo[1]}
      newline=$(echo "${originfo[0]},${originfo[1]},${originfo[2]},${continfo[1]},${array[3]},${originfo[5]}")
    fi
    echo " New Line: " $newline

    ## change to sed in Linux
    ## gsed for OS-X
    n_origline=$(echo "$origline" | gsed 's/\//\\\//g')
    n_newline=$(echo "$newline" | gsed 's/\//\\\//g')
    # echo $n_origline
    # echo $n_newline
    title="ErrorFix:${array[1]}:${array[2]}:${array[3]}"
    echo " Title: " $title

    # this script does not generate commit but provide commands
    echo
    echo "gsed -i '/$n_origline/c\\$n_newline' $instfile"
    # gsed -i '/$n_origline/c\\$n_newline' $instfile
    echo "git add $instfile && git commit -m '$title'"
    # git commit
    # git add $instfile
    # git commit -m "$title"
  fi
done < "$input"
