from typing import Tuple, List, Callable



class ETLDataSetInfo():
    """A convenience class for storing information about a data set part.
        
        Attributes:
            code               [str] : The code which can be used to decode the
                                        stored data files of this data set.
            struct_size        [int] : The size (in bytes) of one entry of this data set type.
            img_size Tuple[int, int] : A Tuple with the dimensions of the images in this data set.
            img_depth          [int] : The depth of the gray channel of this entry's image.
            label_index        [int] : The index of the loaded struct in which the label is coded.
            decoder       [function] : The function which can be used to decode an entry of this data set.
    """

    def __init__(self, code : str, struct_size : int,
                    img_size : Tuple[int, int],
                    img_depth : int,
                    label_index : List[int],
                    decoder : Callable[[List[bytes]], str]) -> None:

        self.code        = code
        self.struct_size = struct_size
        self.img_size    = img_size
        self.img_depth   = img_depth
        self.label_index = label_index
        self.decoder     = decoder