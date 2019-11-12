import argparse
import shutil
from pathlib import Path, PurePath
import os

'''
Copies this_file to destination directory.  Uses the destination root specified as the second 
parameter on command line.  Rest of the path is same as the relative path from source root, 
which is specified as the first parameter on the command line.
'''
def copy_file(this_file):
    # this_file is the absolute path to the file to be copied
    # Build destination path for this_file
    dest_file_location = PurePath.joinpath(dst_dir, PurePath(this_file).relative_to(src_dir))
    # If the file does not exist at the destination, copy the file to the destination
    if dest_file_location.exists():
        # Check if file at source was modified  more recently than the same file at destination
        if Path(this_file).stat().st_mtime > dest_file_location.stat().st_mtime:
            # copy from source to destination
            print ('Copying more recent ', this_file, ' to ', dest_file_location)
    else:
        # File does not exist at destination, so copy it form source
        try:
            shutil.copyfile(this_file, dest_file_location)
        except OSError:
            print ('Destination not writeable.  Cannot backup file.')
            exit(1)
        except shutil.SameFileError:
            print ('Source and destination cannot be the same.')
            exit(1)
        print('Copied ', this_file, ' to ', dest_file_location)


def check_create_directory(this_dir):
    # this_file is the absolute path to the directory to be copied
    # Build destination path for this_dir
    dest_directory_location = PurePath.joinpath(dst_dir, PurePath(this_dir).relative_to(src_dir))
    if not dest_directory_location.exists():
        try:
            os.mkdir(dest_directory_location)
        except FileExistsError:
            print ('Directory ', dest_directory_location, ' already exists.')
            exit(1)


def backup_directory(this_dir):
    for x in this_dir.iterdir():
        if x.is_dir():
            # if directory does not exist at destination, create this directory at destination
            check_create_directory(x)
            # back up directory x
            backup_directory(x)
        else:
            # x is a file
            copy_file(x)
            # dest_file_location = PurePath.joinpath(dst_dir, PurePath(x).relative_to(src_dir))
            # print ('File ', dest_file_location, ' last modified ', Path(x).stat().st_mtime)


parser = argparse.ArgumentParser()
parser.add_argument("source_directory",
                    help="The absolute path to the directory to be backed up.",
                    type=str)
parser.add_argument("destination_directory",
                    help="The absolute path to the directory to which the source directory should be backed up.",
                    type=str)
args = parser.parse_args()
print (args.source_directory)
print (args.destination_directory)

src_dir = Path(args.source_directory)
dst_dir = Path(args.destination_directory)

# Make sure source directory exists
if not src_dir.is_dir():
    print ("Source directory does not exist.")
    exit(1)
# Make sure destination directory exists
if not dst_dir.is_dir():
    print ("Destination directory does not exist.")
    exit(1)
# Make sure source and destination are not the same
if src_dir.samefile(dst_dir):
    print ('Source and destination directories can not be the same.')
    exit(1)

backup_directory(src_dir)