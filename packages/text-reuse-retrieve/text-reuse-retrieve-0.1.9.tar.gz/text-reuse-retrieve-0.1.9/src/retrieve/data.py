
import itertools
import uuid
import functools
import operator
import collections
from typing import Any, List, Dict, Tuple
import string
import re
import logging
from dataclasses import dataclass

import numpy as np

from retrieve import utils
from retrieve.methods import (jaccard, containment, containment_min,
                              weighted_containment, weighted_jaccard, cosine)
from retrieve.methods import local_alignment, get_horizontal_alignment

logger = logging.getLogger(__name__)


@dataclass(eq=True, frozen=True)
class Ref:
    """
    Dataclass to store reference information. It's hashable and allows
    to incorporate metadata in the `meta` field as a tuple
    """
    source: Tuple[Any]
    target: Tuple[Any]
    meta: tuple = ()


def printable_doc_id(doc_id, levels=('-', ':', '+')):
    def _printable_doc_id(doc_id, level):
        if isinstance(doc_id, (list, tuple)):
            for it in doc_id:
                yield from _printable_doc_id(it, level + 1)
        else:
            yield level, str(doc_id)

    last, output, groups = None, None, list(_printable_doc_id(doc_id, -1))
    for level, group in itertools.groupby(groups, key=lambda tup: tup[0]):
        group = levels[level].join(it for _, it in group)
        if output is None:
            output = group
        else:
            output = levels[min(level, last)].join([output, group])
        last = level
    return output


class Doc:
    """
    Convenience class representing a document.

    Keeps any morphological tags passed to the constructor in memory
    as well as doc ids and refs

    Arguments
    =========
    fields : dict containing input
        must include a "token" field with the tokenized text
        currently it also assumes a "lemma" field
        "pos" can be used for further preprocessing
    doc_id : any document identifier
    ref : Ref
    """
    def __init__(self,
                 fields: Dict[str, List[any]],
                 doc_id: Any,
                 ignore_fields=set(['_'])):

        if isinstance(doc_id, int):
            raise ValueError("Can't use `doc_id` of type integer")
        if 'token' not in fields:
            raise ValueError("`fields` requires 'token' data")

        self.doc_id = doc_id
        self.fields = {f: data for f, data in fields.items() if f not in ignore_fields}
        # check lengths
        self._check_fields(self.fields)
        # data
        self._features = None
        self._preprocessed_features = None

    @staticmethod
    def _check_fields(fields):
        length = None
        for field, data in fields.items():
            if length is None:
                length = len(data)
            else:
                if len(data) != length:
                    raise ValueError("Expected {} of {} but got {}".format(
                        length, field, len(data)))

    @property
    def text(self):
        return ' '.join(self.get_features(field='token'))

    def get_printable_doc_id(self):
        return printable_doc_id(self.doc_id)

    def to_counter(self, field=None):
        return collections.Counter(self.get_features(field=field))

    def __repr__(self):
        return '<Doc doc_id={} text="{}"/>'.format(
            str(self.doc_id), self.text[:30] + "...")

    @property
    def feature_density(self):
        if self._preprocessed_features == 0:
            return 0
        return len(self.get_features()) / self._preprocessed_features

    def set_features(self, features):
        self._features = features
        self._preprocessed_features = len(features)

    def get_features(self, field=None):
        if not field:
            if self._features is None:
                raise ValueError("Unprocessed doc: [{}]".format(str(self.doc_id)))
            text = self._features
        else:
            text = self.fields[field]

        return text

    def print_alignment(self, doc, **kwargs):
        a1 = a2 = None
        if 'lemma' in self.fields and 'lemma' in doc.fields:
            a1, a2, _ = local_alignment(self.get_features('lemma'), doc.get_features('lemma'), **kwargs)
        s1, al, s2 = get_horizontal_alignment(
            self.get_features('token'), doc.get_features('token'), a1=a1, a2=a2, **kwargs)
        print(s1 + '\n' + al + '\n' + s2)


def _wrap_fn(fn, use_counter=False):
    def wrapped(this, that, field='lemma', **kwargs):
        if use_counter:
            return fn(this.to_counter(field), that.to_counter(field), **kwargs)
        else:
            return fn(this.get_features(field), that.get_features(field), **kwargs)
    return wrapped


