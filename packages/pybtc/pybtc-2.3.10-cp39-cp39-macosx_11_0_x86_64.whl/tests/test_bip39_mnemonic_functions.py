import pytest

from pybtc.functions.entropy import generate_entropy
from pybtc.functions.entropy import igam
from pybtc.functions.entropy import igamc
from pybtc.functions.bip39_mnemonic import load_word_list
from pybtc.functions.bip39_mnemonic import entropy_to_mnemonic
from pybtc.functions.bip39_mnemonic import mnemonic_to_entropy
from pybtc.functions.bip39_mnemonic import mnemonic_to_seed
from pybtc.functions.bip39_mnemonic import is_mnemonic_checksum_valid
from pybtc.functions.bip39_mnemonic import split_mnemonic
from pybtc.functions.bip39_mnemonic import combine_mnemonic
from pybtc.functions.bip39_mnemonic import create_mnemonic_additional_share

def test_generate_entropy():
    assert len(generate_entropy()) == 64
    assert len(generate_entropy(strength=256)) == 64
    assert len(generate_entropy(strength=128)) == 32
    assert len(generate_entropy(strength=160)) == 40
    assert len(generate_entropy(strength=192)) == 48
    assert len(generate_entropy(strength=224)) == 56
    with pytest.raises(ValueError):
        generate_entropy(strength=40)

def test_gam_funtions():
    q = 0.0000000000001
    assert igam(0.56133437, 7.79533309) - 0.99989958147838275959 < q
    assert igam(3.80398274, 0.77658461) - 0.01162079725209424867 < q
    assert igam(6.71146614, 0.39790492) - 0.00000051486912406477 < q
    assert igam(5.05505886, 6.08602125) - 0.71809645160316382118 < q
    assert igam(9.45603411, 4.60043366) - 0.03112942473115925396 < q
    assert igamc(3.08284045, 0.79469709) - 0.95896191705843125686 < q
    assert igamc(7.91061495, 9.30889249) - 0.27834295370900602462 < q
    assert igamc(4.89616780, 5.75314859) - 0.30291667399717547848 < q
    assert igamc(8.11261940, 4.05857957) - 0.95010562492501993148 < q
    assert igamc(1.34835811, 6.64708856) - 0.00295250273836756942 < q


def test_load_word_list():
    assert len(load_word_list()) == 2048
    with pytest.raises(ValueError):
        load_word_list(word_list_dir="notexist")

def test_entropy__mnemonic():
    m = 'young crime force door joy subject situate hen pen sweet brisk snake nephew sauce ' \
        'point skate life truly hockey scout assault lab impulse boss'
    e = "ff46716c20b789aff26b59a27b74716699457f29d650815d2db1e0a0d8f81c88"

    assert entropy_to_mnemonic(e) == m
    assert mnemonic_to_entropy(m) == e
    with pytest.raises(ValueError):
        entropy_to_mnemonic(e+"00")
    w = load_word_list()
    with pytest.raises(TypeError):
        entropy_to_mnemonic(e, word_list=[])
    with pytest.raises(TypeError):
        entropy_to_mnemonic(e, word_list="ttt")

    with pytest.raises(TypeError):
        mnemonic_to_entropy(m, word_list=[])
    with pytest.raises(TypeError):
        mnemonic_to_entropy(m, word_list="ttt")

    with pytest.raises(ValueError):
        mnemonic_to_entropy(m + " crime")

    assert entropy_to_mnemonic(e, word_list=w) == m
    assert mnemonic_to_entropy(m, word_list=w) == e

    for i in range(100):
        e = generate_entropy()
        m = entropy_to_mnemonic(e)
        assert mnemonic_to_entropy(m) == e

    for i in range(100):
        e = generate_entropy(strength=128)
        m = entropy_to_mnemonic(e)
        assert mnemonic_to_entropy(m) == e

    for i in range(100):
        e = generate_entropy(strength=160)
        m = entropy_to_mnemonic(e)
        assert mnemonic_to_entropy(m) == e

    for i in range(100):
        e = generate_entropy(strength=192)
        m = entropy_to_mnemonic(e)
        assert mnemonic_to_entropy(m) == e

    for i in range(100):
        e = generate_entropy(strength=224)
        m = entropy_to_mnemonic(e)
        assert mnemonic_to_entropy(m) == e

