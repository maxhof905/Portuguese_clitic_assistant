"""
Implement clitics in portuguese sentences
"""

import spacy
from spacy.matcher import Matcher
from typing import Tuple, Any, Union

from grammar import get_iobj_sg, get_iobj_pl, get_dobj

nlp = spacy.load('pt_core_news_sm')


def instantiate_matcher(direct_object: bool = False, indirect_object: bool = False, both_objects: bool = False) \
        -> Union[Matcher, Matcher]:
    """
    creates a matcher object with specified parameters
    :param direct_object: flag for replacing direct_object
    :param indirect_object: flag for replacing indirect_object
    :param both_objects: flag for replacing both objects
    :return: spacy matcher object
    """
    matcher = Matcher(nlp.vocab)
    if direct_object:
        patterns = [
            [{'DEP': 'ROOT'}, {'POS': 'DET'}, {'DEP': 'obj', 'POS': 'PROPN'}],
            [{'DEP': 'ROOT'}, {'POS': 'DET'}, {'DEP': 'obj', 'POS': 'NOUN'}]
        ]
        matcher.add("direct_object", patterns)

    if indirect_object:
        pattern = [
            [{'POS': 'ADP', 'DEP': 'case'}, {'POS': 'PROPN'}],
            [{'POS': 'ADP', 'DEP': 'case'}, {'POS': 'NOUN'}]
        ]
        matcher.add("indirect_object", pattern)

    if both_objects:
        patterns = [
            [{'POS': 'VERB'}, {'OP': '+'}, {'POS': 'ADP'}, {'POS': 'PROPN'}],
            [{'POS': 'VERB'}, {'OP': '+'}, {'POS': 'ADP'}, {'POS': 'NOUN'}]
        ]
        matcher.add("both_objects", patterns)
    return matcher


def get_indexed_complement(sentence: str, direct_object: bool, indirect_object: bool) \
        -> Tuple[list, Any]:
    """
    locates the index of the complement in the sentence
    :param sentence: sentence to be analyzed
    :param direct_object: flag for replacing direct_object
    :param indirect_object: flag for replacing direct_object
    :return: start and end index and text of spacy span
    """
    doc = nlp(sentence)
    matcher = instantiate_matcher(direct_object, indirect_object)
    matches = matcher(doc)
    # interrupt further processing of unmatchable sentences
    if len(matches) == 0:
        print(sentence)
        raise TypeError('The object you wanted to replace could not be identified.'
                        'Try again with a less complex sentence or use a sample sentence.'
                        'Don\'t forget to indicate a suitable flag.')
    for match_id, start, end in matches:
        span = doc[start:end]
        return [start, end], span.text


def get_sentence_parts(sentence: str, direct_object: bool, indirect_object: bool) -> Tuple[str, str]:
    """
    retrieves the part to the left of the complement and the remainder of the sentence
    :param sentence: sentence to be analyzed
    :param direct_object: flag for replacing direct_object
    :param indirect_object: flag for replacing direct_object
    :return: sentence start, sentence_end
    """
    index_span, span_text = get_indexed_complement(sentence, direct_object, indirect_object)
    doc = nlp(sentence)
    sentence_list = [token.text for token in doc]
    sentence_start = ' '.join(sentence_list[:index_span[0]])
    sentence_end = ' '.join(sentence_list[index_span[1]:])
    return sentence_start, sentence_end


def get_cliticized_object(sentence: str, direct_object: bool, indirect_object: bool) -> str:
    """
    cliticizes the complement
    :param sentence: sentence to be analyzed
    :param direct_object: flag for replacing direct_object
    :param indirect_object: flag for replacing direct_object
    :return: cliticized complement
    """
    index_span, span_text = get_indexed_complement(sentence, direct_object, indirect_object)
    doc = nlp(span_text)
    complement_phrase = [token.text for token in doc]
    if indirect_object:
        verb = [token.text for token in nlp(sentence) if token.dep_ == 'ROOT']
        # Singular
        if complement_phrase[0] == 'ao':
            return get_iobj_sg(verb[0])
        if complement_phrase[0] == 'à':
            return get_iobj_sg(verb[0])
        # Plural
        if complement_phrase[0] == 'aos':
            return get_iobj_pl(verb[0])
        if complement_phrase[0] == 'às':
            return get_iobj_pl(verb[0])

    if direct_object:
        complement = complement_phrase[1:]
        # Singular
        complement[0] = complement[0].replace('uma', 'a')  # get treated the same; avoid error prone 'or' syntax
        complement[0] = complement[0].replace('um', 'o')
        # Plural
        complement[0] = complement[0].replace('algumas', 'as')
        complement[0] = complement[0].replace('umas', 'as')
        complement[0] = complement[0].replace('alguns', 'os')
        complement[0] = complement[0].replace('uns', 'os')
        # Singular
        if complement[0] == 'o':
            return get_dobj(complement_phrase[0], 'm', 'sg')
        if complement[0] == 'a':
            return get_dobj(complement_phrase[0], 'f', 'sg')
        # Plural
        if complement[0] == 'os':
            return get_dobj(complement_phrase[0], 'm', 'pl')
        if complement[0] == 'as':
            return get_dobj(complement_phrase[0], 'f', 'pl')


