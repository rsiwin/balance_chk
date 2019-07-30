#!/bin/bash
#  Balance_Check
#  Version : 1.0

DIR=/home/rsi
LOGS=/home/rsi/logs
BIN=/home/rsi/bin


function show_version ()
{
        echo "Balance_Check"
        echo "Version : 1.0"
        echo "";
}

function start_bal ()
{
    nohup /usr/bin/python ${BIN}/balance.py & > ${LOGS}/balance.log
}

function display ()
{
    ps -ef |grep rsi/bin |grep balance
}

function stop_bal ()
{
    echo -n "Stopping Balance_Check Process..."
    PID=`ps -ef |grep rsi/bin |grep balance |cut -d ' ' -f 7`
    
    if [ "$PID" == "" ]; then
        echo "no process exist"
    else
        echo "      process id (${PID}) will be killed by force!"
        kill -9 ${PID}
    fi
}

# void usage(void)
function usage ()
{
    echo "`basename $0` [ dis | start | stop | version ]"
}

# int main(String[] args)
function main ()
{
    case "$1" in
        version)
            show_version;
            ;;

        start)
            start_bal;
            ;;

        stop)
            stop_bal;
            ;;

        dis)
            display;
            ;;

        *)
            usage;
            ;;
    esac
    return 0;
}

# it begins
main $*

# EOF

