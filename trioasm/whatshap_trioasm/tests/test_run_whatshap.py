"""
Integration tests that use the command-line entry points run_whatshap, run_haplotag etc.
"""
from tempfile import TemporaryDirectory
import os
from io import StringIO
from collections import namedtuple
from collections import defaultdict

from pytest import raises, fixture, mark
import pysam
from whatshap.phase import run_whatshap
from whatshap.haplotag import run_haplotag
from whatshap.hapcut2vcf import run_hapcut2vcf
from whatshap.vcf import VcfReader, VariantCallPhase

trio_bamfile = 'tests/data/trio.pacbio.bam'
trio_merged_bamfile = 'tests/data/trio-merged-blocks.bam'
trio_paired_end_bamfile = 'tests/data/paired_end.sorted.bam'
ped_samples_bamfile = 'tests/data/ped_samples.bam'
recombination_breaks_bamfile = 'tests/data/recombination_breaks.sorted.bam'
quartet2_bamfile = 'tests/data/quartet2.bam'
short_bamfile = 'tests/data/short-genome/short.bam'
short_duplicate_bamfile = 'tests/data/short-genome/short-one-read-duplicate.bam'
indels_bamfile = 'tests/data/indels.bam'

bam_files = [trio_bamfile, trio_merged_bamfile, trio_paired_end_bamfile,
	recombination_breaks_bamfile, quartet2_bamfile, short_bamfile, short_duplicate_bamfile,
	indels_bamfile]


@fixture(params=['whatshap', 'hapchat'])
def algorithm(request):
	return request.param


def setup_module():
	# This function is run once for this module
	for bam_path in bam_files:
		assert bam_path.endswith('.bam')
		sam_path = bam_path[:-4] + '.sam'
		pysam.view(sam_path, '-b', '-o', bam_path, catch_stdout=False)
		pysam.index(bam_path, catch_stdout=False)


def teardown_module():
	for path in bam_files:
		os.remove(path)
		os.remove(path + '.bai')


def test_one_variant(algorithm):
	run_whatshap(
		phase_input_files=['tests/data/oneread.bam'],
		variant_file='tests/data/onevariant.vcf',
		output='/dev/null',
		algorithm=algorithm)


def test_default_output(algorithm):
	"""Output to stdout"""
	run_whatshap(
		phase_input_files=['tests/data/oneread.bam'],
		variant_file='tests/data/onevariant.vcf',
		algorithm=algorithm)


def test_one_variant_cram(algorithm):
	run_whatshap(
		phase_input_files=['tests/data/oneread.cram'],
		reference='tests/data/oneread-ref.fasta',
		variant_file='tests/data/onevariant.vcf',
		output='/dev/null',
		algorithm=algorithm)


def test_cram_no_reference(algorithm):
	# This needs to fail because CRAM requires a reference, but it was not given.

	# If REF_PATH is not set, pysam/htslib tries to retrieve the reference from EBI via
	# the internet.
	os.environ['REF_PATH'] = '/does/not/exist'
	with raises(SystemExit):
		run_whatshap(
			phase_input_files=['tests/data/oneread.cram'],
			variant_file='tests/data/onevariant.vcf',
			output='/dev/null',
			algorithm=algorithm)


def test_bam_without_readgroup(algorithm):
	run_whatshap(
		phase_input_files=['tests/data/no-readgroup.bam'],
		variant_file='tests/data/onevariant.vcf',
		output='/dev/null',
		ignore_read_groups=True,
		algorithm=algorithm)


def test_requested_sample_not_found(algorithm):
	with raises(SystemExit):
		run_whatshap(
			phase_input_files=['tests/data/oneread.bam'],
			variant_file='tests/data/onevariant.vcf',
			output='/dev/null',
			samples=['DOES_NOT_EXIST'],
		        algorithm=algorithm)


@mark.parametrize('algorithm,expected_vcf', [
	('whatshap', 'tests/data/pacbio/phased.vcf'),
	('hapchat', 'tests/data/pacbio/phased_hapchat.vcf'),
])
def test_with_reference(algorithm, expected_vcf):
	# This tests also whether lowercase reference FASTA files work:
	# If lowercase and uppercase are treated differently, then the
	# output is slightly different from the expected.

	# note: because hapchat has a different dynamic programming
	# scheme, it may phase some variants differently, e.g., the
	# variant at site 11221 of phased.vcf.  It also phases each
	# heterozygous site, even if the scores (in the DP table) of
	# its (two) possible phasings are identical -- such is the
	# case for sites 13300 and 14324 of phased.vcf.  It is for
	# this reason that we have a second phased_hapchat.vcf which
	# is different in these above three sites.  Whether or not
	# this a desired behaviour is subject to discussion --
	# possible handling (i.e., avoiding the phasing of) sites with
	# identical phasing scores is a possible future work, etc.
	out = StringIO()
	run_whatshap(
		phase_input_files=['tests/data/pacbio/pacbio.bam'],
		variant_file='tests/data/pacbio/variants.vcf',
		reference='tests/data/pacbio/reference.fasta',
		output=out,
		write_command_line_header=False,  # for easier VCF comparison
		algorithm=algorithm
	)
	with open(expected_vcf) as f:
		expected = f.read()
	assert out.getvalue() == expected, 'VCF output not as expected'


