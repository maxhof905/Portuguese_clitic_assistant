"""
Grammar rules for replacing iobj and dobj
"""


def get_iobj_sg(verb) -> str:
    """ masc and fem singular iobj"""
    # mesoclitic futur 3PSG
    if verb[-1] == 'á':
        if len(verb) > 2:
            return '-'.join((verb[:-1], 'lhe', 'á'))

    # mesoclitic futur 3PPL
    if verb[-2:] == 'ão':
        if len(verb) > 3:
            return '-'.join((verb[:-2], 'lhe', 'ão'))

    # mesoclitic conditional 3PSG
    if verb == 'diria':  # exceptional verb form
        return '-'.join(('dizer', 'lhe', 'ia'))
    if verb[-2:] == 'ia':
        return '-'.join((verb[:-2], 'lhe', 'ia'))

    # mesoclitic conditional 3PPL
    if verb == 'diriam':  # exceptional verb form
        return '-'.join(('dizer', 'lhe', 'iam'))
    if verb[-3:] == 'iam':
        if len(verb) > 3:
            return '-'.join((verb[:-3], 'lhe', 'iam'))
    else:  # other tenses
        connector = '-'
        return f'{verb}{connector}lhe'


def get_iobj_pl(verb) -> str:
    """ masc and fem plural iobj"""
    # mesoclitic futur 3PSG
    if verb[-1] == 'á':
        if len(verb) > 2:
            return '-'.join((verb[:-1], 'lhes', 'á'))

    # mesoclitic futur 3PPL
    if verb[-2:] == 'ão':
        if len(verb) > 3:
            return '-'.join((verb[:-2], 'lhes', 'ão'))

    # mesoclitic conditional 3PSG
    if verb == 'diria':  # exceptional verb form
        return '-'.join(('dizer', 'lhes', 'ia'))
    if verb[-2:] == 'ia':
        return '-'.join((verb[:-2], 'lhes', 'ia'))

    # mesoclitic conditional 3PPL
    if verb == 'diriam':  # exceptional verb form
        return '-'.join(('dizer', 'lhes', 'iam'))
    if verb[-3:] == 'iam':
        if len(verb) > 3:
            return '-'.join((verb[:-3], 'lhes', 'iam'))
    else:  # other tenses
        connector = '-'
        return f'{verb}{connector}lhes'


def get_dobj(verb, genus, numerus) -> str:
    """ masc and fem singular and plural dobj"""
    if genus == 'm':
        if numerus == 'sg':
            bare_clitic = 'o'
            clitic = 'lo'
            nasal_clitic = 'no'
        if numerus == 'pl':
            bare_clitic = 'os'
            clitic = 'los'
            nasal_clitic = 'nos'
    if genus == 'f':
        if numerus == 'sg':
            bare_clitic = 'a'
            clitic = 'la'
            nasal_clitic = 'na'
        if numerus == 'pl':
            bare_clitic = 'as'
            clitic = 'las'
            nasal_clitic = 'nas'

    if verb[-1] == 'm':
        if verb[-4:] != 'riam':  # distinguish from 3PPL conditional form
            return '-'.join((verb, nasal_clitic))
    if verb[-1] == 's':
        return '-'.join((verb[:-1], clitic))
    if verb[-1] == 'z':
        if verb[-2] == 'a':
            return '-'.join((verb[:-2] + 'á', clitic))
        if verb[-2] == 'e':
            return '-'.join((verb[:-2] + 'ê', clitic))
        if verb[-2] == 'i':
            return '-'.join((verb[:-1], clitic))
    if verb[-1] == 'a':
        if verb[-3:] != 'ria':
            return '-'.join((verb, bare_clitic))
    if verb[-1] == 'e':
        return '-'.join((verb, bare_clitic))
    if verb[-1] == 'ê':
        return '-'.join((verb, bare_clitic))
    if verb[-1] == 'u':
        return '-'.join((verb, bare_clitic))
    if verb[-1] == 'r':
        return '-'.join((verb[:-2] + 'é', clitic))

    # mesoclitic futur 3PSG
    if verb[-1] == 'á':
        if len(verb) > 2:  # exclude monosyllabic verbs that are accentuated
            if verb[-3] == 'a':
                stem = ''.join((verb[:-3], 'á'))
                return '-'.join((stem, clitic, 'á'))
            if verb[-3] == 'e':
                stem = ''.join((verb[:-3], 'ê'))
                return '-'.join((stem, clitic, 'á'))
            if verb[-3] == 'i':
                stem = ''.join((verb[:-3], 'i'))
                return '-'.join((stem, clitic, 'á'))
        else:
            return '-'.join((verb, bare_clitic))

    # mesoclitic futur 3PPL
    if verb[-2:] == 'ão':
        if len(verb) > 3:  # exclude monosyllabic present 3PPL forms
            if verb[-4] == 'a':
                stem = ''.join((verb[:-4], 'á'))
                return '-'.join((stem, clitic, 'ão'))
            if verb[-4] == 'e':
                stem = ''.join((verb[:-4], 'ê'))
                return '-'.join((stem, clitic, 'ão'))
            if verb[-4] == 'i':
                stem = ''.join((verb[:-4], 'i'))
                return '-'.join((stem, clitic, 'ão'))
        else:
            return '-'.join((verb, bare_clitic))

    # mesoclitic conditional 3PSG
    if verb[-3:] == 'ria':
        if verb[-4] == 'a':
            stem = ''.join((verb[:-4], 'á'))
            return '-'.join((stem, clitic, 'ia'))
        if verb[-4] == 'e':
            stem = ''.join((verb[:-4], 'ê'))
            return '-'.join((stem, clitic, 'ia'))
        if verb[-4] == 'i':
            stem = ''.join((verb[:-4], 'i'))
            return '-'.join((stem, clitic, 'ia'))

    # mesoclitic conditional 3PPL
    if verb[-4:] == 'riam':
        if verb[-5] == 'a':
            stem = ''.join((verb[:-5], 'á'))
            return '-'.join((stem, clitic, 'iam'))
        if verb[-5] == 'e':
            stem = ''.join((verb[:-5], 'ê'))
            return '-'.join((stem, clitic, 'iam'))
        if verb[-5] == 'i':
            stem = ''.join((verb[:-5], 'i'))
            return '-'.join((stem, clitic, 'iam'))
