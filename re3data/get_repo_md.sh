#!/bin/bash

input="./list_id.txt"
while IFS= read -r line
do
  echo "$line"
  curl https://www.re3data.org/api/v1/repository/$line -o "repo_md/$line.xml"
done < "$input"