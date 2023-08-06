import os
import win32com.client
import shutil
from datetime import datetime
from progress_bar import *
import sys

from colorama import init
init()
from colorama import Fore, Back, Style

class FileUpdater: 
    def __init__(self, output_console=True):
        self.output_console = output_console

    def __get_num_files(self, path):
        num_files = 0
        for base, dirs, files in os.walk(path):
            num_files += len(dirs) + len(files);
        return num_files

    def __modified_date_file(self, path, file_name):
        sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(path)

        item = ns.ParseName(str(file_name))
        last_modified = ns.GetDetailsOf(item, 3) # 3 --> last modified
        return datetime.strptime(last_modified, '%d.%m.%Y %H:%M')

    def __replace_file_if_newer(self, path_source, path_dest, file_name):
        source_last_modified = self.__modified_date_file(path_source, file_name)
        dest_last_modified = self.__modified_date_file(path_dest, file_name)

        if(source_last_modified > dest_last_modified):
            full_path_source = fr"{path_source}\{file_name}"
            full_path_dest = fr"{path_dest}\{file_name}"
            os.remove(full_path_dest)
            shutil.copy2(full_path_source, full_path_dest)
            self.progressbar.print_progress(self.iteration, f'{Fore.MAGENTA}Updated {Fore.CYAN}{file_name} {Fore.MAGENTA}in{Style.RESET_ALL} {path_dest}')

    def __update_files_rec(self, path_source, path_dest):
        for file_name in os.listdir(path_source):
            full_path_source = fr"{path_source}\{file_name}"
            full_path_dest = fr"{path_dest}\{file_name}"
            if(os.path.isfile(full_path_source)):
                if(not os.path.exists(full_path_dest)):
                    shutil.copy2(full_path_source, full_path_dest)
                    self.progressbar.print_progress(self.iteration, f'{Fore.GREEN}Copied {Fore.CYAN}{file_name} {Fore.GREEN}to{Style.RESET_ALL} {path_dest}')
                else:
                    self.__replace_file_if_newer(path_source, path_dest, file_name)

            else:
                next_source_path = fr"{path_source}\{file_name}"
                next_dest_path = fr"{path_dest}\{file_name}"
                if(not os.path.exists(next_dest_path)):
                    os.mkdir(next_dest_path)
                    self.progressbar.print_progress(self.iteration, f'{Fore.GREEN}Created folder {Fore.CYAN}{file_name}{Style.RESET_ALL}')
                self.__update_files_rec(next_source_path, next_dest_path)
            self.iteration += 1
            self.progressbar.print_progress(self.iteration)

    def update_files(self, path_source, path_dest):
        self.num_files = self.__get_num_files(path_source)
        self.progressbar = Progressbar(self.num_files, 50, 'Progress', 'Complete', 2)
        self.iteration = 0

        self.__update_files_rec(path_source, path_dest)
        
    

    