setattr(Doc, 'jaccard', _wrap_fn(jaccard, use_counter=True))
setattr(Doc, 'weighted_jaccard', _wrap_fn(weighted_jaccard, use_counter=True))
setattr(Doc, 'containment', _wrap_fn(containment, use_counter=True))
setattr(Doc, 'containment_min', _wrap_fn(containment_min, use_counter=True))
setattr(Doc, 'weighted_containment', _wrap_fn(weighted_containment, use_counter=True))
setattr(Doc, 'cosine', _wrap_fn(cosine, use_counter=True))
setattr(Doc, 'local_alignment', _wrap_fn(local_alignment))
setattr(Doc, 'get_horizontal_alignment', _wrap_fn(get_horizontal_alignment))


class Collection:
    """
    Class representing a collection of docs

    Arguments
    =========
    docs : list of Doc
    """
    def __init__(self, docs, name=None):
        self._docs = docs
        self._doc_ids = {doc.doc_id: idx for idx, doc in enumerate(docs)}
        # identifier for collection
        self.name = name or str(uuid.uuid4())[:8]
        # processing metadata
        self.preprocesing_summary = None
        self.fsel_summary = None

    def __getitem__(self, idx):
        if isinstance(idx, np.integer):
            idx = int(idx)

        if isinstance(idx, int):
            # access by index
            return self._docs[idx]
        # access by key
        return self._docs[self._doc_ids[idx]]

    def __len__(self):
        return len(self._docs)

    def __contains__(self, doc_id):
        return doc_id in self._doc_ids

    def __iter__(self):
        yield from self.get_docs()

    def get_doc_idx(self, doc_id):
        # access by doc id
        return self._doc_ids[doc_id]

    def get_docs(self, index=None):
        """
        Generator over docs

        Arguments
        =========
        index : list or set or dict of document indices to get (optional)
        """
        # TODO: index should probably be based on doc ids
        if index is not None:
            index = set(index)
        for idx, doc in enumerate(self._docs):
            if index is not None and idx not in index:
                continue
            yield doc

    def get_nonempty_features(self, **kwargs):
        """
        Avoid getting empty bags of features. Documents might
        be empty after preprocessing or feature selection.

        Output
        ======
        Tuple of (features, index):
            features, list of document features
            index, list of indices mapping the document idx in the original collection
        """
        output, index = [], []
        for idx, feats in enumerate(self.get_features(**kwargs)):
            # handle empty documents
            if feats:
                output.append(feats)
                index.append(idx)

        return output, index

    def get_features(self, cast=None, min_features=0, min_feature_density=0, **kwargs):
        """
        Get preprocessed text.

        Arguments
        =========
        cast : func (optonal), document features are casted with `cast` if passed

        Output
        ======
        list of lists with features
        """
        output = []
        for doc in self.get_docs():
            # get features
            feats = doc.get_features(**kwargs)

            # empty input if number of features falls below threshold
            if (min_features > 0 and len(feats) < min_features) or \
               (min_feature_density > 0 and doc.feature_density > min_feature_density):
                feats = []

            if cast is not None:
                feats = cast(feats)

            output.append(feats)
        return output

    def get_field_vocab(self, field):
        """
        Get vocabulary of a given input field (ignores preprocessing)
        """
        return collections.Counter(
            w for doc in self.get_docs() for w in doc.fields[field])

    @classmethod
    def from_file(cls, *paths, 
                  # shingling
                  do_shingling=False, shingle_overlap=10, shingle_window=20):

        docs = []
        for path in paths:
            lines = []
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    lines.append(line.split())
            if do_shingling:
                for doc in shingle_docs(
                        {'token': [tok for l in lines for tok in l]}, path,
                        overlap=shingle_overlap, window=shingle_window):
                    docs.append(doc)
            else:
                d_id = 0
                for line in lines:
                    docs.append(Doc({'token': line}, doc_id=(path, d_id)))
                    d_id += 1

        return cls(docs)

    @classmethod
    def from_csv(cls, *paths, drop_diacritics=None, 
                 fields=('token', 'lemma', 'pos'), sep='\t', read_header=False,
                 ignore_empty_lines=False, 
                 # shingling
                 do_shingling=False, shingle_overlap=10, shingle_window=20):
        """
        Arguments
        =========

        Create collection from space-separated csv like file

        Sic sic PROPN
        itur itur PROPN
        ad ad PROPN
        astra astra PROPN
        . . PUNCT

        En en ADP
        una uno DET
        mañana mañana NOUN
        de de ADP
        Diciembre diciembre NOUN

        using sentence numbers as doc ids
        """
        docs = []
        for path in paths:
            d_id = 0
            for doc in read_csv(path,
                    fields=fields, sep=sep, read_header=read_header, 
                    ignore_empty_lines=ignore_empty_lines):
                if do_shingling:
                    for shingle in shingle_docs(
                            doc, path, overlap=shingle_overlap, window=shingle_window):
                        docs.append(shingle)
                else:
                    docs.append(Doc(doc, doc_id=(path, d_id)))
                    d_id += 1

        return cls(docs)


