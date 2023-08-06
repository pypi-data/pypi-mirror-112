import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import ntpath
import glob2 as glob
from collections import OrderedDict
import datetime
import numpy as np
from scipy.spatial import distance

def about(header=False):
    """
    Provides a header and front-end interface for new users and pipeline workflows.
    
    Parameters
    ----------
    header : boolean, default: False
        Determines whether to display a header or a front-end interface. By default, this is set
        to ``False``, meaning that it automatically generates a front-end interface if passed.
        
    Notes
    -----
    This is the most frontend aspect about **mednoise**. Beyond this, **mednoise** is 
    a series of scripts to be included in a terminal or pipeline workflow.
    

    Examples
    --------
    >>> md.about()
        #############################################################################################
                                             8I                                                     
                                             8I                                                     
                                             8I                              gg                     
                                             8I                              ""                     
          ,ggg,,ggg,,ggg,    ,ggg,     ,gggg,8I   ,ggg,,ggg,     ,ggggg,     gg     ,g,      ,ggg,  
         ,8" "8P" "8P" "8,  i8" "8i   dP"  "Y8I  ,8" "8P" "8,   dP"  "Y8ggg  88    ,8'8,    i8" "8i 
         I8   8I   8I   8I  I8, ,8I  i8'    ,8I  I8   8I   8I  i8'    ,8I    88   ,8'  Yb   I8, ,8I 
        ,dP   8I   8I   Yb, `YbadP' ,d8,   ,d8b,,dP   8I   Yb,,d8,   ,d8'  _,88,_,8'_   8)  `YbadP' 
        8P'   8I   8I   `Y8888P"Y888P"Y8888P"`Y88P'   8I   `Y8P"Y8888P"    8P""Y8P' "YY8P8P888P"Y888
        #############################################################################################
    
    >>> md.about(header=True)
        #############################################################################################
                                             8I                                                     
                                             8I                                                     
                                             8I                              gg                     
                                             8I                              ""                     
          ,ggg,,ggg,,ggg,    ,ggg,     ,gggg,8I   ,ggg,,ggg,     ,ggggg,     gg     ,g,      ,ggg,  
         ,8" "8P" "8P" "8,  i8" "8i   dP"  "Y8I  ,8" "8P" "8,   dP"  "Y8ggg  88    ,8'8,    i8" "8i 
         I8   8I   8I   8I  I8, ,8I  i8'    ,8I  I8   8I   8I  i8'    ,8I    88   ,8'  Yb   I8, ,8I 
        ,dP   8I   8I   Yb, `YbadP' ,d8,   ,d8b,,dP   8I   Yb,,d8,   ,d8'  _,88,_,8'_   8)  `YbadP' 
        8P'   8I   8I   `Y8888P"Y888P"Y8888P"`Y88P'   8I   `Y8P"Y8888P"    8P""Y8P' "YY8P8P888P"Y888
        #############################################################################################
        Copyright 2021 Ravi Bandaru
        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this package except in compliance with the License.
        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
        #############################################################################################
        Welcome to mednoise, a python package that contains algorithms to handle and pre-process 
        large amounts of image-based metadata to remove noise and enhance the accuracy of machine
        learning and deep learning models for scientific research.
        #############################################################################################
        You can bring up the help menu (h) or exit (e).
    """
    if header==True:
        logo = """
        #############################################################################################
                                             8I                                                     
                                             8I                                                     
                                             8I                              gg                     
                                             8I                              ""                     
          ,ggg,,ggg,,ggg,    ,ggg,     ,gggg,8I   ,ggg,,ggg,     ,ggggg,     gg     ,g,      ,ggg,  
         ,8" "8P" "8P" "8,  i8" "8i   dP"  "Y8I  ,8" "8P" "8,   dP"  "Y8ggg  88    ,8'8,    i8" "8i 
         I8   8I   8I   8I  I8, ,8I  i8'    ,8I  I8   8I   8I  i8'    ,8I    88   ,8'  Yb   I8, ,8I 
        ,dP   8I   8I   Yb, `YbadP' ,d8,   ,d8b,,dP   8I   Yb,,d8,   ,d8'  _,88,_,8'_   8)  `YbadP' 
        8P'   8I   8I   `Y8888P"Y888P"Y8888P"`Y88P'   8I   `Y8P"Y8888P"    8P""Y8P' "YY8P8P888P"Y888
        #############################################################################################
        """
        print(logo)
        global storeddictionary
        global analyzedval
        storeddictionary = 1
        analyzedval = 1

    if header==False:
        logo = """
        #############################################################################################
                                             8I                                                     
                                             8I                                                     
                                             8I                              gg                     
                                             8I                              ""                     
          ,ggg,,ggg,,ggg,    ,ggg,     ,gggg,8I   ,ggg,,ggg,     ,ggggg,     gg     ,g,      ,ggg,  
         ,8" "8P" "8P" "8,  i8" "8i   dP"  "Y8I  ,8" "8P" "8,   dP"  "Y8ggg  88    ,8'8,    i8" "8i 
         I8   8I   8I   8I  I8, ,8I  i8'    ,8I  I8   8I   8I  i8'    ,8I    88   ,8'  Yb   I8, ,8I 
        ,dP   8I   8I   Yb, `YbadP' ,d8,   ,d8b,,dP   8I   Yb,,d8,   ,d8'  _,88,_,8'_   8)  `YbadP' 
        8P'   8I   8I   `Y8888P"Y888P"Y8888P"`Y88P'   8I   `Y8P"Y8888P"    8P""Y8P' "YY8P8P888P"Y888
        #############################################################################################
        Copyright 2021 Ravi Bandaru
        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this package except in compliance with the License.
        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
        #############################################################################################
        Welcome to mednoise, a python package that contains algorithms to handle and pre-process 
        large amounts of image-based metadata to remove noise and enhance the accuracy of machine
        learning and deep learning models for scientific research.
        #############################################################################################
        You can bring up the help menu (h) or exit (e).
        """
        print(logo)
        response = input("    ")
        print("    #############################################################################################")
        print("")
        if response == "e":
            print("    exiting.")
        if response == "h":
            print("    documentation can be accessed at https://mednoise.github.io/documentation.")
        print("")
        print("    #############################################################################################")
    if header != True and header != False:
        raise ValueError('header argument was incorrectly specified. note that it is a boolean attribute.')

