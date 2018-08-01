#!/usr/bin/python2
#-*- encoding: UTF-8 -*-
#encoding: UTF-8
#author: Hadi Cahyadi <licface@yahoo.com>
#licence: MiT

import psutil
import sys
from texttable import Texttable
import cmdw
MAX_LENGTH = cmdw.getWidth() - 4
if not sys.platform == 'win32':
    MAX_LENGTH = MAX_LENGTH - 4
from make_colors import make_colors
import colorama
colorama.init(autoreset=True)
import time
import os
import math
import traceback
import random
import cmdw
from debug import * 
PID = os.getpid()

class ProcessList(object):
    def __init__(self):
        super(ProcessList, self)
        self.NAME = ''
        self.NAME_FIRST = True
        self.NUMBER_FIRST = 0

    def convert_size(self, size_bytes):
        if (size_bytes == 0):
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return '%s %s' % (s, size_name[i])

    def printList(self, name, pid, exe, mem, cmd, cpu, status, fast_list_mode, number="*"):
        if fast_list_mode:
            print str(number) + ". " + make_colors(str(name), 'lightcyan', color_type= 'colorama') + " " \
                  + "[" + make_colors(str(pid), 'lightyellow', color_type= 'colorama') + "]" + " " \
            + make_colors(str(mem), 'lightgreen', color_type= 'colorama') + " " \
            + "(" + make_colors(str(status), 'lightmagenta', color_type= 'colorama') + ")"
        else:
            print "NAME   :", make_colors(str(name), 'lightcyan', color_type= 'colorama')
            print "PID    :", make_colors(str(pid), 'lightyellow', color_type= 'colorama')
            print "EXE    :", make_colors(str(exe), 'lightred', color_type= 'colorama')
            print "MEM    :", make_colors(str(mem), 'lightgreen', color_type= 'colorama')
            print "CMD    :", make_colors(str(cmd), 'lightblue', color_type= 'colorama')
            print "CPU    :", make_colors(str(cpu), 'lightcyan', color_type= 'colorama')
            print "STATUS :", make_colors(str(status), 'lightmagenta', color_type= 'colorama')

    def printListNetworks(self, local_address, local_port, remote_address, remote_port, status, type, family, fd, fast_list_mode, number=None, name=None, pid=None, dont_print_number=True, mode_tree=True, fast_group = True):
        number_out = number
        if number:
            number = str(number) + ". "
        else:
            number = ''
            
        if dont_print_number:
            number = '-'
        
        if not name:
            name =''

        if not pid:
            pid = ''
        else:
            pid = "(" + str(pid) + ")"
        if mode_tree:
            tree_add_1 = "   |"
            tree_add_2 = "   +-"
        else:
            tree_add_1 = ""
            tree_add_2 = ""
        if fast_list_mode:
            if local_address:
                if fast_group:
                    if name == self.NAME:
                        self.NAME_FIRST = False
                        name = ''
                        pid = ''
                        number = '-'
                        try:
                            print "   |"
                        except:
                            pass
                        tree_add_2 = "   +-"
                        
                    else:
                        try:
                            print "\n"
                        except:
                            pass
                        self.NAME_FIRST = True
                        #number = number_out + 1
                    if self.NAME_FIRST:
                        tree_add_2 = ''
                        number_out += 1
                try:
                    sys.stdout.write(tree_add_2 + number + make_colors(str(name), 'lightcyan', color_type= 'colorama') \
                    + make_colors(pid, 'lightyellow', color_type= 'colorama') + " " \
                    + "[" + "local=" + make_colors(str(local_address) + ":" + str(local_port), 'lightgreen', color_type= 'colorama') + "]" + " " \
                    + "[" + "remote=" + make_colors(str(remote_address) + ":" + str(remote_port), 'lightblue', color_type= 'colorama') + "]" + " " \
                    + "(" + make_colors("fd:" + str(fd), 'lightgreen', color_type= 'colorama') \
                    + "," + make_colors("type:" + str(type), 'lightmagenta', color_type= 'colorama') \
                    + "," + make_colors("family:" + str(family), 'lightred', color_type= 'colorama') + ")" + " " \
                    + "| " "STATUS: " + make_colors(str(status), 'lightyellow', color_type= 'colorama') + '\n')
                except:
                    pass
                self.NAME = name

        else:
            if name and pid:
                print "NAME           :", make_colors(str(name), 'lightcyan', color_type= 'colorama')
                print "PID            :", make_colors(str(pid), 'lightyellow', color_type= 'colorama')
            print "LOCAL ADDRESS  :", make_colors(str(local_address), 'lightgreen', color_type= 'colorama')
            print "LOCAL PORT     :", make_colors(str(local_port), 'lightgreen', color_type= 'colorama')
            print "REMOTE ADDRESS :", make_colors(str(remote_address), 'lightblue', color_type= 'colorama')
            print "REMOTE PORT    :", make_colors(str(remote_port), 'lightblue', color_type= 'colorama')
            print "STATUS         :", make_colors(str(status), 'lightyellow', color_type= 'colorama')
            print "FD             :", make_colors(str(fd), 'lightgreen', color_type= 'colorama')
            print "PROTOCOL       :", make_colors(str(type), 'lightmagenta', color_type= 'colorama')
            print "SOCK           :", make_colors(str(family), 'lightred', color_type= 'colorama')
        
        return name, number_out

    def getData(self, i, sort=False, data_search=None):
        #debug(data_search = data_search)
        #debug(SORT = sort)
        list_networks = []
        
        if not sort:
            try:
                mem = data_search.get(i).get('mem')
            except:
                mem = ''            
            name = data_search.get(i).get('name')
            pid = data_search.get(i).get('pid')
            exe =  data_search.get(i).get('exe')
            cmd = " ".join(data_search.get(i).get('cmd'))
            cpu = data_search.get(i).get('cpu')
            time  = data_search.get(i).get('time')
            if mem:
                mem = self.convert_size(data_search.get(i).get('mem'))
            status = data_search.get(i).get('status')
            connections = data_search.get(i).get('connections')
        else:
            mem = i[1].get('mem')
            name = i[1].get('name')
            pid = i[1].get('pid')
            exe =  i[1].get('exe')
            cpu =  i[1].get('cpu')
            time =  i[1].get('time')
            cmd = " ".join(i[1].get('cmd'))
            status = i[1].get('status')
            if mem:
                mem = self.convert_size(i[1].get('mem'))
            connections = i[1].get('connections')

        return name, pid, exe, cmd, cpu, time, status, mem, connections

    def getDataNetworks(self, connections):
        local_address = ''
        local_port = ''
        remote_address = ''
        remote_port = ''
        fd = ''
        protocol = ''
        type = ''
        status = ''
        list_networks = []
        if connections:
            for i in connections:
                fd = connections.get(i).get('fd')
                protocol = connections.get(i).get('protocol')
                type = connections.get(i).get('type')
                laddr = connections.get(i).get('laddr')
                raddr = connections.get(i).get('raddr')
                if laddr:
                    local_address, local_port = laddr
                if raddr:
                    remote_address, remote_port = raddr
                status = connections.get(i).get('status')
                if status == "NONE":
                    status = ''
                list_networks.append((fd, type, protocol, local_address, local_port, remote_address, remote_port, status))

        return list_networks


    def makeTableAdd(self, table, number, name, pid, exe, mem, cpu, cmd, show_cpu, status=None):
        try:
            if status:
                if show_cpu:
                    table.add_row([str(number), name, str(pid), exe, mem, cpu, cmd, status])
                else:
                    table.add_row([str(number), name, str(pid), exe, mem, cmd, status])
            else:
                if show_cpu:
                    table.add_row([str(number), name, str(pid), exe, mem, cpu, cmd])
                else:
                    table.add_row([str(number), name, str(pid), exe, mem, cmd])
        except:
            print traceback.format_exc()
            print "="*MAX_LENGTH
            if status:
                if show_cpu:
                    table.add_row([
                        str(number),
                        unicode(name).encode(sys.stdout.encoding, errors='replace'),
                        unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                        unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                        unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                        unicode(cpu).encode(sys.stdout.encoding, errors='replace'),
                        unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                        unicode(status).encode(sys.stdout.encoding, errors='replace'), 
                    ])
                else:
                    table.add_row([
                        str(number),
                        unicode(name).encode(sys.stdout.encoding, errors='replace'),
                        unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                        unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                        unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                        unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                        unicode(status).encode(sys.stdout.encoding, errors='replace'), 
                    ])
            else:
                if show_cpu:
                    table.add_row([
                        str(number),
                        unicode(name).encode(sys.stdout.encoding, errors='replace'),
                        unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                        unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                        unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                        unicode(cpu).encode(sys.stdout.encoding, errors='replace'),
                        unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                    ])
                else:
                    table.add_row([
                        str(number),
                        unicode(name).encode(sys.stdout.encoding, errors='replace'),
                        unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                        unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                        unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                        unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                    ])
        return table

    def makeTableAddNetworks(self, table, number, name, pid, exe, local_address, local_port, remote_address, remote_port, fd, type, protocol, status, print_networks_only=False):
        if self.NUMBER_FIRST == number:
            number_print = ''
        else:
            number_print = number
        
        try:
            if print_networks_only:
                table.add_row([
                    local_address,
                    local_port, 
                    remote_address,
                    remote_port,
                    protocol,
                    fd,
                    type,
                    status
                ])
            else:
                table.add_row([
                    str(number_print),
                    name,
                    str(pid),
                    local_address,
                    local_port, 
                    remote_address,
                    remote_port,
                    type,
                    fd,
                    protocol,
                    status,
                    exe
                ])
        except:
            if print_networks_only:
                table.add_row([
                    unicode(local_address).encode(sys.stdout.encoding, errors='replace'),
                    unicode(local_port).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(remote_address).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(remote_port).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(type).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(fd).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(protocol).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(type).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(status).encode(sys.stdout.encoding, errors='replace'), 
                ])
            else:
                table.add_row([
                    str(number_print),
                    unicode(name).encode(sys.stdout.encoding, errors='replace'),
                    unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                    unicode(local_address).encode(sys.stdout.encoding, errors='replace'),
                    unicode(local_port).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(remote_address).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(remote_port).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(type).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(fd).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(protocol).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(status).encode(sys.stdout.encoding, errors='replace'), 
                    unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                ])
        self.NUMBER_FIRST = number
        if not self.NAME_FIRST == name:        
            number += 1
        self.NAME_FIRST = name
        return table, number

    def printNetworks(self, networks, fast_list_mode, number=None, name=None, pid=None, fast_group = True):
        if number:
            dont_print_number = False
        else:
            dont_print_number = True
        for i in self.getDataNetworks(networks):
            fd, type, protocol, local_address, local_port, remote_address, remote_port, status = i
            if name and pid:
                name, number = self.printListNetworks(local_address, local_port, remote_address, remote_port, status, type, protocol, fd, fast_list_mode, number, name, pid, fast_group = fast_group, dont_print_number= dont_print_number)
            else:
                name, number = self.printListNetworks(local_address, local_port, remote_address, remote_port, status, type, protocol, fd, fast_list_mode, number, fast_group = fast_group, dont_print_number= dont_print_number)
        return number

    def makeTable(self, data_search, filter = None, sort=None, tail = None, show_cpu = False, reverse=False, show_status=False, list_details=False, fast_list_mode=False, show_networks=False, show_networks_only=False):
        number = 1
        if fast_list_mode:
            list_details = True
        # debug(data_search0 = data_search)
        debug(sort = sort)
        if sort:
            data_search = self.sort_dict(data_search, sort, reverse)
            if tail:
                data_search = data_search[-int(tail):]
        else:
            if tail:
                data_search1 = {}
                data_search_keys = data_search.keys()[-int(tail):]
                for i in data_search_keys:
                    data_search1.update({i:data_search.get(i)})
                data_search = data_search1
        if MAX_LENGTH <= (220 / 2) or list_details:
            number_network = 1
            if not sort: #MAX_LENGTH <= (220 / 2)
                if filter: #MAX_LENGTH <= (220 / 2)
                    for i in data_search:
                        if os.path.splitext(data_search.get(i).get('name'))[0].lower() in filter or data_search.get(i).get('pid') in filter:
                            name, pid, exe, cmd, cpu, time, status, mem, connections = self.getData(i, False, data_search)
                            if show_networks_only:
                                number_network = self.printNetworks(connections, fast_list_mode, number_network, name, pid)
                            else:
                                self.printList(name, pid, exe, mem, cmd, cpu, status, fast_list_mode, number_network)
                                if show_networks:
                                    number_network = self.printNetworks(connections, fast_list_mode, number = number_network)
                            if not fast_list_mode:
                                print "-" * MAX_LENGTH
                            number += 1
                else:
                    for i in data_search:
                        name, pid, exe, cmd, cpu, time, status, mem, connections = self.getData(i, False, data_search)
                        if show_networks_only:
                            number_network = self.printNetworks(connections, fast_list_mode, number_network, name, pid)
                        else:
                            self.printList(name, pid, exe, mem, cmd, cpu, status, fast_list_mode, number)
                            if show_networks:
                                number_network = self.printNetworks(connections, fast_list_mode, number = number_network)
                        if not fast_list_mode:
                            print "-" * MAX_LENGTH
                        number += 1
            else: #MAX_LENGTH <= (220 / 2)
                if filter: #MAX_LENGTH <= (220 / 2)
                    for i in data_search:
                        if os.path.splitext(i[1].get('name'))[0].lower() in filter or i[1].get('pid') in filter:
                            name, pid, exe, cmd, cpu, time, status, mem, connections = self.getData(i, sort)
                            if show_networks_only:
                                self.printNetworks(connections, fast_list_mode, number)
                            else:
                                self.printList(name, pid, exe, mem, cmd, cpu, status, fast_list_mode, number)
                                if show_networks:
                                    self.printNetworks(connections, fast_list_mode, number)
                            if not fast_list_mode:
                                print "-" * MAX_LENGTH
                            number += 1
                else:
                    for i in data_search:
                        name, pid, exe, cmd, cpu, time, status, mem, connections = self.getData(i, sort)
                        if show_networks_only:
                            self.printNetworks(connections, fast_list_mode, number)
                        else:
                            self.printList(name, pid, exe, mem, cmd, cpu, status, fast_list_mode, number)
                            if show_networks:
                                self.printNetworks(connections, fast_list_mode, number)
                        if not fast_list_mode:
                            print "-" * MAX_LENGTH
                        number += 1
        #END ~ MAX_LENGTH <= (220 / 2)
        else:
            table = Texttable()
            if show_cpu:
                if show_status:
                    table.header(['No','Name','PID','EXE', 'Mem', 'CPU %', 'CMD', 'STATUS'])
                    table.set_cols_align(["l", "l", "l", "l", "c", "c", "c", "c"])
                    table.set_cols_valign(["t", "m", "m", "m", "m", "m", "t", "m"])
                else:
                    table.header(['No','Name','PID','EXE', 'Mem', 'CPU %', 'CMD'])
                    table.set_cols_align(["l", "l", "l", "l", "c", "c", "c"])
                    table.set_cols_valign(["t", "m", "m", "m", "m", "m", "t"])
                if sys.platform == 'win32':
                    if show_status:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.02), #No
                                int(MAX_LENGTH * 0.1),  #Name
                                int(MAX_LENGTH * 0.03), #PID
                                int(MAX_LENGTH * 0.24), #EXE
                                int(MAX_LENGTH * 0.05), #Mem
                                int(MAX_LENGTH * 0.03), #CPU
                                int(MAX_LENGTH * 0.38), #CMD
                                int(MAX_LENGTH * 0.06), #STATUS
                        ])
                    else:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.02), #No
                            int(MAX_LENGTH * 0.1),  #Name
                            int(MAX_LENGTH * 0.03), #PID
                            int(MAX_LENGTH * 0.24), #EXE
                            int(MAX_LENGTH * 0.05), #Mem
                            int(MAX_LENGTH * 0.03), #CPU
                            int(MAX_LENGTH * 0.44), #CMD
                        ])
                else:
                    table.header(['No','Name','PID','EXE', 'Mem', 'CPU %', 'CMD', 'STATUS'])
                    if show_status:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.03), #No
                                int(MAX_LENGTH * 0.1),  #Name
                                int(MAX_LENGTH * 0.04), #PID
                                int(MAX_LENGTH * 0.28), #EXE
                                int(MAX_LENGTH * 0.05), #Mem
                                int(MAX_LENGTH * 0.03), #CPU
                                int(MAX_LENGTH * 0.33), #CMD
                                int(MAX_LENGTH * 0.06), #STATUS
                        ])
                    else:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.03), #No
                            int(MAX_LENGTH * 0.1),  #Name
                            int(MAX_LENGTH * 0.04), #PID
                            int(MAX_LENGTH * 0.28), #EXE
                            int(MAX_LENGTH * 0.05), #Mem
                            int(MAX_LENGTH * 0.03), #CPU
                            int(MAX_LENGTH * 0.39), #CMD
                        ])
            elif show_networks_only or show_networks:
                table.header(['No','Name','PID', 'L_Address', 'L_Port', 'R_Address', 'R_Port','Type','Fd','Sock', 'Status','EXE'])
                table.set_cols_align(["l", "l", "l", "l", "c", "c", "c", "c", "c", "c", "c", "c"])
                table.set_cols_valign(["t", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m"])
                if sys.platform == 'win32':
                    #self.makeTableAddNetworks(number, name, pid, exe, local_address, local_port, remote_address, remote_port, fd, type, protocol, status
                    table.set_cols_width([
                        int(MAX_LENGTH * 0.02), #No
                        int(MAX_LENGTH * 0.1),  #Name
                        int(MAX_LENGTH * 0.03), #PID
                        int(MAX_LENGTH * 0.08), #L_Address
                        int(MAX_LENGTH * 0.05), #L_Port
                        int(MAX_LENGTH * 0.08), #R_Address
                        int(MAX_LENGTH * 0.05), #R_Port
                        int(MAX_LENGTH * 0.05), #Sock
                        int(MAX_LENGTH * 0.02), #Fd
                        int(MAX_LENGTH * 0.03), #Family
                        int(MAX_LENGTH * 0.08), #Status
                        int(MAX_LENGTH * 0.25), #EXE
                    ])
                else:
                    table.set_cols_width([
                        int(MAX_LENGTH * 0.03), #No
                        int(MAX_LENGTH * 0.1),  #Name
                        int(MAX_LENGTH * 0.04), #PID
                        int(MAX_LENGTH * 0.08), #L_Address
                        int(MAX_LENGTH * 0.05), #L_Port
                        int(MAX_LENGTH * 0.08), #R_Address
                        int(MAX_LENGTH * 0.05), #R_Port
                        int(MAX_LENGTH * 0.05), #Sock
                        int(MAX_LENGTH * 0.02), #Fd
                        int(MAX_LENGTH * 0.03), #Family
                        int(MAX_LENGTH * 0.08), #Status
                        int(MAX_LENGTH * 0.22), #EXE
                    ])
            else:
                if show_status:
                    table.header(['No','Name','PID','EXE', 'Mem', 'CMD', 'STATUS'])
                    table.set_cols_align(["l", "l", "l", "l", "c", "c", "c"])
                    table.set_cols_valign(["t", "m", "m", "m", "m", "t", "m"])
                else:
                    table.header(['No','Name','PID','EXE', 'Mem', 'CMD'])
                    table.set_cols_align(["l", "l", "l", "l", "c", "c"])
                    table.set_cols_valign(["t", "m", "m", "m", "m", "t"])
                if sys.platform == 'win32':
                    if show_status:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.02), #No
                                int(MAX_LENGTH * 0.1),  #Name
                                int(MAX_LENGTH * 0.03), #PID
                                int(MAX_LENGTH * 0.28), #EXE
                                int(MAX_LENGTH * 0.05), #Mem
                                int(MAX_LENGTH * 0.38), #CMD
                                int(MAX_LENGTH * 0.06), #STATUS
                        ])
                    else:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.02), #No
                            int(MAX_LENGTH * 0.1),  #Name
                            int(MAX_LENGTH * 0.03), #PID
                            int(MAX_LENGTH * 0.28), #EXE
                            int(MAX_LENGTH * 0.05), #Mem
                            int(MAX_LENGTH * 0.44), #CMD
                        ])
                else:
                    if show_status:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.03), #No
                                int(MAX_LENGTH * 0.1),  #Name
                                int(MAX_LENGTH * 0.04), #PID
                                int(MAX_LENGTH * 0.28), #EXE
                                int(MAX_LENGTH * 0.05), #Mem
                                int(MAX_LENGTH * 0.36), #CMD
                                int(MAX_LENGTH * 0.06), #Status
                        ])
                    else:
                        table.set_cols_width([
                            int(MAX_LENGTH * 0.03), #No
                            int(MAX_LENGTH * 0.1),  #Name
                            int(MAX_LENGTH * 0.04), #PID
                            int(MAX_LENGTH * 0.28), #Mem
                            int(MAX_LENGTH * 0.05), #CMD
                            int(MAX_LENGTH * 0.42), #Status
                        ])

            sys.dont_write_bytecode = True
            number = 1
            number_network = 1
            if not sort:
                if filter:
                    data = {}
                    m = 1
                    for x in data_search.keys():
                        if os.path.splitext(data_search.get(x).get('name'))[0].lower() in filter:
                            data.update({m: data_search.get(x)})
                            m +=1
                    data_search = data
                    #debug(data_search=data_search)
                for i in data_search:
                    name, pid, exe, cmd, cpu, time, status, mem, connections = self.getData(i, False, data_search)
                    if not show_status:
                        status = None
                    if show_networks or show_networks_only:
                        if connections:
                            for conn in self.getDataNetworks(connections):
                                fd, type, protocol, local_address,\
                                    local_port, remote_address, remote_port,\
                                    status_network = conn
                                table, number_network = self.makeTableAddNetworks(table, number_network, name, pid, exe, local_address, local_port, remote_address, remote_port, fd, type, protocol, status_network, print_networks_only=False)

                    else:
                        table = self.makeTableAdd(table, number, name, pid, exe, mem, cpu, cmd, show_cpu, status)
                    number += 1
                    #number_network += 1
            else:
                if filter:
                    data = []
                    for x in data_search:
                        if os.path.splitext(x[1].get('name'))[0].lower() in filter:
                            data.append(x)
                    data_search = data

                for i in data_search:
                    name, pid, exe, cmd, cpu, time, status, mem, connections = self.getData(i, True, data_search)
                    if not show_status:
                        status = None
                    if show_networks or show_networks_only:
                        if connections:
                            for conn in self.getDataNetworks(connections):
                                fd, type, protocol, local_address,\
                                    local_port, remote_address, remote_port,\
                                    status_network = conn
                                table, number_network = self.makeTableAddNetworks(table, number_network, name, pid, exe, local_address, local_port, remote_address, remote_port, fd, type, protocol, status_network, print_networks_only=False)

                    else:
                        table = self.makeTableAdd(table, number, name, pid, exe, mem, cpu, cmd, show_cpu, status)
                    number += 1
                    number_network += 1

            print table.draw()
        return data_search, number

    def sort_dict(self, myDict, value_sort_name, reverse = False):
        dicts = myDict.items()
        dicts.sort(key=lambda (k,d): (d[value_sort_name]), reverse = reverse)
        return dicts

    def get_memory_full_info(self, pid, separted = True, process_instance = None, tab = 1):
        random_colors = ['yellow', 'green', 'blue', 'cyan', 'magenta', 'white', 'red']
        lens = []
        pid = int(pid)
        try:
            if not process_instance:
                p = psutil.Process(pid)
                mem = p.memory_full_info()
            else:
                mem = process_instance.memory_full_info()
        except:
            return ()
        for i in mem._fields:
            lens.append(len(i))
        MAX = max(lens)

        print "\t" * (tab - 1) + make_colors("MEMORY DETAILS:", 'yellow', ['bold'])
        print "\t" * tab + "RSS" + " " * (MAX - len("RSS")) + " = " + make_colors(self.convert_size(mem.rss), "yellow")
        print "\t" * tab + "VMS" + " " * (MAX - len("VMS")) + " = " + make_colors(self.convert_size(mem.vms), "green")
        if sys.platform == 'win32':
            print "\t" * tab + "NUM PAGE FAULTS" + " " * (MAX - len("NUM PAGE FAULTS")) + " = " + make_colors(self.convert_size(mem.num_page_faults), "magenta")
            print "\t" * tab + "WSET" + " " * (MAX - len("WSET")) + " = " + make_colors(self.convert_size(mem.wset), "cyan")
            print "\t" * tab + "PEAK WSET" + " " * (MAX - len("PEAK WSET")) + " = " + make_colors(self.convert_size(mem.peak_wset), "red")
            print "\t" * tab + "PAGED POOL" + " " * (MAX - len("PAGED POOL")) + " = " + make_colors(self.convert_size(mem.paged_pool), "blue")
            print "\t" * tab + "PEAK PAGED POOL" + " " * (MAX - len("PEAK PAGED POOL")) + " = " + make_colors(self.convert_size(mem.peak_paged_pool), "red")
            print "\t" * tab + "NONPAGED POOL" + " " * (MAX - len("NONPAGED POOL")) + " = " + make_colors(self.convert_size(mem.nonpaged_pool), "green")
            print "\t" * tab + "PEAK NONPAGED POOL" + " " * (MAX - len("PEAK NONPAGED POOL")) + " = " + make_colors(self.convert_size(mem.peak_nonpaged_pool), "red")
            print "\t" * tab + "PAGEFILE" + " " * (MAX - len("PAGEFILE")) + " = " + make_colors(self.convert_size(mem.pagefile), "yellow")
            print "\t" * tab + "PEAK PAGEFILE" + " " * (MAX - len("PEAK PAGEFILE")) + " = " + make_colors(self.convert_size(mem.peak_pagefile), "red")
            print "\t" * tab + "PRIVATE" + " " * (MAX - len("PRIVATE")) + " = " + make_colors(self.convert_size(mem.private), "white")
        else:
            print "\t" * tab + "PSS" + " " * (MAX - len("PSS")) + " = " + make_colors(self.convert_size(mem.pss), "white")
            print "\t" * tab + "SHARED" + " " * (MAX - len("SHARED")) + " = " + make_colors(self.convert_size(mem.shared), "white")
            print "\t" * tab + "SWAP" + " " * (MAX - len("SHARED")) + " = " + make_colors(self.convert_size(mem.swap), "white")
            print "\t" * tab + "TEXT" + " " * (MAX - len("TEXT")) + " = " + make_colors(self.convert_size(mem.text), "white")
            print "\t" * tab + "LIB" + " " * (MAX - len("LIB")) + " = " + make_colors(self.convert_size(mem.lib), "white")
            print "\t" * tab + "DATA" + " " * (MAX - len("DATA")) + " = " + make_colors(self.convert_size(mem.data), "white")
            print "\t" * tab + "DIRTY" + " " * (MAX - len("DIRTY")) + " = " + make_colors(self.convert_size(mem.dirty), "white")
            print "\t" * tab + "DIRTY" + " " * (MAX - len("DIRTY")) + " = " + make_colors(self.convert_size(mem.dirty), "white")
        print "\t" * tab + "USS" + " " * (MAX - len("USS")) + " = " + make_colors(self.convert_size(mem.uss), "magenta")
        if separted:
            print "-" * (MAX + 15)
        return mem

    def get_child(self, pid, separated = True, process_instance = None, memory_detail = False, tab = 2, kill = False):
        if not process_instance:
            childs = psutil.Process(int(pid)).children()
            print make_colors("CHILDS PROCESS DETAILS:", 'yellow', ['bold'])
            for i in childs:
                print "\t" * tab + "Name   :", make_colors(str(i.name()), 'yellow')
                print "\t" * tab + "PID    :", make_colors(str(i.pid), 'white', 'red')
                print "\t" * tab + "EXE    :", make_colors(str(i.exe()), 'white', 'green')
                print "\t" * tab + "MEM    :", make_colors(self.convert_size(i.memory_info().vms), 'white', 'blue')
                if str(i.name()) == str(" ".join(i.cmdline())):
                    print "\t" * tab + "CMD    :"
                else:
                    print "\t" * tab + "CMD    :", make_colors(str(" ".join(i.cmdline())), 'white', 'blue')
                if kill:
                    i.terminate()
                try:
                    print "\t" * tab + "STATUS :", make_colors(str(i.status().upper()), 'white', 'yellow', ['bold', 'blink'])
                except:
                    print "\t" * tab + "STATUS :", make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                try:
                    pid = i.pid
                    if memory_detail:
                        self.get_memory_full_info(pid, False, tab = 2)
                except:
                    print make_colors("PROCESS TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                if separated:
                    print "+" * 100            

        else:
            childs = process_instance.children()
            print make_colors("CHILDS PROCESS DETAILS:", 'yellow', ['bold'])
            for i in childs:
                print "\t" * tab + "Name   :", make_colors(str(i.name()), 'yellow')
                print "\t" * tab + "PID    :", make_colors(str(i.pid), 'white', 'red')
                print "\t" * tab + "EXE    :", make_colors(str(i.exe()), 'white', 'green')
                print "\t" * tab + "MEM    :", make_colors(self.convert_size(i.memory_info().vms), 'white', 'blue')
                if str(i.name()) == str(" ".join(i.cmdline())):
                    print "\t" * tab + "CMD    :"
                else:
                    print "\t" * tab + "CMD    :", make_colors(str(" ".join(i.cmdline())), 'white', 'blue')
                if kill:
                    i.terminate()
                try:
                    print "\t" * tab + "STATUS :", make_colors(str(i.status().upper()), 'white', 'yellow', ['bold', 'blink'])
                except:
                    print "\t" * tab + "STATUS :", make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                try:
                    pid = i.pid
                    if memory_detail:
                        self.get_memory_full_info(pid, False, tab = 2)
                except:
                    print make_colors("PROCESS TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                if separated:
                    print "+" * 100                        


    def psItem(self, process, n, show_cpu=False, show_all=False, user='all', pid = None, process_dict = None):
        #n = 1        
        with process.oneshot():
            list_network = {}
            name, exe, cmd, mem = "", "", [], ()
            try:
                name = process.name()   
                cmd = process.cmdline()
                exe = process.exe()
                pid = process.pid
                if show_cpu:
                    # cpu = process.cpu_percent(interval = 0.116)
                    cpu = process.cpu_percent()
                else:
                    cpu = 0.0
                mem = process.memory_full_info().vms
                time = process._create_time
                status = process.status()
                connections = process.connections()
                if connections:
                    nn = 1
                    for i in connections:
                        fd, protocol, type, laddr, raddr, status_networks = i
                        if laddr:
                            laddr = (laddr[0], laddr[1])
                        if raddr:
                            laddr = (raddr[0], raddr[1])
                        if type == 1:
                            type = 'TCP'
                        elif type == 2:
                            type = 'UDP'
                        if protocol == 2:
                            protocol = 'IPv4'
                        elif protocol == 23:
                            protocol = 'IPv6'
                        list_network.update({
                            nn: {
                                'fd':fd,
                                'protocol':protocol,
                                'type':type,
                                'laddr':laddr,
                                'raddr':raddr,
                                'status':status_networks
                            }
                        })
                        nn += 1

                if not show_all:
                    if str(pid) == str(PID):
                        pass
                    else:
                        process_dict.update({
                            n: {
                                    'name': name,
                                    'cmd': cmd,
                                    'exe': exe,
                                    'pid': pid,
                                    'cpu': cpu,
                                    'mem': mem,
                                    'time': time,
                                    'status': status,
                                    'connections': list_network
                                    },
                        })                
                        n += 1
            # except (psutil.AccessDenied, psutil.ZombieProcess):
            except psutil.AccessDenied:
                if user == 'all' :
                    name = process.name()   
                    try:
                        cmd = process.cmdline()
                    except psutil.AccessDenied:
                        cmd = ''
                    try:
                        exe = process.exe()
                    except psutil.AccessDenied:
                        exe = ''
                    pid = process.pid
                    if show_cpu:
                        # cpu = process.cpu_percent(interval = 0.116)
                        cpu = process.cpu_percent()
                    else:
                        cpu = 0.0
                    try:
                        mem = process.memory_full_info().vms
                    except psutil.AccessDenied:
                        mem = ''
                    time = process._create_time
                    status = process.status()
                    connections = process.connections()
                    if connections:
                        fd, protocol, type, laddr, raddr, status_networks = connections[0]
                        if laddr:
                            laddr = (laddr[0], laddr[1])
                        if raddr:
                            laddr = (raddr[0], raddr[1])
                        if type == 1:
                            type = 'TCP'
                        elif type == 2:
                            type = 'UDP'
                        if protocol == 2:
                            protocol = 'IPv4'
                        elif protocol == 23:
                            protocol = 'IPv6'
                        list_network.update({
                            'fd':fd,
                            'protocol':protocol,
                            'type':type,
                            'laddr':laddr,
                            'raddr':raddr,
                            'status':status_networks
                        })

                    if not show_all:
                        if str(pid) == str(PID):
                            pass
                        else:
                            process_dict.update({
                                n: {
                                        'name': name,
                                        'cmd': cmd,
                                        'exe': exe,
                                        'pid': pid,
                                        'cpu': cpu,
                                        'mem': mem,
                                        'time': time,
                                        'status': status,
                                        'connections': list_network
                                        },
                            })                
                            n += 1

            except psutil.ZombieProcess:
                print "ZombieProcess=", process
            except psutil.NoSuchProcess:
                print "Process Inai =", process
            except:
                traceback.format_exc()
        return process_dict, n
                
    def ps(self, show_cpu=False, show_all=False, user='all', pid = None):
        list_process = {}
        n = 1
        if pid:
            process = psutil.Process(pid)
            dict_process, n = self.psItem(process, n, show_cpu, show_all, user, pid, list_process)
        for process in psutil.process_iter():
            dict_process, n = self.psItem(process, n, show_cpu, show_all, user, pid, list_process)
            #debug(list_process = list_process)
            #list_process.update(list_process_add)
        #debug(list_process_x = list_process)
        return list_process

    def kill(self, kills, always_kill = False):
        list_process, list_filter = self.ps()
        #print "-" * 100
        ver = 0
        for i in kills:
            if str(i).isdigit():
                for n in list_process:
                    if int(i) == list_process.get(n).get('pid'):
                        p = psutil.Process(int(i))
                        p.terminate()
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                        if p.is_running():
                            print "STATUS :", make_colors("RUNNING !", 'white', 'red', ['bold', 'blink'])
                            if always_kill:
                                while 1:
                                    if p.is_running():
                                        print make_colors("Re-Terminating .....", 'red', attrs= ['bold', 'blink'])
                                        p.terminate()
                                        time.sleep(1)
                                    else:
                                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                            print "CMD    :"
                                        else:
                                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                                
                                        print "STATUS :", make_colors("TERMINATED / KILLED", 'white', 'red', ['bold', 'blink'])
                                        break
                        else:
                            try:
                                print "STATUS :", make_colors(p.status().title(), 'white', 'red', ['bold', 'blink'])
                            except:
                                print "STATUS :", make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                        print "-" * 100
            else:
                for n in list_process:
                    if str(i) == list_process.get(n).get('name'):
                        ver += 1
                        p = psutil.Process(list_process.get(n).get('pid'))
                        p.terminate()
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                        if p.is_running():
                            print "STATUS :", make_colors("RUNNING !", 'white', 'red', ['bold', 'blink'])
                            if always_kill:
                                while 1:
                                    if p.is_running():
                                        print make_colors("Re-Terminating .....", 'red', attrs= ['bold', 'blink'])
                                        p.terminate()
                                        time.sleep(1)
                                    else:
                                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                        print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                            print "CMD    :"
                                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                            print "CMD    :"
                                        else:
                                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                                
                                        print "STATUS :", make_colors("TERMINATED / KILLED", 'white', 'red', ['bold', 'blink'])
                                        break
                        else:
                            try:
                                print "STATUS :", make_colors(p.status().upper(), 'white', 'red', ['bold', 'blink'])
                            except:
                                print make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                        print "-" * 100
                    else:
                        if str(i) in list_process.get(n).get('name'):
                            ver += 1
                            p = psutil.Process(list_process.get(n).get('pid'))
                            p.terminate()
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                            if p.is_running():
                                print "STATUS :", make_colors("RUNNING !", 'white', 'red', ['bold', 'blink'])
                                if always_kill:
                                    while 1:
                                        if p.is_running():
                                            print make_colors("Re-Terminating .....", 'red', attrs= ['bold', 'blink'])
                                            p.terminate()
                                            time.sleep(1)
                                        else:
                                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                            print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                                print "CMD    :"
                                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                                print "CMD    :"
                                            else:
                                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                                
                                            print "STATUS :", make_colors("TERMINATED / KILLED", 'white', 'red', ['bold', 'blink'])
                                            break
                            else:
                                try:
                                    print "STATUS :", make_colors(p.status().upper(), 'white', 'red', ['bold', 'blink'])
                                except:
                                    print make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                            print "-" * 100
            if ver == 0:
                print "STATUS :", make_colors("NOT FOUND !!!", 'white', 'red', ['bold', 'blink'])

    def search(self, query, kill = False, fast = False, memory_detail = False, child_detail = False, kill_recursive = False):
        list_process, list_filter = self.ps()
        ver = 0
        if fast:
            list_process1, list_filter1 = self.ps(query, 'time')
            for p in list_filter1[-len(query):]:
                try:
                    x = psutil.Process(p[1].get('pid'))
                except:
                    pass
                print "Name   :", make_colors(str(p[1].get('name')), 'yellow')
                print "PID    :", make_colors(str(p[1].get('pid')), 'white', 'red')
                print "EXE    :", make_colors(str(p[1].get('exe')), 'white', 'green')
                print "MEM    :", make_colors(self.convert_size(p[1].get('mem')), 'white', 'blue')
                if str(p[1].get('name')) == str(" ".join(p[1].get('cmd'))):
                    print "CMD    :"
                elif str(p[1].get('exe')) == str(" ".join(p[1].get('cmd'))):
                    print "CMD    :"                    
                else:
                    print "CMD    :", make_colors(str(" ".join(p[1].get('cmd'))), 'white', 'blue')
                if kill:
                    try:
                        x.terminate()
                    except:
                        pass
                try:
                    STATUS = x.status()
                except:
                    STATUS = "TERMINATED !!!"                    
                print "STATUS : " + make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                #print make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                if memory_detail:
                    self.get_memory_full_info(p[1].get('pid'), False)
                if child_detail:
                    self.get_child(p[1].get('pid'), False, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                print "-" * MAX_LENGTH        
            #print "list_process =", list_process[-len(query):]
            #print "list_filter  =", list_filter[-len(query):]
            #print "-" * 200
        else:
            for i in query:
                if str(i).isdigit():
                    for n in list_process:
                        if int(i) == list_process.get(n).get('pid'):
                            p = psutil.Process(int(i))
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"                    
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                            if kill:
                                p.terminate()                        
                            try:
                                STATUS = p.status()
                            except:
                                STATUS = "TERMINATED !!!"                    
                            print "STATUS : " + make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            #print make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            if memory_detail:
                                self.get_memory_full_info(list_process.get(n).get('pid'), False)
                            if child_detail:
                                self.get_child(list_process.get(n).get('pid'), True, process_instance= p, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                            print "-" * MAX_LENGTH
                else:
                    for n in list_process:
                        if str(i).lower() == list_process.get(n).get('name').lower():
                            ver += 1
                            try:
                                p = psutil.Process(list_process.get(n).get('pid'))
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                else:
                                    print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                                if kill:
                                    p.terminate()                            
                                try:
                                    STATUS = p.status()
                                except:
                                    STATUS = "TERMINATED !!!"                    
                                print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                if memory_detail:
                                    self.get_memory_full_info(list_process.get(n).get('pid'), False)
                                if child_detail:
                                    self.get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive) 
                                print "-" * MAX_LENGTH
                            except psutil.NoSuchProcess:
                                pass
                            except:
                                traceback.format_exc()
                        else:
                            if str(i).lower() in list_process.get(n).get('name').lower():
                                ver += 1
                                try:
                                    p = psutil.Process(list_process.get(n).get('pid'))
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    else:
                                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                                    if kill:
                                        p.terminate()                                
                                    try:
                                        STATUS = p.status()
                                    except:
                                        STATUS = "TERMINATED !!!"                    
                                    print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                    if memory_detail:
                                        self.get_memory_full_info(list_process.get(n).get('pid'), False)
                                    if child_detail:
                                        self.get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                                    print "-" * MAX_LENGTH
                                except psutil.NoSuchProcess:
                                    pass
                                except:
                                    traceback.format_exc()
                    if ver == 0:
                        for n in list_process:
                            if not sys.platform == 'win32':
                                n_check = list_process.get(n).get('exe')
                            else:
                                n_check = list_process.get(n).get('exe')[0]
                            if str(i) == n_check.lower():
                                ver += 1
                                p = psutil.Process(list_process.get(n).get('pid'))
                                if kill:
                                    p.terminate()
                                try:
                                    STATUS = p.status()
                                except:
                                    STATUS = "TERMINATED !!!"                        
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                else:
                                    print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                                print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                if memory_detail:
                                    self.get_memory_full_info(list_process.get(n).get('pid'), False)
                                if child_detail:
                                    self.get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                                print "-" * MAX_LENGTH
                            else:
                                if str(i) in list_process.get(n).get('exe').lower():
                                    ver += 1
                                    p = psutil.Process(list_process.get(n).get('pid'))
                                    if kill:
                                        p.terminate()
                                    try:
                                        STATUS = p.status()
                                    except:
                                        STATUS = "TERMINATED !!!"                        
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    else:
                                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                                    print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                    if memory_detail:
                                        self.get_memory_full_info(list_process.get(n).get('pid'), False)
                                    if child_detail:
                                        self.get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive)  
                                    print "-" * MAX_LENGTH
                    if ver == 0:
                        print make_colors("NOT FOUND !", 'white', 'red', ['bold', 'blink'])

    def restart(self, query):
        import subprocess
        list_process, process = self.ps()
        ver = 0
        for i in query:
            if str(i).isdigit():
                for n in list_process:
                    if int(i) == list_process.get(n).get('pid'):
                        cmd = []
                        p = psutil.Process(int(i))
                        p.terminate()
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"                    
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                        try:
                            STATUS = p.status()
                        except:
                            STATUS = "TERMINATED !!!"                    
                        print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                        print "+" * 100
                        while 1:
                            try:
                                p.status()
                            except:
                                a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                p1 = psutil.Process(int(a.pid))
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(self.convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                print "CMD    :", " ".join(cmd)
                                print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                try:
                                    x = p.status()
                                    if x == 'running':
                                        break
                                    if not a.poll():
                                        break
                                except:
                                    if not a.poll():
                                        break
                                    else:
                                        pass
                                (out, err) = a.communicate()
                                if err:
                                    print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                    print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                break
                        print "-" * 100
            else:
                for n in list_process:
                    if str(i).lower() == list_process.get(n).get('name').lower():
                        cmd = []
                        ver += 1
                        p = psutil.Process(list_process.get(n).get('pid'))
                        p.terminate()
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                        try:
                            STATUS = p.status()
                        except:
                            STATUS = "TERMINATED !!!"                    
                        print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                        print "+" * 100
                        while 1:
                            try:
                                p.status()
                            except:
                                a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                p1 = psutil.Process(int(a.pid))
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(self.convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                print "CMD    :", " ".join(cmd)
                                print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                try:
                                    x = p.status()
                                    if x == 'running':
                                        break
                                    if not a.poll():
                                        break
                                except:
                                    if not a.poll():
                                        break
                                    else:
                                        pass
                                (out, err) = a.communicate()
                                if err:
                                    print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                    print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                break
                        print "-" * 100
                    else:
                        if str(i).lower() in list_process.get(n).get('name').lower():
                            cmd = []
                            ver += 1
                            p = psutil.Process(list_process.get(n).get('pid'))
                            p.terminate()
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                            try:
                                STATUS = p.status()
                            except:
                                STATUS = "TERMINATED !!!"                    
                            print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            print "+" * 100
                            while 1:
                                try:
                                    p.status()
                                except:
                                    a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                    p1 = psutil.Process(int(a.pid))
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    print "MEM    :", make_colors(self.convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                    print "CMD    :", " ".join(cmd)
                                    print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                    try:
                                        x = p.status()
                                        if x == 'running':
                                            break
                                        if not a.poll():
                                            break
                                    except:
                                        if not a.poll():
                                            break
                                        else:
                                            pass
                                    (out, err) = a.communicate()
                                    if err:
                                        print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                        print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                    break
                            print "-" * 100
                if ver == 0:
                    for n in list_process:
                        if str(i) == list_process.get(n).get('exe')[0].lower():
                            cmd = []
                            ver += 1
                            p = psutil.Process(list_process.get(n).get('pid'))
                            p.terminate()
                            try:
                                STATUS = p.status()
                            except:
                                STATUS = "TERMINATED !!!"                        
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) in str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                                cmd = list_process.get(n).get('cmd')
                            print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            print "+" * 100
                            while 1:
                                try:
                                    p.status()
                                except:
                                    a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                    p1 = psutil.Process(int(a.pid))
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    print "MEM    :", make_colors(self.convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                    print "CMD    :", " ".join(cmd)
                                    print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                    try:
                                        x = p.status()
                                        if x == 'running':
                                            break
                                        if not a.poll():
                                            break
                                    except:
                                        if not a.poll():
                                            break
                                        else:
                                            pass
                                    (out, err) = a.communicate()
                                    if err:
                                        print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                        print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                    break
                            print "-" * 100
                        else:
                            if str(i) in list_process.get(n).get('exe').lower():
                                cmd = []
                                ver += 1
                                p = psutil.Process(list_process.get(n).get('pid'))
                                p.terminate()
                                try:
                                    STATUS = p.status()
                                except:
                                    STATUS = "TERMINATED !!!"                        
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(self.convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                elif str(list_process.get(n).get('exe')) in str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                else:
                                    print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                                    cmd = list_process.get(n).get('cmd')
                                print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                print "+" * 100
                                while 1:
                                    try:
                                        p.status()
                                    except:
                                        a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                        p1 = psutil.Process(int(a.pid))
                                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                        print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                        print "MEM    :", make_colors(self.convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                        print "CMD    :", " ".join(cmd)
                                        print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                        try:
                                            x = p.status()
                                            if x == 'running':
                                                break
                                            if not a.poll():
                                                break
                                        except:
                                            if not a.poll():
                                                break
                                            else:
                                                pass
                                        (out, err) = a.communicate()
                                        if err:
                                            print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                            print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                        break
                                print "-" * 100
                if ver == 0:
                    print make_colors("NOT FOUND !", 'white', 'red', ['bold', 'blink'])

    def usage(self):
        help = """
        pl.py -f xporcess1 xporcess2
        pl.py --filter xporcess1.exe xporcess2.exe
        pl.py -f 9939 9877
        pl.py -k killprocess
        pl.py --kill killprocess.exe
        pl.py --kill 9919

    Options:
        -h --help      Show this help
        -f --filter    filter process, this will show at end
        -k --kill      list process and kill process
        -v --version   this version

    """
        import argparse
        parse = argparse.ArgumentParser(formatter_class= argparse.RawTextHelpFormatter, version= '1.0')
        parse.add_argument('-f', '--filter', help = 'Filter', action = 'store', nargs = '*')
        parse.add_argument('-k', '--kill', help = 'Kill process with name or PID', action = 'store', nargs = '*')
        parse.add_argument('-K', '--always-kill', help = 'Kill process with name or PID', action = 'store', nargs = '*')
        parse.add_argument('-S', '--show-status', help = 'Show status process', action = 'store_true')
        parse.add_argument('-s', '--sort-by', help = 'Sort list by [name, pid, exe, mem, cmd]', action = 'store', type = str)
        parse.add_argument('-t', '--sort-time', help = 'Sort list by time of start/creation', action = 'store_true')
        parse.add_argument('-m', '--sort-mem', help = 'Sort list by Private Memory usage', action = 'store_true')
        parse.add_argument('-p', '--sort-pid', help = 'Sort list by PID', action = 'store_true')
        parse.add_argument('-w', '--sort-cpu-percent', help = 'Sort list by CPU Load Percent', action = 'store_true')
        parse.add_argument('-e', '--sort-exe', help = 'Sort list by Exe Name', action = 'store_true')
        parse.add_argument('-n', '--sort-name', help = 'Sort list by Name', action = 'store_true')
        parse.add_argument('-T', '--tail', help = 'Sort list by time and show last of N', action = 'store', type = int)
        parse.add_argument('-x', '--search', help = 'search by input [name, pid, mem] for mem which approaching', action = 'store', nargs = '*')
        parse.add_argument('-X', '--search-kill', help = 'search by input [name, pid, mem] for mem which approaching then kill', action = 'store', nargs = '*')
        parse.add_argument('-z', '--fast', help = 'search by the last of list process', action = 'store_true')
        parse.add_argument('-r', '--reverse', help = 'List reverse', action = 'store_true')
        parse.add_argument('-rr', '--recursive', help = 'Recursive process and child', action = 'store_true')
        parse.add_argument('-R', '--restart', help = 'Restart process', action = 'store', nargs='*')
        parse.add_argument('-a', '--all', help = 'Show all list include this', action = 'store_true')
        parse.add_argument('-c', '--childs', help = 'Show all Childs process of process', action = 'store_true')
        parse.add_argument('-M', '--memory-details', help = 'Show all memory details of process', action = 'store_true')
        parse.add_argument('-d', '--details', help = 'Show all details of process', action = 'store_true')
        parse.add_argument('-l', '--list-details', help = 'Show all details of process', action = 'store_true')
        parse.add_argument('-F', '--fast-list-details', help = 'Show all details of process', action = 'store_true')
        parse.add_argument('-C', '--show-cpu-percent', help = 'Show CPU Load Percent', action = 'store_true')
        parse.add_argument('-MM', '--memory-detail', help = 'Show all memory detail of one process by given pid or correct name', action = 'store', type = int)
        parse.add_argument('-N', '--show-networks', help='Show with networks connection if available, this is only for list mode, for table mode (default) there is only networks connection showing', action='store_true')
        parse.add_argument('-No', '--show-networks-only', help='Show networks connection only if available', action='store_true')
        parse.add_argument('-A', '--user-all', action='store_true', help='Run with current user')
        args = parse.parse_args()
        #print "args.filter =", args.filter
        #if len(sys.argv) == 1:
            #p, p1 = self.ps()
            #self.makeTable(p, p1)
        #else:
        SORTED = False
        sorting = args.sort_by
        if args.search:
            self.search(args.search, False, args.fast, args.details, args.childs, args.recursive)
        elif args.restart:
            self.restart(args.restart)
        elif args.search_kill:
            self.search(args.search_kill, True, args.fast, args.details, args.childs, args.recursive)
        elif args.memory_detail:
            self.get_memory_full_info(args.memory_detail, True)
        else:
            if args.sort_time:
                sorting = 'time'
            if args.sort_cpu_percent:
                sorting = 'cpu'
            if args.sort_mem:
                sorting = 'mem'
            if args.sort_pid:
                sorting = 'pid'
            if args.sort_exe:
                sorting = 'exe'
            if args.sort_name:
                sorting = 'name'
            if args.sort_by:
                sorting = args.sort_by
            if args.kill:
                self.kill(args.kill)
            if args.always_kill:
                self.kill(args.always_kill, True)
            pfilter = []
            if args.filter:
                for i in args.filter:
                    pfilter.append(str(i).lower())
            if args.user_all:
                user = 'all'
            else:
                user = ''
            lister = self.ps(args.show_cpu_percent, args.all, user)

            try:
                self.makeTable(lister, pfilter, sorting, args.tail, args.show_cpu_percent, args.reverse, args.show_status, args.list_details, args.fast_list_details, args.show_networks, args.show_networks_only)
            except:
                if os.getenv('DEBUG') or os.getenv('debug'):
                    traceback.format_exc(print_msg= True)
                else:
                    traceback.format_exc(print_msg= False)
                pass

if __name__ == '__main__':
    #p, p1 = self.ps()
    #self.makeTable(p)
    c = ProcessList()
    c.usage()
    #query = ['python', 'fmedia']
    #self.search(query, False, True)
