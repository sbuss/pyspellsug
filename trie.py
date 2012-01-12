class TrieNode(object):
    def __init__(self):
        self.children = {}
        self.is_terminal = False

    def insert(self, word):
        if word is None or len(word) == 0:
            self.is_terminal = False
            return self.is_terminal

        if len(word) == 1:
            self.is_terminal = True
            return self.is_terminal

        first_letter = word[0]
        if first_letter not in self.children:
            self.children[first_letter] = TrieNode()

        return self.children[first_letter].insert(word[1:])

    def lookup(self, word):
        if word is None or len(word) == 0 or len(word) == 1:
            return self.is_terminal

        first_letter = word[0].lower()
        if first_letter not in self.children:
            return False  # TODO look at all the children
        else:
            return self.children[first_letter].lookup(word[1:])


def build_edict(wordfile):
    f = open(wordfile, 'r')
    edict = TrieNode()
    for line in f:
        edict.insert(line.lower().strip())
    return edict
