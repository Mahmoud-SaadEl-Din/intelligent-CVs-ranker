class paragraphPreprocessing:

    def sentenceSplitter(self,txt):
        return list(filter(None,txt.split('\n')))

    