about(True)


def manual_merge(filepath, find = (0,0,0), replace = (255,255,255)):
    """
    Combines multiple input images of the same size to yield one binary image that allows for 
    common feature detection.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    replace : RGB tuple, default: (255,255,255)
        A value that indicates complete noise. Usually is considered the 
        complement of the background color of the input image, often ``(255,255,255)``.
        
    Notes
    -----
    This allows users to find common features and then pass them through their own package scripts,
    or predeveloped scripts like ``md.manual_find`` and ``md.manual_edit``.
    

    Examples
    --------
    >>> md.manual_merge("/example/directory/*, (0,0,0), (255, 0, 0)) #for 4 images, yielding the below image
    md.manual_merge - Image 1 Importing:0:00:01
    md.manual_merge - Image 2 Importing:0:00:01md.manual_merge - Image 1 Pixel Cleaning:0:00:00
    md.manual_merge - Image 2 Pixel Cleaning:0:00:00
    md.manual_merge - Image 1 and 2 Pixel Merge:0:00:50
    md.manual_merge - Image 3  Pixel Merge:0:00:59
    md.manual_merge - Image 4  Pixel Merge:0:00:51
    md.manual_merge - Final Merge and Conversion:0:00:50
    md.manual_merge - Image Save:0:00:01
    
    .. figure:: combined_image.png
       :scale: 50 %
       :align: center
       
       ``md.manual_merge`` output image
    """
    files = glob.glob(filepath)
    original = []
    
    
    startTime = datetime.datetime.now().replace(microsecond=0)
    image = Image.open(files[0])
    rgb1 = image.convert('RGB')
    width, height = image.size
    pixel_values1 = list(rgb1.getdata())
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print ("md.manual_merge - Image 1 Importing:" + str(durationTime))

    
    startTime = datetime.datetime.now().replace(microsecond=0)
    image2 = Image.open(files[1])
    rgb2 = image2.convert('RGB')
    pixel_values2 = list(rgb2.getdata())
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print ("md.manual_merge - Image 2 Importing:" + str(durationTime))

    
    startTime = datetime.datetime.now().replace(microsecond=0)
    for index, item in enumerate(pixel_values1):
        if item != find:
            pixel_values1[index] = 2
        else:
            pixel_values1[index] = 1
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print ("md.manual_merge - Image 1 Pixel Cleaning:" + str(durationTime))
    
    
    startTime = datetime.datetime.now().replace(microsecond=0)
    for index, item in enumerate(pixel_values2):
        if item != find:
            pixel_values2[index] = 2
        else:
            pixel_values2[index] = 1
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print ("md.manual_merge - Image 2 Pixel Cleaning:" + str(durationTime))

    
    startTime = datetime.datetime.now().replace(microsecond=0)
    for index, item in enumerate(pixel_values1) and enumerate(pixel_values2):
        print(round((100*index)/(width*height),1), end = "\r")
        if pixel_values1[index] == 1 and pixel_values2[index]== 1:
            original.append(1)
        else:
            original.append(2)
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print ("md.manual_merge - Image 1 and 2 Pixel Merge:" + str(durationTime))

    
    i=1
    for index,item in enumerate(files):
        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[index])
        rgb1 = image.convert('RGB')
        pixel_values1 = list(rgb1.getdata())
        width, height = rgb1.size
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            else: 
                pixel_values1[index] = 1
        for index, item in enumerate(pixel_values1) and enumerate(original):
            print(round((100*index)/(width*height),1), end = "\r")
            if pixel_values1[index] == 1 and original[index]== 1:
                original[index] = 1
            else:
                original[index] = 2
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime
        print ("md.manual_merge - Image", i, " Pixel Merge:" + str(durationTime))
        i+=1

        
    startTime = datetime.datetime.now().replace(microsecond=0)
    for index, item in enumerate(original):
            print(round((100*index)/(width*height),1), end = "\r")
            if original[index]== 1:
                original[index] = find
            else:
                original[index] = replace
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print("md.manual_merge - Final Merge and Conversion:" + str(durationTime))

    
    startTime = datetime.datetime.now().replace(microsecond=0)
    image_out = Image.new("RGB",(width,height))
    image_out.putdata(original)
    image_out.save('combined_image.png')
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print("md.manual_merge - Image Save:" + str(durationTime))