def test_with_reference_and_indels(algorithm):
	run_whatshap(
		phase_input_files=['tests/data/pacbio/pacbio.bam'],
		variant_file='tests/data/pacbio/variants.vcf',
		reference='tests/data/pacbio/reference.fasta',
		indels=True,
		algorithm=algorithm)


@mark.parametrize('algorithm,expected_lines', [
	('whatshap',
		["1\t60906167\t.\tG\tA\t.\tPASS\tAC=2;AN=6\tGT:PS\t0/1:.\t0|1:60906167\t0/0:.\n",
		 "1\t60907394\t.\tG\tA\t.\tPASS\tAC=4;AN=6\tGT:PS\t0|1:60907394\t1/1:.\t0/1:.\n",
		 "1\t60907460\t.\tG\tT\t.\tPASS\tAC=2;AN=6\tGT:PS\t0|1:60907394\t0|1:60906167\t0/0:.\n",
		 "1\t60907473\t.\tC\tA\t.\tPASS\tAC=2;AN=6\tGT:PS\t0|1:60907394\t0/1:.\t0/0:.\n",
		 "1\t60909718\t.\tT\tC\t.\tPASS\tAC=2;AN=6\tGT\t0/1\t0/1\t0/0\n"]),
	('hapchat',
		["1\t60906167\t.\tG\tA\t.\tPASS\tAC=2;AN=6\tGT:PS\t0/1:.\t1|0:60906167\t0/0:.\n",
		 "1\t60907394\t.\tG\tA\t.\tPASS\tAC=4;AN=6\tGT:PS\t1|0:60907394\t1/1:.\t0/1:.\n",
		 "1\t60907460\t.\tG\tT\t.\tPASS\tAC=2;AN=6\tGT:PS\t1|0:60907394\t1|0:60906167\t0/0:.\n",
		 "1\t60907473\t.\tC\tA\t.\tPASS\tAC=2;AN=6\tGT:PS\t1|0:60907394\t0/1:.\t0/0:.\n",
		 "1\t60909718\t.\tT\tC\t.\tPASS\tAC=2;AN=6\tGT\t0/1\t0/1\t0/0\n"]),
])
def test_ps_tag(algorithm, expected_lines):
	out = StringIO()
	run_whatshap(
		variant_file='tests/data/trio.vcf',
		phase_input_files=['tests/data/trio.pacbio.bam'],
		output=out,
		tag='PS',
		algorithm=algorithm)
	out.seek(0)
	lines = [ line for line in out.readlines() if not line.startswith('#') ]

	# TODO This is quite an ugly way to test phased VCF writing (see parametrization)
	for i in range(5) :
		assert lines[i] == expected_lines[i]


def assert_phasing(phases, expected_phases):
	# TODO: this code is not "block aware". Would be useful to extend it to compare phasings per block
	print('assert_phasing({}, {})'.format(phases, expected_phases))
	assert len(phases) == len(expected_phases)
	p_unchanged = []
	p_inverted = []
	p_expected = []
	for phase, expected_phase in zip(phases, expected_phases):
		if (phase is None) and (expected_phase is None):
			continue
		assert phase is not None and expected_phase is not None
		assert phase.block_id == expected_phase.block_id
		p_unchanged.append(phase.phase)
		p_inverted.append(1-phase.phase)
		p_expected.append(expected_phase.phase)
	assert (p_unchanged == p_expected) or (p_inverted == p_expected)


def test_phase_three_individuals(algorithm):
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		outreadlist = tempdir + '/readlist.tsv'
		run_whatshap(
			phase_input_files=[trio_bamfile],
			variant_file='tests/data/trio.vcf',
			read_list_filename=outreadlist,
			output=outvcf,
			algorithm=algorithm)
		assert os.path.isfile(outvcf)
		assert os.path.isfile(outreadlist)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase1 = VariantCallPhase(60906167, 0, None)
		phase3 = VariantCallPhase(60907394, 0, None)
		assert_phasing(table.phases_of('HG004'), [None, phase3, phase3, phase3, None])
		assert_phasing(table.phases_of('HG003'), [phase1, None, phase1, None, None])
		assert_phasing(table.phases_of('HG002'), [None, None, None, None, None])


