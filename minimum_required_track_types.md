#Minimum required track files:

This document aims at describing a minimum set of analysis tracks that should be provided for any dataset, for IHEC Core Assays. Other non-core assays are also described at the end of the document.

##IHEC Core Assays 

#### ChIP-Seq Histone (H3K*):


| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| Signal/Coverage                | `signal`                         | bigWig | ✓         | |
| Peak calls                     | `peak_calls`                     | bigBed | ✓         | |
  

### ChIP-Seq Input:

| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| Signal/Coverage                | `signal`                         | bigWig | ✓         | |

  
### DNA Methylation:

| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| Fractional Methylation Calls   | `methylation_profile`            | bigWig | ✓         | Needs to be formally specified, intended as a way of reporting #Cs vs #Ts on every CpG, currently a track with values between 0-10 |
| Signal/Coverage                | `signal` OR `signal_forward`,`signal_reverse` | bigWig |  ✓         | Raw coverage over CpGs as a measure of confidence in Fractional Methtylation Calls |


### mRNA / total RNA :

#### For strand specific signal:
| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| RPKM on positive strand        | `rpkm_positive_strand`           | bigWig | ?        | Computation needs to be standardized |
| RPKM on negative strand        | `rpkm_negative_strand`           | bigWig | ?        | Computation needs to be standardized |
| Signal/Coverage forward strand | `signal_forward`                 | bigWig | ?        | |
| Signal/Coverage reverse strand | `signal_reverse`                 | bigWig | ?        | |

 


#### For single stranded signal:

| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| RPKM                           | `rpkm_unstranded`                | bigWig | ?         |Computation needs to be standardized |
| Signal/Coverage                | `signal`                         | bigWig | ?        | Computation needs to be standardized |



##Non-core Assays
  
### smRNA-Seq signal: 

| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| Reads per million miRNA mapped | `reads_per_million_miRNA_mapped` | bigWig | ?         | Computation needs to be standardized |
| Signal/Coverage                | `signal`                         | bigWig | ?         | |



### Whole Genome Sequencing:

| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| Copy Number Variation          | `copy_number_variation`          | bigWig |           | |



### ATAC-Seq: 

| Track Type                     | Data Hub Identifier              | Format | Mandatory | Notes |
|--------------------------------|----------------------------------|--------|-----------|-------|
| Signal/Coverage                | `signal`                         | bigWig | ✓         | |
| Peak calls                     | `peak_calls`                     | bigBed | ✓         | |
