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