def test_phase_one_of_three_individuals(algorithm):
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(
			phase_input_files=[trio_bamfile],
			variant_file='tests/data/trio.vcf',
			output=outvcf,
			samples=['HG003'],
			algorithm=algorithm)
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase0 = VariantCallPhase(60906167,0,None)
		assert_phasing(table.phases_of('HG004'), [None, None, None, None, None])
		assert_phasing(table.phases_of('HG003'), [phase0, None, phase0, None, None])
		assert_phasing(table.phases_of('HG002'), [None, None, None, None, None])


def test_phase_trio():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		outreadlist = tempdir + '/readlist.tsv'
		run_whatshap(phase_input_files=[trio_bamfile], variant_file='tests/data/trio.vcf', read_list_filename=outreadlist, output=outvcf,
		        ped='tests/data/trio.ped', genmap='tests/data/trio.map')
		assert os.path.isfile(outvcf)
		assert os.path.isfile(outreadlist)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase0 = VariantCallPhase(60906167, 0, None)
		assert_phasing(table.phases_of('HG004'), [phase0, phase0, phase0, phase0, phase0])
		assert_phasing(table.phases_of('HG003'), [phase0, None, phase0, phase0, phase0])
		assert_phasing(table.phases_of('HG002'), [None, phase0, None, None, None])


def test_phase_trio_hapchat() :
	# This needs to fail because pedigree phasing is not (yet) a
	# feature of hapchat
	with raises(SystemExit) :
		run_whatshap(
			phase_input_files=[trio_bamfile],
			variant_file='tests/data/trio.vcf',
			output='/dev/null',
			ped='tests/data/trio.ped',
			genmap='tests/data/trio.map',
			algorithm='hapchat')


def test_phase_trio_use_ped_samples():
	with TemporaryDirectory() as tempdir:
		for ped_samples in [True, False]:
			outvcf = tempdir + '/output_ped_samples.vcf'
			outreadlist = tempdir + '/readlist.tsv'
			run_whatshap(phase_input_files=[ped_samples_bamfile], variant_file='tests/data/ped_samples.vcf', read_list_filename=outreadlist, output=outvcf,
				ped='tests/data/trio.ped', genmap='tests/data/trio.map', use_ped_samples=ped_samples)
			assert os.path.isfile(outvcf)
			assert os.path.isfile(outreadlist)

			tables = list(VcfReader(outvcf, phases=True))
			assert len(tables) == 1
			table = tables[0]
			assert table.chromosome == '1'
			assert len(table.variants) == 5
			assert table.samples == ['HG004', 'HG003', 'HG002', 'orphan']

			phase0 = VariantCallPhase(60906167, 0, None)
			phase1 = VariantCallPhase(60907394, 0, None)
			assert_phasing(table.phases_of('HG004'), [phase0, phase0, phase0, phase0, phase0])
			assert_phasing(table.phases_of('HG003'), [phase0, None, phase0, phase0, phase0])
			assert_phasing(table.phases_of('HG002'), [None, phase0, None, None, None])

			if ped_samples:
				assert_phasing(table.phases_of('orphan'), [None, None, None, None, None])
			else:
				assert_phasing(table.phases_of('orphan'), [None, phase1, phase1, phase1, None])

def test_phase_ped_sample():
	with TemporaryDirectory() as tempdir:
		# running with --ped and --sample on subset of trio, should give same results as running with only --sample
		# the trio information should be ignored
		outvcf1 = tempdir + '/output1.vcf'
		outvcf2 = tempdir + '/output2.vcf'
		for sample_set in [['HG002'], ['HG003'], ['HG004'], ['HG002','HG003'], ['HG002','HG004'], ['HG003','HG004']]:
			run_whatshap(phase_input_files=[ped_samples_bamfile], variant_file='tests/data/ped_samples.vcf', output=outvcf1,
				ped='tests/data/trio.ped', samples=sample_set)
			run_whatshap(phase_input_files=[ped_samples_bamfile], variant_file='tests/data/ped_samples.vcf', output=outvcf2,
				samples=sample_set)

			assert os.path.isfile(outvcf1)
			assert os.path.isfile(outvcf2)

			tables1 = list(VcfReader(outvcf1, phases=True))
			tables2 = list(VcfReader(outvcf2, phases=True))

			assert( (len(tables1) == 1) and (len(tables2) == 1) )
			table1, table2 = tables1[0], tables2[0]

			for individual in sample_set:
				assert_phasing(table1.phases_of(individual), table2.phases_of(individual))

