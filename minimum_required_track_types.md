#Minimum required track files:

This document aims at describing a minimum set of analysis tracks that should be provided for any dataset, for IHEC Core Assays. Other non-core assays are also described at the end of the document.

##IHEC Core Assays 

### ChIP-Seq Histone (H3K*):

* Signal/Coverage
  - Track type: "signal", Format: "bigWig"
* Peak calls
  - Track type: "peak_calls", Format: "bigBed"
  

### ChIP-Seq Input:
  
* Signal/Coverage
  - Track type: "signal", Format: "bigWig"
  
### DNA Methylation:

* Fractional Methylation Calls (needs to be formally specified, intended as a way of reporting #Cs vs #Ts on every CpG, currently a track with values between 0-10)
  - Track type: "methylation_profile", Format: bigWig 

* Signal/Coverage (raw coverage over CpGs as a measure of confidence in Fractional Methtylation Calls)

  - Track type: "signal", Format: "bigWig"

### mRNA / total RNA :

* Expression
 
#### For strand specific: 
  - [Computation needs to be standardized] rpkm_positive_strand 
  - [Computation needs to be standardized] rpkm_negative_strand

#### For single stranded:

  - [Computation needs to be standardized] rpkm_unstranded

##Non-core Assays
  
### smRNA-Seq: 

* Expression

  - [Computation needs to be standardized] reads per million miRNA mapped** 
  
    * Track type: "reads_per_million_miRNA_mapped", Format: "bigWig"

  - [Optional] Signal/Coverage
  
    * Track type: "signal", Format: "bigWig"

### Whole Genome Sequencing:

* [Optional] Copy Number Variation
 
  - Copy number variation
  
    * Track type: "copy_number_variation", Format: "bigWig"
