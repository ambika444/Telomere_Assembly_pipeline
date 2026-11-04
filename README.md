# PacBio HiFi Genome Assembly and Telomere Analysis in *C. elegans*

An end-to-end bioinformatics workflow for processing PacBio HiFi sequencing data, performing de novo genome assembly, and investigating telomeric sequence variation in *Caenorhabditis elegans*.

## Project Overview

Long-read sequencing technologies such as PacBio HiFi provide opportunities to investigate repetitive genomic regions that are difficult to resolve using short-read sequencing.

This repository documents a practical genome assembly and downstream analysis workflow developed during research on *C. elegans* telomeres.

The goal is to provide a reproducible example for researchers and students interested in long-read sequencing, genome assembly, high-performance computing, and telomere biology.

## Biological Question

How can PacBio HiFi genome assemblies be used to identify chromosome-end telomeric sequences and characterize variation within the canonical TTAGGC repeat?

## Analysis Workflow

**PacBio HiFi BAM → FASTQ conversion → Read quality control → De novo assembly → Assembly statistics → Telomere identification → Sequence variation analysis**

## 1. Input Data

PacBio HiFi circular consensus sequencing (CCS) reads were obtained from a sequencing facility in BAM format.

Example input:

`m84165_250618_165658_s3.hifi_reads.bc2043.bam`

Large sequencing files are not included in this repository.

## 2. BAM to FASTQ Conversion

PacBio HiFi BAM files were converted to compressed FASTQ format using Samtools.

The conversion script supports batch processing of BAM files and includes logging and gzip integrity checks.

**Script:** [bam_to_fastq.sh](scripts/bam_to_fastq.sh)

Example command:

    samtools fastq -@ 16 input.bam | gzip > output.fastq.gz

## 3. Read Quality Control

Sequencing read quality was assessed using FastQC. Additional read statistics were generated using SeqKit.

The following metrics can be evaluated:

- Total number of reads
- Total sequencing bases
- Minimum and maximum read lengths
- Mean read length
- Read length N50
- Read quality distributions

**Scripts:**

- [run_fastqc.sh](scripts/run_fastqc.sh)
- [basic_stats.sh](scripts/basic_stats.sh)

Example commands:

    fastqc input.fastq.gz

    seqkit stats -a input.fastq.gz

Read length N50 describes the input reads and should not be confused with assembly contig N50.

## 4. De Novo Genome Assembly

PacBio HiFi reads were assembled using Hifiasm on the University of North Carolina at Chapel Hill Longleaf high-performance computing cluster.

Assembly jobs were managed using SLURM.

### Computational resources

| Parameter | Setting |
|---|---|
| Cluster | UNC Longleaf |
| Assembler | Hifiasm |
| Partition | general |
| Nodes | 1 |
| Tasks | 1 |
| CPUs per task | 32 |
| Memory | 120 GB |
| Time limit | 48 hours |
| Environment | Anaconda 2024.02 / hifiasm_env |

**Script:** [run_hifiasm_longleaf.sh](scripts/run_hifiasm_longleaf.sh)

Example Hifiasm command:

    hifiasm -o assembly/bc2043 -t 32 input.fastq.gz

Hifiasm produces assembly graph files in GFA format. Primary contig sequences can be extracted and converted to FASTA for downstream analysis.

## 5. Assembly Evaluation

Genome assembly statistics can be calculated from the assembled contigs.

Metrics of interest include:

- Total assembly length
- Number of contigs
- Longest contig
- Contig N50 and L50
- Contig N90 and L90

Example:

    seqkit stats -a assembly.fasta

Assembly statistics and example outputs will be added as the repository documentation develops.

## 6. Telomere Identification and Analysis

The downstream workflow focuses on identifying and characterizing telomeric DNA sequences in assembled *C. elegans* chromosomes.

The canonical telomeric repeat is:

`TTAGGC`

The analysis includes identification of telomere-containing contigs, extraction of chromosome-end regions, measurement of telomeric tract length, and characterization of noncanonical repeat sequences.

Custom analysis scripts and examples will be documented in this section.

## Repository Structure

    Telomere_Assembly_pipeline/
    ├── README.md
    └── scripts/
        ├── bam_to_fastq.sh
        ├── run_fastqc.sh
        ├── basic_stats.sh
        └── run_hifiasm_longleaf.sh

Additional example results, figures, and downstream telomere analysis scripts will be added as they become available for sharing.

## Reproducibility

The scripts document computational steps performed on a SLURM-managed HPC system. Users should adapt input paths, software environments, and computational resources to their own systems.
