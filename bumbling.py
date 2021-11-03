#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2021-10-23

import os
import platform
import re
import time
from datetime import datetime
from exif import Image

def main():

    # specify 00-99
    mode_iterate=False

    # specify grouping
    mode_grouping=False

    # specify directory
    path_directory_input = ""
    path_directory_output = ""

    # specify undefined files
    mode_rename_no_exif_=False
    str_rename_no_exif=""

    # specify non-image file
    mode_rename_non_image = False
    str_rename_non_image = ""

    # specify if the program should move files or copy them to output directory
    mode_copy=False

    # specify verbose
    mode_verbose = False

    # specify help
    mode_help = False

    # specify permutation
    # 0	datetime > datetime_digitized > datetime_original
    # 1	datetime > datetime_original > datetime_digitized
    # 2	datetime_digitized > datetime > datetime_original
    # 3	datetime_digitized > datetime_original > datetime
    # 4	datetime_original > datetime > datetime_digitized
    # 5	datetime_original > datetime_digitized > datetime
    mode_permutation=0

    #   todo:   remove hardcode
    path_directory_input = "sample_input"
    path_directory_output = "sample_ouput"
    str_rename_no_exif="9999-99-99_"

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

if __name__ == "__main__":
    main()
