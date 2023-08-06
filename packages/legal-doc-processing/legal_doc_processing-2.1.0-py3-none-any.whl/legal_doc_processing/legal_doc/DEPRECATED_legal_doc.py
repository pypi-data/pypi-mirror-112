import os
import time

from legal_doc_processing.utils import (
    get_pipeline,
    get_spacy,
    _if_not_pipe,
    _if_not_spacy,
)

from legal_doc_processing.legal_doc.reference import predict_reference
from legal_doc_processing.legal_doc.monetary_sanction import predict_monetary_sanction
from legal_doc_processing.legal_doc.decision_date import predict_decision_date
from legal_doc_processing.legal_doc.defendant import predict_defendant
from legal_doc_processing.legal_doc.extracted_authorities import (
    predict_extracted_authorities,
)
from legal_doc_processing.legal_doc.plaintiff import predict_plaintiff
from legal_doc_processing.legal_doc.sentence import predict_sentence
from legal_doc_processing.legal_doc.nature_of_violations import (
    predict_nature_of_violations,
)
from legal_doc_processing.legal_doc.currency import predict_currency
from legal_doc_processing.legal_doc.structure import structure_legal_doc


class LegalDoc:
    """main legal doc class """

    def __init__(
        self,
        text: str,
        file_path: str = None,
        nlpipe=None,
        nlspa=None,
    ):
        """init method of the LegalDoc
        pos args :
            text (str) : the complete text to proceed
            nlpipe (pipleline) : a pre instanciated pipline. default None (a object will be created)
        opt args :
            -
        raise :
            -
        return :
            a LegalDoc object"""

        # args as attr
        self.file_path = os.path.dirname(file_path) if file_path else None
        self.file_name = os.path.basename(file_path) if file_path else None

        self.nlpipe = nlpipe if nlpipe else get_pipeline()
        self.nlspa = nlspa if nlspa else get_spacy()
        try:
            self.nlspa.add_pipe("sentencizer")
        except Exception as e:
            pass

        # text and cleanstructure
        self.raw_text = text
        # self.clean_pages = clean.clean_doc(text)
        # self.structured_text = struct.structure_legal_doc(text)
        self.structured_text = structure_legal_doc(text)
        self.h1 = self.structured_text["header"]
        self.first_page = self.structured_text["pages"][0]

        if len(self.structured_text["pages"] > 1):
            self.first_2_pages = (
                self.structured_text["pages"][0] + self.structured_text["pages"][1]
            )
        else:
            self.first_2_pages = self.structured_text["pages"][0]

        self.h1_sents = [i.txt for i in nlspa(self.h1).sents]
        self.first_page_sents = [i.text for i in nlspa(" ".join(self.first_page)).sents]

        # data points private
        self._feature_list = [
            "_currency",
            "_code_law_violation",
            "_country_of_violation",
            "_decision_date",
            "_defendant",
            "_extracted_authorities",
            "_id",
            "_juridiction",
            "_monetary_sanction",
            "_nature_of_violations",
            "_plaintiff",
            "_reference",
            "_sentence",
            "_violation_date",
        ]
        self.feature_list = [i[1:] for i in self._feature_list]

        _ = [setattr(self, k, [(None, -1)]) for k in self._feature_list]

    def strize(self, item_list):
        """ """

        clean_l = lambda item_list: [str(i).strip() for i, j in item_list]
        return ",".join(clean_l(item_list))

    @property
    def currency(self):
        return self.strize(self._currency)

    @property
    def code_law_violation(self):
        return self.strize(self._code_law_violation)

    @property
    def country_of_violation(self):
        return self.strize(self._country_of_violation)

    @property
    def decision_date(self):
        return self.strize(self._decision_date)

    @property
    def defendant(self):
        return self.strize(self._defendant)

    @property
    def extracted_authorities(self):
        return self.strize(self._extracted_authorities)

    @property
    def id(self):
        return self.strize(self._id)

    @property
    def juridiction(self):
        return self.strize(self._juridiction)

    @property
    def monetary_sanction(self):
        return self.strize(self._monetary_sanction)

    @property
    def nature_of_violations(self):
        return self.strize(_nature_of_violations)

    @property
    def plaintiff(self):
        return self.strize(self._plaintiff)

    @property
    def reference(self):
        return self.strize(self._reference)

    @property
    def sentence(self):
        return self.strize(self._sentence)

    @property
    def violation_date(self):
        return self.strize(self._violation_date)

    @property
    def _feature_dict(self):
        return {k: getattr(self, k) for k in self._feature_list}

    @property
    def feature_dict(self):
        return {str(k[1:]): self.strize(getattr(self, k)) for k in self._feature_list}

    def predict(self, feature) -> str:
        """ """

        if feature == "reference":
            self._reference = predict_reference(self.structured_text)
            return self._reference
        elif feature == "monetary_sanction":
            self._monetary_sanction = predict_monetary_sanction(
                self.first_page, self.nlpipe
            )
            return self._monetary_sanction
        elif feature == "currency":
            self._currency = predict_currency(
                self.first_page,
            )
            return self._currency
        elif feature == "decision_date":
            self._decision_date = predict_decision_date(self.first_page)
            return self._decision_date
        elif feature == "defendant":
            self._defendant = predict_defendant(self.first_page, self.nlpipe)
            return self._defendant
        elif feature == "extracted_authorities":
            self._extracted_authorities = predict_extracted_authorities(
                self.first_page, self.nlpipe
            )
            return self._extracted_authorities
        elif feature == "plaintiff":
            self._plaintiff = predict_plaintiff(self.first_page, self.nlpipe)
            return self._plaintiff
        elif feature == "sentence":
            self._sentence = predict_sentence(self.first_page, self.nlpipe)
            return self._sentence
        elif feature == "nature_of_violations":
            self._nature_of_violations = predict_nature_of_violations(
                self.first_page, self.nlpipe
            )
            return self._nature_of_violations
        elif feature == "all":
            self._reference = predict_reference(self.structured_text)
            self._monetary_sanction = predict_monetary_sanction(
                self.first_page, self.nlpipe
            )
            self._decision_date = predict_decision_date(self.first_page)
            self._defendant = predict_defendant(self.first_page, self.nlpipe)
            self._extracted_authorities = predict_extracted_authorities(
                self.first_page, self.nlpipe
            )
            self._plaintiff = predict_plaintiff(self.first_page, self.nlpipe)
            self._sentence = predict_sentence(self.first_page, self.nlpipe)
            self._nature_of_violations = predict_nature_of_violations(
                self.first_page, self.nlpipe
            )
            self._currency = predict_currency(self.first_page)

            return self.feature_dict
        else:
            raise AttributeError("feature Not Implemented")

    def predict_all(self) -> str:
        """return self.predict("all") """

        return self.predict("all")

    def __repr__(self):
        """__repr__ method """

        _pipe = "OK" if self.nlpipe else self.nlpipe
        _spa = "OK" if self.nlspa else self.nlspa
        _feat_dict = {k: v[:8] for k, v in self.feature_dict.items()}
        return f"LegalDoc(path:{self.file_path}, file:{self.file_name}, {_feat_dict}, pipe/spacy:{_pipe}/{_spa}"

    def __str__(self):
        """__str__ method """

        return self.__repr__()


def from_text(text: str, nlpipe=None, nlspa=None):
    """ """

    return LegalDoc(text, nlpipe=nlpipe, nlspa=nlspa)


def from_file(file_path: str, nlpipe=None, nlspa=None):
    """read a file and return a LegalDoc object """

    with open(file_path, "r") as f:
        text = f.read()

    return LegalDoc(text, file_path=file_path, nlpipe=nlpipe, nlspa=nlspa)


if __name__ == "__main__":

    # import
    from legal_doc_processing.legal_doc.loader import legal_doc_X_y
    from legal_doc_processing.legal_doc.structure import structure_legal_doc

    # laod
    nlpipe = get_pipeline()
    nlpspa = get_spacy()

    # legal_doc structured
    df = legal_doc_X_y()
    df = df.iloc[:4, :]
    df["obj"] = df.txt.apply(lambda i: LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa))

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["preds"] = df.obj.apply(lambda i: i.predict_all())
    t = time.time() - t

    # labels
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = one.obj
    one_pred = one.preds
