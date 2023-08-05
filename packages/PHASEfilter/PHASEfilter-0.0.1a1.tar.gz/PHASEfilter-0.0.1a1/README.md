
[![License: MIT](https://img.shields.io/badge/License-MIT%20-blue.svg)]


# PHASEfilter
PHASEfilter is a software package that is possible to filter variants, SNPs and INDELs, that are present in heterozygous form, in phased genomes.

# Installation

This installation is oriented for Linux distributions.

### Install directly

```
$ pip install PHASEfilter
```

### Install with virtualenv

```
$ virtualenv PHASEfilter --python=python3 --prompt "(PHASEfilter version) "
$ . PHASEfilter/bin/activate
$ pip install PHASEfilter
```


The follow software must be available in your computer:
* [python3](https://www.python.org/downloads/)
* [minimpa2](https://github.com/lh3/minimap2) v2.0 or up
* [lastz](https://github.com/lastz/lastz) v1.4 or up
* [bcftools](http://www.htslib.org/download/) v1.3 or up
* [samtools](http://www.htslib.org/download/) v1.3 or up
* [htslib](http://www.htslib.org/download/) v1.3 or up
* [blastn](https://www.ncbi.nlm.nih.gov/books/NBK52640/) [Optional] v2.3 or up 


# All software available

## Filter variants in phased genomes

This software that can identify heterozygosity positions between two phased references.
The software starts by aligning pairs of diploid chromosomes, based on three different approaches, Minimap2, Lastz and Blastn summing the match positions and obtaining the percentage of effective alignment. The alignment software with a higher percentage is the one chosen for the synchronization of a specific chromosome. With synchronization done it is possible to identify the position of a variation, in both elements of a pair of chromosomes, allowing variants removal if it meets a following established criteria.
To classify variants it is necessary to pass two VCF files, one for each reference phase. After that, the PHASEfilter will go through the variants called in reference A and check if there are any homologous in the variants called in reference B. For each variant called in the reference A it can happen three situations: 1) both references, for the position in analysis, are equal and the variant is valid; 2) position is heterozygous in the reference and the variant reflects it, so the variant is removed.

```
$ phasefilter.py --help
$ phasefilter.py --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --vcf1 A-M_S4_chrA_filtered_snps.vcf.gz --vcf2 A-M_S4_chrB_filtered_snps.vcf.gz --out_vcf out_result.vcf.gz
```

## Synchronize annotation genomes

Synchronize annotations genomes adapting the annotations that are in reference 1 to the reference 2, adding the tags 'StartHit' and 'EndHit' to the result file. In VCF type files only add 'StartHit' tag in Info. The annotations, input file, need to be in VCF or GFF3, and belong to the reference 1.

```
$ synchronize_genomes.py --help
$ synchronize_genomes.py --ref1 S288C_reference.fna --ref2 S01.assembly.final.fa --gff S288C_reference.gff3 --out result.gff3 --pass_chr chrmt
$ synchronize_genomes.py --ref1 S288C_reference.fna --ref2 S01.assembly.final.fa --vcf S288C_reference.vcf.gz --out result.vcf.gz
```

## Best alignment

Create a list with the best algorithm to make the alignment between chromosomes.

```
$ best_alignment.py --help
$ best_alignment.py --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --out report.txt
$ best_alignment.py --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --out report.txt --pass_chr chrmt --out_alignment syncronizationSacharo
```

## Reference Statistics

With this application it is possible to obtain the number of nucleotides by chromosome.

```
$ reference_statistics.py --help
$ reference_statistics.py --ref some_fasta_file.fasta --out retport.txt
$ reference_statistics.py --ref Ca22chr1A_C_albicans_SC5314.fasta --out retport.txt
```

<!--
# Documentation
PHASEfilter documentation is available https://phasefilter.readthedocs.io/en/latest/
-->