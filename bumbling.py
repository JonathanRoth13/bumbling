#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2021-10-23

import os
import time
import getopt
import sys
import glob
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

    # 0	datetime > datetime_digitized > datetime_original
    # 1	datetime > datetime_original > datetime_digitized
    # 2	datetime_digitized > datetime > datetime_original
    # 3	datetime_digitized > datetime_original > datetime
    # 4	datetime_original > datetime > datetime_digitized
    # 5	datetime_original > datetime_digitized > datetime
    mode_permutation = 0

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
    path_directory_input = None

    #   output directory
    path_directory_output = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:],"chrxy",["help","y=","p="])
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
        if(o=="--p"):
            if not a.isnumeric():
                print("--p must specify an integer")
                usage()
                sys.exit(2)
            x = int(a)
            if(x<0 or x>5):
                print("--p must be between 0 and 5")
                usage()
                sys.exit(2)
            mode_permutation = x
            continue
        if(o=="-r"):
            mode_recursive = True
            continue
        if(o=="-x"):
            mode_rename = True
        if(o=="-y"):
            mode_prefix = "%Y-%m-%d_" 
        if(o=="--y"):
            mode_prefix = a 



        usage()
        sys.exit(2)


    if(len(args)==0):
        path_directory_input=os.getcwd()
        path_directory_output=os.getcwd()
    elif(len(args)==1):
        path_directory_input=args[0]
        path_directory_output=os.getcwd()
    elif(len(args)==2):
        path_directory_input=args[0]
        path_directory_output=args[1]
    else:
        usage()
        sys.exit(2)

    if(os.path.isdir(path_directory_input)):
        path_directory_input=os.path.abspath(path_directory_input)
    else:
        if(os.path.isdir(os.path.abspath(path_directory_input))):
            path_directory_input = os.path.abspath(path_directory_input)
        else:
            print(path_directory_input," is not a valid path",sep="")
            usage()
            sys.exit(2)
    if(os.path.isdir(path_directory_output)):
        path_directory_output=os.path.abspath(path_directory_output)
    else:
        if(os.path.isdir(os.path.abspath(path_directory_output))):
            path_directory_output = os.path.abspath(path_directory_output)
        else:
            print(path_directory_output," is not a valid path",sep="")
            usage()
            sys.exit(2)
    #   command line arguments have been verified

    bumbling(mode_copy, mode_prefix, mode_permutation, mode_recursive, path_directory_input, path_directory_output)

def bumbling(mode_copy, mode_prefix, mode_permutation, mode_recursive, path_directory_input, path_directory_output):
 

    recursive_str = ""
    if(mode_recursive):
        recursive_str = "/**"

    #   list of files recognized
    list_files_input=[]
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

    data = None
    with exiftool.ExifTool() as et:
        data = et.get_tag_batch("EXIF:DateTimeOriginal",list_files_input)

    var = datetime.datetime.strptime("string", "%d/%m/%Y %H:%M:%S")

    for i in range(len(list_files_input)):
        dtime=datetime.strptime(data[i], "%d/%m/%Y %H:%M:%S")
        #print(i,list_files_input[i], data[i],sep="\t")
        print(i,list_files_input[i], dtime,sep="\t")
    
    return





    list_files_output = list()

    for path in list_files_input:
        datetime = get_exif_datetime(path, mode_permutation)
        if(datetime != None):
            list_files_output.append([path, datetime])


    if(len(list_files_output)==0):
        return None

    sort = sorted(list_files_output, key=lambda i:os.path.dirname(i[0]))


    yeah = os.path.dirname(sort[0][0])
    boxes = list()
    box = list()
    for a in sort:
        if(os.path.dirname(a[0])==yeah):
            box.append(a)
        else:
            yeah=os.path.dirname(a[0])
            boxes.append(box)
            box=[a]
    boxes.append(box)


    sort_boxes=list()

    for box in boxes:
        sort_boxes.append(sorted(box, key=lambda i:i[1]))


    #for box in sort_boxes:
    #    for a in box:
    #        print(a[0],a[1],sep="\n",end="\n---\n")
    #    print("---end---")


    for box in sort_boxes:
        for a in box:
            b,c = os.path.split(a[0])
            d = os.path.commonpath([path_directory_input, b])
            e = c.split(".")[-1]
            f = c[:-(len(e)+1)]
            g=a[1].strftime(mode_prefix)
            print(a[0],b,c,d,e,f,g,sep="\n",end="\n---\n")
        print("---end---")



