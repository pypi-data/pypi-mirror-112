from updater import FileUpdater
import sys

if(len(sys.argv) != 3):
    print(f'Please use the following format:')
    print(f'fup.py [Source path] [Destination path]')
    print(fr'e.g. fup.py C:\Users\max\programming H:\code\snippets')
else:
    file_updater = FileUpdater(output_console=True)

    file_updater.update_files(
        path_source=sys.argv[1], 
        path_dest=sys.argv[2])