class TextPreprocessor:
    """
    Preprocess docs based on doc metadata
    """

    PUNCT = r"[{}]+".format(string.punctuation)

    def __init__(self,
                 field='lemma',
                 lower=True,
                 field_regexes={},
                 drop_punctuation=True, punct_field='token',
                 replace_unk=False, drop_unk=False, unk_token='$unk$', unk_field='token',
                 stopwords=None, stop_field='lemma'):
        """
        field : str, what field to use to extract features
        lower : bool, whether to lowercase input text
        field_regexes : dict (field : regex), a dict mapping fields to regexes that tokens
            should match in order to not be filtered out
        drop_punctuation : bool, whether to drop punctuation
        punct_field : str, field that should be used to check for punctuation
        replace_unk : bool, whether to replace unknown lemmas with the corresponding token
            from the field specified by `unk_field`
        drop_unk : bool, whether to remove tokens with unknown lemmas
        unk_token : str, token used to represent unknown lemmas in the lemma field
        unk_field : str, field to use for the replacement of the unknown lemma 
            if `replace_unk` is True.
        stopwords : retrieve.utils.Stopwords, stopwords to filter out
        stop_field : str, field to be used for checking stopwords
        """
        self.field = field
        self.lower = lower
        # punctuation
        self.drop_punctuation = drop_punctuation
        self.punct_field = punct_field
        # unks
        self.replace_unk = replace_unk
        self.drop_unk = drop_unk
        self.unk_token = unk_token
        self.unk_field = unk_field
        # stopwords
        self.stopwords = stopwords
        self.stop_field = stop_field
        # regexes
        self.field_regexes = field_regexes

    def get_summary(self):
        return dict({
            'field': self.field,
            'lower': self.lower,
            # punctuation
            'drop_punctuation': self.drop_punctuation,
            'punct_field': self.punct_field,
            # unks
            'replace_unk': self.replace_unk,
            'drop_unk': self.drop_unk,
            'unk_token': self.unk_token,
            'unk_field': self.unk_field,
            # stopwords
            'stopwords': self.stopwords.get_summary() if self.stopwords else None,
            'stop_field': self.stop_field,
            # regexes
            'field_regexes': self.field_regexes
        })

    def process_generator(self, doc):
        for i in range(len(doc.fields['token'])):
            target = doc.fields[self.field][i]

            if self.drop_punctuation and re.fullmatch(
                    TextPreprocessor.PUNCT, doc.fields[self.punct_field][i]):
                logger.debug("Dropping punctuation: {}".format(
                    doc.fields[self.punct_field][i]))
                continue

            if self.stopwords is not None:
                if doc.fields[self.stop_field][i].lower() in self.stopwords:
                    logger.debug("Dropping stopword: {}".format(
                        doc.fields[self.stop_field][i]))
                    continue

            reg_match = True
            for re_field, regex in self.field_regexes.items():
                if not re.match(regex, doc.fields[re_field][i]):
                    reg_match = False
                    break
            if not reg_match:
                logger.debug("Dropping regex {}: {}".format(
                    re_field, doc.fields[re_field][i]))
                continue

            if (self.replace_unk or self.drop_unk):
                if 'lemma' in doc.fields and doc.fields['lemma'][i] == self.unk_token:
                    if self.replace_unk:
                        target = doc.fields[self.unk_field][i]
                    elif self.drop_unk:
                        logger.debug("Dropping unknown")
                        continue

            if self.lower:
                target = target.lower()

            yield target

    def process(self, doc, ngram_extractor=None):
        """
        Process input text creating n-grams on the processed output.
        """
        processed = self.process_generator(doc)
        if ngram_extractor is not None:
            yield from ngram_extractor.get_ngrams_generator(list(processed))
        else:
            yield from processed

    def process_collections(self, *colls, post_fn=None, **kwargs):
        """
        Process entire collections

        post_fn : function that takes generator of ngrams and produces a new generator
        kwargs : Ngrams additional arguments
        """
        ngram_extractor = utils.Ngrams(**kwargs)
        summary = self.get_summary()
        summary['ngrams'] = ngram_extractor.get_summary()
        for coll in colls:
            coll.preprocesing_summary = summary
            for doc in coll.get_docs():
                features = self.process(doc, ngram_extractor=ngram_extractor)
                if post_fn is not None:
                    features = post_fn(features)
                doc.set_features(list(features))