def manual_find(filepath):
    """
    Offers an interface through tkinter to identify pixel coordinates and create tuple-lists that can be passed through a filter.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Must be a path to a file, not a directory or other ``glob`` parseable structure.
        
    Notes
    -----
    This allows users to find polygon coordinates and then pass them through their own package scripts,
    or predeveloped scripts like ``md.manual_edit``.
    

    Examples
    --------
    >>> md.manual_find("/example/directory/file.png") #after four clicks on the tkinter interface
    (51,78),
    (51,275),
    (7,261),
    (8,78),
    """
    window = tk.Tk()
    window.title("Pixel Finder")
    window.geometry("960x720")
    window.configure(background='grey')
    img = ImageTk.PhotoImage(Image.open(filepath))
    panel = tk.Label(window, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    def pressed1(event):
        print("(" + str(event.x) + "," + str(event.y) + ")" + ",")
    window.bind('<Button-1>', pressed1)
    window.mainloop()


def manual_edit(filepath, xy, find = (0,0,0)):
    """
    Offers a manual method through which sections of input images can be silenced.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Must be a path to a file, not a directory or other ``glob`` parseable structure.
        
    xy : tuple
        A tuple of restraint tuples for the polygon to be silenced. This can be either generated 
        by setting the output of ``md.manual_find`` to a list or developing your own algorithm.
    
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
        
    Notes
    -----
    This allows users to silence polygon coordinates after then pass them through their own package scripts,
    or predeveloped scripts like ``md.manual_merge`` or ``md.manual_find``.
    

    Examples
    --------
    >>> restraints = [(473,91),(214,601),(764,626)]
    >>> md.manual_edit("/example/directory/file.png", xy = restraints) #removing a triangle from input image
    md.manual_edit - Image 1 Save:0:00:01
    
    .. figure:: edited.png
       :scale: 50 %
       :align: center
       
       ``md.manual_edit`` output image
    """
    files = glob.glob(filepath)
    restraints = xy
    for index,item in enumerate(files):
        with Image.open(files[index]) as im:
            startTime = datetime.datetime.now().replace(microsecond=0)
            name = ntpath.basename(files[index])
            size = len(name)
            mod_string = name[:size - 4]
            print(mod_string)
            draw = ImageDraw.Draw(im)
            draw.polygon(restraints, fill=find, outline=find)
            im.save(mod_string + "_clean" + ".PNG")
            endTime = datetime.datetime.now().replace(microsecond=0)
            durationTime = endTime - startTime
            print("md.manual_edit - Image " + str(index+1) + " Save:" + str(durationTime))
            
            
def manual_primer(filepath, find = (0,0,0)):
    """
    Creates one binary image from an imput image that allows for common feature detection.
    
    Parameters
    ----------
    filepath : string
         A filepath for images to be selected from. Must be a path to a file, not a directory or other ``glob`` parseable structure.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
        
    Notes
    -----
    This function is almost entirely useless without an outside algorithm that a user develops. **mednoise**
    is already optimized to not require primed images, so this function instead serves as a tool for user
    developed algorithms that have not been optimized.
    

    Examples
    --------
    >>> md.manual_primer("/example/directory/*") 
    md.manual_primer - Importing Images:0:00:00
    md.manual_primer - Image 1 Importing:0:00:01
    md.manual_primer - Image 1 Cleaning:0:00:00
    md.manual_primer - Image 1 Conversion:0:00:47
    md.manual_primer - Image 1 Image Save:0:00:01
    
    .. figure:: primed.png
       :scale: 50 %
       :align: center
       
       ``md.manual_primer`` output image
    """
    
    replace = (255,255,255)
    
    
    startTime = datetime.datetime.now().replace(microsecond=0)
    files = glob.glob(filepath)
    original = []
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime
    print ("md.manual_primer - Importing Images:" + str(durationTime))
    
    
    startTime = datetime.datetime.now().replace(microsecond=0)
    for indexor,item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        pixel_values1 = list(rgb1.getdata())
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime
        print ("md.manual_primer - Image" + " " + str(indexor+1) + " Importing:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            else:
                pixel_values1[index] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime
        startTime = datetime.datetime.now().replace(microsecond=0)
        print ("md.manual_primer - Image" + " " + str(indexor+1) +" Cleaning:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        const = (width*height)/100
        for index, item in enumerate(pixel_values1):
                print(str(round((index)/(const),1)) + "%" , end = "\r")
                if pixel_values1[index] == 1:
                    original.append(find)
                else:
                    original.append(replace)
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime
        print ("md.manual_primer - Image" + " " + str(indexor+1) +" Conversion:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        image_out = Image.new("RGB",(width,height))
        image_out.putdata(original)
        image_out.save(mod_string + "_primed" + ".PNG")
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime
        print ("md.manual_primer - Image" + " " + str(indexor+1) + " Image Save:" + str(durationTime))


def hotspot_complete(filepath, x, y, find=(0,0,0)):
    """
    Processes inputted images using a hotspot algorithm, 
    essentially acting as an intuitive paintbrush across the image. 
    Allows a user to selectively filter instances of noise based off of size.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    x : integer, default: (0,0,0)
        The width, in pixels, of the hotspot matrix calculator. Think of this as the width of the intuitive paintbrush.
    y : integer, default: (0,0,0)
        The height, in pixels, of the hotspot matrix calculator. Think of this as the height of the intuitive paintbrush.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works.
    

    Examples
    --------
    >>> md.hotspot_complete("/example/directory/file.png", 50, 50)
    md.hotspot_complete - Image 1 Importing:0:00:01
    md.hotspot_complete - Image 1 Converting:0:00:00
    md.hotspot_complete - Image 1 Hotspot Calculating:0:00:53
    md.hotspot_complete - Image 1 Hotspot Analyzing:0:03:47
    md.hotspot_complete - Image 1 Hotspot Isolating:0:00:04
    md.hotspot_complete - Image 1 Array Priming:0:00:00
    md.hotspot_complete - Image 1 Translating:0:00:00
    md.hotspot_complete - Image 1 Saving:0:00:00
    
    .. figure:: isolatedhotspot.png
       :scale: 30 %
       :align: center
       
       ``md.hotspot_complete`` output result
    
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        pixel_copy = pixel_values1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print ("md.hotspot_complete - Image " + str(indexor+1) + " Importing:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            if item == find:
                pixel_values1[index] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Converting:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        pixel_values1 = np.array(pixel_values1)
        shape = (height, width)
        pixel_values2 = np.reshape(pixel_values1, shape)
        pixel_copy2 = np.reshape(pixel_copy, shape)
        const = (width*height)/100
        store = {}
        analyzedval = {}
        for w in range (x,width+1):
            for h in range (y,height+1):
                store[str(h-y)+":"+str(h)+", "+str(w-x)+":" + str(w)] = pixel_values2[h-y:h, w-x:w]
                a=(w-1)*height+h
                print(str(round((a)/(const),1)) + "%" , end = "\r")  
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Hotspot Calculating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        for w in range (x,width):
            for h in range (y,height):
                keytocheck = store.get(str(h-y)+":"+str(h)+", "+str(w-x)+":" + str(w))
                stringforkey = str(h-y)+":"+str(h)+", "+str(w-x)+":" + str(w)
                
                if np.sum(keytocheck[0,:]) == x and np.sum(keytocheck[y-1,:]) == x and np.sum(keytocheck[:,0]) == y and np.sum(keytocheck[:,x-1]) == y:
                    valueforkey = True
                else:
                    valueforkey = False
                a=(w-1)*height+h
                print(str(round((a)/(const),1)) + "%" , end = "\r")
                analyzedval[stringforkey] = valueforkey
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Hotspot Analyzing:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0) 
        fillmatrix = np.full((y, x), 1)
        for key, value in analyzedval.items():
            if value == True:
                txt = key
                splitter = txt.split(", ")
                split, splitone = splitter[0], splitter[1]
                a = split.split(":")
                b = splitone.split(":")
                one =  int(a[0])
                two = int(a[1])
                three = int(b[0])
                four = int(b[1])
                pixel_copy2[one:two, three:four] = fillmatrix
        
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Hotspot Isolating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        result = pixel_copy2.reshape([1, width*height])
        reult = result.tolist()
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Array Priming:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        pixel_values1 = list(rgb1.getdata())
        for i in range(0,width*height):
            if reult[0][i] == 1:
                pixel_values1[i] = find
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Translating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        image_out = Image.new("RGB",(width,height))
        image_out.putdata(pixel_values1)
        image_out.save(mod_string + "_isolated" + ".PNG")
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_complete - Image " + str(indexor+1) + " Saving:" + str(durationTime))

        
def hotspot_calculator(filepath, x, y, find = (0,0,0)):
    """
    Calculates partition matrixes from input images, 
    essentially divides the input image into all possiblehotspot combinations. 
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    x : integer, default: (0,0,0)
        The width, in pixels, of the hotspot matrix calculator. Think of this as the width of the intuitive paintbrush.
    y : integer, default: (0,0,0)
        The height, in pixels, of the hotspot matrix calculator. Think of this as the height of the intuitive paintbrush.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works. Note that the ``calculator`` outputs a dictionary, where the key is a 2D array index of
    the image's RGB pixel matrix and the value is the submatrix itself from the index key. The dictionary is stored as the global variable ``storeddictionary``.
    

    Examples
    --------
    >>> md.hotspot_calculator("/example/directory/file.png", 50, 50)
    md.hotspot_calculator - Image 1 Importing:0:00:01
    md.hotspot_calculator - Image 1 Converting:0:00:01
    md.hotspot_calculator - Image 1 Hotspot Calculating:0:00:54
    >>> list(storeddictionary.items())[:4]
    [('0:50, 0:50', array([[2, 2, 2, ..., 2, 2, 2],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       ...,
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1]])), ('1:51, 0:50', array([[2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       ...,
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1]])), ('2:52, 0:50', array([[2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       ...,
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1]])), ('3:53, 0:50', array([[2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       ...,
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1],
       [2, 2, 2, ..., 1, 1, 1]]))]
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        pixel_copy = pixel_values1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print ("md.hotspot_calculator - Image " + str(indexor+1) + " Importing:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            if item == find:
                pixel_values1[index] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_calculator - Image " + str(indexor+1) + " Converting:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        pixel_values1 = np.array(pixel_values1)
        shape = (height, width)
        pixel_values2 = np.reshape(pixel_values1, shape)
        pixel_copy2 = np.reshape(pixel_copy, shape)
        const = (width*height)/100
        global storeddictionary
        storeddictionary = {}
        for w in range (x,width+1):
            for h in range (y,height+1):
                storeddictionary[str(h-y)+":"+str(h)+", "+str(w-x)+":" + str(w)] = pixel_values2[h-y:h, w-x:w]
                a=(w-1)*height+h
                print(str(round((a)/(const),1)) + "%" , end = "\r")  
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_calculator - Image " + str(indexor+1) + " Hotspot Calculating:" + str(durationTime))
     
    
def hotspot_analyzer(calc=None, filepath = None, x = None, y = None, find = (0,0,0)):
    """
    Analyzes partition matrixes from input images, 
    essentially determining the clinical significance of each spot,
    preparing the image for isolation. 
    
    Parameters
    ----------
    calc : dictionary
        A dictionary to analyze where the key is a 2D array index of the image's RGB pixel matrix and the value is the submatrix itself from the index key.
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    x : integer, default: (0,0,0)
        The width, in pixels, of the hotspot matrix calculator. Think of this as the width of the intuitive paintbrush.
    y : integer, default: (0,0,0)
        The height, in pixels, of the hotspot matrix calculator. Think of this as the height of the intuitive paintbrush.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works. Note that the ``analyzer`` outputs a dictionary, where the key is a 2D array index of
    the image's RGB pixel matrix and the value is boolean, depending on the analysis (see source code for more details) of the input matricies. The dictionary is stored 
    as the global variable``analyzedval``.
    

    Examples
    --------
    >>> md.hotspot_analyzer(calc = storeddictionary, filepath = "/example/directory/file.png", x = 50, y = 50)
    md.hotspot_analyzer - Image 1 Importing:0:00:01
    md.hotspot_analyzer - Image 1 Hotspot Analyzing:0:02:22
    >>> list(analyzedval.items())[:4]
    [('0:50, 0:50', False), ('1:51, 0:50', False), ('2:52, 0:50', False), ('3:53, 0:50', False)]
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]


        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        pixel_copy = pixel_values1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print ("md.hotspot_analyzer - Image " + str(indexor+1) + " Importing:" + str(durationTime))


        startTime = datetime.datetime.now().replace(microsecond=0)
        global analyzedval
        analyzedval = {}
        for w in range (x,width):
            for h in range (y,height):
                keytocheck = calc.get(str(h-y)+":"+str(h)+", "+str(w-x)+":" + str(w))
                stringforkey = str(h-y)+":"+str(h)+", "+str(w-x)+":" + str(w)

                if np.sum(keytocheck[0,:]) == x and np.sum(keytocheck[y-1,:]) == x and np.sum(keytocheck[:,0]) == y and np.sum(keytocheck[:,x-1]) == y:
                    valueforkey = True
                else:
                    valueforkey = False
                    a=(w-1)*height+h
                    const = (width*height)/100
                    print(str(round((a)/(const),1)) + "%" , end = "\r")
                analyzedval[stringforkey] = valueforkey
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_analyzer - Image " + str(indexor+1) + " Hotspot Analyzing:" + str(durationTime))

        
def hotspot_isolator(calc=None, filepath = None, x = None, y = None, find = (0,0,0)):
    """
    Isolates and silences relevant partition matrixes from input images, 
    essentially removing noise with unremarkable clinical significance from each image.
    
    Parameters
    ----------
    calc : dictionary
        A dictionary to analyze where the key is a 2D array index of the image's RGB pixel matrix and the value is a boolean analysis of noise relevance.
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    x : integer, default: (0,0,0)
        The width, in pixels, of the hotspot matrix calculator. Think of this as the width of the intuitive paintbrush.
    y : integer, default: (0,0,0)
        The height, in pixels, of the hotspot matrix calculator. Think of this as the height of the intuitive paintbrush.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works. 

    Examples
    --------
    >>> md.hotspot_isolator(calc = analyzedval, filepath = "/example/directory/file.png", x = 50, y = 50)
    md.hotspot_isolator - Image 1 Converting:0:00:00
    md.hotspot_isolator - Image 1 Importing:0:00:02
    md.hotspot_isolator - Image 1 Hotspot Isolating:0:00:04
    md.hotspot_isolator - Image 1 Array Priming:0:00:00
    md.hotspot_isolator - Image 1 Translating:0:00:00
    md.hotspot_isolator - Image 1 Saving:0:00:00
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]


        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        
        
        
        starttTime = datetime.datetime.now().replace(microsecond=0)
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            if item == find:
                pixel_values1[index] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - starttTime        
        print("md.hotspot_isolator - Image " + str(indexor+1) + " Converting:" + str(durationTime))
        
        pixel_copy = pixel_values1
        pixel_values1 = np.array(pixel_values1)
        shape = (height, width)
        pixel_values2 = np.reshape(pixel_values1, shape)
        pixel_copy2 = np.reshape(pixel_copy, shape)
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print ("md.hotspot_isolator - Image " + str(indexor+1) + " Importing:" + str(durationTime))
            
            
        startTime = datetime.datetime.now().replace(microsecond=0) 
        fillmatrix = np.full((y, x), 1)
        for key, value in calc.items():
            if value == True:
                txt = key
                splitter = txt.split(", ")
                split, splitone = splitter[0], splitter[1]
                a = split.split(":")
                b = splitone.split(":")
                one =  int(a[0])
                two = int(a[1])
                three = int(b[0])
                four = int(b[1])
                pixel_copy2[one:two, three:four] = fillmatrix
        
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_isolator - Image " + str(indexor+1) + " Hotspot Isolating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        result = pixel_copy2.reshape([1, width*height])
        reult = result.tolist()
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_isolator - Image " + str(indexor+1) + " Array Priming:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        pixel_values1 = list(rgb1.getdata())
        for i in range(0,width*height):
            if reult[0][i] == 1:
                pixel_values1[i] = find
        durationTime = endTime - startTime        
        print("md.hotspot_isolator - Image " + str(indexor+1) + " Translating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        image_out = Image.new("RGB",(width,height))
        image_out.putdata(pixel_values1)
        image_out.save(mod_string + "_isolated" + ".PNG")
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.hotspot_isolator - Image " + str(indexor+1) + " Saving:" + str(durationTime))

def branch_complete(filepath, x, y, find = (0,0,0), iterations=100):
    """
    Processes inputted images using a branching algorithm, 
    essentially acting as an intuitive selector of a figure in the image. 
    Allows a user to selectively filter one instance of clinical relevance.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    x : integer
        The horizontal location, in pixels, of any relevant pixel on the image.
    y : integer
        The vertical location, in pixels, of any relevant pixel on the image.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    iterations : integer, default: 100
        The number of branching algorithms to run. The higher this value, the farther the pixels will branch out, and the more likely you are to get a noise-free image.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works.
    

    Examples
    --------
    >>> md.branch_complete("/example/directory/file.png", 450, 350, iterations = 500)
    
    
    
    .. figure:: isolatedbranch.png
       :scale: 30 %
       :align: center
       
       ``md.hotspot_complete`` output result
    
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        pixel_copy = pixel_values1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print ("md.branch_complete - Image " + str(indexor+1) + " Importing:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            if item == find:
                pixel_values1[index] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Converting:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        pixel_values1 = np.array(pixel_values1)
        shape = (height, width)
        global pixel_values2
        pixel_values2 = np.reshape(pixel_values1, shape)
        pixel_copy2 = np.reshape(pixel_copy, shape)
        global coords
        coords = []
        const = (width*height)/100
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Translating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        proximal_brancher(coords, y,x)
        global coordsfinal
        coordsfinal = []
        i = 0
        global diflist
        diflist = coords
        while i != iterations:
            coordsfinalinit = []
            filteredcoords = []
            print(str(round((i*100)/(iterations),1)) + "%", end = "\r")
            for index, item in enumerate(diflist):
                txt = str(diflist[index])
                newstr = txt.replace("[", "")
                finalstr = newstr.replace("]", "")
                splitter = finalstr.split(", ")
                newy, newx = splitter[0], splitter[1]
                newx = int(newx)
                newy = int(newy) 
                if manual_checker(newy, newx) == 2:
                    proximal_brancher(coordsfinal, newy, newx)
            for index, item in enumerate(coordsfinal):
                coordsfinal[index] = str(coordsfinal[index])
            for index, item in enumerate(coords):
                coords[index] = str(coords[index])   
            list(set(coordsfinal))
            list(set(coords))
            diflist = list(set(coordsfinal) - set(coords))
            coords = []
            for index, item in enumerate(coordsfinal):
                coords.append(coordsfinal[index])     
            i += 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Branching:" + str(durationTime))  
            

        startTime = datetime.datetime.now().replace(microsecond=0)
        a = []
        g = []
        list(set(coords))
        a = coords
        for index, item in enumerate(a):  
            print(str(round((index*100)/(len(coords)),1)) + "%", end = "\r")
            txt = str(a[index])
            newstr = txt.replace("[", "")
            finalstr = newstr.replace("]", "")
            splitter = finalstr.split(", ")
            newy, newx = splitter[0], splitter[1]
            newx = int(newx)
            newy = int(newy)
            if manual_checker(newy, newx) == 2:
                g.append([newy, newx])
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Branch Analyzing:" + str(durationTime)) 
        
                                                  
        startTime = datetime.datetime.now().replace(microsecond=0)
        complement = []
        for w in range(width):
            for h in range(height):
                complement.append([h,w])
        setc = {tuple(item) for item in g}
        finalset = [item for item in complement if tuple(item) not in setc]
        for index, item in enumerate(finalset):      
            txt = str(finalset[index])
            newstr = txt.replace("[", "")
            finalstr = newstr.replace("]", "")
            splitter = finalstr.split(", ")
            newy, newx = splitter[0], splitter[1]
            newx = int(newx)
            newy = int(newy) 
            pixel_copy2[newy,newx] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Branch Isolating:" + str(durationTime))
        
                                                  
        startTime = datetime.datetime.now().replace(microsecond=0)      
        result = pixel_copy2.reshape([1, width*height])
        reult = result.tolist()
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Array Priming:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        pixel_values1 = list(rgb1.getdata())
        for i in range(0,width*height):
            if reult[0][i] == 1:
                pixel_values1[i] = find
            if reult[0][i] == 3:
                pixel_values1[i] = (255,0,255)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Translating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)      
        image_out = Image.new("RGB",(width,height))
        image_out.putdata(pixel_values1)
        image_out.save(mod_string + "_isolated" + ".PNG")
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_complete - Image " + str(indexor+1) + " Saving:" + str(durationTime))
                                                  
 
def branch_calculator(filepath, x, y, find = (0,0,0), iterations = 100):
    """
    Calculates branches for inputted images using a branching algorithm, 
    essentially acting as an intuitive selector of a figure in the image.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    x : integer
        The horizontal location, in pixels, of any relevant pixel on the image.
    y : integer
        The vertical location, in pixels, of any relevant pixel on the image.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    iterations : integer, default: 100
        The number of branching algorithms to run. The higher this value, the farther the pixels will branch out, and the more likely you are to get a noise-free image.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works. Note that the ``calculator`` outputs a list of tuples, 
    where each tuple is a pixel ``x, y`` coordinate of a branch. The list is stored as the global variable ``coords``.
    

    Examples
    --------
    >>> md.branch_calculator("/example/directory/file.png", 450, 350, iterations = 500)
    md.branch_complete - Image 1 Importing:0:00:01
    md.branch_complete - Image 1 Converting:0:00:00
    md.branch_complete - Image 1 Translating:0:00:00
    md.branch_complete - Image 1 Branching:0:42:04
    md.branch_complete - Image 1 Branch Analyzing:0:03:02
    md.branch_complete - Image 1 Branch Isolating:0:00:10
    md.branch_complete - Image 1 Array Priming:0:00:00
    md.branch_complete - Image 1 Translating:0:00:00
    md.branch_complete - Image 1 Saving:0:00:01
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
        name = ntpath.basename(files[indexor])
        size = len(name)
        mod_string = name[:size - 4]
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        image = Image.open(files[indexor])
        rgb1 = image.convert('RGB')
        width, height = image.size
        pixel_values1 = list(rgb1.getdata())
        pixel_copy = pixel_values1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print ("md.branch_calculator - Image " + str(indexor+1) + " Importing:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        for index, item in enumerate(pixel_values1):
            if item != find:
                pixel_values1[index] = 2
            if item == find:
                pixel_values1[index] = 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_calculator - Image " + str(indexor+1) + " Converting:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        pixel_values1 = np.array(pixel_values1)
        shape = (height, width)
        global pixel_values2
        pixel_values2 = np.reshape(pixel_values1, shape)
        global pixel_copy2
        pixel_copy2 = np.reshape(pixel_copy, shape)
        global coords
        coords = []
        const = (width*height)/100
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_calculator - Image " + str(indexor+1) + " Translating:" + str(durationTime))
        
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        proximal_brancher(coords, y,x)
        global coordsfinal
        coordsfinal = []
        i = 0
        global diflist
        diflist = coords
        while i != iterations:
            coordsfinalinit = []
            filteredcoords = []
            print(str(round((i*100)/(iterations),1)) + "%", end = "\r")
            for index, item in enumerate(diflist):
                txt = str(diflist[index])
                newstr = txt.replace("[", "")
                finalstr = newstr.replace("]", "")
                splitter = finalstr.split(", ")
                newy, newx = splitter[0], splitter[1]
                newx = int(newx)
                newy = int(newy) 
                if manual_checker(newy, newx) == 2:
                    proximal_brancher(coordsfinal, newy, newx)
            for index, item in enumerate(coordsfinal):
                coordsfinal[index] = str(coordsfinal[index])
            for index, item in enumerate(coords):
                coords[index] = str(coords[index])   
            list(set(coordsfinal))
            list(set(coords))
            diflist = list(set(coordsfinal) - set(coords))
            coords = []
            for index, item in enumerate(coordsfinal):
                coords.append(coordsfinal[index])     
            i += 1
        endTime = datetime.datetime.now().replace(microsecond=0)
        durationTime = endTime - startTime        
        print("md.branch_calculator - Image " + str(indexor+1) + " Branching:" + str(durationTime))  

        
def branch_analyzer(calc):
    """
    Analyzes branches for inputted images, 
    essentially determining the clinical significance of each spot,
    preparing the image for isolation.
    
    Parameters
    ----------
    calc : list
        A list of tuples containg the coordinates of all branched pixels.
        
    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works. Note that the ``analyzer`` outputs a list of tuples, 
    where each tuple is a pixel ``x, y`` coordinate of a branch. The list is stored as the global variable ``g``.
    

    Examples
    --------
    >>> md.branch_analyzer(coords)
    md.branch_analyzing - Branch Analyzing:0:03:02
    """
    startTime = datetime.datetime.now().replace(microsecond=0)
    a = []
    global g
    g = []
    list(set(calc))
    a = calc
    for index, item in enumerate(a):  
        print(str(round((index*100)/(len(coords)),1)) + "%", end = "\r")
        txt = str(a[index])
        newstr = txt.replace("[", "")
        finalstr = newstr.replace("]", "")
        splitter = finalstr.split(", ")
        newy, newx = splitter[0], splitter[1]
        newx = int(newx)
        newy = int(newy)
        if manual_checker(newy, newx) == 2:
            g.append([newy, newx])
    endTime = datetime.datetime.now().replace(microsecond=0)
    durationTime = endTime - startTime        
    print("md.branch_analyzer - Branch Analyzing:" + str(durationTime)) 

    
def branch_isolator(filepath, calc, find = (0,0,0)):
    """
    Analyzes branches for inputted images, 
    essentially determining the clinical significance of each spot,
    preparing the image for isolation.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    calc : list
        A list of tuples containg the coordinates of all branched pixels.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``

    Notes
    -----
    See ``mednoise`` API explanations to understand how this algorithm works. 
    

    Examples
    --------
    >>> md.branch_isolator("/example/directory/file.png", g)
    
    md.branch_isolator - Image 1 Branch Isolating:0:00:10
    md.branch_isolator - Image 1 Array Priming:0:00:00
    md.branch_isolator - Image 1 Translating:0:00:00
    md.branch_isolator - Image 1 Saving:0:00:01
    """
    files = glob.glob(filepath)
    for indexor, item in enumerate(files):
            name = ntpath.basename(files[indexor])
            size = len(name)
            mod_string = name[:size - 4]


            startTime = datetime.datetime.now().replace(microsecond=0)
            image = Image.open(files[indexor])
            rgb1 = image.convert('RGB')
            width, height = image.size
            pixel_values1 = list(rgb1.getdata())
            pixel_copy = pixel_values1
            endTime = datetime.datetime.now().replace(microsecond=0)
            durationTime = endTime - startTime        
            print ("md.branch_isolator - Image " + str(indexor+1) + " Importing:" + str(durationTime))
            startTime = datetime.datetime.now().replace(microsecond=0)
            complement = []
            for w in range(width):
                for h in range(height):
                    complement.append([h,w])
            setc = {tuple(item) for item in calc}
            finalset = [item for item in complement if tuple(item) not in setc]
            for index, item in enumerate(finalset):      
                txt = str(finalset[index])
                newstr = txt.replace("[", "")
                finalstr = newstr.replace("]", "")
                splitter = finalstr.split(", ")
                newy, newx = splitter[0], splitter[1]
                newx = int(newx)
                newy = int(newy) 
                pixel_copy2[newy,newx] = 1
            endTime = datetime.datetime.now().replace(microsecond=0)
            durationTime = endTime - startTime        
            print("md.branch_isolator - Image " + str(indexor+1) + " Branch Isolating:" + str(durationTime))


            startTime = datetime.datetime.now().replace(microsecond=0)      
            result = pixel_copy2.reshape([1, width*height])
            reult = result.tolist()
            endTime = datetime.datetime.now().replace(microsecond=0)
            durationTime = endTime - startTime        
            print("md.branch_isolator - Image " + str(indexor+1) + " Array Priming:" + str(durationTime))


            startTime = datetime.datetime.now().replace(microsecond=0)      
            pixel_values1 = list(rgb1.getdata())
            for i in range(0,width*height):
                if reult[0][i] == 1:
                    pixel_values1[i] = find
                if reult[0][i] == 3:
                    pixel_values1[i] = (255,0,255)
            durationTime = endTime - startTime        
            print("md.branch_isolator - Image " + str(indexor+1) + " Translating:" + str(durationTime))


            startTime = datetime.datetime.now().replace(microsecond=0)      
            image_out = Image.new("RGB",(width,height))
            image_out.putdata(pixel_values1)
            image_out.save(mod_string + "_isolated" + ".PNG")
            endTime = datetime.datetime.now().replace(microsecond=0)
            durationTime = endTime - startTime        
            print("md.branch_isolator - Image " + str(indexor+1) + " Saving:" + str(durationTime))    


def proximal_brancher(calc, y,x):
            d = calc
            pixel_values2
            r = y
            c = x
            m, n = pixel_values2.shape
            
            for i in [-1, 0, 1]: 
                for j in [-1, 0, 1]: 
                    if 0 <= r + i < m and 0 <= c + j < n:
                        d.append([r + i, c + j])
                            
def manual_checker(y, x):
    if pixel_values2[y,x] == 2:
        return 2
    else:
        return 1

def artificial_complete():
    """
    Processes inputted images using a jaccard-similarity algorithm, 
    similar to the ones used in machine learning and deep learning. 
    Allows a user to selectively filter instances of noise that may 
    be slightly different with each image.
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    matrix : tuple
        A series of ``x, y`` coordinates that defines opposite coordinates 
        of a rectangular selection of a picture. This is passed as a 
        number-tuple, in the format ``(x1, y1, x2, y2)``. Used to compare 
        similarity and forms the basis of this algorithm.
        
    Notes
    -----
    This algorithm objectively contains the most complex and computing-intensive 
    calculations. It should only be used as a last resort after trying other algorithms 
    unsuccessfully, or in the case of high-performance computing.
    

    Examples
    --------
    >>> md.artificial_complete()
    This feature is still being worked on.
    """
    print("This feature is still being worked on.")

def artificial_calculator():
    """
    Calculates scores for inputted images using a jaccard-similarity algorithm, 
    similar to the ones used in machine learning and deep learning. 
    
    Parameters
    ----------
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    matrix : tuple
        A series of ``x, y`` coordinates that defines opposite coordinates 
        of a rectangular selection of a picture. This is passed as a 
        number-tuple, in the format ``(x1, y1, x2, y2)``. Used to compare 
        similarity and forms the basis of this algorithm.
        
    Notes
    -----
    This algorithm objectively contains the most complex and computing-intensive 
    calculations. It should only be used as a last resort after trying other algorithms 
    unsuccessfully, or in the case of high-performance computing.
    

    Examples
    --------
    >>> md.artificial_calculate()
    This feature is still being worked on.
    """
    print("This feature is still being worked on.")

def artificial_analyzer():
    """
    Analyzes scores for inputted images to determine noise significance based on jaccard-similiarity.
    
    Parameters
    ----------
    calc : matrix
        A matrix of calculated scores. More details about the specifications of this
        matrix will be available when ``artificial`` is released in a later version.
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    matrix : tuple, default: None
        A series of ``x, y`` coordinates that defines opposite coordinates 
        of a rectangular selection of a picture. This is passed as a 
        number-tuple, in the format ``(x1, y1, x2, y2)``. Used to compare 
        similarity and forms the basis of this algorithm.
        
    Notes
    -----
    This algorithm objectively contains the most complex and computing-intensive 
    calculations. It should only be used as a last resort after trying other algorithms 
    unsuccessfully, or in the case of high-performance computing.
    

    Examples
    --------
    >>> md.artificial_analyze()
    This feature is still being worked on.
    """
    print("This feature is still being worked on.")

def artificial_isolator():
    """
    Selectively reduces noise based on analyzed scores for inputted images.
    
    Parameters
    ----------
    calc : list
        A list of analyzed scores. More details about the specifications of this
        list will be available when ``artificial`` is released in a later version.
    filepath : string
        A filepath for images to be selected from. Since **mednoise** uses ``glob``, 
        it can take any argument that ``glob`` can parse through.
    find : RGB tuple, default: (0,0,0)
        A value that indicates silenced noise. Usually is considered the 
        background color of the input image, often ``(0,0,0)``.
    matrix : tuple, default: None
        A series of ``x, y`` coordinates that defines opposite coordinates 
        of a rectangular selection of a picture. This is passed as a 
        number-tuple, in the format ``(x1, y1, x2, y2)``. Used to compare 
        similarity and forms the basis of this algorithm.
        
    Notes
    -----
    This algorithm objectively contains the most complex and computing-intensive 
    calculations. It should only be used as a last resort after trying other algorithms 
    unsuccessfully, or in the case of high-performance computing.
    

    Examples
    --------
    >>> md.artificial_isolator()
    This feature is still being worked on.
    """
    print("This feature is still being worked on.")