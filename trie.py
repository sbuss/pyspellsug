class TrieNode(object):
    """ A node in a Trie, intended for dictionary lookups.

    >>> t = TrieNode()
    >>> t.insert('salmon')
    True
    >>> 'salmon' in t
    True
    >>> t.lookup('sal')
    False
    >>> t.lookup('salmon')
    True
    """
    def __init__(self):
        self.children = {}
        self.is_terminal = False

    def insert(self, word):
        """ Insert a word into the Trie.

        Args:
            word - Any iterable, though a string is most useful.

        Word is inserted one element at a time (one letter at a time for
        strings). Each element is either looked up or added to children.
        When the end of the iterable is reached, that node is marked as
        terminal.
        """
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

    def __contains__(self, word):
        return self.lookup(word)

    def lookup(self, word):
        """ Check if a word is in the Trie.

        Args:
            word - The iterable to lookup, though a string is more useful.

        Return True if the word is in the Trie, False otherwise.

        """
        if word is None or len(word) == 0 or len(word) == 1:
            return self.is_terminal

        first_letter = word[0].lower()
        if first_letter not in self.children:
            return False  # TODO look at all the children
        else:
            return self.children[first_letter].lookup(word[1:])


def build_dict(wordfile):
    """ Build a dictionary.

    >>> d = build_dict('/usr/share/dict/words')
    >>> d.lookup('salmon')
    True
    >>> d.lookup('abdks')
    False
    """

    f = open(wordfile, 'r')
    d = TrieNode()
    for line in f:
        d.insert(line.lower().strip())
    return d


def _test():
    import doctest
    doctest.testmod()


def _benchmark():
    """ Benchmark the performance of the trie compared to a set & dict. """
    import datetime

    def elapsed(f):
        def timer(*args, **kwargs):
            t1 = datetime.datetime.now()
            ret = f(*args, **kwargs)
            t2 = datetime.datetime.now()
            return (t2 - t1, ret)
        return timer

    @elapsed
    def lookup(word_iterable, ds):
        c = 0
        for word in word_iterable:
            if word.lower().strip() in ds:
                c += 1
            else:
                pass
        return c

    (elapsed, d) = elapsed(build_dict)('/usr/share/dict/words')
    print("Took %s to build dictionary" % elapsed)

    words = open('/usr/share/dict/words')
    words_set = set()
    words_dict = {}
    for word in words:
        w = word.lower().strip()
        words_set.add(w)
        words_dict[w] = True

    words.seek(0)
    (elapsed, c) = lookup(words, d)
    print("Took %s to look up %s words using the trie" % (elapsed, c))

    words.seek(0)
    (elapsed, c) = lookup(words, words_set)
    print("Took %s to look up %s words using the set" % (elapsed, c))

    words.seek(0)
    (elapsed, c) = lookup(words, words_dict)
    print("Took %s to look up %s words using the dict" % (elapsed, c))


if __name__ == "__main__":
    _test()
    #_benchmark()