class MetaCriterion(type):
    @property
    def DF(cls):
        return cls("DF")

    @property
    def FREQ(cls):
        return cls("FREQ")

    @property
    def IDF(cls):
        return cls("IDF")


class Criterion(object, metaclass=MetaCriterion):
    def __init__(self, field):
        self.field = field
        self.ops = []
        self.fields_, self.ops_ = [], []

    def _get_index(self, stats, val, operator):
        if val < 1 or (val == 1 and isinstance(val, float)):
            # convert stats to normalized ranks
            # assumes stats has already been argsorted
            stats = np.linspace(0, 1, len(stats))[stats.argsort().argsort()]

        index, = np.where(operator(stats, val))
        return index

    def get_fields_and_ops(self):
        # concat current field to extra fields
        fields = [self.field] + self.fields_
        ops = [self.ops] + self.ops_
        return fields, ops

    def apply(self, f_sel):
        if not self.ops:
            raise ValueError("Criterion not set until comparison")

        fields, ops = self.get_fields_and_ops()
        stats = {f: f_sel._get_stats(f) for f in set(fields)}

        index = []
        for field, ops in zip(fields, ops):
            for val, op in ops:
                index.append(self._get_index(stats[field], val, op))

        if len(index) == 1:
            index = index[0]
        else:
            index = functools.reduce(np.intersect1d, index)

        return index

    def __and__(self, other):
        if not self.ops or not other.ops:
            raise ValueError("Criterion not set until comparison")

        self.fields_ += [other.field]
        self.ops_ += [other.ops]
        return self

    def __le__(self, val):
        self.ops.append((val, operator.le))
        return self

    def __lt__(self, val):
        self.ops.append((val, operator.lt))
        return self

    def __ge__(self, val):
        self.ops.append((val, operator.ge))
        return self

    def __gt__(self, val):
        self.ops.append((val, operator.gt))
        return self

    def __eq__(self, val):
        self.ops.append((val, operator.eq))
        return self


