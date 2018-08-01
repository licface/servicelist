#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LICFACE --<licface@yahoo.com>
  Purpose: 
  Created: 7/19/2018
"""

import os
import sys
import win32service
from pprint import pprint
from debug import *
from make_colors import make_colors
import cmdw
MAX_LENGTH = cmdw.getWidth()
from texttable import Texttable
from textwrap import wrap

class ServiceList(object):
    def __init__(self):
        super(ServiceList, self)
        self.service_status = {
            1: 'STOPPED',
            2: 'START PENDING',
            3: 'STOP PENDING',
            4: 'RUNNING',
            6: 'PAUSE PENDING',
            7: 'PAUSED',
            16: 'START',
            32: 'STOPPING',
            64: 'PAUSE CONTINUE',
        }
        
        self.service_state = {
            0: 'BOOT START',
            1: 'SYSTEM START',
            2: 'AUTO START',
            3: 'DEMAND START',
            4: 'DISABLED',
        }
        
        self.service_type = {
            
        }
        
    def makeHandle(self, server = 'localhost', dbname = None, desiredaccess = win32service.SC_MANAGER_ALL_ACCESS):
        '''
           @API:
                win32service.OpenSCManager(machineName, dbName , desiredAccess)
        '''
        handle = win32service.OpenSCManager(server, dbname, desiredaccess)
        return handle
    
    def makehandleService(self, service_name):
        handle = self.makeHandle()
        try:
            handle_service = win32service.OpenService(handle, service_name, win32service.SERVICE_ALL_ACCESS)
            return handle_service
        except:
            return False
        
    def ConfigDict(self, service_name):
        config_dict = {}
        handle = self.makehandleService(service_name)
        try:
            config_list = win32service.QueryServiceConfig(handle)
            #debug(config_list = config_list)
        except:
            # debug(ERROR = traceback.format_exc())
            config_list = ()
        
        if config_list:
            config_dict.update({
                'name': service_name,
                'start': self.service_state.get(config_list[1]),
                'dependencies': config_list[6],
                'user': config_list[7],
                'display_name': config_list[8],
            })
        #debug(config_dict = config_dict)
        return config_dict
    
    def getDescription(self, service_name):
        #debug(service_name = service_name)
        descriptions = 'Access Denied'
        handle = self.makehandleService(service_name)
        if handle:
            try:
                descriptions = win32service.QueryServiceConfig2(handle, win32service.SERVICE_CONFIG_DESCRIPTION)
            except:
                descriptions = 'The resource loader failed to find MUI file.'
        return descriptions
    
    def getService(self):
        n = 1
        handle = self.makeHandle()
        service_list = win32service.EnumServicesStatusEx(handle)
        #pprint(service_list)
        service_dict = {}
        for i in service_list:
            service_dict.update({
                n: {
                    'name': i.get('ServiceName'),
                    'status': self.service_status.get(i.get('CurrentState')),
                    'pid': i.get('ProcessId'),
                    'displayname': i.get('DisplayName'),
                    'descriptions': self.getDescription(i.get('ServiceName')),
                    'start_config': self.ConfigDict(i.get('ServiceName')).get('start'),
                }
            })
            n += 1
        #debug(service_dict = service_dict)
        return service_dict
            
    def getState(self):  #for test only
        dir_service = dir(win32service)
        for i in dir_service:
            x = getattr(win32service, i)
            if isinstance(x, int) or isinstance(x, str):
                print i, "=", x
                
    def setFilter(self, filter, data, sort = False):
        #debug(data = data)
        debug(filter = filter)
        debug(sort = sort)
        n = 1
        data_filter = {}
        data_filter_sort = []
        for i in filter:
            for x in data:
                if not sort:
                    name = data.get(x).get('name')
                    pid = data.get(x).get('pid')
                    display_name = data.get(x).get('display_name')
                    descriptions = data.get(x).get('descriptions')
                    if i in str(name).lower() or i in str(pid) or i in str(display_name).lower() or i in str(descriptions).lower():
                        data_filter.update({n: data.get(x),})
                        n += 1
                else:
                    if i in x[1].get('name').lower() or i in str(x[1].get('pid')) or i in x[1].get('displayname').lower() or i in x[1].get('descriptions').lower():
                        data_append = (i, x[1])
                        data_filter_sort.append(data_append)
        debug(data_filter_sort = data_filter_sort)
        debug(data_filter = data_filter)
        if sort:
            data_filter = data_filter_sort
        return data_filter
                
    def sortState(self, data, sort = False, status = False, start_config = False):
        #debug(data = data)
        debug(sort = sort)
        debug(status0 = status)
        debug(start_config0 = start_config)
        n = 1
        data_append = ()
        data_dict = {}
        if sort:
            data_sort = []
            for x in data:
                if x[1]:
                    data_append = (n, x[1].get(sort))
                    data_sort.append(data_append)
                    n += 1
        else:
            if status:
                #debug(status = status)
                data_dict = {}
                for x in data:
                    #debug(get_status = data.get(x).get('status'))
                    if data.get(x).get('status') == status:
                        data_dict.update({n: data.get(x),})
                        n += 1
            if start_config:
                #debug(start_config = start_config)
                data_dict = {}
                for x in data:
                    #debug(get_start_config = data.get(x).get('start_config'))
                    if data.get(x).get('start_config') == start_config:
                        data_dict.update({n: data.get(x),})
                        n += 1
        debug(sort_x = sort)             
        if sort:
            data_dict = data_sort
                
        return data_dict
                
    def makeTable(self, data, filter = None, sort=None, tail = None, reverse=False, list_details = False, fast_list_mode = False, status = False, start_config = False):
        number = 1
        if fast_list_mode:
            list_details = True
        debug(sort = sort)
        if sort:
            data = self.sort_dict(data, sort, reverse)
            if tail:
                data = data[-int(tail):]
        else:
            if tail:
                data1 = {}
                data_keys = data.keys()[-int(tail):]
                for i in data_keys:
                    data1.update({i:data.get(i)})
                data = data1
        if MAX_LENGTH <= (220 / 2) or list_details:
            debug(list_details = list_details)
            debug(fast_list_mode = fast_list_mode)
            if filter: #MAX_LENGTH <= (220 / 2)
                data = self.setFilter(filter, data, sort)
            if status:
                data = self.sortState(data, sort, status)
            if start_config:
                data = self.sortState(data, sort, start_config)
            debug(data_220 = data)
            for i in data:
                name, displayname, pid, status, description, start_config = self.getData(i, sort, data)
                self.printList(name, displayname, pid, status, description, start_config, number, fast_list_mode)
                if not fast_list_mode:
                    print "-" * MAX_LENGTH
                number += 1
        #END ~ MAX_LENGTH <= (220 / 2)
        else:
            table = Texttable()
            table.header(['No','Name', 'Display Name','PID', 'STATUS', 'DESCRIPTIONS', 'START'])
            table.set_cols_align(["l", 'l', "l", "l", "l", "l", "c"])
            table.set_cols_valign(["t", "m", "m", "m", "m", "t", "m"])
            table.set_cols_width([
                int(MAX_LENGTH * 0.03), #No
                int(MAX_LENGTH * 0.15),  #Name
                int(MAX_LENGTH * 0.20),  #DisplayName
                int(MAX_LENGTH * 0.05),  #Pid
                int(MAX_LENGTH * 0.06), #STATUS
                int(MAX_LENGTH * 0.33),  #Descriptions
                int(MAX_LENGTH * 0.07),  #Start Config
            ])

            sys.dont_write_bytecode = True
            number = 1
            
            debug(status = status)
            debug(start_config = start_config)
            if filter:
                data = self.setFilter(filter, data, sort)
            if status:
                data = self.sortState(data, sort, status)
            if start_config:
                data = self.sortState(data, sort, start_config= start_config)
            debug(data=data)
            for i in data:
                name, displayname, pid, status, descriptions, start_config = self.getData(i, sort, data)
                table = self.makeTableAdd(table, number, name, displayname, pid, status, descriptions, start_config)
                number += 1

            print table.draw()
        return data, number
    
    def makeTableAdd(self, table, number, name, displayname, pid, status, descriptions, start_config):
        if not start_config:
            start_config = ''
        try:
            table.add_row([str(number), name, displayname, str(pid), status, str(descriptions), start_config])
        except:
            print traceback.format_exc()
            table.add_row([
                str(number),
                unicode(name).encode(sys.stdout.encoding, errors='replace'),
                unicode(displayname).encode(sys.stdout.encoding, errors='replace'),
                unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                unicode(status).encode(sys.stdout.encoding, errors='replace'),
                unicode(descriptions).encode(sys.stdout.encoding, errors='replace'), 
                unicode(start_config).encode(sys.stdout.encoding, errors='replace'), 
            ])
            
        return table    

    def printList(self, name, displayname, pid, status, description, start_config, number, fast_list_mode = False):
        debug(fast_list_mode = fast_list_mode)
        if fast_list_mode:
            print str(number) + ". " + make_colors(str(name), 'lightcyan', color_type= 'colorama', attrs = ['bold']) + " " \
                + "(" + make_colors(str(displayname), 'lightyellow', color_type= 'colorama', attrs = ['bold']) + ")" + " " \
                + "[" + make_colors(str(pid), 'lightgreen', color_type= 'colorama', attrs = ['bold']) + "]" + " " \
                + "{" + make_colors(str(status), 'lightmagenta', color_type= 'colorama', attrs = ['bold']) + "}" + " "\
                + "[" + make_colors(str(start_config), 'lightred', color_type= 'colorama', attrs = ['bold']) + "]"
        else:
            print "NAME           :", make_colors(str(name), 'lightcyan', color_type= 'colorama', attrs= ['bold'])
            print "DISPLAY_NAME   :", make_colors(str(displayname), 'lightcyan', color_type= 'colorama', attrs= ['bold'])
            print "PID            :", make_colors(str(pid), 'lightyellow', color_type= 'colorama', attrs= ['bold'])
            print "STATUS         :", make_colors(str(status), 'white', 'lightred', color_type= 'colorama', attrs= ['bold'])
            print "DESCRIPTIONS   :", make_colors(wrap(str(description), (MAX_LENGTH - 20)), 'green', attrs= ['bold'], color_type= 'colorama')
            print "START CONFIG   :", make_colors(str(start_config), 'white', 'lightred', color_type= 'colorama', attrs= ['bold'])
            
    def getData(self, i, sort=False, data=None):
        if not sort:
            name = data.get(i).get('name')
            displayname = data.get(i).get('displayname')
            pid = data.get(i).get('pid')
            status = data.get(i).get('status')
            descriptions = data.get(i).get('descriptions')
            start_config = data.get(i).get('start_config')
        else:
            name = i[1].get('name')
            displayname = i[1].get('displayname')
            pid = i[1].get('pid')
            status = i[1].get('status')
            descriptions = i[1].get('descriptions')
            start_config = i[1].get('start_config')

        return name, displayname, pid, status, descriptions, start_config
    
    def usage(self):
        
        import argparse
        parse = argparse.ArgumentParser(formatter_class= argparse.RawTextHelpFormatter, version= '1.0')
        parse.add_argument('-f', '--filter', help = 'Filter', action = 'store', nargs = '*')
        parse.add_argument('-sa', '--start', help = 'Start Service by Name or PID', action = 'store', nargs = '*')
        parse.add_argument('-sp', '--pause', help = 'Puse Service by Name or PID', action = 'store', nargs = '*')
        parse.add_argument('-st', '--stop', help = 'Stop Service by Name or PID', action = 'store', nargs = '*')
        parse.add_argument('-k', '--kill', help = 'Kill process/Hard Stop with Name or PID if available', action = 'store', nargs = '*')
        parse.add_argument('-S', '--sort-by', help = 'Sort list by, available argument: [name, pid, status, start, display_name, description]', action = 'store', type = str)
        parse.add_argument('-s', '--sort-status', help = 'Sort list by Status', action = 'store_true')
        parse.add_argument('-ss', '--sort-status-only', help = 'Sort list and Only Show Sorted by Status, available argument: [STOPPED, START PENDING, STOP PENDING, RUNNING, PAUSE PENDING, PAUSED, START, STOPPING, PAUSE CONTINUE]', action = 'store')
        parse.add_argument('-p', '--sort-pid', help = 'Sort list by PID', action = 'store_true')
        parse.add_argument('-n', '--sort-name', help = 'Sort list by Name', action = 'store_true')
        parse.add_argument('-d', '--sort-displayname', help = 'Sort list by Display Name', action = 'store_true')
        parse.add_argument('-c', '--sort-start-config', help = "Sort list by Config Start type", action = 'store_true')
        parse.add_argument('-cc', '--sort-start-config-only', help = "Sort list and Only Show Sorted by Config Start type, available argument: ['BOOT START', 'SYSTEM START', 'AUTO START', 'DEMAND_START', 'DISABLED']", action = 'store')
        parse.add_argument('-T', '--tail', help = 'Sort list by time and show last of N', action = 'store', type = int)
        parse.add_argument('-z', '--fast', help = 'search by the last of list service', action = 'store_true')
        parse.add_argument('-r', '--reverse', help = 'List reverse', action = 'store_true')
        parse.add_argument('-rr', '--recursive', help = 'Recursive service and child', action = 'store_true')
        parse.add_argument('-R', '--restart', help = 'Restart service', action = 'store', nargs='*')
        parse.add_argument('-F', '--fast-list-details', help = 'Show all details of service', action = 'store_true')
        parse.add_argument('-x', '--search', help = 'search by input [name, pid, status, start, display_name, description]', action = 'store', nargs = '*')
        parse.add_argument('-xx', '--search-stop', help = 'search by input [name, pid, status, start, display_name, description] and stop', action = 'store', nargs = '*')
        parse.add_argument('-xs', '--search-start', help = 'search by input [name, pid, status, start, display_name, description] and start', action = 'store', nargs = '*')
        parse.add_argument('-xp', '--search-pause', help = 'search by input [name, pid, status, start, display_name, description] and pause', action = 'store', nargs = '*')
        parse.add_argument('-X', '--search-kill', help = 'search by input [name, pid, status, start, display_name, description] and kill by PID if available', action = 'store', nargs = '*')
        parse.add_argument('-l', '--list-details', help = 'Show all details of process', action = 'store_true')
        #parse.add_argument('-t', '--sort-time', help = 'Sort list by time of start/creation', action = 'store_true')
        #parse.add_argument('-m', '--sort-mem', help = 'Sort list by Private Memory usage', action = 'store_true')
        #parse.add_argument('-w', '--sort-cpu-percent', help = 'Sort list by CPU Load Percent', action = 'store_true')
        #parse.add_argument('-e', '--sort-exe', help = 'Sort list by Exe Name', action = 'store_true')
        #parse.add_argument('-a', '--all', help = 'Show all list include this', action = 'store_true')
        #parse.add_argument('-c', '--childs', help = 'Show all Childs process of process', action = 'store_true')
        #parse.add_argument('-M', '--memory-details', help = 'Show all memory details of process', action = 'store_true')
        #parse.add_argument('-d', '--details', help = 'Show all details of process', action = 'store_true')
        #parse.add_argument('-C', '--show-cpu-percent', help = 'Show CPU Load Percent', action = 'store_true')
        #parse.add_argument('-MM', '--memory-detail', help = 'Show all memory detail of one process by given pid or correct name', action = 'store', type = int)
        #parse.add_argument('-N', '--show-networks', help='Show with networks connection if available, this is only for list mode, for table mode (default) there is only networks connection showing', action='store_true')
        #parse.add_argument('-No', '--show-networks-only', help='Show networks connection only if available', action='store_true')
        
        args = parse.parse_args()
        
        SORTED = False
        sorting = args.sort_by
        if args.search:
            self.search(args.search, False, args.fast, args.details, args.childs, args.recursive)
        elif args.restart:
            self.restart(args.restart)
        elif args.search_kill:
            self.search(args.search_kill, True, args.fast, args.details, args.childs, args.recursive)
        #elif args.memory_detail:
            #self.get_memory_full_info(args.memory_detail, True)
        else:
            #if args.sort_time:
                #sorting = 'time'
            #if args.sort_cpu_percent:
                #sorting = 'cpu'
            #if args.sort_mem:
                #sorting = 'mem'
            if args.sort_pid:
                sorting = 'pid'
            if args.sort_status:
                sorting = 'status'
            #if args.sort_exe:
                #sorting = 'exe'
            if args.sort_name:
                sorting = 'name'
            if args.sort_displayname:
                sorting = 'displayname'
            if args.sort_status:
                sorting = 'status'            
            if args.sort_start_config:
                sorting = 'start_config'            
            if args.sort_by:
                sorting = args.sort_by
            #if args.kill:
                #self.kill(args.kill)
            #if args.always_kill:
                #self.kill(args.always_kill, True)
            pfilter = []
            if args.filter:
                for i in args.filter:
                    pfilter.append(str(i).lower())
            
            service_dict = self.getService()
            
            try:
                debug(args = args)
                list_details = args.list_details
                if args.fast_list_details:
                    list_details = True
                
                debug(list_details = list_details)
                self.makeTable(service_dict, pfilter, sorting, args.tail, args.reverse, list_details, args.fast_list_details, args.sort_status_only, args.sort_start_config_only)
            except:
                if os.getenv('DEBUG') or os.getenv('debug'):
                    traceback.format_exc(print_msg= True)
                else:
                    traceback.format_exc(print_msg= False)
                pass

    def sort_dict(self, myDict, value_sort_name, reverse = False):
        dicts = myDict.items()
        dicts.sort(key=lambda (k,d): (d[value_sort_name]), reverse = reverse)
        return dicts    
    
if __name__ == '__main__':
    c = ServiceList()
    #c.getServiceList()
    #c.getState()
    c.usage()