def get_exif_datetime(path, mode_permutation):



    return None

    #   read exif data
    f = pyexiv2.metadata.ImageMetadata(path)
    f.read()

    #   find datetime data
    dtime=None
    dtime_original=None
    dtime_digitized=None
    try:
        dtime=f.__getitem__("Exif.Image.DateTime").value
    except KeyError:
        a=None
    try:
        dtime_original=f.__getitem__("Exif.Photo.DateTimeOriginal").value
    except KeyError:
        a=None
    try:
        dtime_digitized=f.__getitem__("Exif.Photo.DateTimeDigitized").value
    except KeyError:
        a=None

    return get_datetime_helper(dtime, dtime_original, dtime_digitized, mode_permutation)



def get_exif_datetime_heic(path, mode_permutation):

    print(path)
    
    #   read exif data
    f = open(path, "rb")
    tags = exifread.process_file(f, details=False)
    f.close()

    #   find datetime data
    dtime=None
    dtime_original=None
    dtime_digitized=None
    try:
        #dtime=datetime.strptime(tags["Image DateTime"].values, "%d/%m/%Y %H:%M:%S")
        dtime=tags["Image DateTime"].values
    except (KeyError, AttributeError) as e:
        a=None
    try:
        #datetime_original=datetime.strptime(tags["EXIF DateTimeDigitized"].values, "%d/%m/%Y %H:%M:%S")
        dtime_original=tags["EXIF DateTimeDigitized"].values
    except (KeyError, AttributeError) as e:
        a=None
    try:
        #dtime_digitized=datetime.strptime(tags["EXIF DateTimeOriginal"].values, "%d/%m/%Y %H:%M:%S")
        dtime_digitized=tags["EXIF DateTimeOriginal"].values
    except (KeyError, AttributeError) as e:
        a=None

    if(dtime != None):
        dtime = datetime.strptime(dtime, "%Y:%m:%d %H:%M:%S")
    if(dtime_original != None):
        dtime_original = datetime.strptime(dtime_original, "%Y:%m:%d %H:%M:%S")
    if(dtime != None):
        dtime_diditized = datetime.strptime(dtime_digitized, "%Y:%m:%d %H:%M:%S")

    return get_datetime_helper(dtime, dtime_original, dtime_digitized, mode_permutation)


def get_datetime_helper(dtime, dtime_original, dtime_digitized, mode_permutation):
    if(mode_permutation==0):
        if(dtime != None):
            return dtime
        if(dtime_digitized != None):
            return dtime_digitized
        if(dtime_original != None):
            return dtime_original
    # 1	datetime > datetime_original > datetime_digitized
    if(mode_permutation==1):
        if(dtime != None):
            return dtime
        if(dtime_original != None):
            return dtime_original
        if(dtime_digitized != None):
            return dtime_digitized
    # 2	datetime_digitized > datetime >datetime_original
    if(mode_permutation==2):
        if(dtime_digitized != None):
            return dtime_digitized
        if(dtime != None):
            return dtime
        if(dtime_original != None):
            return dtime_original
    # 3	datetime_digitized > datetime_original > datetime
    if(mode_permutation==3):
        if(dtime_digitized != None):
            return dtime_digitized
        if(dtime_original != None):
            return dtime_original
        if(dtime != None):
            return dtime
    # 4	datetime_original > datetime > datetime_digitized
    if(mode_permutation==4):
        if(dtime_original != None):
            return dtime_original
        if(dtime != None):
            return dtime
        if(dtime_digitized != None):
            return dtime_digitized
    # 5	datetime_original > datetime_digitized > datetime
    if(mode_permutation==5):
        if(dtime_original != None):
            return dtime_original
        if(dtime_digitized != None):
            return dtime_digitized
        if(dtime != None):
            return dtime
    return None
           

def usage():
    print("they call me saturday")

if __name__ == "__main__":
    main()
