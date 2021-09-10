"""
Parse provided sentence argument or random sentence with imported functions
"""

import spacy
from argparse import ArgumentParser
from random import choice

from implement_clitics import get_joined_sentence, get_dobj_complement, instantiate_matcher

nlp = spacy.load('pt_core_news_sm')

sample_sentence = choice((open('data/sample_sentences.txt').readlines()))


def get_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Implement direct and/or indirect complement clitics in portuguese sentences",
                            epilog='You can use this sample sentence:' + ' \'' + sample_sentence.strip() + '\'')
    parser.add_argument('-s', '--sentence',
                        type=str,
                        help='Sentence to be analysed. In quotes.')
    parser.add_argument('-s_sent', '--sample_sentence',
                        action='store_true',
                        help='provides a random sentence.')
    parser.add_argument('-dobj', '--direct_object',
                        action='store_true',
                        help='Replace the direct object with a clitic')
    parser.add_argument('-iobj', '--indirect_object',
                        action='store_true',
                        help='Replace the indirect object with a clitic')
    parser.add_argument('-bobj', '--both_objects',
                        action='store_true',
                        help='Convert the dobj and the iobj into clitics.')
    return parser


def main():
    print('\n', '._._._._._._._._._._._._._._._._._._._._', '\n')
    parser = get_argument_parser()
    args = parser.parse_args()

    # if -s_sent
    if args.sample_sentence:
        args.sentence = sample_sentence
        print('original sentence: ', sample_sentence)

        # decide based on the matcher which flag the program should choose
        doc = nlp(sample_sentence)
        matcher = instantiate_matcher(True, True, True)
        matches = matcher(doc)
        # retrieve hash values for matched patterns
        dobj_pattern = nlp.vocab.strings['direct_object']
        iobj_pattern = nlp.vocab.strings['indirect_object']
        both_patterns = nlp.vocab.strings['both_objects']
        matchlist = [match[0] for match in matches]

        if both_patterns in matchlist:
            final_sentence = get_joined_sentence(args.sentence, False, True)
            print('--> both_complements were cliticized: ', get_dobj_complement(final_sentence))

        if dobj_pattern in matchlist:
            print('--> dobj cliticized: ',
                  get_joined_sentence(args.sentence, True, False))

        if iobj_pattern in matchlist:
            print('--> iobj cliticized: ',
                  get_joined_sentence(args.sentence, False, True))

    # if -s 'user sentence'
    else:
        print('\n', 'original sentence:', args.sentence)
        if args.direct_object:
            print('\n', '--> dobj cliticized: ', get_joined_sentence(args.sentence, args.direct_object,
                                                                     args.indirect_object))
        if args.indirect_object:
            print('\n', '--> iobj cliticized: ', get_joined_sentence(args.sentence, args.direct_object,
                                                                     args.indirect_object))
        if args.both_objects:
            final_sentence = get_joined_sentence(args.sentence, False, True)
            print('\n', '--> both complements were cliticized: ', get_dobj_complement(final_sentence), '\n')

    print('\n', '._._._._._._._._._._._._._._._._._._._._', '\n')


if __name__ == '__main__':
    main()
