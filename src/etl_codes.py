import codecs
import jaconv
from etldr.etl_data_names import ETLDataNames 
from etldr.etl_data_set_info import ETLDataSetInfo


class ETLCodes():
    """
    A convenience class for using all codecs which are used in the ETL data set.

    Warning:
        The 'euc_co59.dat'-file from the ETL data set is required in the data set directory. 
    """

    def __init__(self, euc_co59_file_path : str) -> None:
        super().__init__()
        self.init_co59(euc_co59_file_path)
        self.init_codes()


    def init_co59(self, euc_co59_file_path : str):
        """
            Initialize reading of "co59"-codes
        """

        with codecs.open(euc_co59_file_path, 'r', 'euc-jp') as f:
            co59t = f.read()
        co59l = co59t.split()
        self.conv = {}
        for c in co59l:
            ch = c.split(':')
            co = ch[1].split(',')
            co59c = (int(co[0]), int(co[1]))
            self.conv[co59c] = ch[0]

    def init_codes(self):
        """
        Setup a dict which contains ETLDataSetInfo-instances with the necessary info about the data set types.
        """

        # TYPE_M -> ETL 1, 6, 7 - works
        self.code_M = ETLDataSetInfo(">H 2s H 6B I 4H 4B 4x 2016s 4x".replace(" ", ""),
                                    2052, (64, 63), 4, [1], self.decode_M_type_character)
        # TYPE_K -> ETL 2
        self.code_K = ETLDataSetInfo("uint:36, uint:6, pad:30, bits:36, bits:36, pad:24, bits:12, pad:180, bytes:2700",
                                    2745, (60, 60), 6, [-2], self.decode_K_type_character)
        # TYPE_C -> ETL 3, 4, 5
        self.code_C = ETLDataSetInfo("uint:36,uint:36,hex:8,pad:28,hex:8,pad:28,bits:24,pad:12,15*uint:36,pad:1008,bytes:2736",
                                    2952, (72, 76), 4, [2, 4], self.decode_C_type_character)
        # TYPE_8B -> ETL 8B
        self.code_8B = ETLDataSetInfo(">H 2s 4s 504s".replace(" ", ""),
                                    512, (64, 63), 1, [1], self.decode_8B_type_character)
        # TYPE_8G -> ETL 8G
        self.code_8G = ETLDataSetInfo(">H 2s 8s I 4B 4H 2B 30x 8128s 11x".replace(" ", ""),
                                    8199, (128, 127), 4, [1], self.decode_8G_type_character)
        # TYPE_9B -> ETL 9B
        self.code_9B = ETLDataSetInfo(">H 2s 4s 504s 64x".replace(" ", ""),
                                    576, (64, 63), 1, [1], self.decode_9B_type_character)
        # TYPE_9G -> ETL 9G
        self.code_9G = ETLDataSetInfo(">H 2s 8s I 4B 4H 2B 34x 8128s 7x".replace(" ", ""),
                                    8199, (128, 127), 4, [1], self.decode_9B_type_character)

    def T56(self, c : int) -> str:
        """Decodes c into a string using the T56-code.

        Args:
            c : An integer which should be decoded using the T56-code.

        Returns:
            The decoded str.
        """

        t56s = '0123456789[#@:>? ABCDEFGHI&.](<  JKLMNOPQR-$*);\'|/STUVWXYZ ,%="!'
        return t56s[c]

    def co59_to_utf8(self, co59) -> str:
        """Decodes co59 to utf-8.

        Args:
            co59 : The string which should be decoded from co59 to utf-8.

        Returns:
            The decoded utf-8 string
        """
        return self.conv[co59]

    def decode_M_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-M type. 

        Args:
            _bytes : The bytes object which should be decoded.

        Returns:
            The decoded label.
        """
    
        return bytes.fromhex(_bytes.hex()).decode('iso2022_jp')

    def decode_K_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-K type. 

        Args:
            _bytes : The bytes object which should be decoded.

        Returns:
            The decoded label.
        """
        
        tup = tuple([b.uint for b in _bytes.cut(6)])
        return self.co59_to_utf8(tup)

    def decode_C_type_character(self, _bytes : bytes, char_code) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-C type. 

        Args:
            _bytes    : The bytes object which should be decoded.
            char_code : The T56 code of the entry.

        Returns:
            [description]
        """

        char_code = ''.join([ self.T56(b.uint) for b in char_code.cut(6) ])

        char = bytes.fromhex(_bytes).decode('shift_jis')
        if char_code[0] == 'H':
            char = jaconv.kata2hira(jaconv.han2zen(char)).replace('ぃ', 'ゐ').replace('ぇ', 'ゑ')
        elif char_code[0] == 'K':
            char = jaconv.han2zen(char).replace('ィ', 'ヰ').replace('ェ', 'ヱ')

        return char

    def decode_8B_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-8B type. 

        Args:
            _bytes : The bytes object which should be decoded.

        Returns:
            The decoded label.
        """

        #print(_bytes, bytes.fromhex(_bytes), bytes.fromhex('1b2442' + _bytes + '1b2842'))
        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')

    def decode_8G_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-8G type. 

        Args:
            _bytes : The bytes object which should be decoded.

        Returns:
            The decoded label.
        """

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')

    def decode_9B_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-9B type. 

        Args:
            _bytes : The bytes object which should be decoded.

        Returns:
            The decoded label.
        """

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')

    def decode_9G_type_character(self, _bytes : bytes) -> str:
        """Decodes _bytes which encode the label from an entry which has the ETL-9G type. 

        Args:
            _bytes : The bytes object which should be decoded.

        Returns:
            The decoded label.
        """

        return bytes.fromhex('1b2442' + _bytes.hex() + '1b2842').decode('iso2022_jp')