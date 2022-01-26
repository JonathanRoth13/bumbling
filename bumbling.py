#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2021-10-23

import os
import time
import getopt
import sys
import glob
import math
from datetime import datetime
import exiftool

def main():

    #   *** begin argument validation ***

    #   true    copy into output directory
    #   false   do not copy into output directory
    mode_copy = False

    #   true    display help message
    #   false   do not display help message
    mode_help = False

    #   true    recurse through directories and do this for all files
    #   false   do not recurse
    mode_recursive = False

    #   true    rename
    #   false   do not rename
    mode_rename = False

    #   what to prefix files with
    #   default is "yyyy-mm-dd_"
    mode_prefix = "%Y-%m-%d_" 

    #   input directory
    list_path_directory_input = list()

    #   output directory
    path_directory_output = None

    #   verify command line arguments
    try:
        optlist, args = getopt.getopt(sys.argv[1:],"chrx",["help","y="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in optlist:
        if(o=="-c"):
            mode_copy = True
            continue
        if(o in ["-h", "--help"]):
                usage()
                sys.exit(0)
                continue
        if(o=="-r"):
            mode_recursive = True
            continue
        if(o=="-x"):
            mode_rename = True
            continue
        if(o=="--y"):
            mode_prefix = a 
            continue
        usage()
        sys.exit(2)

    if(len(args)<2):
        usage()
        sys.exit(2)
    list_path_directory_input = args[:-1]
    path_directory_output = args[-1]

    #   verify paths
    for i in range(len(list_path_directory_input)):
        path=list_path_directory_input[i]
        if(os.path.isdir(path)):
            list_path_directory_input[i]=os.path.abspath(path)
        else:
            if(os.path.isdir(os.path.abspath(path))):
                list_path_directory_input[i] = os.path.abspath(path)
            else:
                print("\"",list_path_directory_input[i],"\" is not a valid path",sep="")
                usage()
                sys.exit(2)

    if(os.path.isdir(path_directory_output)):
        path_directory_output=os.path.abspath(path_directory_output)
    else:
        if(os.path.isdir(os.path.abspath(path_directory_output))):
            path_directory_output = os.path.abspath(path_directory_output)
        else:
            print("\"",path_directory_output,"\" is not a valid path",sep="")
            usage()
            sys.exit(2)

    #   all command line arguments have been verified
    bumbling(mode_copy, mode_prefix, mode_recursive, mode_rename, list_path_directory_input, path_directory_output)

def bumbling(mode_copy, mode_prefix, mode_recursive, mode_rename, list_path_directory_input, path_directory_output):
 
    recursive_str = ""
    if(mode_recursive):
        recursive_str = "/**"

    #   list of files recognized
    list_files_input=[]
    for i in range(len(list_path_directory_input)):
        path_directory_input=list_path_directory_input[i]
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.png",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.PNG",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.jpg",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.JPG",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.jpeg",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.JPEG",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.exv",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.EXV",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.cr2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.CR2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.crw",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.CRW",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.mwr",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.MWR",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.tiff",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.TIFF",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.webp",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.WEBP",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.dng",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.DNG",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.nef",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.NEF",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.pef",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.PEF",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.arw",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.ARW",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.rw2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.RW2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.sr2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.SR2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.srw",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.SRW",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.orf",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.ORF",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.pgf",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.PGF",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.raf",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.RAF",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.psd",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.PSD",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.jp2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.JP2",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.heic",recursive=mode_recursive))
        list_files_input.extend(glob.glob(path_directory_input+recursive_str+"/*.HEIC",recursive=mode_recursive))

    if(len(list_files_input)==0):
        return

    #   remove duplicates and sort
    list_files_input=list(set(list_files_input))
    list_files_input.sort()



    #for a in range(50):
    #    str_output='{str_0:0>{str_1}}'.format(str_0=str(a),str_1=str(pad))
    #    print(str_output)
    #return

    #   read exif data from input files
    data = None
    with exiftool.ExifTool() as et:
        data = et.get_tag_batch("EXIF:DateTimeOriginal",list_files_input)

    #   sort by date, ignore files without exif data
    sort=list()
    for i in range(len(list_files_input)):
            if(data[i] != None):
                #sort.append((list_files_input[i], datetime.strptime(data[i], "%Y:%m:%d %H:%M:%S")))
                sort.append((datetime.strptime(data[i], "%Y:%m:%d %H:%M:%S"),list_files_input[i]))
    sort.sort()



    #   calculate new filenames
    trans=list()
    if(mode_rename):

        #   calculate padding
        pad=math.ceil(math.log(len(sort),10))
        if(pad % 2 != 0):
            pad=pad+1
        index=0

        for i in range(len(sort)):
            trans.append(sort[i][0].strftime(mode_prefix)+'{str_0:0>{str_1}}'.format(str_0=str(index),str_1=str(pad))+os.path.splitext(sort[i][1])[1])
            index=index+1
        
    else:
        index=0
        last=None
        for i in range(len(sort)):
            name = os.path.basename(sort[i])

            index=0
            if(data[i] != None):
                dtime=datetime.strptime(data[i], "%Y:%m:%d %H:%M:%S")

    for i in range(len(trans)):
        print(trans[i])



    return






    for i in range(len(list_files_input)):
        index=0
        if(data[i] != None):
            dtime=datetime.strptime(data[i], "%Y:%m:%d %H:%M:%S")





def usage():
    print("usage they call me saturday")

if __name__ == "__main__":
    main()