def get_joined_sentence(sentence: str, direct_object: bool, indirect_object: bool) -> str:
    """
    joins the sentence start and the cliticized object
    :param sentence: sentence to be analyzed
    :param direct_object: flag for replacing direct_object
    :param indirect_object: flag for replacing direct_object
    :return: sentence
    """
    sentence_start, sentence_end = get_sentence_parts(sentence, direct_object, indirect_object)
    cliticized_complement = get_cliticized_object(sentence, direct_object, indirect_object)
    if direct_object:
        sentence_end = sentence_end.rstrip()
        sentence_end = sentence_end.rstrip('.')
        if len(sentence_end) <= 2:
            joined_sentence = ' '.join((sentence_start, cliticized_complement))
        else:
            joined_sentence = ' '.join((sentence_start, cliticized_complement, sentence_end))
        return joined_sentence

    if indirect_object:
        sentence_list = [token for token in nlp(sentence_start)]
        sentence_tokens = [token.text for token in sentence_list]
        for i, token in enumerate(sentence_list):
            if token.dep_ == 'ROOT':
                sentence_tokens.pop(i)
                sentence_tokens.insert(i, str(cliticized_complement))
                return ' '.join(sentence_tokens)


def get_dobj_complement(final_sentence: str) -> str:  # adding dobj clitic to iobj is easier than the other way around
    """
    aglutinates the remaining dobj to the cliticized iobj
    :param final_sentence: sentence with a cliticized iobj
    :return: sentence where both obj are cliticized
    """
    sentence_list = [token for token in nlp(final_sentence)]
    sentence_tokens = [token.text for token in sentence_list]
    for i, token in enumerate(sentence_list):
        if token.dep_ == 'obj':
            replaced_object = token.text
            sentence_tokens.pop(i)
            sentence_tokens.pop(i - 1)
            reduced_final_sentence = ' '.join(sentence_tokens)
            if reduced_final_sentence[-1:] == 's':
                if replaced_object[-1] == 's':  # lhes + as = lhas
                    combined_final_sentence = ''.join((reduced_final_sentence[:-2], replaced_object[-2], 's'))
                else:  # lhes + a = lha
                    combined_final_sentence = ''.join((reduced_final_sentence[:-2], replaced_object[-1:]))
            else:
                if replaced_object[-1] == 's':  # lhe + as = lhas
                    combined_final_sentence = ''.join((reduced_final_sentence[:-1], replaced_object[-2], 's'))
                else:  # lhe + a = lha
                    combined_final_sentence = ''.join((reduced_final_sentence[:-1], replaced_object[-1:]))
            # mesoclise
            if reduced_final_sentence[-3:] == '-ia':
                if replaced_object[-1] == 's':  # lhes + as = lhas
                    combined_final_sentence = ''.join((reduced_final_sentence[:-4], replaced_object[-2:],
                                                       reduced_final_sentence[-3:]))
                else:
                    combined_final_sentence = ''.join((reduced_final_sentence[:-4], replaced_object[-1],
                                                       reduced_final_sentence[-3:]))
            if reduced_final_sentence[-4:] == '-iam':
                if replaced_object[-1] == 's':  # lhes + as = lhas
                    combined_final_sentence = ''.join((reduced_final_sentence[:-5], replaced_object[-2:],
                                                       reduced_final_sentence[-4:]))
                else:
                    combined_final_sentence = ''.join((reduced_final_sentence[:-5], replaced_object[-1],
                                                       reduced_final_sentence[-4:]))
            if reduced_final_sentence[-2:] == '-á':
                if replaced_object[-1] == 's':  # lhes + as = lhas
                    combined_final_sentence = ''.join((reduced_final_sentence[:-3], replaced_object[-2:],
                                                       reduced_final_sentence[-2:]))
                else:
                    combined_final_sentence = ''.join((reduced_final_sentence[:-3], replaced_object[-1],
                                                       reduced_final_sentence[-2:]))
            if reduced_final_sentence[-3:] == '-ão':
                if replaced_object[-1] == 's':  # lhes + as = lhas
                    combined_final_sentence = ''.join((reduced_final_sentence[:-3], replaced_object[-2:],
                                                       reduced_final_sentence[-2:]))
                else:
                    combined_final_sentence = ''.join((reduced_final_sentence[:-4], replaced_object[-1],
                                                       reduced_final_sentence[-3:]))
            return combined_final_sentence
