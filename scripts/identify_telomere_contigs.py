
#!/usr/bin/env python3
"""
Identify candidate telomere-containing contigs from an assembled FASTA.

Requires: Biopython
Example:
    python scripts/identify_telomere_contigs.py bc2043.contigs.fa
"""

import argparse
from Bio import SeqIO


def count_max_repeats(sequence, motif):
    """Return the maximum number of consecutive perfect motif repeats."""
    i = 0
    count = 0
    max_count = 0
    motif_len = len(motif)

    while i <= len(sequence) - motif_len:
        if sequence[i:i + motif_len] == motif:
            count += 1
            i += motif_len
        else:
            max_count = max(max_count, count)
            count = 0
            i += 1

    return max(max_count, count)


def main():
    parser = argparse.ArgumentParser(
        description="Find candidate telomeric repeat runs at contig ends."
    )
    parser.add_argument("fasta_file", help="Input assembly FASTA")
    parser.add_argument("--min-repeats", type=int, default=10)
    parser.add_argument("--check-region", type=int, default=1000)
    args = parser.parse_args()

    repeat_fwd = "TTAGGC"
    repeat_rev = "GCCTAA"

    for record in SeqIO.parse(args.fasta_file, "fasta"):
        seq = str(record.seq).upper()
        contig_id = record.id
        contig_len = len(seq)

        start_seq = seq[:args.check_region]
        end_seq = seq[-args.check_region:]

        results = {
            "START forward": count_max_repeats(start_seq, repeat_fwd),
            "START reverse": count_max_repeats(start_seq, repeat_rev),
            "END forward": count_max_repeats(end_seq, repeat_fwd),
            "END reverse": count_max_repeats(end_seq, repeat_rev),
        }

        matches = {
            label: count
            for label, count in results.items()
            if count >= args.min_repeats
        }

        if matches:
            print(f"\nContig: {contig_id}")
            print(f"  Length: {contig_len} bp")
            for label, count in matches.items():
                print(f"  {label}: {count} consecutive repeats")


if __name__ == "__main__":
    main()