def test_phase_trio_distrust_genotypes():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output_gl.vcf'
		outreadlist = tempdir + '/readlist.tsv'
		run_whatshap(phase_input_files=[trio_bamfile], variant_file='tests/data/trio_genotype_likelihoods.vcf', read_list_filename=outreadlist, output=outvcf,
		        ped='tests/data/trio.ped', genmap='tests/data/trio.map', distrust_genotypes=True)
		assert os.path.isfile(outvcf)
		assert os.path.isfile(outreadlist)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase0 = VariantCallPhase(60906167, 0, None)
		assert_phasing(table.phases_of('HG004'), [None, phase0, phase0, phase0, None])
		assert_phasing(table.phases_of('HG003'), [phase0, None, phase0, phase0, phase0])
		assert_phasing(table.phases_of('HG002'), [phase0, None, phase0, phase0, phase0])


def test_phase_trio_merged_blocks():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output-merged-blocks.vcf'
		run_whatshap(phase_input_files=[trio_merged_bamfile], variant_file='tests/data/trio-merged-blocks.vcf', output=outvcf,
		        ped='tests/data/trio.ped', genmap='tests/data/trio.map')
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 8
		assert table.samples == ['HG002', 'HG003', 'HG004']
		assert table.num_of_blocks_of('HG004') == 1
		assert table.num_of_blocks_of('HG003') == 1
		assert table.num_of_blocks_of('HG002') == 1

		phase0 = VariantCallPhase(752566, 0, None)
		phase1 = VariantCallPhase(752566, 1, None)
		assert_phasing(table.phases_of('HG004'), [phase1, phase1, phase1, None, phase1, phase1, phase1, phase1])
		assert_phasing(table.phases_of('HG003'), [None, None, None, None, phase0, phase0, phase0, phase1])
		assert_phasing(table.phases_of('HG002'), [None, None, None, None, None, None, None, phase1])


def test_phase_trio_dont_merge_blocks():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output-merged-blocks.vcf'
		run_whatshap(phase_input_files=[trio_merged_bamfile], variant_file='tests/data/trio-merged-blocks.vcf', output=outvcf,
				ped='tests/data/trio.ped', genmap='tests/data/trio.map', genetic_haplotyping=False)
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 8
		assert table.samples == ['HG002', 'HG003', 'HG004']
		assert table.num_of_blocks_of('HG004') == 2
		assert table.num_of_blocks_of('HG003') == 1
		assert table.num_of_blocks_of('HG002') == 1

		phase1 = VariantCallPhase(752566, 1, None)
		phase2_0 = VariantCallPhase(853954, 0, None)
		phase2_1 = VariantCallPhase(853954, 1, None)
		assert_phasing(table.phases_of('HG004'), [phase1, phase1, phase1, None, phase2_1, phase2_1, phase2_1, phase2_1])
		assert_phasing(table.phases_of('HG003'), [None, None, None, None, phase2_0, phase2_0, phase2_0, phase2_1])
		assert_phasing(table.phases_of('HG002'), [None, None, None, None, None, None, None, phase2_1])


def test_genetic_phasing_symbolic_alt():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(phase_input_files=[], variant_file='tests/data/trio-symbolic-alt.vcf', output=outvcf,
		        ped='tests/data/trio.ped', indels=True)
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True, indels=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase0 = VariantCallPhase(60906167, 0, None)
		assert_phasing(table.phases_of('HG004'), [phase0, phase0, phase0, phase0, phase0])
		assert_phasing(table.phases_of('HG003'), [phase0, None, phase0, phase0, phase0])
		assert_phasing(table.phases_of('HG002'), [None, phase0, None, None, None])


def test_phase_mendelian_conflict():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(phase_input_files=[trio_bamfile], variant_file='tests/data/trio-mendelian-conflict.vcf', output=outvcf,
				ped='tests/data/trio.ped', genmap='tests/data/trio.map')
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase = VariantCallPhase(60906167, 0, None)
		assert_phasing(table.phases_of('HG004'), [phase, None, phase, phase, phase])
		assert_phasing(table.phases_of('HG003'), [phase, None, phase, phase, phase])
		assert_phasing(table.phases_of('HG002'), [None, None, None, None, None])


def test_phase_missing_genotypes():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(phase_input_files=[trio_bamfile], variant_file='tests/data/trio-missing-genotypes.vcf', output=outvcf,
				ped='tests/data/trio.ped', genmap='tests/data/trio.map')
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 5
		assert table.samples == ['HG004', 'HG003', 'HG002']

		phase = VariantCallPhase(60906167, 0, None)
		assert_phasing(table.phases_of('HG004'), [phase, phase, None, phase, None])
		assert_phasing(table.phases_of('HG003'), [phase, None, None, phase, None])
		assert_phasing(table.phases_of('HG002'), [None, phase, None, None, None])


