import os
from eventloop import EventLoop, FileSystemWatch, SingleShotTimer, walk
import eventloop.base
import eventloop
import argparse
from colorama import Fore, Back, Style, init as colorama_init
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE, check_output
import datetime
import sys
import shutil

def debug_print_on(*args):
    print(*args)

def debug_print_off(*args):
    pass

if 'DEBUG_WATCH_UI' in os.environ and os.environ['DEBUG_WATCH_UI'] == "1":
    debug_print = debug_print_on
else:
    debug_print = debug_print_off

try:
    import PySide2
    debug_print("using PySide2")
except ImportError:
    try:
        import PyQt5
        debug_print("using PyQt5")
    except:
        raise Exception("PySide2 not found and PyQt5 not found")

has_PySide2 = 'PySide2' in globals()
has_PyQt5 = 'PyQt5' in globals()

def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class UiData:
    def __init__(self, path):
        self._path = path
        tree = ET.parse(path)
        root = tree.getroot()
        item = root.find('class')
        class_ = item.text
        item = root.find('widget')
        widget = item.get('class')
        self._class = class_
        self._widget = widget
        #print(class_, widget)

    def class_(self):
        return self._class

    def widget(self):
        return self._widget

    def dst_path(self):
        return os.path.join(os.path.dirname(self._path), 'Ui_{}.py'.format(self._class))

    def src_path(self):
        return self._path

    def src_rel_path(self):
        return os.path.basename(self._path)

    def dst_rel_path(self):
        return os.path.basename(self.dst_path())

    def class_path(self):
        return os.path.join(os.path.dirname(self._path), '{}.py'.format(self._class))

    def src_dirname(self):
        return os.path.dirname(self._path)

    def class_text(self):
        # TODO template in appdata
        if has_PySide2:
            package = 'PySide2'
        elif has_PyQt5:
            package = 'PyQt5'
        class_ = self._class
        widget = self._widget
        return """
from {} import QtWidgets
from Ui_{} import Ui_{}

class {}(QtWidgets.{}):
    def __init__(self, parent = None):
        super().__init__(parent)
        ui = Ui_{}()
        ui.setupUi(self)
        self._ui = ui

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = {}()
    widget.show()
    app.exec_()

""".format(package, class_, class_, class_, widget, class_, class_)

class RcData:
    def __init__(self, path):
        self._path = path
        
    def dst_path(self):
        root = os.path.dirname(self._path)
        name = os.path.splitext(os.path.basename(self._path))[0]
        return os.path.join(root, name + "_rc.py")

    def files(self):
        res = []
        tree = ET.parse(self._path)
        root = tree.getroot()
        for qresource in root:
            if qresource.tag != 'qresource':
                debug_print("qresource.tag != 'qresource'", qresource.tag)
                continue
            for file in qresource:
                if file.tag != 'file':
                    debug_print("file.tag != 'file'", file.tag)
                    continue
                path = os.path.join(os.path.dirname(self._path), os.path.normpath(file.text))
                res.append(path)
        return res
    
    def src_rel_path(self):
        return os.path.basename(self._path)

    def dst_rel_path(self):
        return os.path.basename(self.dst_path())

    def src_dirname(self):
        return os.path.dirname(self._path)

class Logger(eventloop.base.Logger):
    def __init__(self, path):
        super().__init__()
        self._path = path
        
    def print_info(self, msg):
        print(Fore.WHITE + now_str() + " " + Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.NORMAL)

    def print_error(self, msg):
        print(Fore.WHITE + now_str() + " " + Fore.RED + msg + Fore.RESET)

    def print_compiled(self, src, dst):
        print(Fore.WHITE + now_str() + " " + Fore.GREEN + Style.BRIGHT + os.path.relpath(src, self._path) + Fore.WHITE + " -> " + Fore.GREEN + os.path.relpath(dst, self._path) + Fore.RESET + Style.NORMAL)
    
    def print_writen(self, class_path):
        print(Fore.WHITE + now_str() + " " + Fore.GREEN + Style.BRIGHT + os.path.relpath(class_path, self._path) + Fore.RESET + Style.NORMAL)

def is_modified_within_n_seconds(path, n):
    if not os.path.exists(path):
        return False
    d1 = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    d2 = datetime.datetime.now()
    debug_print(d1, d2, (d2 - d1).total_seconds())
    return d1 <= d2 and (d2 - d1).total_seconds() < n

