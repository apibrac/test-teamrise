'''Module that creates a logistic regression object in order to analyze sentences.
Parameters can be set manually in order to have useful results even withour a learning database.
The Objective_Analyzer can be extend with deterministic functions such as the extract_numbers_and_symbols for a deterministic part of the analyze.
'''

from math import exp
import re

def vector_addition(*vectors):
    '''Extends all vectors with zero so they have the shape of the biggest one, then add them'''
    if not vectors:
        return None
    size = max(len(v) for v in vectors)
    for v in vectors :
        v += [0]*(size-len(v))
    return [sum(v) for v in zip(*vectors)]

def extend_vector(v, n):
    '''Extend a vector to have the n first dimensions empty'''
    return [0]*n+v

def extract_numbers_and_symbols(objective):
    '''Extract numbers and symbols of objective'''
    out = dict()
    numbers = re.findall(r'\d+', objective)
    symbols = [s for s in ['%', '$', '€'] if s in objective]
    if len(numbers) == 1 :
        out['progress_target'] = numbers[0]
    elif numbers  :
        out['numbers'] = numbers
    if len(symbols) == 1:
        out['progress_unit'] = symbols[0]
    elif symboles :
        out['symbols'] = symbols
    return out

class Objective_Analyzer():
    '''Analyze an objective in order to extract characteristics
    Use the logistic regression.
    Rewritten in order to be able to manually set some coefficients.
    '''
    def __init__(self, additional_functions = []):
        '''Empty'''
        self.conclusions = []
        self.subgroups = [] # for s in subgroups : s['conclusions']=list of positions of corresponding conclusions
        self.parameters = dict()
        self.additional_functions = additional_functions
    def prepare_sentence(self, sentence_in_string):
        '''Split a sentence in a list of words.
        For now it is very simple but it can be improved to treat numbers, symbols etc.
        '''
        return sentence_in_string.split()
    def compute_vector(self, sentence):
        '''Compute the vector for a sentence.'''
        return vector_addition(*[self.parameters.get(word, []) for word in sentence])
    def decisions(self, vector):
        '''Draw conclusions from the vector of a sentence.'''
        out=[]
        if not vector:
            return None
        vector = [exp(v) for v in vector+[0]*(len(self.conclusions)-len(vector))] # for the use of the logistic regression, but is useless here
        for subg in self.subgroups :
            choice = self.take_best(*[(vector[i],i) for i in subg['conclusions']])
            if choice is not None :
                out.append(self.conclusions[choice])
        return out
    def take_best(self, *args):
        '''Brutal decision :
        take the best one.
        '''
        M = max(args)
        for v in args :
            if v[0] == M[0] and v!=M :#it's a tie
                return None
        return M[1]
    def analyze(self, sentence_in_string):
        '''Analyse a sentence (=objective)'''
        out = {'characteristics':self.decisions(self.compute_vector(self.prepare_sentence(sentence_in_string)))}
        for f in self.additional_functions :
            out.update(f(sentence_in_string))
        return out
    def add_words_with_weight(self, words, weight_vector, rank=0):
        '''Add words and the corresponding weight. 
        Rank is used if the weighted vector is set only for one characteristic that is not the first.
        '''
        vector = extend_vector(weight_vector, rank)
        assert len(vector) <= len(self.conclusions), 'Too many weights for {} : {}'.format(words, vector)
        for word in words:
            if word in self.parameters :
                self.parameters[word] = vector_addition(self.parameters[word], vector)
            else :
                self.parameters[word] = vector
    def add_to_guess(self, guess_conclusions, **kwargs):
        '''Add new conclusions in a cluster (exclusive).
        Additional arguments are stored in the cluster dictionary, can be used later for different kind of clusters?
        Return the rank (that can be used to add words).
        '''
        rank = len(self.conclusions)
        self.conclusions+=guess_conclusions
        self.subgroups.append(dict(conclusions = [rank + i  for i in range(len(guess_conclusions))], **kwargs))
        return rank
        
