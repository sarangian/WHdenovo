from io import StringIO
from whatshap.unphase import run_unphase


def test_unphase():
	out = StringIO()
	run_unphase('tests/data/phased-via-mixed-HP-PS.vcf', out)
	with open('tests/data/unphased.vcf') as f:
		expected = f.read()
	actual = out.getvalue()
	assert expected == actual
