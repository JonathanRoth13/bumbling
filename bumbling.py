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
import exifread
import pyexiv2

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

    #   what to prefix files with
    #   default is "yyyy-mm-dd_"
    mode_include_prefix = "%Y-%m-%d_" 

    #   input directory
    path_directory_input = None

    #   output directory
    path_directory_output = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:],"chr",["help","i=","p="])
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

    bumbling(mode_copy, mode_include_prefix, mode_permutation, mode_recursive, path_directory_input, path_directory_output)

def bumbling(mode_copy, mode_include_prefix, mode_permutation, mode_recursive, path_directory_input, path_directory_output):

    #   list of files recognized
    list_files_input=[]
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.png",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.PNG",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.jpg",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.JPG",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.jpeg",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.JPEG",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.exv",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.EXV",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.cr2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.CR2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.crw",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.CRW",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.mwr",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.MWR",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.tiff",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.TIFF",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.webp",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.WEBP",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.dng",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.DNG",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.nef",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.NEF",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.pef",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.PEF",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.arw",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.ARW",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.rw2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.RW2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.sr2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.SR2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.srw",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.SRW",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.orf",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.ORF",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.pgf",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.PGF",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.raf",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.RAF",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.psd",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.PSD",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.jp2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.JP2",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.heic",recursive=mode_recursive))
    list_files_input.extend(glob.glob(path_directory_input+"/**/*.HEIC",recursive=mode_recursive))

    list_files_ouput = list()

    for path in list_files_input:
        datetime = None
        if(path.endswith(".heic") or path.endswith(".HEIC")):
            continue
            datetime = get_exif_datetime_heic(path, mode_permutation)
        else:
            datetime = get_exif_datetime(path, mode_permutation)
    return None

def get_exif_datetime(path, mode_permutation):
    f = pyexiv2.Image(path)
    tags = f.read_exif()
    f.close()
    print(tags)
    return None

def get_exif_datetime_heic(path, mode_permutation):
    
    #   read exif data
    f = open(path, "rb")
    tags = exifread.process_file(f, details=False)
    f.close()

    #   find datetime data
    str_datetime_original=None
    str_datetime_digitized=None
    str_datetime=None
    str_select=None
    try:
        str_datetime_original=tags["EXIF DateTimeDigitized"]
    except KeyError:
        a=None
    try:
        str_datetime_digitized=tags["EXIF DateTimeOriginal"]
    except KeyError:
        a=None
    try:
        str_datetime=tags["Image DateTime"]
    except KeyError:
        a=None
    return None





'''
def get_date_exif(path, mode_permutation):
    
        flag_exif=False
        flag_no_exif=False
        flag_error=False

        if not sys.warnoptions:
            warnings.simplefilter("ignore","ASCII tag contains 1 fewer bytes than specified")

        with open(path,"rb") as image_file:
            try:
                image = Image(image_file)
                if(image.has_exif):
                    flag_exif=True
                else:
                    flag_no_exif=True

            # catch exceptions resulting from "%d is not a valid TiffByteOrder"
            except:
                flag_error=True
            if(flag_error):
                #   debug
                #print("file is either not an image or and image that does not contain exif data")
                return None
            if(flag_no_exif):
                #   debug
                #print("file is an image than does not contain exif data")
                return None
            if(flag_exif):
                str_datetime_original=None
                str_datetime_digitized=None
                str_datetime=None
                # catch exceptions resulting from "image does not have attribute %s                
                try:
                    str_datetime_orginal=image.datetime_original
                except:
                    #nothing operation
                    a=None
                try:
                    str_datetime_digitized=image.datetime_digitized
                except:
                    #nothing operation
                    a=None
                try:
                    str_datetime=image.datetime
                except:
                    #nothing operation
                    a=None

                str_datetime_select = None
                while(True):
                    # 0	datetime > datetime_digitized > datetime_original
                    if(mode_permutation==0):
                        if(str_datetime != None and str_datetime != "" and str_datetime != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_digitized != None and str_datetime_digitized != "" and str_datetime_digitized != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime_original != None and str_datetime_original != "" and str_datetime_original != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_original
                        break
                    # 1	datetime > datetime_original > datetime_digitized
                    if(mode_permutation==1):
                        if(str_datetime != None and str_datetime != "" and str_datetime != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_original != None and str_datetime_original != "" and str_datetime_original != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime_digitized != None and str_datetime_digitized != "" and str_datetime_digitized != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_digitized
                        break
                    # 2	datetime_digitized > datetime >datetime_original
                    if(mode_permutation==2):
                        if(str_datetime_digitized != None and str_datetime_digitized != "" and str_datetime_digitized != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime != None and str_datetime != "" and str_datetime != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_original != None and str_datetime_original != "" and str_datetime_original != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_original
                        break
                    # 3	datetime_digitized > datetime_original > datetime
                    if(mode_permutation==3):
                        if(str_datetime_digitized != None and str_datetime_digitized != "" and str_datetime_digitized != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime_original != None and str_datetime_original != "" and str_datetime_original != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime != None and str_datetime != "" and str_datetime != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime
                        break
                    # 4	datetime_original > datetime > datetime_digitized
                    if(mode_permutation==4):
                        if(str_datetime_original != None and str_datetime_original != "" and str_datetime_original != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime != None and str_datetime != "" and str_datetime != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_digitized != None and str_datetime_digitized != "" and str_datetime_digitized != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_digitized
                        break
                    # 5	datetime_original > datetime_digitized > datetime
                    if(mode_permutation==5):
                        if(str_datetime_original != None and str_datetime_original != "" and str_datetime_original != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime_digitized != None and str_datetime_digitized != "" and str_datetime_digitized != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime != None and str_datetime != "" and str_datetime != "0000:00:00 00:00:00"):
                            str_datetime_select=str_datetime
                        break   
                if(str_datetime_select == None):
                    return None
                
                try:
                    a = time.strptime(str_datetime_select,"%Y:%m:%d %H:%M:%S")
                except ValueError:
                    return None
                return a
'''

def usage():
    print("they call me saturday")

if __name__ == "__main__":
    main()
