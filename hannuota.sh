#!/bin/bash
fpan () {
    if [ $1 -eq 1 ];then
        echo "$2 ==>  $4"
    else
        fpan $[$1-1] $2 $4 $3
            echo "$2 ==> $4"
        fpan $[$1-1] $3 $2 $4
    fi
}

fpan 3 a b c