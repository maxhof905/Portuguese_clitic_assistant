from grammar import get_iobj_sg, get_iobj_pl, get_dobj


def test_get_iobj_sg():
    assert get_iobj_sg('traz') == 'traz-lhe'
    assert '-' in get_iobj_sg('leva')
    assert get_iobj_sg('falará') == 'falar-lhe-á'
    assert get_iobj_sg('dá') == 'dá-lhe'
    assert get_iobj_sg('deixarão') == 'deixar-lhe-ão'
    assert get_iobj_sg('dão') == 'dão-lhe'
    assert get_iobj_sg('levaria') == 'levar-lhe-ia'
    assert get_iobj_sg('diriam') == 'dizer-lhe-iam'
    assert get_iobj_sg('diria') == 'dizer-lhe-ia'


def test_get_iobj_pl():
    assert get_iobj_pl('traz') == 'traz-lhes'
    assert '-' in get_iobj_pl('leva')
    assert get_iobj_pl('falará') == 'falar-lhes-á'
    assert get_iobj_pl('dá') == 'dá-lhes'
    assert get_iobj_pl('deixarão') == 'deixar-lhes-ão'
    assert get_iobj_pl('dão') == 'dão-lhes'
    assert get_iobj_pl('levaria') == 'levar-lhes-ia'
    assert get_iobj_pl('diriam') == 'dizer-lhes-iam'
    assert get_iobj_pl('diria') == 'dizer-lhes-ia'


def test_get_dobj():
    assert get_dobj('tem', 'f', 'sg') == 'tem-na'
    assert '-' in get_dobj('quis', 'm', 'pl')
    assert get_dobj('quis', 'm', 'pl') == 'qui-los'
    assert get_dobj('faz', 'f', 'pl') == 'fá-las'
    assert get_dobj('fez', 'm', 'pl') == 'fê-los'
    assert get_dobj('diz', 'm', 'sg') == 'di-lo'
    assert get_dobj('deixa', 'f', 'sg') == 'deixa-a'
    assert get_dobj('escreve', 'f', 'pl') == 'escreve-as'
    assert get_dobj('lê', 'm', 'sg') == 'lê-o'
    assert get_dobj('comprou', 'm', 'pl') == 'comprou-os'
    assert get_dobj('quer', 'f', 'sg') == 'qué-la'
    assert get_dobj('dá', 'f', 'pl') == 'dá-as'
    assert get_dobj('cortará', 'm', 'sg') == 'cortá-lo-á'
    assert get_dobj('escreverá', 'm', 'pl') == 'escrevê-los-á'
    assert get_dobj('dirá', 'f', 'sg') == 'di-la-á'
    assert get_dobj('dão', 'f', 'pl') == 'dão-as'
    assert get_dobj('cortarão', 'm', 'sg') == 'cortá-lo-ão'
    assert get_dobj('escreverão', 'm', 'pl') == 'escrevê-los-ão'
    assert get_dobj('dirão', 'f', 'sg') == 'di-la-ão'
    assert get_dobj('cortaria', 'm', 'sg') == 'cortá-lo-ia'
    assert get_dobj('escreveria', 'm', 'pl') == 'escrevê-los-ia'
    assert get_dobj('diria', 'f', 'sg') == 'di-la-ia'
    assert get_dobj('cortariam', 'm', 'sg') == 'cortá-lo-iam'
    assert get_dobj('escreveriam', 'm', 'pl') == 'escrevê-los-iam'
    assert get_dobj('diriam', 'f', 'sg') == 'di-la-iam'
