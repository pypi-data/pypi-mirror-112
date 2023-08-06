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
