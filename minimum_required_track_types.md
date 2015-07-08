#Minimum required track files and corresponding controlled vocabulary:

Track type: key in json hub correspinng to a possibly verbose description of the track e.g. "fractional_methylation_calls". 

Track tag: short name for track type in json hub for use with templating track description which may be length limited.

#Experiment:

## ChIP-Seq:
  
### Peak calls

- [Controlled vocaublary]: Track type: "peak_calls", Track tag: "peaks" 

### Signal/Coverage track
  
- [Controlled vocaublary]: Track type: "signal", Track tag: "sig"
  
## WGS (?):
  
### Copy number variation

- [Controlled vocaublary]: Track type: "copy_number_variation", Track tag: "cnv" 

## DNA Methylation:
  
### Fractional Methylation Calls 

*(alternatively some way of reporting #Cs vs #Ts on every CpG)*
  
- [Controlled vocaublary]: Track type: "fractional_methylation_calls", Track tag: "frc_mth"
  
### Coverage
  
- [Controlled vocaublary]: Track type: "coverage", Track tag: "cov"

## mRNA:
  
*(need agreement on how rpkm are computed)*
  
##*Strand specific:*
  
### rpkm values on positive strand 
  
- [Controlled vocaublary]: Track type: "rpkm_positive_strand", Track tag: "rpkm[pos]"
  
### rpkm values on negative strand 

- [Controlled vocaublary]: Track type: "rpkm_negative_strand", Track tag: "rpkm[neg]"
  
##*Unstranded:*

### rpkm values
  
- [Controlled vocaublary]: Track type: "rpkm", Track tag: "rpkm"
  
## smRNA (?) : 
  
### reads per million miRNA mapped ?

- [Controlled vocaublary]: Track type: "reads_per_million_miRNA_mapped", Track tag: "rpmmm"
