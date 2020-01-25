#pep8 compliance states that import should go biggest to smallest
#in alphabetical order of items of the same length
from time import sleep
import subprocess
import json
import math
import time
import io
import os
import re

#Simulates a call to the system with less overhead
#functions in prodecural python scripts should be created above
#where they are called
def touch(path):
    """
    Emulates the 'touch' command by creating the file at *path* if it does not
    exist.  If the file exist its modification time will be updated.
    """
    with io.open(path, 'ab'):
        return os.utime(path, None)

def get_last_timestamp(path):
    return int(os.stat(path).st_mtime)

#Set up watch services object

start_time = time.time()
watch_services = {    
    'uwsgi' : {
        'folders': [
        	'/webapps/day_score/day_score',
        	'/webapps/day_score/api'
        ],
        'action' : 'touch /etc/uwsgi/vassals/uwsgi.ini',
        'do_action': False,
        'skip_action': False
    },
    'webpack' : {
        'folders' : [
        	'/webapps/day_score/static/app/src'
        ],
        'action' : 'something',
        'do_action': False,
        'skip_action': False
    }
}

#Set up required varibles
main_dir = '/webapps/day_score/scripts/file_watcher'
uwsgi_ini_path = '/etc/uwsgi/vassals/uwsgi.ini'
watch_stats_file = '/webapps/day_score/scripts/file_watcher/last_modified.json'
file = None
file_json = None
out_file_json = dict()
folder_list = dict()

#Read the last modified information if it exists
try:
    file = open(watch_stats_file, 'r')
    file_json = json.load(file)
    file.close()
except:
    pass

#loop on the watch services object key = service name value is object
for key, value in watch_services.items():
    for folder in value['folders']:#loop folder in value object
        #call a subprocess to get the latest modified timestamp from each file
        if key == 'webpack':#logic specific to webpack
            proc = subprocess.Popen([main_dir+'/subprocWebpack.sh', folder],
                                stdout=subprocess.PIPE)
            (out, err) = proc.communicate()#get output from subprocess
            webpack_list = str(out).split('\\n')
            for webpack_item in webpack_list:#must watch all files under src
                matches = re.match('(\d+)\.\d+\s(.*)', str(webpack_item))
                if matches is not None:
                    folder_list[str(matches.group(2))]=int(matches.group(1))

        #I have a feeling this can be limited  to not run for webpack
        proc = subprocess.Popen([main_dir+'/subproc.sh', folder],
                                stdout=subprocess.PIPE)
        (out, err) = proc.communicate()#get output from subprocess
        numbers = re.findall('\d+', str(out))#capture numbers from output
        if len(numbers):#verify we have results
            folder_list[folder]=int(numbers[0])#store the {folder:modified ts}

#TODO loop once - Kinda accomplished
#loop services again
for key, value in watch_services.items():
    for folder, timestamp in folder_list.items():#loop captured folder info
        if folder in value['folders']:
            out_file_json[folder] = timestamp
            if file_json is None:#is this our first run?
                value['do_action'] = True;
            elif key == 'webpack' and int(file_json[folder]) < int(timestamp):
                value['do_action'] = True;
                print (out_file_json)
            elif key != 'webpack' and not file_json[folder] == timestamp:
                value['do_action'] = True;

    #TODO add logic for migrations maybe
    if value['do_action']:#if do action is True        
        if key == 'uwsgi' and not value['skip_action']:
            touch(uwsgi_ini_path)#restart backend rest api
            value['do_action'] = False;
        elif key == 'webpack':#TODO
            value['do_action'] = False#its done that enouch
            print('preoutput', out_file_json)
            for folder, timestamp in folder_list.items():
                if value['folders'][0] in folder:
                    try:
                        touch(folder)
                    except:
                        print('cant touch this', folder)
            time.sleep(3)
            for folder, timestamp in folder_list.items():
                if value['folders'][0] in folder and \
                folder != value['folders'][0]:
                    out_file_json[folder] = get_last_timestamp(folder)
            #a dirty fix
            proc = subprocess.Popen([main_dir+'/subproc.sh',
                                    value['folders'][0]],
                                    stdout=subprocess.PIPE)
            (out, err) = proc.communicate()#get output from subprocess
            numbers = re.findall('\d+', str(out))#capture numbers from output
            if len(numbers):#verify we have results
                out_file_json[value['folders'][0]] = int(numbers[0])
            print('output', out_file_json)

file = open(watch_stats_file, 'w+')
json.dump(out_file_json, file)
file.close()

print('--- %s seconds ---' % (time.time() - start_time))
