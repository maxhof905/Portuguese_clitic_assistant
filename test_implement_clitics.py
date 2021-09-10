import pytest
from implement_clitics import instantiate_matcher, get_indexed_complement, get_sentence_parts, get_cliticized_object, \
    get_joined_sentence, get_dobj_complement


@pytest.fixture
def example_dobj():
    return 'O Pedro lê um livro'


@pytest.fixture
def example_iobj():
    return 'O Pedro escreve uma carta à Teresa'


@pytest.fixture
def example_bobj():
    return 'O Pedro escreve-lhe uma carta'


def test_instantiate_matcher():
    assert instantiate_matcher(True, False, False) is not None


def test_get_indexed_complement(example_dobj, example_iobj):
    assert get_indexed_complement(example_dobj, True, False)[1] == 'lê um livro'
    assert type(get_indexed_complement(example_dobj, True, False)) is tuple
    assert get_indexed_complement(example_iobj, False, True)[1] == 'à Teresa'
    assert type(get_indexed_complement(example_iobj, False, True)[1]) is str


def test_get_sentence_parts(example_dobj, example_iobj):
    assert get_sentence_parts(example_dobj, True, False)[0] == 'O Pedro'
    assert len(get_sentence_parts(example_dobj, True, False)[1]) == 0
    assert get_sentence_parts(example_iobj, False, True) == ('O Pedro escreve uma carta', '')
    assert len(get_sentence_parts(example_iobj, False, True)[0]) >= 0


def test_get_cliticized_object(example_dobj, example_iobj):
    assert get_cliticized_object(example_dobj, True, False) == 'lê-o'
    assert '-' in get_cliticized_object(example_dobj, True, False)
    assert get_cliticized_object(example_iobj, False, True) == 'escreve-lhe'
    assert '-' in get_cliticized_object(example_iobj, False, True)
    # r, s, z, m, a, á, ê, u, futur, conditional
    assert get_cliticized_object('O Pedro quer um livro', True, False) == 'qué-lo'
    assert get_cliticized_object('O Pedro faz um bolo', True, False) == 'fá-lo'
    assert get_cliticized_object('O Pedro traz as prenda', True, False) == 'trá-las'
    assert get_cliticized_object('O Pedro tem alguns libro', True, False) == 'tem-nos'
    assert get_cliticized_object('O Pedro corta o bolo', True, False) == 'corta-o'
    assert get_cliticized_object('O Pedro dá o bolo', True, False) == 'dá-o'
    assert get_cliticized_object('O Pedro comprou os livros', True, False) == 'comprou-os'
    assert get_cliticized_object('O Pedro comeria os bolos', True, False) == 'comê-los-ia'
    assert get_cliticized_object('O Pedro esquecerá o livro', True, False) == 'esquecê-lo-á'


def test_get_joined_sentence(example_dobj, example_iobj):
    assert get_joined_sentence(example_dobj, True, False) == 'O Pedro lê-o'
    assert '.' not in get_joined_sentence(example_dobj, True, False)
    assert get_joined_sentence(example_iobj, False, True) == 'O Pedro escreve-lhe uma carta'
    assert len(get_joined_sentence(example_iobj, False, True)) < len(example_iobj)


def test_get_dobj_complement(example_bobj):
    assert get_dobj_complement(example_bobj) == "O Pedro escreve-lha"
    assert get_dobj_complement(example_bobj) is not None
    assert 'lh' in get_dobj_complement(example_bobj)
    assert type(get_dobj_complement(example_bobj)) is str
    assert get_dobj_complement('Os meninos dá-lhe-iam um conselho') == 'Os meninos dá-lho-iam'
