from Corpus.Corpus cimport Corpus


cdef class AnnotatedCorpus(Corpus):

    cpdef exportUniversalDependencyFormat(self, str outputFileName, str path=*)
    cpdef checkMorphologicalAnalysis(self)
    cpdef checkNer(self)
    cpdef checkShallowParse(self)
    cpdef checkSemantic(self)
