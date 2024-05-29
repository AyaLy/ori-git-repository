#!/bin/sh
# the next line restarts using tclsh \
exec tclsh "$0" ${1+"$@"}

foreach {key value} [array get env] {
    puts "$key:    $value"
}