def test_phase_specific_chromosome():
	for requested_chromosome in ['1','2']:
		with TemporaryDirectory() as tempdir:
			outvcf = tempdir + '/output.vcf'
			run_whatshap(phase_input_files=[trio_bamfile], variant_file='tests/data/trio-two-chromosomes.vcf', output=outvcf,
					ped='tests/data/trio.ped', genmap='tests/data/trio.map', chromosomes=[requested_chromosome])
			assert os.path.isfile(outvcf)

			tables = list(VcfReader(outvcf, phases=True))
			assert len(tables) == 2
			for table in tables:
				assert len(table.variants) == 5
				assert table.samples == ['HG004', 'HG003', 'HG002']
				if table.chromosome == '1' == requested_chromosome:
					phase0 = VariantCallPhase(60906167, 0, None)
					assert_phasing(table.phases_of('HG004'), [phase0, phase0, phase0, phase0, phase0])
					assert_phasing(table.phases_of('HG003'), [phase0, None, phase0, phase0, phase0])
					assert_phasing(table.phases_of('HG002'), [None, phase0, None, None, None])
				elif table.chromosome == '2' == requested_chromosome:
					phase0 = VariantCallPhase(60906167, 0, None)
					phase1 = VariantCallPhase(60906167, 1, None)
					assert_phasing(table.phases_of('HG004'), [phase0, None, None, None, phase1])
					assert_phasing(table.phases_of('HG003'), [phase0, None, None, None, None])
					assert_phasing(table.phases_of('HG002'), [None, None, None, None, phase0])
				else:
					assert_phasing(table.phases_of('HG004'), [None, None, None, None, None])
					assert_phasing(table.phases_of('HG003'), [None, None, None, None, None])
					assert_phasing(table.phases_of('HG002'), [None, None, None, None, None])


def test_phase_trio_paired_end_reads():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output-paired_end.vcf'
		run_whatshap(phase_input_files=[trio_paired_end_bamfile], variant_file='tests/data/paired_end.sorted.vcf', output=outvcf,
		        ped='tests/data/trio_paired_end.ped', genmap='tests/data/trio.map')
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 3
		assert table.samples == ['mother', 'father', 'child']
		assert table.num_of_blocks_of('mother') == 1
		assert table.num_of_blocks_of('father') == 0
		assert table.num_of_blocks_of('child') == 1

		phase0 = VariantCallPhase(80050, 0, None)
		phase1 = VariantCallPhase(80050, 1, None)

		assert_phasing(table.phases_of('mother'), [phase1, phase1, phase0])
		assert_phasing(table.phases_of('father'), [None, None, None])
		assert_phasing(table.phases_of('child'), [None, None, phase1])


def test_phase_quartet_recombination_breakpoints():
	parameter_sets = [
		(False, {'genmap':'tests/data/recombination_breaks.map'}),
		(True, {'recombrate':1000000}),
		(False, {'recombrate':.0000001})
	]
	
	for expect_recombination, parameters in parameter_sets:
		with TemporaryDirectory() as tempdir:
			outvcf = tempdir + '/output-recombination_breaks.vcf'
			outlist = tempdir + '/output.recomb'
			run_whatshap(phase_input_files=[recombination_breaks_bamfile], variant_file='tests/data/quartet.vcf.gz', output=outvcf,
					ped='tests/data/recombination_breaks.ped', recombination_list_filename = outlist, **parameters)
			assert os.path.isfile(outvcf)

			tables = list(VcfReader(outvcf, phases=True))
			assert len(tables) == 1
			table = tables[0]
			assert table.chromosome == '1'
			assert len(table.variants) == 4
			assert table.samples == ['HG002', 'HG005', 'HG003', 'HG004']
			assert table.num_of_blocks_of('HG002') == 0
			assert table.num_of_blocks_of('HG005') == 0
			assert table.num_of_blocks_of('HG003') == 1
			assert table.num_of_blocks_of('HG004') == 0

			phase0 = VariantCallPhase(68735304, 0, None)
			phase1 = VariantCallPhase(68735304, 1, None)

			assert_phasing(table.phases_of('HG002'), [None, None, None, None])
			assert_phasing(table.phases_of('HG005'), [None, None, None, None])
			if expect_recombination:
				assert_phasing(table.phases_of('HG003'), [phase0, phase0, None, phase1])
			else:
				assert_phasing(table.phases_of('HG003'), [phase0, phase0, None, phase0])
			assert_phasing(table.phases_of('HG004'), [None, None, None, None])
			
			lines = open(outlist).readlines()
			if expect_recombination:
				assert len(lines) == 3
				assert lines[1]=='HG002 1 68735433 68738308 0 0 0 1 3\n'
				assert lines[2]=='HG005 1 68735433 68738308 0 0 0 1 3\n'
			else:
				assert len(lines) == 1


