# Telomere_Assembly_pipeline
De Novo Genome assembly and telomere analysis pipeline for C. elegans long-read sequencing (PacBio)

## Pipeline Workflow

###  Input Data
PacBio HiFi CCS reads were obtained from the sequencing facility in BAM format.

Example input file:

```bash
m84165_250618_165658_s3.hifi_reads.bc2043.bam
### BAM to FASTQ Conversion

The input BAM file was converted to FASTQ format using `samtools fastq` for downstream analysis.

Example command:

```bash
samtools fastq -@ 8 m84165_250618_165658_s3.hifi_reads.bc2043.bam > bc2043.fastq

---

### Quality Control

Read quality was assessed using FastQC to evaluate read length distribution and sequencing quality.

Example command:

```bash
fastqc bc2043.fastq

---
### Genome Assembly

De novo genome assembly was performed using Hifiasm, which is optimized for PacBio HiFi reads.

Example command:

```bash
hifiasm -o bc2043.asm -t 32 bc2043.fastq

---
## Assembly Statistics

Assembly quality was evaluated using tools such as QUAST or seqkit.

Metrics include:
- N50
- total assembly size
- number of contigs


