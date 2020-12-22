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