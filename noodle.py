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
        printHelp()
    return args

def doJob(cmdType, args):
    if cmdType == 999:
        printHelp()
    if cmdType == 1:
        writeToConfig()
    if cmdType == 2:
        removeFromConfig(args)
    if cmdType == 3:
        listOutConfig(args)
    if cmdType == 4:
        editConfigEntry(args)
    if cmdType == 5:
        conf = getConfig()
        connectToServer(conf, args)

def writeToConfig():
    checkConfig()
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    name = ''
    server = ''
    login = ''
    port = ''
    while len(name) < 1 or name in config:
        print('  Enter a name for the entry: ', end='')
        name = input()
    while len(server) < 4:
        print('  Enter IP address or domain: ', end='')
        server = input()
    print("  Enter login (default 'root'): ", end='')
    login = input()
    login = server or 'root'
    print("  Enter port (default '22'): ", end='')
    port = input()
    port = port or '22'
    config[name] = [{"name":name, "server":server, "login":login, "port":port}]
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w') as data_file:
        json.dump(config, data_file)
    print('  Added new entry with the name: ' + name)

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
        ['', 'Name', 'Server', 'Login', 'Port'],
        ['', '', '', '', '']
    ]
    index = 1
    with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'r') as data_file:
        config = json.load(data_file)
    if len(config) > 0:
        for el in config:
            name = config[el]
            for servers in name:
                table.append([str(index) + '.', servers['name'], servers['server'], servers['login'], servers['port']])
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
        if len(args) > 1:
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

    def help():
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
        'c': connect(),
        'help': help(),
        'h': help()
    }
    return statement.get(argument, 999)

def checkConfig():
    if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.config', 'noodle')):
        print('  No configuration directory detected, creating...')
        os.makedirs(os.path.join(os.path.expanduser('~'), '.config', 'noodle'))
        print('  Created configuration directory in: ' + os.path.join(os.path.expanduser('~'), '.config', 'noodle'))
    if not os.path.isfile(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json')):
        print('  No configuration file found, creating...')
        f = open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w+')
        f.write('{}')
        f.close()
        print('  Created configuration file in: ' + os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'))
        return
    if not os.stat(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json')).st_size > 1:
        print('  Detected invalid content of configuration file, recreating...')
        f = open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w+')
        f.write('{}')
        f.close()
        print('  Recreated configuration file')
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
        for el in config.get(args[2]):
            servName = el['name']
            servServer = el['server']
            servLogin = el['login']
            servPort = el['port']
        print('  Enter new name for the element [' + servName + ']: ', end='')
        newName = input()
        newName = newName or servName
        print('  Enter new server for the element [' + servServer + ']: ', end='')
        newServer = input()
        newServer = newServer or servServer
        print('  Enter new login for the element [' + servLogin + ']: ', end='')
        newLogin = input()
        newLogin = newLogin or servLogin
        print('  Enter new port for the element [' + servPort + ']: ', end='')
        newPort = input()
        newPort = newPort or servPort
        config.pop(args[2], None)
        config[newName] = [{"name": newName, "server": newServer, "login":newLogin, "port":newPort}]
        with open(os.path.join(os.path.expanduser('~'), '.config', 'noodle', 'noodle.json'), 'w') as data_file:
            json.dump(config, data_file)
        print('  Edited the entry')
    else:
        print('  No entry with that name')

def connectToServer(config, args):
    for server in config:
        if server['name'] == args[2]:
            serv = server['server']
            login = server['login']
            port = server['port']
            print('  Trying to resolve SSH connection to ' + serv, end='\n\n  ')
    spawn_process(parse_program_path('ssh' + ' -l ' + login + ' -p ' + port + ' ' + serv))

def printHelp():
    print('  Usage:')
    print('    General form: noodle [option] <arguments>')
    print('    Arguments inside [ ] are required, arguments inside < > are optional')
    print()
    print('    Options:')
    print('      help, h - no arguments, shows this page')
    print('      add, a - no arguments, prompts the user to add a new entry into the config')
    print('      delete, del, d - one argument: <name> of an entry present in config, removes an entry from the config')
    print('      edit, e - one argument: <name> of an entry present in config, prompts the user to enter new values for an entry')
    print('      list, l - no arguments, lists out all entries in the config')
    print('      connect, con, c - one argument: <name> of an entry present in config, connects to a server')
    print()
    print('    Example usage:')
    print('      noodle add')
    print('      noodle delete example')
    print('      noodle edit example')
    print('      noodle list')
    print('      noodle connect example')
    exit()
                
def main():
    arguments = getArguments()
    commandType = parseArguments(arguments[1], arguments)
    doJob(commandType, arguments)

if __name__ == '__main__':
    print('\nNoodle ssh manager\n')
    main()
    print()
    