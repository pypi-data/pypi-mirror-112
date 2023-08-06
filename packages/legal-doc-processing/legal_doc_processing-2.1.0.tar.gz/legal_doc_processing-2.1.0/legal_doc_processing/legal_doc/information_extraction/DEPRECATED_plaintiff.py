import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)


def _ask_all(txt, nlpipe) -> list:
    """ask all questions and return a list of dict """

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # question, funct
    quest_pairs = [
        # ("Who is the acusator?", "ask_who_acusator"),
        ("Who is the plaintiff?", "ask_who_plaintiff"),
        # ("Who is the victim?", "ask_who_victim"),
        # ("Who is the defendant?", "ask_who_defendant"),
        # ("Who violated?", "ask_who_violated"),
        # ("Who has to pay?", "ask_who_pay"),
        # ("Who is accused?", "ask_who_accused"),
        ("What are the defendant's names?", "Names of the defendants"),
    ]

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    # clean
    ans = [i for i in ans if (i["answer"].lower() != "defendants")]

    return ans


def _clean_ans(ans, threshold=0.00):
    """ """

    # build dataframe
    df = pd.DataFrame(ans)
    df = df.loc[:, ["score", "answer"]]

    # group by ans and make cumutavie score of accuracy
    ll = [
        {"answer": k, "cum_score": v.score.sum()}
        for k, v in df.groupby("answer")
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll


def predict_plaintiff(cleaned_legal_doc: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # # pipe
    # nlpipe = _if_not_pipe(nlpipe)

    # # prepar
    # fp_55_legal_doc = [i for i in cleaned_legal_doc if len(i) > 55]
    # txt = " ".join(fp_55_legal_doc)

    # # ask all and get all possible response
    # ans = _ask_all(txt, nlpipe)

    # # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    # ll = _clean_ans(ans)

    # # reponse
    # resp = ", ".join([i["answer"] for i in ll])

    # return resp
    return [("--None--", -1)]


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.legal_doc.utils import *

    # from legal_doc_processing.legal_doc.segmentation.clean import clean_doc

    # from legal_doc_processing.legal_doc.segmentation.structure import (
    #     structure_legal_doc,
    # )

    # pipe
    nlpipe = get_pipeline()

    # # clean_legal_doc_list
    # legal_doc_txt_list = load_legal_doc_text_list()
    # clean_legal_doc_list = [clean_doc(i) for i in legal_doc_txt_list]

    # # test one
    # cleaned_legal_doc = clean_legal_doc_list[0]
    # p0_p1 = []
    # _ = [p0_p1.append(i) for i in cleaned_legal_doc[0]]
    # _ = [p0_p1.append(i) for i in cleaned_legal_doc[1]]
    # p0_p1

    # fp_legal_doc = p0_p1
    # fp_55_legal_doc = [i for i in fp_legal_doc if len(i) > 55]

    # # all_ans_dot = _ask_all(".".join(cleaned_legal_doc[0]), nlpipe)
    # all_ans_space = _ask_all(" ".join(fp_55_legal_doc), nlpipe)

    # # all_ans_h2 = _ask_all(cleaned_legal_doc["h2"], nlpipe)
    # # all_ans_article = _ask_all(cleaned_legal_doc["article"], nlpipe)

    # ans = predict_plaintiff(".".join(cleaned_legal_doc[0]), nlpipe)

    # # # test others
    # # ans_list = [predict_plaintiff(p, nlpipe) for p in clean_legal_doc_list]
    # # clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    # # clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