def test_phase_trio_zero_distance():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(phase_input_files=[trio_bamfile], variant_file='tests/data/trio.vcf', output=outvcf,
		        ped='tests/data/trio.ped', genmap='tests/data/zero-genetic-distance.map')
		assert os.path.isfile(outvcf)


def test_phase_quartet_recombination_breakpoints():
	parameter_sets = [
		(False, {'genmap':'tests/data/recombination_breaks.map'}),
		(True, {'recombrate':1000000}),
		(False, {'recombrate':.0000001})
	]


def test_haplotag():
	with TemporaryDirectory() as tempdir:
		outbam1 = tempdir + '/output1.bam'
		outbam2 = tempdir + '/output2.bam'

		# run haplotag with two vcfs containing opposite phasings (i.e. 1|0 - 0|1 ..)
		run_haplotag(variant_file='tests/data/haplotag_1.vcf.gz', alignment_file='tests/data/haplotag.bam', output=outbam1)
		run_haplotag(variant_file='tests/data/haplotag_2.vcf.gz', alignment_file='tests/data/haplotag.bam', output=outbam2)
		for a1, a2 in zip(pysam.AlignmentFile(outbam1), pysam.AlignmentFile(outbam2)):
			assert a1.query_name == a2.query_name
			if a1.has_tag('HP'):
				assert a2.has_tag('HP')
				assert a1.get_tag('HP') != a2.get_tag('HP')


def test_haplotag2():
	with TemporaryDirectory() as tempdir:
		outbam = tempdir + '/output.bam'
		run_haplotag(variant_file='tests/data/haplotag_2.vcf.gz', alignment_file='tests/data/haplotag.bam', output=outbam)
		ps_count = 0
		for alignment in pysam.AlignmentFile(outbam):
			if alignment.has_tag('PS'):
				ps_count += 1
			if alignment.has_tag('HP'):
				# simulated bam, we know from which haplotype each read originated (given in read name)
				true_ht = int(alignment.query_name[-1])
				assert true_ht == alignment.get_tag('HP')
		assert ps_count > 0


def test_haplotag_missing_chromosome():
	with TemporaryDirectory() as tempdir:
		outbam = tempdir + '/output.bam'

		# input BAM contains a chromosom for which there is no variant in the input VCF
		run_haplotag(variant_file='tests/data/haplotag.missing_chr.vcf.gz', alignment_file='tests/data/haplotag.large.bam', output=outbam)
		ps_count = 0
		for alignment in pysam.AlignmentFile(outbam):
			if alignment.has_tag('PS'):
				ps_count += 1
		assert ps_count > 0


def test_haplotag_no_readgroups1():
	with TemporaryDirectory() as tempdir:
		outbam1 = tempdir + '/output1.bam'
		outbam2 = tempdir + '/output2.bam'

		# run haplotag with/without --ignore-read-groups, results should be identical since files contain only data for one sample
		run_haplotag(variant_file='tests/data/haplotag_1.vcf.gz', alignment_file='tests/data/haplotag.bam', output=outbam1)
		run_haplotag(variant_file='tests/data/haplotag_1.vcf.gz', alignment_file='tests/data/haplotag_noRG.bam', output=outbam2, ignore_read_groups=True)
		for a1, a2 in zip(pysam.AlignmentFile(outbam1), pysam.AlignmentFile(outbam2)):
			assert a1.query_name == a2.query_name
			if a1.has_tag('HP'):
				assert a2.has_tag('HP')
				assert a1.get_tag('HP') == a2.get_tag('HP')


def test_haplotag_no_readgroups2():
	with raises(SystemExit):
		# vcf contains multiple samples, there should be an error
		run_haplotag(alignment_file='tests/data/haplotag_noRG.bam', variant_file='tests/data/haplotag_noRG.vcf.gz',
			output='/dev/null', ignore_read_groups=True)


def test_haplotag_sample_given():
	with TemporaryDirectory() as tempdir:
		outbam = tempdir + '/output.bam'
		run_haplotag(variant_file='tests/data/haplotag_sample.vcf.gz', alignment_file='tests/data/haplotag_sample.bam', given_samples=['mother'], output=outbam)
		for alignment in pysam.AlignmentFile(outbam):
			if alignment.get_tag('RG') == 'mother':
				assert alignment.has_tag('HP')
			else:
				assert not alignment.has_tag('HP')


