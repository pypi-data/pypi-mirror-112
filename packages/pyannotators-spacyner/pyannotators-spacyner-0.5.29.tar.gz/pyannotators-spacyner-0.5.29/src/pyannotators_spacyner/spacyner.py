from functools import lru_cache
from typing import Type, List, cast
import spacy
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Span, Annotation
from spacy.cli.download import download_model, get_compatibility, get_version
from spacy.errors import OLD_MODEL_SHORTCUTS
from spacy.language import Language
from spacy.util import run_command
from wasabi import msg
import sys


class SpacyNERParameters(AnnotatorParameters):
    model: str = Field("en_core_web_sm",
                       description="Name of the [spacy model](https://spacy.io/models) to use for NER extraction")


class SpacyNERAnnotator(AnnotatorBase):
    """[SpacyNER](https://github.com/facebook/spacyner) annotator.
    """

    def annotate(self, documents: List[Document], parameters: AnnotatorParameters) \
            -> List[Document]:
        params: SpacyNERParameters = \
            cast(SpacyNERParameters, parameters)
        # Create parsing context with time and language information
        nlp = get_nlp(params.model)

        for document in documents:
            document.annotations = []
            if not document.sentences:
                document.sentences = [Span(start=0, end=len(document.text))]
            sents = [document.text[s.start:s.end] for s in document.sentences]
            asents = nlp.pipe(sents)
            for sent, asent in zip(document.sentences, asents):
                for ent in asent.ents:
                    start = sent.start + ent.start_char
                    end = sent.start + + ent.end_char
                    document.annotations.append(Annotation(start=start, end=end,
                                                           labelName=ent.label_.lower(),
                                                           label=ent.label_,
                                                           text=document.text[start:end]))
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SpacyNERParameters


@lru_cache(maxsize=None)
def get_nlp(model):
    try:
        nlp: Language = spacy.load(model)
    except BaseException:
        nlp = load_spacy_model(model)
    return nlp


def load_spacy_model(model, *pip_args):
    if '_sci_' in model:
        model_name = model
        download_sci_model(model)
    else:
        suffix = "-py3-none-any.whl"
        dl_tpl = "{m}-{v}/{m}-{v}{s}#egg={m}=={v}"
        model_name = model
        if model in OLD_MODEL_SHORTCUTS:
            msg.warn(
                f"As of spaCy v3.0, shortcuts like '{model}' are deprecated. Please "
                f"use the full pipeline package name '{OLD_MODEL_SHORTCUTS[model]}' instead."
            )
            model_name = OLD_MODEL_SHORTCUTS[model]
        compatibility = get_compatibility()
        version = get_version(model_name, compatibility)
        download_model(dl_tpl.format(m=model_name, v=version, s=suffix), pip_args)
    msg.good(
        "Download and installation successful",
        f"You can now load the package via spacy.load('{model_name}')",
    )
    # If a model is downloaded and then loaded within the same process, our
    # is_package check currently fails, because pkg_resources.working_set
    # is not refreshed automatically (see #3923). We're trying to work
    # around this here be requiring the package explicitly.
    require_package(model_name)
    return spacy.load(model_name)


def require_package(name):
    try:
        import pkg_resources

        pkg_resources.working_set.require(name)
        return True
    except:  # noqa: E722
        return False


def download_sci_model(
        filename: str, user_pip_args=None) -> None:
    download_url = f"https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/{filename}-0.4.0.tar.gz"
    pip_args = list(user_pip_args) if user_pip_args is not None else []
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]
    run_command(cmd)
