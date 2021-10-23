#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2021-10-23

import os
import re
from datetime import datetime
from exif import Image



# specify date
mode_date=False

# specify 00-99
mode_iterate=False

# specify grouping
mode_grouping=False

# specify directory
path_output_directory=""

# spefify recursive
mode_recursive=False

# specify undefined files
mode_rename_incompatable_files=False

# specify verbose
mode_verbose = False

# specify help
mode_help = False

# specify permutation
# 0	datetime > datetime_digitized > datetime_original
# 1	datetime > datetime_original > datetime_digitized
# 2	datetime_digitized > datetime >datetime_original
# 3	datetime_digitized > datetime_original > datetime
# 4	datetime_original > datetime > datetime_digitized
# 5	datetime_original > datetime_digitized > datetime
mode_permutation=0

path_directory_input = 'life/'
path_directory_output = 'life_output/'

argument_permutation=0

pattern=re.compile("\d\d\d\d-\d\d-\d\d_")
#tags=["datetime_original", "datetime_digitized", "datetime"]

for path_filename in os.listdir(path_directory_input):
    path_absolute = os.path.join(path_directory_input, path_filename)

    flag_formatted_correctly=False
    flag_exif=False
    flag_no_exif=False
    flag_error=False

    #  what to do with hidden directories? what to do with inplicit directories?
    if(path_filename==".directory"):
        continue
    
    # debug
    print(path_filename,end="")
    print()

    if(os.path.isfile(path_absolute)):
        if(pattern.match(path_filename)):
            # debug
            flag_formatted_correctly=True

        with open(path_absolute,"rb") as image_file:
            try:
                image = Image(image_file)
                if(image.has_exif):
                    flag_exif=True
                else:
                    flag_no_exif=True

            # catch exceptions resulting from "%d is not a valid TiffByteOrder"
            except:
                flag_error=True

            if(flag_formatted_correctly):
               print("file has a prefix that is already correctly formatted")
               continue
            if(flag_error):
                print("file is either not an image or and image that does not contain exif data")
                continue
            if(flag_no_exif):
                print("file is an image than does not contain exif data")
            if(flag_exif):

                flag_datetime_original=False
                flag_datetime_digitized=False
                flag_datetime=False

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
                        if(str_datetime != None):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_digitized != None):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime_original != None):
                            str_datetime_select=str_datetime_original
                        break
                    # 1	datetime > datetime_original > datetime_digitized
                    if(mode_permutation==1):
                        if(str_datetime != None):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_original != None):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime_digitized != None):
                            str_datetime_select=str_datetime_digitized
                        break
                    # 2	datetime_digitized > datetime >datetime_original
                    if(mode_permutation==2):
                        if(str_datetime_digitized != None):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime != None):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_original != None):
                            str_datetime_select=str_datetime_original
                        break
                    # 3	datetime_digitized > datetime_original > datetime
                    if(mode_permutation==3):
                        if(str_datetime_digitized != None):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime_original != None):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime != None):
                            str_datetime_select=str_datetime
                        break
                    # 4	datetime_original > datetime > datetime_digitized
                    if(mode_permutation==4):
                        if(str_datetime_original != None):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime != None):
                            str_datetime_select=str_datetime
                            break
                        if(str_datetime_digitized != None):
                            str_datetime_select=str_datetime_digitized
                        break
                    # 5	datetime_original > datetime_digitized > datetime
                    if(mode_permutation==5):
                        if(str_datetime_original != None):
                            str_datetime_select=str_datetime_original
                            break
                        if(str_datetime_digitized != None):
                            str_datetime_select=str_datetime_digitized
                            break
                        if(str_datetime != None):
                            str_datetime_select=str_datetime
                        break   
                if(str_datetime_select==None):
                    print("file is an image that contains exif data that does not specify a date")
                    continue
                print(str_datetime_select)
            print()