def write_text(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

class Collection:
    def __init__(self):
        self._paths = set()
    
    def append(self, rc, file):
        debug_print('rc', rc, 'file',file)
        self._paths.add((rc, file))
        
    def find(self, path):
        for (rc, path_) in self._paths:
            if path == path_:
                return rc

    def exts(self):
        exts = set()
        for (rc, file) in self._paths:
            ext = os.path.splitext(file)[1]
            if ext == '':
                continue
            exts.add(ext)
        return exts

def update_collection(rc_path, collection):
    rc = RcData(rc_path)
    for file in rc.files():
        collection.append(rc_path, file)

class Schedule(eventloop.Schedule):

    def __init__(self, executor, collection):
        super().__init__(executor)
        self._collection = collection

    def append(self, task, timeout):
        if isinstance(task, list):
            for item in task:
                self.append(item, timeout)
            return
        ext = os.path.splitext(task)[1]
        if ext not in ['.qrc','.ui']:
            rc = self._collection.find(task)
            if rc is not None:
                self.append(rc, timeout)
            else:
                debug_print(task, 'not found')
            return
        return super().append(task, timeout)

class Executor(eventloop.base.Executor):

    def __init__(self, logger, collection, no_class_files):
        super().__init__()
        self._logger = logger
        self._collection = collection
        self._no_class_files = no_class_files
        if has_PySide2:
            name = "pyside2-uic"
        elif has_PyQt5:
            name = "pyuic5"

        uic = shutil.which(name)
        if uic is None:
            raise Exception("{} not found in PATH".format(name))

        self._uic = uic

        if has_PySide2:
            name = "pyside2-rcc"
        elif has_PyQt5:
            name = "pyrcc5"
        rcc = shutil.which(name)
        if rcc is None:
            raise Exception("{} not found in PATH".format(name))

        self._rcc = rcc
        
    def execute(self, task):
        src = task

        if not os.path.exists(src):
            return True

        ext = os.path.splitext(src)[1]

        if ext == '.ui':
            data = UiData(src)
        elif ext == '.qrc':
            data = RcData(src)
            update_collection(src, self._collection)
        
        dst = data.dst_path()
        uic = self._uic
        rcc = self._rcc

        logger = self._logger
        
        if ext == '.ui':
            command = [uic, "-x", "-o", data.dst_rel_path(), data.src_rel_path()]
        elif ext == '.qrc':
            command = [rcc, "-o", data.dst_rel_path(), data.src_rel_path()]

        process = Popen(command, stdout=PIPE, stderr=PIPE, cwd=data.src_dirname())
        stdout, stderr = process.communicate()
        modified = is_modified_within_n_seconds(dst, 5)
        ok = process.returncode == 0 and modified

        debug_print("process.returncode", process.returncode)
        debug_print("modified", modified)

        if ok:
            logger.print_compiled(src, dst)
        else:
            logger.print_error("Failed to compile {}".format(src))
            codec = 'cp1251' if sys.platform == 'win32' else 'utf-8'
            print(stdout.decode(codec))
            print(stderr.decode(codec))

        if ext == '.ui':
            if not self._no_class_files:
                class_path = data.class_path()
                if not os.path.exists(class_path):
                    write_text(class_path, data.class_text())
                    logger.print_writen(class_path)

        # no point in rescheduling - must be something wrong with uic
        return True

def main():
    parser = argparse.ArgumentParser(prog="watch-ui")
    parser.add_argument('path',nargs='?',help="Path to watch, defaults to current directory")
    parser.add_argument('--no-initial-scan', action='store_true', help="Skip initial scan")
    parser.add_argument('--no-class-files', action='store_true', help="")
    args = parser.parse_args()

    #print(args); exit(0)

    colorama_init()

    watch_path = args.path if args.path is not None else os.getcwd()
    
    logger = Logger(watch_path)

    collection = Collection()

    executor = Executor(logger, collection, args.no_class_files)
    
    loop = EventLoop()

    schedule = Schedule(executor, collection)

    def on_event(path, _):
        schedule.append(path, 1)

    def initial_scan():

        _, files = walk(watch_path, ["*.qrc"], [])
        for path in files:
            update_collection(path, collection)

        _, files = walk(watch_path, ["*.ui", "*.qrc"], [])
        tasks = []
        for path in files:
            src = path
            ext = os.path.splitext(src)[1]
            if ext == ".ui":
                data = UiData(path)
                dst = data.dst_path()
                add = True
                if os.path.exists(dst):
                    m1 = os.path.getmtime(src)
                    m2 = os.path.getmtime(dst)
                    add = m2 <= m1
                if add:
                    tasks.append(src)
            elif ext == ".qrc":
                data = RcData(path)
                dst = data.dst_path()
                add = False
                if os.path.exists(dst):
                    m1 = os.path.getmtime(src)
                    m2 = os.path.getmtime(dst)
                    add = m2 <= m1
                if add:
                    tasks.append(src)

        if len(tasks) > 0:
            schedule.append(tasks, 0)

    if not args.no_initial_scan:
        logger.print_info("Initial scan")
        initial_scan()

    watch = FileSystemWatch()
    logger.print_info("Watching {}".format(watch_path))

    resource_includes = ["*" + ext for ext in collection.exts()]

    debug_print('resource_includes', resource_includes)

    watch.start(watch_path, on_event, recursive=True, include=["*.ui", "*.qrc"] + resource_includes)
    loop.start()

if __name__ == "__main__":
    main()