def haplotag_different_sorting():
	with TemporaryDirectory() as tempdir:
		outbam1 = tempdir + '/output1.bam'
		outbam2 = tempdir + '/output2.bam'
		
		# both VCFs contain the same positions, but chromosomes are sorted differently
		run_haplotag(variant_file='tests/data/haplotag.large.vcf.gz', alignment_file='tests/data/haplotag.large.bam', output=outbam1)
		run_haplotag(variant_file='tests/data/haplotag.large.2.vcf.gz', alignment_file='tests/data/haplotag.large.bam', output=outbam2)
		for a1, a2 in zip(pysam.AlignmentFile(outbam1), pysam.AlignmentFile(outbam2)):
			assert a1.query_name == a2.query_name
			if a1.has_tag('HP'):
				assert a2.has_tag('HP')
				assert a1.get_tag('HP') == a2.get_tag('HP')


def test_haplotag_10X():
	with TemporaryDirectory() as tempdir:
		outbam = tempdir + '/output.bam'
		run_haplotag(variant_file='tests/data/haplotag.10X.vcf.gz', alignment_file='tests/data/haplotag.10X.bam', output=outbam)
		# map BX tag --> readlist
		BX_tag_to_readlist = defaultdict(list)
		for alignment in pysam.AlignmentFile(outbam):
			if alignment.has_tag('BX') and alignment.has_tag('HP'):
				BX_tag_to_readlist[alignment.get_tag('BX')].append(alignment)
		# reads having same BX tag need to be assigned to same haplotype
		for tag in BX_tag_to_readlist.keys():
			haplotype = BX_tag_to_readlist[tag][0].get_tag('HP')
			for read in BX_tag_to_readlist[tag]:
				assert haplotype == read.get_tag('HP')


def test_haplotag_10X_2():
	with TemporaryDirectory() as tempdir:
		outbam = tempdir + '/output.bam'
		run_haplotag(variant_file='tests/data/haplotag.10X_2.vcf.gz', alignment_file='tests/data/haplotag.10X.bam', output=outbam)
		for a1, a2 in zip(pysam.AlignmentFile('tests/data/haplotag.10X.bam'), pysam.AlignmentFile(outbam)):
			assert a1.query_name == a2.query_name
			if a1.has_tag('HP') and a2.has_tag('HP'):
				assert a1.get_tag('HP') == a2.get_tag('HP')


def test_hapcut2vcf():
	with TemporaryDirectory() as tempdir:
		out = os.path.join(tempdir, 'hapcut.vcf')
		run_hapcut2vcf(
			hapcut='tests/data/pacbio/hapcut.txt', vcf='tests/data/pacbio/variants.vcf', output=out)


def test_ignore_read_groups(algorithm):
	run_whatshap(
		variant_file='tests/data/pacbio/variants.vcf',
		phase_input_files=['tests/data/pacbio/pacbio.bam'],
		reference='tests/data/pacbio/reference.fasta',
		ignore_read_groups=True,
		output='/dev/null',
		algorithm=algorithm)


def test_readgroup_without_sample_name(algorithm):
	run_whatshap(
		phase_input_files=['tests/data/oneread-readgroup-without-sample.bam'],
		variant_file='tests/data/onevariant.vcf',
		output='/dev/null',
		ignore_read_groups=True,
		algorithm=algorithm)


def test_genetic_haplotyping():
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		outrecomb = tempdir + '/output.recomb'
		run_whatshap(variant_file='tests/data/genetic-haplotyping.vcf', phase_input_files=[],
			ped='tests/data/genetic-haplotyping.ped', output=outvcf,
			recombination_list_filename=outrecomb)
		tables = list(VcfReader(outvcf, phases=True))

		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == '1'
		assert len(table.variants) == 3
		assert table.samples == ['sampleA', 'sampleB', 'sampleC', 'sampleD', 'sampleE']
		assert table.num_of_blocks_of('sampleA') == 1
		assert table.num_of_blocks_of('sampleB') == 1
		assert table.num_of_blocks_of('sampleC') == 0
		assert table.num_of_blocks_of('sampleD') == 1
		assert table.num_of_blocks_of('sampleE') == 1

		phase0 = VariantCallPhase(10327, 0, None)
		phase1 = VariantCallPhase(10327, 1, None)

		assert_phasing(table.phases_of('sampleA'), [phase0, phase0, phase1])
		assert_phasing(table.phases_of('sampleB'), [phase0, None, None])
		assert_phasing(table.phases_of('sampleC'), [None, None, None])
		assert_phasing(table.phases_of('sampleD'), [phase0, None, phase1])
		assert_phasing(table.phases_of('sampleE'), [phase0, phase0, None])

		lines = [l.split() for l in open(outrecomb)]
		assert len(lines) == 2
		Fields = namedtuple('Fields', [f.strip('#\n') for f in lines[0]])
		recomb = Fields(*lines[1])
		print(recomb)
		assert recomb.child_id == 'sampleC'
		assert recomb.chromosome == '1'
		assert recomb.position1 == '31295'
		assert recomb.position2 == '102596'

		#assert recomb.transmitted_hap_mother1 != recomb.transmitted_hap_mother2
		#assert recomb.transmitted_hap_father1 == recomb.transmitted_hap_father2


