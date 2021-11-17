#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2021-10-23

import os
import platform
import re
import time
import getopt
import sys
import glob
from datetime import datetime
from exif import Image

def main():

    #   *** begin argument validation ***

    #   0   include only images with valid exif date
    #   1   include only images
    #   2   include all files
    mode_include = 0

    #   true    copy into output directory
    #   false   do not copy into output directory
    mode_copy = False

    #   0   do not create new directories
    #   n>0 create a new directorys for groups of a size greater than or equal to n
    mode_group = 0

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

    #   true    rename grouped files chronologically
    #   false   do not rename grouped files chronologically
    mode_rename = False

    #   what to prefix files with
    #   default is "yyyy-mm-dd_"
    mode_include_prefix = "%Y-%m-%d_" 

    mode_exclude_prefix = ""

    #   input directory
    path_directory_input = None

    #   output directory
    path_directory_output = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:],"chrwx",["g=","help","i=","p="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in optlist:
        if(o=="-c"):
            mode_copy = True
            continue
        if(o=="--g"):
            if not a.isnumeric():
                print("--g must specify an integer")
                usage()
                sys.exit(2)
            x = int(a)
            if(x>1):
                print("--g must be greater than 0")
                usage()
                sys.exit(2)
            mode_group = x
            continue
        if(o in ["-h", "--help"]):
                usage()
                sys.exit(0)
        if(o=="--i"):
            if not a.isnumeric():
                print("--i must specify an integer")
                usage()
                sys.exit(2)
            x = int(a)
            if(x<0 or x>2):
                print("--i must be between 0 and 2")
                usage()
                sys.exit(2)
            mode_include = x
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
            continue
        if(o=="--y"):
            mode_include_prefix = a
            continue
        if(o=="--x"):
            mode_exclude_prefix = a
            continue
        print("invalid argument")
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

    #   *** end argument validation ***

    list_files_input=glob.glob(path_directory_input+"/**",recursive=mode_recursive)

    for a in list_files_input:
        print(a)






    return





    
     







    yeah = list()

    # regex for YYYY-mm-dd_
    pattern=re.compile("\d\d\d\d-\d\d-\d\d_")

    for path_filename in os.listdir(path_directory_input):
        path_absolute = os.path.join(path_directory_input, path_filename)
        date = None

        #   case where 
        #  what to do with hidden directories? what to do with inplicit directories?
        if(path_filename==".directory"):
            continue

        if(path_filename.split(".")[-1].lower() not in ["jpg","jpeg","png"]):
            if(mode_rename_non_image):
                yeah.append
            print("error:",path_absolute,"not an image",sep="\t")
            continue
        if(os.path.isfile(path_absolute)):
            if(pattern.match(path_filename)):
                date = path_filename[0:11]
            else:
                date = get_date_exif(path_absolute, mode_permutation)
            if(date==None):
                #print(path_absolute,os.path.join(path_directory_input, str_rename_no_exif+path_filename),sep="\t")
                date = get_date_os(path_absolute)
                print(date)
                yeah.append(os.path.join(path_directory_input, str_rename_no_exif+path_filename))
                continue
            #print(path_absolute, os.path.join(path_directory_input,date+path_filename))
            yeah.append(os.path.join(path_directory_input,date+path_filename))

        yeah.sort()
        #for a in yeah:
            #print(a)
        




def get_date_exif(path, mode_permutation):
    
        flag_exif=False
        flag_no_exif=False
        flag_error=False

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
                if(str_datetime_select != None):
                    return (str_datetime_select[0:4]+"-"+str_datetime_select[5:7]+"-"+str_datetime_select[8:10]+"_")
                    str_datetime_select = str_datetime_select[0:11]
                    str_datetime_select[4]="-"
                    str_datetime_select[6]="-"
                    str_datetime_select[11]="_"
                return None

#   returns a string representing the date created if available, otherwise the date modified
def get_date_os(path_to_file):
    date_c = None
    if platform.system() == 'Windows':
        date_c= os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            date_c = stat.st_birthtime
        except AttributeError:
            date_c = stat.st_mtime
    return datetime.fromtimestamp(date_c).strftime("%Y-%m-%d_")

def usage():
    print("they call me saturday")

if __name__ == "__main__":
    main()
