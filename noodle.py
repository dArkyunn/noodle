#!/usr/bin/env python3

from subprocess import run as spawn_process
from shlex import split as parse_program_path
from sys import argv, exit
import json
import os

def getArguments():
    args = []
    if len(argv) > 1:
        for el in argv:
            args.append(el)
    else:
        print('  Usage:\n  noodle [option] <arg1> <arg2> <argN>\n') # change to a help call
        exit(3)
    return args

def doJob(cmdType, args):
    if cmdType == 999:
        print('  Usage:\n  noodle [option] <arg1> <arg2> <argN>')
    if cmdType == 1:
        writeToConfig(args)
    if cmdType == 2:
        removeFromConfig(args)
    if cmdType == 3:
        listOutConfig(args)
    if cmdType == 4:
        editConfigEntry(args)
    if cmdType == 5:
        conf = getConfig()
        connectToServer(conf, args)

def writeToConfig(args):
    checkConfig()
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    if args[2] in config:
        print('  Element with that name already exists')
        return
    config[args[2]] = [{"name":args[2], "server":args[3]}]
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w') as data_file:
        json.dump(config, data_file)
    print('  Added new entry with the name: ' + args[2])

def removeFromConfig(args):
    checkConfig()
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    if args[2] in config:
        config.pop(args[2], None)
    else:
        print('  Element with that name doesn\'t exist')
        return
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w') as data_file:
        json.dump(config, data_file)
    print('  Removed config entry with the name: ' + args[2])

def listOutConfig(args):
    checkConfig()
    table = [
        ['', 'Name', 'Server'],
        ['', '', '']
    ]
    index = 1
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    if len(config) > 0:
        for el in config:
            name = config[el]
            for servers in name:
                table.append([str(index) + '.', servers['name'], servers['server']])
                index += 1
        print_table(table)
    else:
        print('  There are no servers saved')

def readFromConfig():
    checkConfig()
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    return config

def print_table(table):
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))

def parseArguments(argument, args):
    def add():
        if len(args) == 4:
            return 1
        else:
            return 999

    def delete():
        if len(args) == 3:
            return 2
        else:
            return 999

    def sList():
        if len(args) > 1:
            return 3
        else:
            return 999

    def edit():
        if len(args) == 3:
            return 4
        else:
            return 999

    def connect():
        if len(args) == 3:
            return 5
        else:
            return 999

    statement = {
        'add': add(),
        'a': add(),
        'delete': delete(),
        'del': delete(),
        'd': delete(),
        'list': sList(),
        'l': sList(),
        'edit': edit(),
        'e': edit(),
        'connect': connect(),
        'con': connect(),
        'c': connect()
    }
    return statement.get(argument, 999)

def checkConfig():
    if not os.path.isfile(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json')):
        f = open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w+')
        f.write('{}')
        f.close()
        return
    if not os.stat(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json')).st_size > 1:
        f = open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w+')
        f.write('{}')
        f.close()
        return

def getConfig():
    checkConfig()
    conf = list()
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    for elem in config:
        el = config[elem]
        conf.extend(el)
    return conf

def editConfigEntry(args):
    config = readFromConfig()
    if args[2] in config:
        print('  Enter new name for the element [' + args[2] + ']: ', end='')
        newName = input()
        newName = newName or args[2]
        print('  Enter new server for the element [none]: ', end='')
        newServer = input()
        newServer = newServer or ''
        config.pop(args[2], None)
        config[newName] = [{"name": newName, "server": newServer}]
        with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w') as data_file:
            json.dump(config, data_file)
        print('  Edited the entry')

def connectToServer(config, args):
    for server in config:
        if server['name'] == args[2]:
            name = server['server']
            print('  Trying to resolve SSH Connection to ' + name, end='\n\n  ')
    spawn_process(parse_program_path('ssh ' + name))
                
def main():
    arguments = getArguments()
    commandType = parseArguments(arguments[1], arguments)
    doJob(commandType, arguments)

if __name__ == '__main__':
    print('\nNoodle ssh manager\n')
    main()
    print('\nEnd of Noodle output', end='\n\n')
    