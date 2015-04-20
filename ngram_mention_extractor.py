
class ngram_mention_extractor(object):

    """ Returns all ngrams as a python list"""
    def get_mentions(self, query, n = 0):

        words = query.split(" ")

        if(n == 0):
            n = len(words)

        mentions = []
        for length in reversed(range(1, n+1)):
            for start_index in range(0, len(words) - length + 1):
                mentions.append(" ".join(words[start_index:start_index+length]).lower())
                
        return mentions

if __name__ == "__main__":
    extractor = ngram_mention_extractor()
    print(extractor.get_mentions("Hello there yoiu bastard"))