class FeatureSelector:
    def __init__(self, *colls):
        self.fitted = False
        self.features = {}
        self.freqs = []
        self.dfs = []
        self.ndocs = 0
        self.register(*colls)

    def register_text(self, text):
        for ft, cnt in collections.Counter(text).items():
            idx = self.features.get(ft, len(self.features))
            if ft not in self.features:
                self.features[ft] = idx
                self.freqs.append(cnt)
                self.dfs.append(1)
            else:
                self.freqs[idx] += cnt
                self.dfs[idx] += 1
        self.ndocs += 1

    def register(self, *colls):
        for coll in colls:
            for feats in coll.get_features():
                self.register_text(feats)
        self._fit()

        return self

    def _fit(self):
        assert len(self.features) == len(self.freqs) == len(self.dfs)
        self.freqs, self.dfs = np.array(self.freqs), np.array(self.dfs)
        self.fitted = True

    def _get_stats(self, field):
        if not self.fitted:
            raise ValueError("Selector isn't fitted")

        if field == "FREQ":
            return self.freqs
        elif field == "DF":
            return self.dfs
        elif field == "IDF":
            return np.log(np.sum(self.freqs) / self.dfs)
        else:
            raise ValueError("Requested unknown stats")

    def get_vocab(self, criterion=None, return_summary=False):
        if not self.fitted:
            raise ValueError("Selector isn't fitted")

        id2ft = {idx: ft for ft, idx in self.features.items()}

        if criterion is None:
            vocab = {id2ft[idx]: self.freqs[idx] for idx in id2ft}

        else:
            index = criterion.apply(self)
            index = sorted(index, key=self.freqs.__getitem__, reverse=True)
            vocab = {id2ft[idx]: self.freqs[idx] for idx in index}

        if return_summary:
            return vocab, criterion.get_fields_and_ops() if criterion else None

        return vocab

    def filter_collections(self, *colls, criterion=None):
        vocab, summary = self.get_vocab(criterion, return_summary=True)
        for coll in colls:
            coll.fsel_summary = summary
            for doc in coll.get_docs():
                doc.set_features(list(filter(vocab.get, doc.get_features())))

        return vocab

    def filter_texts(self, texts, criterion):
        vocab = self.get_vocab(criterion)
        for text in texts:
            yield [ft for ft in text if ft in vocab]


def read_csv(path, drop_diacritics=None,
             fields=('token', 'pos', '_', 'lemma'), sep='\t', 
             read_header=False, ignore_empty_lines=False):
    """
    Read sentences from csv file. Assumes that empty lines correspond to sentence
    boundaries. This functionality can be turned off with `ignore_empty_lines`.
    The function `shingle_docs` can be used to segment a dataset read
    with this function if no sentence segmentation is present in the csv file.

    Arguments
    =========

    path : str, path to file
    drop_diacritics : iterable or None (optional), fields of the csv file for which
        diacritics should be ignored.
    fields : tuple (optional), field names corresponding to the columns in the csv.
        Ignored if `read_header` is True.
    sep : str, separator
    read_header : bool, whether to use the header to read the fields
    """
    output = []
    c_id = 0

    with open(path) as f:
        if read_header:
            fields = next(f).strip().split(sep)
        if 'token' not in fields:
            raise ValueError("At least field `token` must be available")
        if drop_diacritics is not None:
            if isinstance(drop_diacritics, str):
                drop_diacritics = [drop_diacritics]
            drop_diacritics = set(drop_diacritics)

        sent = collections.defaultdict(list)
        for line in f:
            line = line.strip()
            if not line:
                if ignore_empty_lines:
                    continue
                elif sent:
                    output.append(dict(sent))
                    sent = collections.defaultdict(list)
                    continue
                else:
                    # unexpected empty line at the beginning
                    continue

            data = line.split(sep)
            if len(data) != len(fields):
                raise ValueError(
                    "Expected {} metadata fields, but got {}. File: {}"
                    .format(len(fields), len(data), path))

            for key, val in zip(fields, data):
                if key == '_':
                    continue
                if drop_diacritics is not None and key in drop_diacritics:
                    val = utils.drop_string_diacritics(val)
                sent[key].append(val)

    return output


def shingle_docs(doc, f_id, overlap=10, window=20):
    """
    Produce shingles from a given input dictionary with fields.

    Arguments
    =========
    doc : Doc, instance of a (possibly very long) document
    f_id : str, identifier for the input file, for example, the input file path
    overlap : int, the overlap in tokens over consecutive documents
    window : int, the size of the shingled documents
    """

    output = []
    n_words = len(doc[next(iter(doc.keys()))])
    for start in range(0, n_words, window - overlap):
        # doc might be smaller than window
        stop = min(start + window, n_words)
        assert start < stop, (start, stop, f_id)
        # doc id
        doc_id = f_id, (start, stop)
        # prepare doc
        fields = {key: vals[start:stop] for key, vals in doc.items()}
        fields['ids'] = list(range(start, stop))

        output.append(Doc(fields=fields, doc_id=doc_id))

    return output