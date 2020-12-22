from co59_to_utf8 import CO59_to_utf8

import os
import struct
from PIL import Image
import numpy as np
import bitstring
import jaconv

from typing import List, Tuple



class ETL_data_reader():
    """[summary]

    Caution:
        This class does not allow to use the following fields:
            K-Type: Mark of Style

    """


    codes         = {}
    dataset_types = {}
    co59_to_utf8 = None

    def __init__(self) -> None:
        path = os.path.join(os.path.dirname(os.getcwd()), "dataset", 'euc_co59.dat')
        self.co59_to_utf8 = CO59_to_utf8(path)
    def read_dataset(self, path : str, data_set_id : str) -> List[Tuple[str, np.array]]:
        """
        Reads the given ETL data set with parameters according to the given data_set_id.

        Args:
            path        : the path to the data set which should be loaded.
            data_set_id : ETL_ + {1, 2, 3, 4, 5, 6, 7, 8B, 8G, 9B, 9G}

        Returns:

        """

        data = []
        
        #check that the given id is a valid one
        if(not data_set_id in self.dataset_types):
            print("Error! The given ID:", data_set_id, "is not valid.")
            print("Legal keys are:")
            print(self.dataset_types.keys())

        else:
            #get the necessary info from the dict
            data_info = self.dataset_types[data_set_id]
            print(data_info)

            #open the file and read it byte by byte
            with open(path, "rb") as f:
                
                #skip dummy entries
                f.seek(data_info["struct_size"], 0)
                while(_bytes := f.read(data_info["struct_size"])):


                    raw = None 

                    #unpack the packed data - byte-coded
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



    def decode_M_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry from a
            data set which follow the M_TYPE from the ETL data set. 

        Args:
            _bytes (bytes): The bytes object which should be decoded.

        Returns:
            str: The decoded label.
        """
    
        return bytes.fromhex(_bytes.hex()).decode('iso2022_jp')

    def decode_K_type_character(self, _bytes : bytes):
        
        tup = tuple([b.uint for b in _bytes.cut(6)])
        return self.co59_to_utf8(tup)

    def decode_C_type_character(self, _bytes : bytes, char_code):

        char_code = ''.join([ self.T56(b.uint) for b in char_code.cut(6) ])

        char = bytes.fromhex(_bytes).decode('shift_jis')
        if char_code[0] == 'H':
            char = jaconv.kata2hira(jaconv.han2zen(char)).replace('ぃ', 'ゐ').replace('ぇ', 'ゑ')
        elif char_code[0] == 'K':
            char = jaconv.han2zen(char).replace('ィ', 'ヰ').replace('ェ', 'ヱ')

        return char

    def decode_8B_type_character(self, _bytes : bytes) -> str:
        """[summary]

        Args:
            _bytes (bytes): [description]

        Returns:
            str: [description]
        """

        #print(_bytes, bytes.fromhex(_bytes), bytes.fromhex('1b2442' + _bytes + '1b2842'))
        return bytes.fromhex('1b2442' + _bytes + '1b2842').decode('iso2022_jp')

    def decode_8G_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry from the ETL8B data set. 

        Args:
            _bytes (bytes): The bytes object which should be decoded.

        Returns:
            str: The decoded label.
        """

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')

    def decode_9B_type_character(self, _bytes : bytes):
        """Decodes _bytes which encode the label from an entry from the ETL9B data set. 

        Args:
            _bytes (bytes): The bytes object which should be decoded.

        Returns:
            str: The decoded label.
        """

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')

    def decode_9G_type_character(self, _bytes : bytes):
        """Decodes _bytes which encode the label from an entry from the ETL9G data set. 

        Args:
            _bytes (bytes): The bytes object which should be decoded.

        Returns:
            str: The decoded label.
        """

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')