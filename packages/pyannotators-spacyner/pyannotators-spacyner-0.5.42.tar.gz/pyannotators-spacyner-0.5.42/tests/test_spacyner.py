from typing import List
from pyannotators_spacyner.spacyner import SpacyNERAnnotator, SpacyNERParameters, get_nlp
from pymultirole_plugins.v1.schema import Document


def test_spacyner():
    model = SpacyNERAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == SpacyNERParameters
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters()
    docs: List[Document] = annotator.annotate([Document(
        text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
        metadata=parameters.dict())], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == 4
    paris = doc0.annotations[0]
    france = doc0.annotations[1]
    macron = doc0.annotations[2]
    republic = doc0.annotations[3]
    assert paris.label == 'GPE'
    assert france.label == 'GPE'
    assert macron.label == 'PERSON'
    assert republic.label == 'GPE'


def test_scispacyner():
    model = SpacyNERAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == SpacyNERParameters
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters(model='en_core_sci_sm')
    docs: List[Document] = annotator.annotate([Document(
        text="Myeloid derived suppressor cells (MDSC) are immature myeloid cells with immunosuppressive activity.\nThey accumulate in tumor-bearing mice and humans with different types of cancer, including hepatocellular carcinoma (HCC).",
        metadata=parameters.dict())], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == 12


def test_cached_nlp():
    parameters1 = SpacyNERParameters()
    nlp1 = get_nlp(parameters1.model)
    parameters2 = SpacyNERParameters()
    nlp2 = get_nlp(parameters2.model)
    assert id(nlp1) == id(nlp2)
