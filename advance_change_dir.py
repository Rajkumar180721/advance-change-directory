
import os, json, argparse, readline
# import signal

basePath = os.path.dirname(os.path.realpath(__file__))
ignore_json = basePath+'/ignore_list.json'

def findDirs(target: str, path: str, exclude: list, detected_dir: list):

    dir_list = os.listdir(path)

    dir_list = [d for d in dir_list if d not in exclude and os.path.isdir(path+d) and not d.startswith('.')]

    detected_dir += [f'{path}{d}/' for d in dir_list if d == target]

    for d in dir_list:
        findDirs(target, f'{path}{d}/', exclude, detected_dir)
    
    return detected_dir


def getDirectories(dir_name: str, xclude=['node_modules'], startPath='/home/raj/Documents/'):
    
    exclude = set(['node_modules', 'lib', '__pycache__'])
    # detected_dir = []

    detected_dir = findDirs(dir_name, startPath, exclude, [])

    # print(detected_dir)
    
    # for dirpath, dirnames, _ in os.walk(startPath):
    #     dirnames[:] = [d for d in dirnames if d not in exclude and not d.startswith('.')]
    #     for dir in dirnames:
    #         if dir == dir_name:
    #             dir = os.path.join(dirpath, dir)
    #             detected_dir.append(dir)
    
    if (len(detected_dir) == 1):
        return detected_dir[0]
    elif(len(detected_dir) > 1):
        print('Mutiple directories detected')
        for i, dir in enumerate(detected_dir):
            print('{0}) {1}'.format(i, dir))
        input_ind = ''
        while(1):
            input_ind = int(input('Enter the index to change dir (Ctrl+c - exit):'))
            if (input_ind < 0 or input_ind > len(detected_dir) -1):
                print('\tUnmatched index')
            else:
                break
        return detected_dir[input_ind]
    return False



def read_input(input_text):
    def complete(text,state):
        # print(text, state)
        results = [x for x in ignore_list['volcab'] if x.startswith(text)]
        return results[state]

    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set colored-completion-prefix on")
    readline.parse_and_bind("set show-all-if-unmodified on")
    readline.parse_and_bind("set horizontal-scroll-mode on")
    readline.set_completer_delims(' ') # this line fixed the *- or Phypen* detection issue
    readline.set_completer(complete)
    input_value = input('Enter the name of the directory. Leave empty to exit: ')
    return input_value

def open_terminal(dir):
    try:
        cmd = 'gnome-terminal --tab --working-directory={}'.format(dir)
        os.system(cmd)
        #  closes the current tab
        # os.kill(os.getppid(), signal.SIGHUP)
    except:
        print('Unable to access directory ', dir)




def writeIgnoreList(ignore_list: dict):
    with open(ignore_json, mode='w') as outfile:
            outfile.write(json.dumps(ignore_list, indent=2))
    


if (__name__ == '__main__'):

    try:
        file = open(ignore_json, mode='r+')
        ignore_list = json.load(file)
        # print(ignore_list)
    except:
        print('Ignore_list file is empty\nCreating new file')
        ignore_list = {
            "ignore": ["node_modules"],
            "default_path": "/home/raj/Documents/",
            "showWarning": True,
            "volcab": []
        }
        writeIgnoreList(ignore_list)

    parser = argparse.ArgumentParser(description='advanced change directory')
    parser.add_argument(
        '--remove_dir', '-r', action='store',
        help = 'Delete a dir from volcab'
    )
    parser.add_argument(
        'dir_name', action='store', nargs='*',
        help = 'change the current working directory to passed directory'
    )


    args = vars(parser.parse_args())

    output = ''
    if args['remove_dir']:
        ignore_list['volcab'] = [dir for dir in ignore_list['volcab'] if dir != args['remove_dir']]
        writeIgnoreList(ignore_list)

    elif (args['dir_name']):
        output = getDirectories(args['dir_name'][0])
        # opens a new tab with specificed path
        if (output):
            newVolcab = ignore_list['volcab']
            newVolcab.append(args['dir_name'][0])
            ignore_list['volcab'] = list(set(newVolcab))
            writeIgnoreList(ignore_list)
            open_terminal(output)
        else:
            print('unable to find directory')
    else:
        dir_name = read_input('Enter the name of the directory. Leave empty to exit: ')
        if (dir_name):
            output = getDirectories(dir_name)
            # opens a new tab with specificed path
            if (output):
                newVolcab = ignore_list['volcab']
                newVolcab.append(dir_name)
                ignore_list['volcab'] = list(set(newVolcab))
                writeIgnoreList(ignore_list)
                # print(ignore_list)
                open_terminal(output)
            else:
                print('unable to find directory')