#Minimum required track files:

This document aims at describing a minimum set of analysis tracks that should be provided for any dataset, for IHEC Core Assays. Other non-core assays are also described at the end of the document.

##IHEC Core Assays 

### ChIP-Seq Histone (H3K*):

* **Signal/Coverage** (Track type: "signal", Format: "bigWig")
* **Peak calls** (Track type: "peak_calls", Format: "bigBed")
  

### ChIP-Seq Input:
  
* **Signal/Coverage** (Track type: "signal", Format: "bigWig")
  

### DNA Methylation:
  
* **Fractional Methylation Calls**  (Track type: "methylation_profile")
*(alternatively some way of reporting #Cs vs #Ts on every CpG)*

* **Signal/Coverage** (Track type: "signal", Format: "bigWig")

  
### mRNA / total RNA :

* **Signal/Coverage** (Track type: "signal", Format: "bigWig")
or
* **rpkm values** (optional?) (Track type: "rpkm", Format: "bigWig")
*(need agreement on how rpkm are computed)*

  


##Non-core Assays
  
### smRNA-Seq: 
  
* **Signal/Coverage** (Track type: "signal", Format: "bigWig")
or
* **reads per million miRNA mapped** (optional?) (Track type: "reads_per_million_miRNA_mapped", Format: "bigWig")


### Whole Genome Sequencing:
  
* **Copy number variation** (Track type: "copy_number_variation", Format: "vcf")