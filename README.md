servicelist
==============
Windows Service List

Usage
============
    usage: sl.py [-h] [-v] [-f [FILTER [FILTER ...]]] [-sa [START [START ...]]]
                 [-sp [PAUSE [PAUSE ...]]] [-st [STOP [STOP ...]]]
                 [-k [KILL [KILL ...]]] [-S SORT_BY] [-s] [-ss SORT_STATUS_ONLY]
                 [-p] [-n] [-d] [-c] [-cc SORT_START_CONFIG_ONLY] [-T TAIL] [-z]
                 [-r] [-rr] [-R [RESTART [RESTART ...]]] [-F]
                 [-x [SEARCH [SEARCH ...]]] [-xx [SEARCH_STOP [SEARCH_STOP ...]]]
                 [-xs [SEARCH_START [SEARCH_START ...]]]
                 [-xp [SEARCH_PAUSE [SEARCH_PAUSE ...]]]
                 [-X [SEARCH_KILL [SEARCH_KILL ...]]] [-l]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -f [FILTER [FILTER ...]], --filter [FILTER [FILTER ...]]
                            Filter
      -sa [START [START ...]], --start [START [START ...]]
                            Start Service by Name or PID
      -sp [PAUSE [PAUSE ...]], --pause [PAUSE [PAUSE ...]]
                            Puse Service by Name or PID
      -st [STOP [STOP ...]], --stop [STOP [STOP ...]]
                            Stop Service by Name or PID
      -k [KILL [KILL ...]], --kill [KILL [KILL ...]]
                            Kill process/Hard Stop with Name or PID if available
      -S SORT_BY, --sort-by SORT_BY
                            Sort list by, available argument: [name, pid, status, start, display_name, description]
      -s, --sort-status     Sort list by Status
      -ss SORT_STATUS_ONLY, --sort-status-only SORT_STATUS_ONLY
                            Sort list and Only Show Sorted by Status, available argument: [STOPPED, START PENDING, STOP PENDING, RUNNING, PAUSE PENDING, PAUSED, START, STOPPING, PAUSE CONTINUE]
      -p, --sort-pid        Sort list by PID
      -n, --sort-name       Sort list by Name
      -d, --sort-displayname
                            Sort list by Display Name
      -c, --sort-start-config
                            Sort list by Config Start type
      -cc SORT_START_CONFIG_ONLY, --sort-start-config-only SORT_START_CONFIG_ONLY
                            Sort list and Only Show Sorted by Config Start type, available argument: ['BOOT START', 'SYSTEM START', 'AUTO START', 'DEMAND_START', 'DISABLED']
      -T TAIL, --tail TAIL  Sort list by time and show last of N
      -z, --fast            search by the last of list service
      -r, --reverse         List reverse
      -rr, --recursive      Recursive service and child
      -R [RESTART [RESTART ...]], --restart [RESTART [RESTART ...]]
                            Restart service
      -F, --fast-list-details
                            Show all details of service
      -x [SEARCH [SEARCH ...]], --search [SEARCH [SEARCH ...]]
                            search by input [name, pid, status, start, display_name, description]
      -xx [SEARCH_STOP [SEARCH_STOP ...]], --search-stop [SEARCH_STOP [SEARCH_STOP ...]]
                            search by input [name, pid, status, start, display_name, description] and stop
      -xs [SEARCH_START [SEARCH_START ...]], --search-start [SEARCH_START [SEARCH_START ...]]
                            search by input [name, pid, status, start, display_name, description] and start
      -xp [SEARCH_PAUSE [SEARCH_PAUSE ...]], --search-pause [SEARCH_PAUSE [SEARCH_PAUSE ...]]
                            search by input [name, pid, status, start, display_name, description] and pause
      -X [SEARCH_KILL [SEARCH_KILL ...]], --search-kill [SEARCH_KILL [SEARCH_KILL ...]]
                            search by input [name, pid, status, start, display_name, description] and kill by PID if available
      -l, --list-details    Show all details of process

Author
============
[LICFACE](mailto:licface@yahoo.com)

Debug
==============
set system environment DEBUG=1 to show debug process

Platform
============
Win32/Win64 Only