def test_quartet2():
	run_whatshap(variant_file='tests/data/quartet2.vcf', phase_input_files=[quartet2_bamfile],
		ped='tests/data/quartet2.ped', output='/dev/null')


@mark.parametrize('algorithm,expected_blocks', [
	('whatshap', [10, 10, None, 200, 200]),
	('hapchat', [10, 10, 10, 10, 10]),
])
def test_phased_blocks(algorithm, expected_blocks):
	# This test involves a simple example on a pair of reads which
	# overlap a single site which is homozygous.  While we are
	# distrusting genotypes AND including homozygous sites, i.e.,
	# we are doing full genotyping, if we were phasing purely from
	# the reads, then whether or not the pair of reads falls on
	# the same or different haplotypes should not matter.  With
	# this in mind, reasoning with genotype likelihoods slighly
	# disfavours a cis-phasing of this pair, which is what
	# whatshap does.  While hapchat, however, does take into
	# account genotype likelihoods, while making the
	# all-heterozygous assumption, hence cis-phasing this pair.

	# Note that taking into account genotype likelihoods is a
	# future work planned for hapchat.  Since the nature of the
	# hapchat DP scheme is such that relaxing the all-heterozygous
	# assumption would be too costly in terms of runtime and
	# memory, a possibility is to (re-) exclude homozygous sites
	# in a preprocessing step based on some threshold on the
	# genotype likelihoods.
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(
			phase_input_files=[short_bamfile],
			variant_file='tests/data/short-genome/short.vcf',
			ignore_read_groups=True, distrust_genotypes=True,
			include_homozygous=True, output=outvcf,
			algorithm=algorithm)
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == 'chr1'
		assert len(table.variants) == 5
		assert table.samples == ['sample']

		blocks = [(p.block_id if p is not None else None) for p in table.phases_of('sample')]
		assert blocks == expected_blocks


@mark.parametrize('algorithm,expected_block', [
	('whatshap', [10, 10, None, None, None]),
	('hapchat', [10, 10, 10, None, None]),
])
def test_duplicate_read(algorithm, expected_block):
	# This test is very similar to the previous test_phased_blocks
	# test, except that there is just a single read this time,
	# with homozygous site.  Still, since hapchat would rather
	# phase this homozygous site, since the context is full
	# genotyping, it does so, regardless of any genotype
	# likelihood.  See above test for more details.
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(
			phase_input_files=[short_duplicate_bamfile],
			variant_file='tests/data/short-genome/short.vcf',
			ignore_read_groups=True,
			distrust_genotypes=True,
			include_homozygous=True,
			output=outvcf,
			algorithm=algorithm)
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == 'chr1'
		assert len(table.variants) == 5
		assert table.samples == ['sample']

		blocks = [(p.block_id if p is not None else None) for p in table.phases_of('sample')]
		assert blocks == expected_block


def test_wrong_chromosome(algorithm):
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		with raises(SystemExit):
			run_whatshap(
				phase_input_files=[short_bamfile],
				ignore_read_groups=True,
				variant_file='tests/data/short-genome/wrongchromosome.vcf',
				output=outvcf,
				algorithm=algorithm)


def test_indel_phasing(algorithm):
	with TemporaryDirectory() as tempdir:
		outvcf = tempdir + '/output.vcf'
		run_whatshap(
			phase_input_files=[indels_bamfile],
			indels=True, variant_file='tests/data/indels.vcf',
			reference='tests/data/random0.fasta',
			output=outvcf,
			algorithm=algorithm)
		assert os.path.isfile(outvcf)

		tables = list(VcfReader(outvcf, indels=True, phases=True))
		assert len(tables) == 1
		table = tables[0]
		assert table.chromosome == 'random0'
		assert len(table.variants) == 4
		assert table.samples == ['sample1']

		phase0 = VariantCallPhase(41, 0, None)
		phase1 = VariantCallPhase(41, 1, None)
		assert_phasing(table.phases_of('sample1'), [phase0, phase1, phase0, phase1])


def test_full_genotyping(algorithm):
	run_whatshap(
		phase_input_files=['tests/data/oneread.bam'],
		variant_file='tests/data/onevariant.vcf',
		output='/dev/null',
		full_genotyping=True,
		algorithm=algorithm)


def test_with_read_merging(algorithm) :
	run_whatshap(
		phase_input_files=['tests/data/pacbio/pacbio.bam'],
		variant_file='tests/data/pacbio/variants.vcf',
		reference='tests/data/pacbio/reference.fasta',
		output='/dev/null',
		read_merging=True,
		algorithm=algorithm)
