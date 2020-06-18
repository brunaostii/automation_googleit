#!/usr/bin/env python3

''' this program process the syslog file and counts the total errors and who user 
is responsible for info and error'''

import re
import csv
import operator

if __name__ == '__main__':
    per_user, error = {}, {}
    arquivo = 'syslog.log'
    usuarios = []
    with open(arquivo, 'r') as file:
        lines = file.readlines()
        for line in lines:
            users = re.search(r'\(([\w]*)\)', line)
            
            if users:
                users = users.group(1)

                if users not in usuarios:
                    usuarios.append(users)
        usuarios = sorted(usuarios)
        per_user['username'] = usuarios
        per_user['INFO'] = [0]*len(usuarios)
        per_user['ERROR'] = [0]*len(usuarios)

        for line in lines:
            errors = re.search(r'ERROR ([\w \'?]*)', line)
            info = re.search(r'INFO ([\w ]*)', line)
            users = re.search(r'\(([\w]*)\)', line)

            if errors:
                try:
                    error[errors.group(1)] += 1
                except:
                    error[errors.group(1)] = 1 

            if users:
                index = usuarios.index(users.group(1))
                if info:
                    per_user['INFO'][index] +=1

                elif errors:
                    per_user['ERROR'][index] +=1

error = sorted(error.items(), key = operator.itemgetter(1), reverse=True)


with open('user_statistics.csv', 'w') as f:
    f.write('{},{},{}\n'.format('username', 'INFO', 'ERROR'))
    for i in range(len(usuarios)):
        f.write('{},{},{}\n'.format(per_user['username'][i], per_user['INFO'][i], per_user['ERROR'][i])) 


with open('error_message.csv', 'w') as f:
    f.write('{},{}\n'.format('Error','Count'))
    [f.write('{0},{1}\n'.format(error[i][0], error[i][1])) for i in range(len(error))]
