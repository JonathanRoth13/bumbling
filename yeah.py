import os
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS







# assign directory
directory_input = 'life/'
directory_output = 'life_output/'

TTags = ['DateTimeOriginal', 'DateTimeDigitized', 'DateTime']  # when img file was changed
pattern=re.compile("\d\d\d\d-\d\d-\d\d_")

for filename in os.listdir(directory_input):
    filename_full = os.path.join(directory_input, filename)
    if os.path.isfile(filename_full):
        if(pattern.match(filename)):
            print(filename)
            continue
        

        i=Image.open(filename_full)._getexif()
        if(i==None):
            print(filename_full+":\t"+"no data")
            continue
        print(filename_full+":\t"+"data")
        continue







        date=None

        for tag in TTags:
            date = exif.get(tag[0])
            if type(date)== tuple:
                date=date[0]

            if date != None: break
            
        if(date == None):
            print("error:\t" + filename_full + "does not contain a date")
            quit()

        date=date[0:4]+"-"+date[5:7]+"-"+date[8:10]+"_"
        print(filename_full +"\t"+ date)

        #filename_output=os.path.join(directory_output, )



            
            


