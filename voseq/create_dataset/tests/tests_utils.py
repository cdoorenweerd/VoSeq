from Bio.Seq import Seq

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from create_dataset.utils import CreateDataset
from public_interface.models import Genes


class CreateDatasetUtilsTest(TestCase):
    def setUp(self):
        args = []
        opts = {'dumpfile': 'test_db_dump.xml', 'verbosity': 0}
        cmd = 'migrate_db'
        call_command(cmd, *args, **opts)

        g1 = Genes.objects.get(gene_code='COI')
        g2 = Genes.objects.get(gene_code='EF1a')
        self.cleaned_data = {
            'gene_codes': [g1, g2],
            'taxonset': None,
            'voucher_codes': 'CP100-10\r\nCP100-11',
            'geneset': None,
            'taxon_names': ['CODE', 'SUPERFAMILY', 'GENUS', 'SPECIES'],
            'positions': ['ALL'],
        }

        self.c = Client()
        self.dataset_creator = CreateDataset(self.cleaned_data)
        self.maxDiff = None

    def test_create_dataset(self):
        expected = '>coi\n--------------------\n>CP100-10_Papilionoidea_Melitaea_diamina'
        result = self.dataset_creator.dataset_str
        self.assertTrue(expected in result)

    def test_create_dataset_with_gene_code(self):
        self.cleaned_data['taxon_names'] = ['CODE', 'GENECODE']
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = ">CP100-10_coi\n"
        result = dataset_creator.dataset_str
        self.assertTrue(expected in result)

    def test_get_taxon_names_for_taxa(self):
        expected = {
            'cp100-10': {'code': 'CP100-10', 'genus': 'Melitaea', 'species': 'diamina', 'superfamily': 'Papilionoidea'},
            'cp100-11': {'code': 'CP100-11', 'genus': 'Melitaea', 'species': 'diamina', 'superfamily': ''},
        }
        result = self.dataset_creator.get_taxon_names_for_taxa()
        self.assertEqual(expected, result)

    def test_from_seq_objs_to_fasta(self):
        expected = 2706
        result = self.dataset_creator.from_seq_objs_to_fasta()
        self.assertEqual(expected, len(result))

    def test_get_taxon_names_for_taxa_additional_fields(self):
        self.cleaned_data['taxon_names'] = ['SUPERFAMILY']
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = {
            'cp100-10': {'superfamily': 'Papilionoidea'},
            'cp100-11': {'superfamily': ''},
        }
        result = dataset_creator.get_taxon_names_for_taxa()

        self.assertEqual(expected, result)

    def test_get_sequence_first_codon_position(self):
        self.cleaned_data['positions'] = ['1st']
        self.cleaned_data['gene_codes'] = [Genes.objects.get(gene_code='wingless')]
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = Seq("CGGTGATAAAGCTATATGGAGACAAGATGAG")
        sequence = Seq("ACACGTCGACTCCGGCAAGTCCACCACCACCGGTCACTTGATTTACAAATGTGGTGGTATCGACAaACGTACCATCGAGAAGTTCGAGAAGGA")
        result = dataset_creator.get_sequence_based_on_codon_positions('wingless', sequence)
        self.assertEqual(expected, result)

    def test_get_sequence_second_codon_position(self):
        self.cleaned_data['positions'] = ['2nd']
        self.cleaned_data['gene_codes'] = [Genes.objects.get(gene_code='wingless')]
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = Seq("ATACGACCCCGATTAAGGGTAaGCTAATAAA")
        sequence = Seq("ACACGTCGACTCCGGCAAGTCCACCACCACCGGTCACTTGATTTACAAATGTGGTGGTATCGACAaACGTACCATCGAGAAGTTCGAGAAGGA")
        result = dataset_creator.get_sequence_based_on_codon_positions('wingless', sequence)
        self.assertEqual(expected, result)

    def test_get_sequence_third_codon_position(self):
        self.cleaned_data['positions'] = ['3rd']
        self.cleaned_data['gene_codes'] = [Genes.objects.get(gene_code='wingless')]
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = Seq("CCCCCGCCCCTCGTCATTTCCATCCGGCGG")
        sequence = Seq("ACACGTCGACTCCGGCAAGTCCACCACCACCGGTCACTTGATTTACAAATGTGGTGGTATCGACAaACGTACCATCGAGAAGTTCGAGAAGGA")
        result = dataset_creator.get_sequence_based_on_codon_positions('wingless', sequence)
        self.assertEqual(expected, result)

    def test_get_sequence_first_and_second_codon_position(self):
        self.cleaned_data['positions'] = ['1st', '2nd']
        self.cleaned_data['gene_codes'] = [Genes.objects.get(gene_code='wingless')]
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = Seq("CAGTGATCGGAATCACACACGGCATTATTAAATGGGGGATGAAaCGACATGAAATTGAAAGA")
        sequence = Seq("ACACGTCGACTCCGGCAAGTCCACCACCACCGGTCACTTGATTTACAAATGTGGTGGTATCGACAaACGTACCATCGAGAAGTTCGAGAAGGA")
        result = dataset_creator.get_sequence_based_on_codon_positions('wingless', sequence)
        self.assertEqual(expected, result)

    def test_get_sequence_first_and_third_codon_position(self):
        self.cleaned_data['positions'] = ['1st', '3rd']
        self.cleaned_data['gene_codes'] = [Genes.objects.get(gene_code='wingless')]
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = Seq("CCGCGCTCGCAGTCACACACGTCCTGATTCAATTGTGTACGCAACTACACGGAGTCGGAGG")
        sequence = Seq("ACACGTCGACTCCGGCAAGTCCACCACCACCGGTCACTTGATTTACAAATGTGGTGGTATCGACAaACGTACCATCGAGAAGTTCGAGAAGGA")
        result = dataset_creator.get_sequence_based_on_codon_positions('wingless', sequence)
        self.assertEqual(expected, result)

    def test_get_sequence_second_and_third_codon_position(self):
        self.cleaned_data['positions'] = ['2nd', '3rd']
        self.cleaned_data['gene_codes'] = [Genes.objects.get(gene_code='wingless')]
        dataset_creator = CreateDataset(self.cleaned_data)
        expected = Seq("ACTCACCCGCAGCCCCCCCCGTACTGTTACAAGTGTGTTCACaAGTCCTCAGAGTCAGAGA")
        sequence = Seq("ACACGTCGACTCCGGCAAGTCCACCACCACCGGTCACTTGATTTACAAATGTGGTGGTATCGACAaACGTACCATCGAGAAGTTCGAGAAGGA")
        result = dataset_creator.get_sequence_based_on_codon_positions('wingless', sequence)
        self.assertEqual(expected, result)
