#!/bin/bash
# Usage: sh curl_by_date.sh year month
if [ ! -d "/mnt/twitter" ]; then
  sudo mkdir "/mnt/twitter"
fi
sudo curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" \
-G \
--data-urlencode 'start_key=["melbourne", '$1','$2',1]' \
--data-urlencode 'end_key=["melbourne",'$1','$2',31]' \
--data-urlencode 'reduce=false' \
--data-urlencode 'include_docs=true' \
--user "readonly:ween7ighai9gahR6" \
-o /mnt/twitter/tweet_by_date_$1_$2.json