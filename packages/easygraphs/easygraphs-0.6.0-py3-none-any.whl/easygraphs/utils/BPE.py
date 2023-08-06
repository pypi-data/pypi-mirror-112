class BPE(object):
    '''
    Subword extraction.

    Args: 
        
    Returns: 
        

    Usage:
        dict_tuples = dict(((('l', 'o', 'w'), 5), (('l', 'o', 'w', 'e', 'r'), 2) , (('n', 'e', 'w', 'e', 's', 't'), 6), (('w', 'i', 'd', 'e', 's', 't'), 3)))
        bpe = BPE(dict_tuples, preprocessed = False)
        bpe.build()

    '''
    SEP = " "
    SUB_SEP = ","
    END = "<END>"
    UNK = "<UNK>"
    ORIGIN_SET = set([str(x) for x in range(100)]) # define as : 1 to n / a to z
    # ORIGIN_SET = set(list("abcdefghijkmlnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    ORIGIN_SET.add(END)

    def __init__(self, word_dict, num_merges = 1000, preprocessed = False):
        self.num_merges = num_merges
        self.word_dict = word_dict
        self.preprocessed = preprocessed
        self.subword_set = set()
        self.subword_result = None

        if not self.preprocessed:
            self.word_dict = self.init_vocab(word_dict)
        else:
            self.word_dict = word_dict


    def build(self, is_save = False):
        vocab = self.word_dict
        cnt = 0
        while cnt != self.num_merges:
            pairs, subword_freq = self.count_subword_freq(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            vocab = self.merge_vocab(best, vocab)
            self.update_set(best, pairs.get(best), subword_freq)
            print(str(cnt+1) + "\t" + str(best) + "\t" + self.SUB_SEP.join(best) + "\t" + "Len:" + str(len(self.subword_set)))
            # print(self.subword_set)
            cnt += 1

        self.subword_set = self.subword_set | self.ORIGIN_SET
        self.subword_result = sorted(self.subword_set, key=lambda x:len(x), reverse = True)
        if is_save:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_subword_result.dict"
            self.save(filename)

    def init_vocab(cls, word_dict):
        vocab = dict()
        for word, freq in word_dict.items():
            word_new = [str(x) for x in word]
            word_new.append(cls.END)
            word_new = cls.SEP.join(word_new)
            vocab[word_new] = word_dict[word]
        return vocab

    def count_subword_freq(cls, vocab):
        pairs = collections.defaultdict(int)
        subword_freq = collections.defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split(cls.SEP)
            for i in range(len(symbols)-1):
                pairs[symbols[i], symbols[i+1]] += freq
                subword_freq[symbols[i]] += freq
                subword_freq[symbols[i+1]] += freq
        return pairs, subword_freq

    def merge_vocab(cls, pair, v_in):
        v_out = {}
        bigram_re = re.escape(cls.SEP.join(pair)) # replace origin bi-gram
        bigram = cls.SUB_SEP.join(pair)
        p = re.compile(r'(?<!\S)' + bigram_re + r'(?!\S)')
        for word in v_in:
            w_out = p.sub(bigram, word) # concat
            v_out[w_out] = v_in[word]
        return v_out

    def update_set(self, pair, value, subword_freq):
        start, end = pair
        bigram = self.SUB_SEP.join(pair)
        self.subword_set.add(bigram)
        n_start = subword_freq[start]
        n_end = subword_freq[end]
        if  (n_start == value) and (start not in self.ORIGIN_SET):
            self.subword_set.remove(start)
        if (n_end == value) and (end not in self.ORIGIN_SET):
            self.subword_set.remove(end)

    def encode(self, list_input):
        str_input = self.SUB_SEP.join(list_input)
        list_subword = []
        list_index = []
        for subword in self.subword_result:
            index = str_input.find(subword)
            if index != -1:
                list_subword.append(subword)
                str_input = str_input.replace(subword, "")
                str_input = str_input.strip(',')
                if not str_input:
                    break
        str_input = self.SUB_SEP.join(list_input)
        for subword in list_subword:
            index = str_input.find(subword)
            list_index.append((subword, index))
        # print(list_subword)
        # print(list_index)
        encode_result = [x[0] for x in sorted(list_index, key=lambda x:x[1])]
        # print(encode_result)
        return encode_result

    def save(self, filename):
        import pickle
        with open(filename, "wb") as f:
            pickle.dump(self.subword_result, f)