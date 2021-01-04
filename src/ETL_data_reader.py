from co59_to_utf8 import CO59_to_utf8

import os
import re
import struct
from PIL import Image
import numpy as np
import bitstring
import jaconv

from typing import List, Tuple



class ETL_data_reader():
    """A class which contains a helper functions to load the data from the ETL data set.

    Attributes:
        codes                (dict) : a dictionary which maps the data set types to info about them. 
        dataset_types        (dict) : a dictionary which maps the data set name to the type it uses.
        co59_to_utf8 (CO59_to_utf8) : an decoder object for the 59-code.

    """

    codes         = {}
    dataset_types = {}
    co59_to_utf8 = None

    def __init__(self) -> None:
        self.init_codes()
        self.init_dataset_types()
        
        path = os.path.join(os.path.dirname(os.getcwd()), "dataset", 'euc_co59.dat')
        self.co59_to_utf8 = CO59_to_utf8(path)

    def T56(self, c : int) -> str:
        """Decodes c into a string using the T56-code.

        Args:
            c (str): An integer which should be decoded using the T56-code.

        Returns:
            [str]: The decoded str.
        """

        t56s = '0123456789[#@:>? ABCDEFGHI&.](<  JKLMNOPQR-$*);\'|/STUVWXYZ ,%="!'
        return t56s[c]

    def init_codes(self):
        """
        Setup a dict which contains dicts with the necessary info about the data set.
        
        The tuples have the form:
            "code"        : the code to read the entry
            "struct_size" : the size of the entry in byte
            "img_size"    : the pixel size of the entry's image
            "img_depth"   : the bit depth of the entry;s image 
            "label_index" : which index the label is in the struct
            "decoder"     : the function to decode the label
        """

        # TYPE_M -> ETL 1, 6, 7 - works
        self.codes["M"] = {"code" : ">H 2s H 6B I 4H 4B 4x 2016s 4x".replace(" ", ""),
                            "struct_size" : 2052,
                            "img_size"    : (64, 63),
                            "img_depth"   : 4,
                            "label_index" : [1],
                            "decoder" : self.decode_M_type_character}

        # TYPE_K -> ETL 2
        self.codes["K"] = {"code" : "uint:36, uint:6, pad:30, bits:36, bits:36, pad:24, bits:12, pad:180, bytes:2700",
                            "struct_size" : 2745,
                            "img_size" : (60, 60),
                            "img_depth" : 6,
                            "label_index" : [-2],
                            "decoder" : self.decode_K_type_character}

        # TYPE_C -> ETL 3, 4, 5
        self.codes["C"] = {"code" : "uint:36,uint:36,hex:8,pad:28,hex:8,pad:28,bits:24,pad:12,15*uint:36,pad:1008,bytes:2736", 
                            "struct_size" : 2952,
                            "img_size" : (72, 76),
                            "img_depth" : 4,
                            "label_index" : [2, 4],
                            "decoder" : self.decode_C_type_character}

        # TYPE_8B -> ETL 8B
        self.codes["8B"] = {"code" : ">H 2s 4s 504s".replace(" ", ""),
                            "struct_size" : 512,
                            "img_size" : (64, 63),
                            "img_depth" : 1,
                            "label_index" : [1],
                            "decoder" : self.decode_8B_type_character}
        # TYPE_8G -> ETL 8G
        self.codes["8G"] = {"code" : ">H 2s 8s I 4B 4H 2B 30x 8128s 11x".replace(" ", ""),
                            "struct_size" : 8199,
                            "img_size" : (128, 127),
                            "img_depth" : 4,
                            "label_index" : [1],
                            "decoder" : self.decode_8G_type_character}
        # TYPE_9B -> ETL 9B
        self.codes["9B"] = {"code" : ">H 2s 4s 504s 64x".replace(" ", ""),
                            "struct_size" : 576,
                            "img_size" : (64, 63),
                            "img_depth" : 1,
                            "label_index" : [1],
                            "decoder" : self.decode_9B_type_character}
        # TYPE_9G -> ETL 9G
        self.codes["9G"] = {"code" : ">H 2s 8s I 4B 4H 2B 34x 8128s 7x",
                            "struct_size" : 8199,
                            "img_size" : (128, 127),
                            "img_depth" : 4,
                            "label_index" : [1],
                            "decoder" : self.decode_9B_type_character}


    def init_dataset_types(self):
        """
        Initialize the dictionary of dataset_types and their codes
        """

        self.dataset_types["ETL1"]  = self.codes["M"]
        self.dataset_types["ETL2"]  = self.codes["K"]
        self.dataset_types["ETL3"]  = self.codes["C"]
        self.dataset_types["ETL4"]  = self.codes["C"]
        self.dataset_types["ETL5"]  = self.codes["C"]
        self.dataset_types["ETL6"]  = self.codes["M"]
        self.dataset_types["ETL7"]  = self.codes["M"]
        self.dataset_types["ETL8"]  = self.codes["8B"]
        self.dataset_types["ETL9"]  = self.codes["8G"]
        self.dataset_types["ETL10"] = self.codes["9B"]
        self.dataset_types["ETL11"] = self.codes["9G"]

    def read_dataset_part(self, path : str, data_set_name : str, status_info : bool = True) -> List[Tuple[str, np.array]]:
        """
        Reads the given ETL data at "path" with parameters according to the given "data_set_id".

        Args:
            path          : the path to the data set which should be loaded.
            data_set_name : The name of the data set to load (valid are: ETL_ + {1, ..., 11})


        Returns:
            List[Tuple[str, np.array]] : A list of all tuples which contain the images
                                        and the labels from the data set given by 'path'.
        """

        data = []

        if(status_info):
            print("Loading:", os.path.basename(path))
        
        #check that the given id is a valid one
        if(not data_set_name in self.dataset_types):
            print("Error! The given ID:", data_set_name, "is not valid.")
            print("Legal keys are:")
            print(self.dataset_types.keys())

        else:
            #get the necessary info from the dict
            data_info = self.dataset_types[data_set_name]

            #open the file and read it byte by byte
            with open(path, "rb") as f:
                
                #skip dummy entries
                f.seek(data_info["struct_size"], 0)
                while(_bytes := f.read(data_info["struct_size"])):

                    #unpack the packed data - byte-coded
                    raw = None 
                    if(data_info["code"].startswith(">")):
                        raw = struct.unpack(data_info["code"], _bytes)
                    #character-coded (1 character = 6 Bit)
                    else:
                        raw = bitstring.ConstBitStream(bytes=_bytes)
                        raw = raw.readlist(data_info["code"])

                    #convert the image to an PIL.image in mode "P"
                    imageF = Image.frombytes('F', data_info["img_size"], raw[-1], 'bit', data_info["img_depth"])
                    #imageP = imageF.convert('P')
                    img = np.array(imageF)

                    indices = data_info["label_index"]
                    label = data_info["decoder"](*list(raw[i] for i in indices))

                    data.append( (img, label) )
            
        return data

    def read_dataset_whole(self, path : str, data_set_name : str, status_info : bool = True) -> List[Tuple[str, Image.Image]]:
        """Reads all parts of an ETL data set in the folder given by path.

        Searches in the folder given by path for parts of the ETL data set.
        Only files matching the regex: data_set_name + "_\d+"

        Caution:
            Loading some data sets completely can use a lot of memory (ETL11 ~ 35GB)

        Args:
            path                   (str): The path to the folder from which all data sets should be loaded.
            data_set_name          (str): The name of the data set to load (valid are: ETL_ + {1, ..., 11})
            status_info (bool, optional): Output information of the loading progress. Defaults to True.

        Returns:
            List[Tuple[str, Image.Image]]: A list of all tuples which contain the images
                                            and the labels from the data set(s) in the directory 'path'.
        """


        data = []

        if(status_info):
            print("Loading all data set files (" + data_set_name + ") from:", path, "...")

        #regex to check if file is valid
        reg = re.compile((data_set_name + r"_\d+"))

        for file in os.listdir(path):
            print(reg.match(file), "file:", file)
            if(not (reg.match(file) is None)):
                data += (self.read_dataset_part(os.path.join(path, file), data_set_name, status_info))

    def read_dataset_whole(self, *include : ETLCharacterGroups,
                            resize : Tuple[int, int] = (64, 64),
                            normalize : bool = True) -> Tuple[np.array, np.array]:
        """ Read, process and filter the whole ETL data set (ETL1 - ETL9G).

        Caution:
            Reading the whole dataset with all available entries will use up a lot of memory (>50GB).

        Warning:
            Will throw an error if not all parts and files of the data set can be found in 'self.path'.
            Also if the images do not get resized to the same size.

        Arguments:
            *include  : All character types (Kanji, Hiragana, Symbols, stc.) which should be included. If unset everyting will be loaded.
            resize    : The size the image should be resized (if resize < 1 the images will not be resized). Defaults to (64, 64).
            normalize : Should the gray values be normalized between [0.0, 1.0]. Defaults to True.

        Returns:
            The loaded and filtered data set entries in the form: (images, labels).
        """
    
        imgs, labels = [], []

        #iterate over all available data_set parts
        for _type in ETLDataNames:
        
            #read all parts
            _imgs, _labels = self.read_dataset_part(_type, *include, resize=resize, normalize=normalize)

            #make sure the loaded data is not an empty array
            if(len(_imgs) > 0 and len(_labels) > 0):
                imgs.append(_imgs)
                labels.append(_labels)

        #only concatenate if there were arrays loaded
        if(len(imgs) > 0 and len(labels) > 0):
            imgs, labels = np.concatenate(imgs), np.concatenate(labels)

        return imgs, labels

    def process_image(self, imageF : Image.Image,
                            img_size : Tuple[int, int],
                            img_depth : int) -> np.array:
        """ Processes the given ETL-image.

        The image will be resized to 'img_size' and the color channel depth will be normalized to its 'img_depth'.

        Args:
            imageF    : The image which should be processed.
            img_size  : The size which the image should be resized to (no resizing if any component < 1).
            img_depth : The gray scale depth of the image (no normalization when set to < 1).

        Returns:
            The processed image.
        """

        #convert to 8-bit
        img = imageF.convert('P')

        #resize the image
        if(img_size[0] > 1 and img_size[1] > 1):
            img = img.resize(size=(img_size[1], img_size[0]), resample=Image.LINEAR)

        img = np.array(img)

        #normalize between 0 and 1
        if(img_depth > 1):
            normalization_factor = (2.0 ** img_depth - 1)
            img = img / normalization_factor

        #reshape to separate the color channel
        img = img.reshape(len(img), len(img[0]), 1)

        return img

    def select_entries(self, label : str, *include : ETLCharacterGroups) -> bool:
        """ Checks if the given entry given by 'label' should be included in the loaded data set.

        Args:
            label    : The label which should be checked if it should be included.
            *include : All character types which should be included. Defaults to all if unset.

        Returns:
            bool: True if the entry should be included, False otherwise.
        """

        #if the parameter is unset load everything
        if(not include):
            include = [ETLCharacterGroups.all]

        #list of regex's for filtering the different groups
        regex = "|".join([i.value for i in include])

        #match with regex if label should be included
        reg = re.compile(regex)
        should_include = reg.match(label) 

        return should_include

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')