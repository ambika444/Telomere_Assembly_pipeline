 for bam in *.bam; do
  [[ -e "$bam" ]] || { echo "No .bam files found in $(pwd)"; exit 1; }

  sample="${bam#PBI23607_pass_}"
  sample="${sample%_22b5deaa_00000000_0.bam}"

  out="Analysis/Fastq_files/${sample}.fastq.gz"

  echo "[$(date)] Converting $bam -> $out" | tee -a logs/bam2fastq.log

  samtools fastq -@ 16 "$bam" | gzip > "${out}.tmp" \
    && mv "${out}.tmp" "$out"

  gzip -t "$out" || { echo "ERROR: gzip test failed for $out"; exit 1; }
done