def test_is_mnemonic_checksum_valid():
    m = 'young crime force door joy subject situate hen pen sweet brisk snake nephew sauce ' \
        'point skate life truly hockey scout assault lab impulse boss'

    w = load_word_list()
    assert is_mnemonic_checksum_valid(m)
    assert is_mnemonic_checksum_valid(m, word_list=w)


    with pytest.raises(TypeError):
        is_mnemonic_checksum_valid(m, word_list=[])
    with pytest.raises(TypeError):
        is_mnemonic_checksum_valid(m, word_list="ttt")

    with pytest.raises(ValueError):
        is_mnemonic_checksum_valid(m + " crime")

    m = 'young crime force door joy subject situate hen pen sweet brisk snake nephew sauce ' \
        'point skate life truly hockey scout assault lab impulse brisk'
    assert is_mnemonic_checksum_valid(m) == False


def test_mnemonic_to_seed():
    m = 'young crime force door joy subject situate hen pen sweet brisk snake nephew sauce ' \
        'point skate life truly hockey scout assault lab impulse boss'
    s = "a870edd6272a4f0962a7595612d96645f683a3378fd9b067340eb11ebef45cb3d28fb64678cadc43969846" \
        "0a3d48bd57b2ae562b6d2b3c9fb5462d21e474191c"
    assert mnemonic_to_seed(m) == s
    with pytest.raises(TypeError):
        mnemonic_to_seed(b"ddjj")
    with pytest.raises(TypeError):
        mnemonic_to_seed(m, passphrase=b"djj")

def test_split_mnemonic():
    m = entropy_to_mnemonic(generate_entropy())
    s = split_mnemonic(m, 3, 5)
    assert combine_mnemonic(s) == m
    with pytest.raises(TypeError):
        split_mnemonic(3, 3, 5)

    shares = ["chest wing flight crazy crush core pottery unaware category marine skull ski",
              "never cotton main promote arena grape cat avocado session chef shoulder risk",
              "supply hub picnic badge exact wonder master second measure virtual road grocery"]
    assert combine_mnemonic(shares) == "flavor relief total decorate flash notice road enter zone tattoo barrel budget"
    shares = ["chest wing flight crazy crush core pottery unaware category marine skull ski",
              "supply hub picnic badge exact wonder master second measure virtual road grocery"]
    assert combine_mnemonic(shares) == "flavor relief total decorate flash notice road enter zone tattoo barrel budget"

    shares = ["edge outer hurry embody faith regular tower plate screen phrase lake pink cloud duty sheriff depart "
              "tube carpet zone suit embrace bar license doll",
              "amused artwork trust cruise ugly want occur change hill cactus half discover attack better loan soul "
              "worth legend smoke brush turkey sweet scorpion liberty",
              "surge evolve math type punch grape build tunnel curve alert rookie valve adjust vibrant wrestle "
              "fashion income endless sunset expect laptop worry hello life",
              "two toilet blood treat oil they concert scrap neglect scrap play glow alert trim song below cricket "
              "credit chaos word replace impact early thrive",
              "salt wear ill butter fade purpose parent pause rose frame era shrug caution invite demand seven cry "
              "wagon unique pilot subject cactus behave tide"]

    assert combine_mnemonic(shares) == "enforce north frost swear trial burst girl soccer rent town sea express other " \
                                       "oblige insect youth swarm violin stable push twin close clump extra"
    shares = ["occur hazard mail question wisdom pill grass tackle fit nephew gown motion",
              "embark fold seat fix quiz pull fortune wagon clever staff analyst symptom"]
    s = create_mnemonic_additional_share(shares)

    assert combine_mnemonic(shares) == combine_mnemonic([shares[0], s])
