# Minimum required track files:

This document aims at describing a minimum set of analysis tracks that should be provided for any dataset, for IHEC Core Assays. Other non-core assays are also described at the end of the document.

Please refer to the [tracks generation standards](./tracks_generation.md) for information on how to generate each track types.

## IHEC Core Assays 

#### ChIP-Seq Histone (H3K*):


| Track Type                     | Data Hub Identifier              | Format   | Mandatory   | Notes |
|--------------------------------|----------------------------------|:--------:|:-----------:|---------------------------------------|
| Signal/Coverage                | `signal_unstranded`              | bigWig   | Y           | |
| Peak calls                     | `peak_calls`                     | bigBed   | Y           | |
  

### ChIP-Seq Input:

| Track Type                     | Data Hub Identifier              | Format   | Mandatory   | Notes |
|--------------------------------|----------------------------------|:--------:|:-----------:|-------|
| Signal/Coverage                | `signal_unstranded`              | bigWig   | Y           | |

  
### DNA Methylation:

| Track Type                 | Data Hub Identifier                  | Format    | Mandatory   | Notes |
|----------------------------|--------------------------------------|:---------:|:-----------:|----------------------------------|
| Fractional Methylation Calls | `methylation_profile`              | bigWig    | Y           | Needs to be formally specified, reports #Cs vs #Ts at each CpG site. See current proposal [here](./Fractional_Methylation_Proposal.md).|
| Signal/Coverage              | `signal_unstranded` OR `signal_forward`, `signal_reverse` | bigWig |  Y         | Raw coverage over CpGs as a measure of confidence in Fractional Methtylation Calls. See current proposal [here](./Fractional_Methylation_Proposal.md).|


### mRNA / total RNA :

#### For strand specific signal:
| Track Type                     | Data Hub Identifier          | Format   | Mandatory | Notes |
|--------------------------------|------------------------------|:--------:|:---------:|---------------------------------|
| Signal/Coverage forward strand | `signal_forward`             | bigWig   | Y         | |
| Signal/Coverage reverse strand | `signal_reverse`             | bigWig   | Y         | |
| RPKM on positive strand        | `rpkm_forward`               | bigWig   |           | Computation needs to be standardized. Proposal available [here](https://github.com/IHEC/ihec-assay-standards/blob/master/RNA_Seq_normalization.md). |
| RPKM on negative strand        | `rpkm_reverse`               | bigWig   |           | Computation needs to be standardized. Proposal available [here](https://github.com/IHEC/ihec-assay-standards/blob/master/RNA_Seq_normalization.md). |


 


#### For single stranded signal:

| Track Type                     | Data Hub Identifier              | Format   | Mandatory | Notes |
|--------------------------------|----------------------------------|:--------:|:---------:|-------------------------------|
| Signal/Coverage                | `signal_unstranded`              | bigWig   | Y         | |
| RPKM                           | `rpkm_unstranded`                | bigWig   |           | Computation needs to be standardized. Proposal available [here](https://github.com/IHEC/ihec-assay-standards/blob/master/RNA_Seq_normalization.md). |




## Non-core Assays
  
### smRNA-Seq signal: 

| Track Type                     | Data Hub Identifier               | Format   | Mandatory | Notes |
|--------------------------------|-----------------------------------|:--------:|:---------:|-------------------------------|
| Signal/Coverage                | `signal_unstranded`               | bigWig   | Y         |                                      |
| Reads per million miRNA mapped | `reads_per_million_ miRNA_mapped` | bigWig   |           | Computation needs to be standardized |



### Whole Genome Sequencing:

| Track Type                     | Data Hub Identifier              | Format   | Mandatory  | Notes |
|--------------------------------|----------------------------------|:--------:|:----------:|-------|
| Copy Number Variation          | `copy_number_variation`          | bigWig   | Y          | |



### ATAC-Seq: 

| Track Type                     | Data Hub Identifier              | Format   | Mandatory  | Notes |
|--------------------------------|----------------------------------|:--------:|:----------:|-------|
| Signal/Coverage                | `signal_unstranded`              | bigWig   | Y          | |
| Peak calls                     | `peak_calls`                     | bigBed   | Y          | |
