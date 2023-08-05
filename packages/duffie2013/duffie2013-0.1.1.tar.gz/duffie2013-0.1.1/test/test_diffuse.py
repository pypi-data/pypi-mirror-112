from duffie2013.diffuse import diff_frac


def test_diff_frac_is_between_0_and_1():
    rgs = (0, 1, 10, 20, 30, 40)
    for i, rg in enumerate(rgs):
        for rg_ext in rgs[i:]:
            assert 0 <= diff_frac(rg, rg_ext) <= 1
