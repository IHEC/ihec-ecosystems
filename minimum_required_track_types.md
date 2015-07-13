#Attributes, using controlled vocabulary

Rules:

- For each assay, a track should be unique for a type/strand combination. (e.g. not having two peak files, or two coverage tracks on the forward strand)
- If a track is stranded, the opposite strand track also needs to be provided.

**Track type**: key in json hub corresponding to a possibly verbose description of the track. e.g. "fractional_methylation_calls".

**Track tag**: short name for track type in json hub for use with templating track description which may be length limited.

**Strand**: "forward", "reverse", "unstranded"

**Format**: "bigWig", "bigBed", "bam"


#Minimum required track files, per experiment:

## ChIP-Seq:
  
### Peak calls

- [Controlled vocabulary]: Track type: "peak_calls", Track tag: "peaks" 

### Signal/Coverage track
  
- [Controlled vocabulary]: Track type: "signal", Track tag: "sig"
  
## WGS (?):
  
### Copy number variation

- [Controlled vocabulary]: Track type: "copy_number_variation", Track tag: "cnv" 

## DNA Methylation:
  
### Fractional Methylation Calls 

*(alternatively some way of reporting #Cs vs #Ts on every CpG)*
  
- [Controlled vocabulary]: Track type: "fractional_methylation_calls", Track tag: "frc_mth"
  
### Signal
  
- [Controlled vocabulary]: Track type: "signal", Track tag: "sig"

## mRNA:

### signal

- [Controlled vocabulary]: Track type: "signal", Track tag: "sig"

### rpkm values (optional?)

*(need agreement on how rpkm are computed)*

- [Controlled vocabulary]: Track type: "rpkm", Track tag: "rpkm"
  
## smRNA (?) : 
  
### signal

- [Controlled vocabulary]: Track type: "signal", Track tag: "sig"  

### reads per million miRNA mapped (optional?)

- [Controlled vocabulary]: Track type: "reads_per_million_miRNA_mapped", Track tag: "rpmmm"
