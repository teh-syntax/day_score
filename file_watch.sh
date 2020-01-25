!#/bin/bash
counter=1
while [ $counter -le 6 ]
do
    AMIRUNNING="$(ps aux | grep '/usr/bin/python3 /webapps/day_score/scripts/file_watcher/file_watcher.py' | wc -l)"
    if [ "$AMIRUNNING" -lt 2 ]; then
        /usr/bin/python3 /webapps/day_score/scripts/file_watcher/file_watcher.py
        echo $counter
    else
        echo "COLLISION"
    fi
    sleep 9
    ((counter++))
done
