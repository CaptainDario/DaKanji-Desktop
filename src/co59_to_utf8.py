import codecs

class CO59_to_utf8:
    """Decodes co59 to utf8 when called like a method.
    """

    def __init__(self, euc_co59_file='euc_co59.dat'):
        with codecs.open(euc_co59_file, 'r', 'euc-jp') as f:
            co59t = f.read()
        co59l = co59t.split()
        self.conv = {}
        for c in co59l:
            ch = c.split(':')
            co = ch[1].split(',')
            co59c = (int(co[0]), int(co[1]))
            self.conv[co59c] = ch[0]

    def __call__(self, co59):
        return self.conv[co59]