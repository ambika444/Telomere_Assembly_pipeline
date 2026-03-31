#!/bin/bash
#SBATCH --job-name=hifiasm_bc2043
#SBATCH --output=logs/bc2043_%j.out
#SBATCH --error=logs/bc2043_%j.err
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=120G
#SBATCH --time=48:00:00

set -euo pipefail

module load anaconda/2024.02
source activate hifiasm_env

INPUT_DIR=/work/users/a/m/ambi/theta/genome_assembly/input
OUTPUT_DIR=/work/users/a/m/ambi/theta/genome_assembly/output/bc2043
INPUT_FILE=m84165_250618_165658_s3.hifi_reads.bc2043.fastq.gz
PREFIX=$OUTPUT_DIR/bc2043.asm

mkdir -p "$OUTPUT_DIR" logs

echo "[$(date)] Starting Hifiasm assembly"
echo "Input: $INPUT_DIR/$INPUT_FILE"
echo "Output prefix: $PREFIX"

hifiasm -o "$PREFIX" -t "$SLURM_CPUS_PER_TASK" "$INPUT_DIR/$INPUT_FILE"

echo "[$(date)] Assembly completed"
