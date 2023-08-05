from DependencyParser.Universal.UniversalDependencyRelation cimport UniversalDependencyRelation
from Dictionary.Word cimport Word
from FrameNet.FrameElement cimport FrameElement
from MorphologicalAnalysis.MetamorphicParse cimport MetamorphicParse
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse
from NamedEntityRecognition.Gazetteer cimport Gazetteer
from NamedEntityRecognition.Slot cimport Slot
from PropBank.Argument cimport Argument


cdef class AnnotatedWord(Word):
    """
     * In order to add another layer, do the following:
     * 1. Select a name for the layer.
     * 2. Add a new constant to ViewLayerType.
     * 3. Add private attribute.
     * 4. Add an if-else to the constructor, where you set the private attribute with the layer name.
     * 5. Update toString method.
     * 6. Add initial value to the private attribute in other constructors.
     * 7. Update getLayerInfo.
     * 8. Add getter and setter methods.
    """
    cdef MorphologicalParse __parse
    cdef MetamorphicParse __metamorphicParse
    cdef str __semantic
    cdef object __namedEntityType
    cdef Argument __argument
    cdef FrameElement __frameElement
    cdef str __shallowParse
    cdef UniversalDependencyRelation __universalDependency
    cdef Slot __slot
    cdef object __polarity
    cdef str ccg

    cpdef str getLayerInfo(self, object viewLayerType)
    cpdef MorphologicalParse getParse(self)
    cpdef setParse(self, str parseString)
    cpdef MetamorphicParse getMetamorphicParse(self)
    cpdef setMetamorphicParse(self, str parseString)
    cpdef str getSemantic(self)
    cpdef setSemantic(self, str semantic)
    cpdef object getNamedEntityType(self)
    cpdef setNamedEntityType(self, str namedEntity)
    cpdef Argument getArgument(self)
    cpdef setArgument(self, str argument)
    cpdef FrameElement getFrameElement(self)
    cpdef setFrameElement(self, str frameElement)
    cpdef Slot getSlot(self)
    cpdef setSlot(self, str slot)
    cpdef object getPolarity(self)
    cpdef str getPolarityString(self)
    cpdef setPolarity(self, str polarity)
    cpdef str getShallowParse(self)
    cpdef setShallowParse(self, str parse)
    cpdef str getCcg(self)
    cpdef setCcg(self, str ccg)
    cpdef str getPosTag(self)
    cpdef setPosTag(self, str posTag)
    cpdef UniversalDependencyRelation getUniversalDependency(self)
    cpdef setUniversalDependency(self, int to, str dependencyType)
    cpdef str getUniversalDependencyFormat(self, int sentenceLength)
    cpdef getFormattedString(self, object wordFormat)
    cpdef checkGazetteer(self, Gazetteer gazetteer)
