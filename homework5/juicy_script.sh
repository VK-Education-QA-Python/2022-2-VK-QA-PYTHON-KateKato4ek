FILE_WITH_RESULTS=bash_results.txt

echo COMMON AMOUNT OF REQUESTS > "$FILE_WITH_RESULTS"
awk '{ print $6, $7 }' $1 | sort -u | wc -l | awk '{ print $1 }' >> "$FILE_WITH_RESULTS"
echo >> "$FILE_WITH_RESULTS"

echo AMOUNT OF REQUESTS BY TYPES >> "$FILE_WITH_RESULTS"
awk '{ print $6, $7 }' $1 | sort -u | awk '{ print substr($1, 2) }' | uniq -c | awk '$2 == "GET" || $2 == "POST" || $2 == "DELETE" || $2 == "PUT" || $2 == "HEAD" || $2 == "CONNECT" || $2 == "OPTIONS" || $2 == "TRACE" || $2 == "PATCH"' >> "$FILE_WITH_RESULTS"
echo >> "$FILE_WITH_RESULTS"

echo 10 MOST FREQUENT REQUESTS >> "$FILE_WITH_RESULTS"
awk '{print $6, $7, $8}' $1 | sort | uniq -c | sort -rnk 1 | head -n 10 | awk '{print $1, $3}' >> "$FILE_WITH_RESULTS"
echo >> "$FILE_WITH_RESULTS"

echo 5 MOST FREQUENT REQUESTS WITH 4XX STATUS CODE >> "$FILE_WITH_RESULTS"
awk '{print $1,$9,$10,$7}' $1 | awk '$2~/^4/' | sort -rnk 3 | head -n 5 >> "$FILE_WITH_RESULTS"
echo >> "$FILE_WITH_RESULTS"

echo 5 USERS BY REQUESTS WITH 5XX STATUS CODE >> "$FILE_WITH_RESULTS"
awk '{print $1, $9}' $1 | sort | uniq -c | awk '$3 ~ /^5/' | sort -rnk 3 | head -n 5 >> "$FILE_WITH_RESULTS"
echo >> "$FILE_WITH_RESULTS"


