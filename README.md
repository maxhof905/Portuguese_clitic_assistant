
maxhof905

2021/09/10


# Implementing direct and indirect object clitics in European Portuguese

The aim of the program is to help language speakers and learners to implement the correct clitic form in a sentence that
either only contains a direct or an indirect complement or both at the same time.

## Usage:
Type "pyhton3 main.py -h" for getting and overview over the available flags.

The user has the option to:
a) provide a sentence in Portuguese (after the flag -s / --sentence, in quotation marks, with or without final point)
and to choose the complement that should be replaced by indicating a second flag
b) use the flag -s_sent without having to indicate further parameters

When following option a) the following flags can be choosen:
1) --direct_object (-dobj) for replacing a direct complement in the sentence.
example:    python3 main.py -s 'A Maria lê a carta à Teresa' -dobj
            '--> dobj cliticized: A Maria lê-a à Teresa'
2) --indirect_object (-iobj) for replacing an indirect complement in the sentence.
example:    python3 main.py -s 'A Maria lê a carta à Teresa' -iobj
            '--> iobj cliticized: A Maria lê-lhe a carta'
3) --both_objects (-bobj) for replacing the direct and indirect complement in the sentence.
example:    python3 main.py -s 'A Maria lê a carta à Teresa' -bobj
            '--> bobj cliticized: A Maria lê-lha'

When choosing option b) the program will replace the argparser argument --sentence (-s) with a sample sentence choosen from
sample_sentences.txt. It then applies a spacy matcher to the random sentence in order to choose the correct flags.
If there is more than one complement in the sentence, the program will provide the output for all three flags. This
functionality is useful when users do either not speak portuguese or want to learn how clitics are replaced.

If the user provides a sentence that is syntactically to complex for the program, an error will be raised. The user is
 asked to provide a less complex sentence or to switch to the flag -s_sent.

## Grammatical restrictions:
The Program works for verbs in the 3 person singular and 3 person plural in indicative present, past and future and also
in conditional (no composed verb forms, no modal verbs followed by infinitive.) Other grammatical persons will accidentally
also work due to similar verb endings but are not systematically implemented. The direct and indirect objects can be in
singular and plural and masculine and feminine. For the program to work correctly only affirmative main clauses should be
introduced. Conjunctions, subordinates and negation cannot be parsed correctly. (In portuguese, a negation prior to the
verb requires the anteposition of the clitic.)

## Background:
The aim of the program is to help language speakers and learners implement the correct clitic form in a sentence that
either only contains a direct or an indirect complement or both at the same time. The problem with Portuguese clitics
is that they are heavily influenced by phonotactic rules, which means that, depending on the syllable structure and the
final consonant of the preceding verb, the clitic changes. Other Romance Languages also present allomorphs in their
clitic system but none seem to have as much variation as Portuguese.

Another factor that makes the implementation of clitics in Portuguese difficult is that Vulgar Latin (the linguistic
predecessor of modern Romance Languages) future and conditional forms are preserved. In Vulgar Latin the notion of future
and conditional were expressed as 'FACERE HABEO'/ 'FACERE HABEBAM' (1PSG) evolving via 'fazer hei'/ fazer (hav)ia
to 'farei'/ 'faria'. This evolution was similar in other romance languages but Portuguese nowadays still opts for
mesoclise when it comes to implementing clitic forms in the future tense, which does not occur anymore in any other
romance language.

> example: python3 main.py -s 'Farei uma celebração' -dobj
         
> '--> dobj cliticized: Fá-la-ei' (< FACERE ILLAM HABEO)

## Data:
For the flag -s_sent the program reads the lines in sample_sentences.txt. This is a file that contains sentences
that are built with 20 distinct verbs that are among the 40 most common verbs in European Portuguese (according to:
https://www.corpusdoportugues.org/web-dial/). There are sentences that contain only an indirect, only a direct or both
types of complement in the file. Modal verbs were excluded from this list.




