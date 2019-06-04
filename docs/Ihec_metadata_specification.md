# IHEC Metadata Specification (version 1.0)

## Introduction
The IHEC metadata standards are extension of the standards used by the Roadmap Epigenomics Project. Please refer to Sections 1 and 2 of original specification (archived at https://github.com/IHEC/ihec-metadata/blob/master/specs/original_docs/IHEC-Metadata.pdf) for the data and metadata model.

This document describes metadata elements extending the __SRA XML Schema 1.2__. The core SRA XML elements are augmented by additional attributes defined for purposes of the NIH Roadmap Epigenomics as described in the official IHEC ecosystem repository.

Documentation for the core SRA XML elements is here: [http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=doc](http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=doc)

The SRA XML schemas are here: [http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=xml_schemas](http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=xml_schemas)

## How to define multiple values per metadata tag

The same attribute may be used multiple times in a single XML record. This may be most useful, for example, for supplying URIs to multiple ontologies or for supplying multiple references to a single ontology such as in the case of DISEASE_ONTOLOGY_URI. For example, describing a brain primary tissue using ontology terms for ('Brodmann (1909) area 8', 'Brodmann (1909) area 9') would be:

```
<SAMPLE_ATTRIBUTE>
    <TAG>SAMPLE_ONTOLOGY_URI</TAG>
    <VALUE>http://purl.obolibrary.org/obo/UBERON_0013539</VALUE>
</SAMPLE_ATTRIBUTE>
<SAMPLE_ATTRIBUTE>
    <TAG>SAMPLE_ONTOLOGY_URI</TAG>
    <VALUE>http://purl.obolibrary.org/obo/UBERON_0013540</VALUE>
</SAMPLE_ATTRIBUTE>
```

## Ontologies

__Only__ terms from following ontologies are acceptable for annotating the metadata:

Field __SAMPLE_ONTOLOGY_URI__:
* Cell Lines: Experimental Factor Ontology (__EFO__ - [https://www.ebi.ac.uk/efo/](https://www.ebi.ac.uk/efo/))
* Primary Cells: Cell Ontology (__CL__ - [http://cellontology.org](http://cellontology.org))
* Primary Tissue: Uberon (__UBERON__ - [http://uberon.org](http://uberon.org))

Fields __DISEASE_ONTOLOGY_URI__ and __DONOR_HEALTH_STATUS_ONTOLOGY_URI__:
* NCI Metathesaurus (__NCIM__ - [https://ncim.nci.nih.gov/ncimbrowser/](https://ncim.nci.nih.gov/ncimbrowser/))

Field __EXPERIMENT_ONTOLOGY_URI__:
* Ontology for Biomedical Investigations (__OBI__ - [http://obi-ontology.org/](http://obi-ontology.org/))

Field __MOLECULE_ONTOLOGY_URI__:
* Sequence Ontology (__SO__ - [http://www.sequenceontology.org/](http://www.sequenceontology.org/)) 

Tags with controlled vocabularies are labelled as "Controlled Vocabulary".

Tags with ontologies are labelled as "Ontology".

# SAMPLES

###### Note for metadata resubmission

In order to pass IHEC metadata validation, all datasets submitted prior to 2018 must include all sample properties defined within each specific BIOMATERIAL_TYPE below.

## Cell Line

__SAMPLE_ONTOLOGY_URI__ - (Ontology: EFO) Links to sample ontology information.

__DISEASE_ONTOLOGY_URI__ - (Ontology: NCIM) Links to sample disease ontology information. This attribute reflects the disease for this particular sample, not the donor health condition. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) and/or in the free form DISEASE attribute.

__DISEASE:__ - Free form field for more specific sample disease information. This property reflects the disease for this particular sample, not the donor health condition.

__BIOMATERIAL_PROVIDER__ - The name of the company, laboratory or person that provided the biological material.

__BIOMATERIAL_TYPE:__ - (Controlled Vocabulary) "Cell Line".

__LINE__ - The name of the cell line.

__LINEAGE__ - The developmental lineage to which the cell line belongs.

__DIFFERENTIATION_STAGE__ - The stage in cell differentiation to which the cell line belongs.

__DIFFERENTIATION_METHOD__ - The protocol used to differentiation the cell line.

__PASSAGE__ - The number of times the cell line has been re-plated and allowed to grow back to confluency or to some maximum density, if using suspension cultures.

__MEDIUM__ - The medium in which the cell line has been grown.

__SEX:__ - (Controlled Vocabulary) "Male", "Female", "Unknown", or "Mixed" for pooled samples.

__BATCH__ - The batch from which the cell line is derived. Primarily applicable to initial H1 cell line batches. NA if not applicable.

## Primary Cell

__SAMPLE_ONTOLOGY_URI__ - (Ontology: CL) links to sample ontology information.

__DISEASE_ONTOLOGY_URI__ - (Ontology: NCIM) Links to sample disease ontology information. This attribute reflects the disease for this particular sample, not the donor health condition. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) and/or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

__DISEASE:__ - Free form field for more specific sample disease information. This property reflects the disease for this particular sample, not the donor health condition. If dealing with a rare disease, please consider identifiability issues.

__BIOMATERIAL_PROVIDER__ - The name of the company, laboratory or person that provided the biological material.

__BIOMATERIAL_TYPE:__ - (Controlled Vocabulary) "Primary Cell".

__ORIGIN_SAMPLE_ONTOLOGY_URI__ - (Ontology: UBERON) Links to the origin tissue from which the sample was extracted.

__ORIGIN_SAMPLE__ - Description of the origin tissue from which the sample was extracted.

__CELL_TYPE__ - The type of cell.

__MARKERS__ - Markers used to isolate and identify the cell type.

__DONOR_ID__ - An identifying designation for the donor that provided the primary cell.

__DONOR_AGE__ - The age of the donor that provided the primary cell. NA if not available. If over 90 years enter as "90+". If entering a range of ages use the format "{age}-{age}".

__DONOR_AGE_UNIT__ - (Controlled Vocabulary) "year", "month", "week", or "day".

__DONOR_LIFE_STAGE__ - (Controlled Vocabulary) "fetal", "newborn", "child", "adult", "unknown", "embryonic", "postnatal".

__DONOR_HEALTH_STATUS_ONTOLOGY_URI__ - (Ontology: NCIM) Links to the health status of the donor that provided the primary cell. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) or in the free form DISEASE attribute. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". If dealing with a rare disease, please consider identifiability issues.

__DONOR_HEALTH_STATUS__ - The health status of the donor that provided the primary cell. NA if not available.

__DONOR_SEX__ - (Controlled Vocabulary) "Male", "Female", "Unknown", or "Mixed" for pooled samples.

__DONOR_ETHNICITY__ - The ethnicity of the donor that provided the primary cell. NA if not available. If dealing with small/vulnerable populations consider identifiability issues.

__PASSAGE_IF_EXPANDED__ - If the primary cell has been expanded, the number of times the primary cell has been re-plated and allowed to grow back to confluency or to some maximum density if using suspension cultures. NA if no expansion.

## Primary Cell Culture

__SAMPLE_ONTOLOGY_URI__ - (Ontology: CL) Links to sample ontology information.

__DISEASE_ONTOLOGY_URI__ - (Ontology: NCIM) Links to sample disease ontology information. This attribute reflects the disease for this particular sample, not the donor health condition. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) and/or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

__DISEASE__ - Free form field for more specific sample disease information. This property reflects the disease for this particular sample, not the donor health condition. If dealing with a rare disease, please consider identifiability issues.

__BIOMATERIAL_PROVIDER__ - The name of the company, laboratory or person that provided the biological material.

__BIOMATERIAL_TYPE__ - (Controlled Vocabulary) "Primary Cell Culture".

__ORIGIN_SAMPLE_ONTOLOGY_URI__ - (Ontology: UBERON) links to the origin tissue from which the sample was extracted.

__ORIGIN_SAMPLE__ - Description of the origin tissue from which the sample was extracted.

__CELL_TYPE__ - The type of cell.

__MARKERS__ - Markers used to isolate and identify the cell type.

__CULTURE_CONDITIONS__ - The conditions under which the primary cell was cultured.

__DONOR_ID__ - An identifying designation for the donor that provided the primary cell.

__DONOR_AGE__ - The age of the donor that provided the primary cell. NA if not available. If over 90 years enter as "90+". If entering a range of ages use the format "{age}-{age}".

__DONOR_AGE_UNIT__ - (Controlled Vocabulary) "year", "month", "week", or "day".

__DONOR_LIFE_STAGE__ - (Controlled Vocabulary) "fetal", "newborn", "child", "adult", "unknown", "embryonic", "postnatal"

__DONOR_HEALTH_STATUS_ONTOLOGY_URI__ - (Ontology: NCIM) Links to the health status of the donor that provided the primary cell. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

__DONOR_HEALTH_STATUS__ - The health status of the donor that provided the primary cell. NA if not available.

__DONOR_SEX__ - (Controlled Vocabulary) "Male", "Female", "Unknown", or "Mixed" for pooled samples.

__DONOR_ETHNICITY__ - The ethnicity of the donor that provided the primary cell. NA if not available. If dealing with small/vulnerable populations consider identifiability issues.

__PASSAGE_IF_EXPANDED__ - If the primary cell culture has been expanded, the number of times the cell culture has been re-plated and allowed to grow back to confluency or to some maximum density if using suspension cultures. NA if no expansion.

## Primary Tissue

__SAMPLE_ONTOLOGY_URI__ - (Ontology: UBERON) Links to sample ontology information.

__DISEASE_ONTOLOGY_URI__ - (Ontology: NCIM) Links to sample disease ontology information. This attribute reflects the disease for this particular sample, not the donor health condition. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) and/or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

__DISEASE:__ - Free form field for more specific sample disease information. This property reflects the disease for this particular sample, not for the donor health condition. If dealing with a rare disease, please consider identifiability issues.

__BIOMATERIAL_PROVIDER__ - The name of the company, laboratory or person that provided the biological material.

__BIOMATERIAL_TYPE:__ - (Controlled Vocabulary) "Primary Tissue".

__TISSUE_TYPE__ - The type of tissue.

__TISSUE_DEPOT__ - Details about the anatomical location from which the primary tissue was collected.

__COLLECTION_METHOD__ - The protocol for collecting the primary tissue.

__DONOR_ID__ - An identifying designation for the donor that provided the primary tissue.

__DONOR_AGE__ - The age of the donor that provided the primary tissue. NA if not available. If over 90 years enter as "90+". If entering a range of ages use the format "{age}-{age}".

__DONOR_AGE_UNIT__ - (Controlled Vocabulary) "year", "month", "week", or "day".

__DONOR_LIFE_STAGE__ - (Controlled Vocabulary) "fetal", "newborn", "child", "adult", "unknown", "embryonic", "postnatal"

__DONOR_HEALTH_STATUS_ONTOLOGY_URI__ - (Ontology: NCIM) Links to the health status of the donor that provided the primary cell. The NCImetathesaurus term C0277545 "Disease type AND/OR category unknown" should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 "None". Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_URIs (if available) or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

__DONOR_HEALTH_STATUS__ - The health status of the donor that provided the primary tissue. NA if not available.

__DONOR_SEX__ - (Controlled Vocabulary) "Male", "Female", "Unknown", or "Mixed" for pooled samples.

__DONOR_ETHNICITY__ - The ethnicity of the donor that provided the primary tissue. NA if not available. If dealing with small/vulnerable populations consider identifiability issues.


# EXPERIMENTS

###### Note for metadata resubmission
In order to pass IHEC metadata validation, all datasets submitted prior to 2018 __must__ include the following properties:

* LIBRARY_STRATEGY
* EXPERIMENT_TYPE or EXPERIMENT_ONTOLOGY_URI
* MOLECULE or MOLECULE_ONTOLOGY_URI, either defined in the experiment or sample object. Because of the complexity to validate the presence of this field in either object, this requirement will be validated at the time of submission to EpiRR.

###### Common fields

All experiments types include these fields:

__EXPERIMENT_TYPE__ - (Controlled Vocabulary) The assay target (e.g. ‘DNA Methylation’, ‘mRNA-Seq’, ‘smRNA-Seq’, 'Histone H3K4me1').

__EXPERIMENT_ONTOLOGY_URI__ - (Ontology: OBI) links to experiment ontology information.

__LIBRARY_STRATEGY__ - (Controlled Vocabulary) The assay used. These are defined within the SRA metadata specifications with a controlled vocabulary (e.g. ‘Bisulfite-Seq’, ‘RNA-Seq’, ‘ChIP-Seq’). For a complete list, see [https://www.ebi.ac.uk/ena/submit/reads-library-strategy](https://www.ebi.ac.uk/ena/submit/reads-library-strategy).

__MOLECULE_ONTOLOGY_URI__ - (Ontology: SO) links to molecule ontology information.

__MOLECULE__ - (Controlled Vocabulary) The type of molecule that was extracted from the biological material. Include one of the following: total RNA, polyA RNA, cytoplasmic RNA, nuclear RNA, small RNA, genomic DNA, protein, or other.


## Chromatin Accessibility

__EXPERIMENT_TYPE:__ (Controlled Vocabulary) 'Chromatin Accessibility'.

__EXPERIMENT_ONTOLOGY_URI:__ (Ontology: OBI) http://purl.obolibrary.org/obo/OBI_0002039, 'http://purl.obolibrary.org/obo/OBI_0001853' or any of its subclasses.

__LIBRARY_STRATEGY:__ (Controlled Vocabulary) 'ATAC-Seq', 'DNase-Hypersensitivity'.

__MOLECULE_ONTOLOGY_URI:__ (Ontology: SO) 'http://purl.obolibrary.org/obo/SO_0000991' or any of its subclasses.

__MOLECULE:__ (Controlled Vocabulary) 'genomic DNA'.

__EXTRACTION_PROTOCOL__ - The protocol used to isolate the extract material.

__EXPERIMENT_PROTOCOL__ - The protocol used for library preparation (e.g. DNAse treatment, transposase treatment, etc.).

## WGBS (NOTE: this is a new name to be used instead of Bisulfite-Seq )

__EXPERIMENT_TYPE:__ (Controlled Vocabulary) 'DNA Methylation'.

__EXPERIMENT_ONTOLOGY_URI:__ (Ontology: OBI) 'http://purl.obolibrary.org/obo/OBI_0001863' or any of its subclasses.

__LIBRARY_STRATEGY:__ (Controlled Vocabulary) 'Bisulfite-Seq'.

__MOLECULE_ONTOLOGY_URI:__ (Ontology: SO) 'http://purl.obolibrary.org/obo/SO_0000991' or any of its subclasses.

__MOLECULE:__ (Controlled Vocabulary) 'genomic DNA'.

__EXTRACTION_PROTOCOL__ - The protocol used to isolate the extract material.

__EXTRACTION_PROTOCOL_TYPE_OF_SONICATOR__ - The type of sonicator used for extraction.

__EXTRACTION_PROTOCOL_SONICATION_CYCLES__ - The number of sonication cycles used for extraction.

__DNA_PREPARATION_INITIAL_DNA_QNTY__ - The initial DNA quantity used in preparation.

__DNA_PREPARATION_FRAGMENT_SIZE_RANGE__ - The DNA fragment size range used in preparation.

__DNA_PREPARATION_ADAPTOR_SEQUENCE__ - The sequence of the adaptor used in preparation.

__DNA_PREPARATION_ADAPTOR_LIGATION_PROTOCOL__ - The protocol used for adaptor ligation.

__DNA_PREPARATION_POST-LIGATION_FRAGMENT_SIZE_SELECTION__ - The fragment size selection after adaptor ligation.

__BISULFITE_CONVERSION_PROTOCOL__ - The bisulfite conversion protocol.

__BISULFITE_CONVERSION_PERCENT__ - The bisulfite conversion percent and how it was determined.

__LIBRARY_GENERATION_PCR_TEMPLATE_CONC__ - The PCR template concentration for library generation.

__LIBRARY_GENERATION_PCR_POLYMERASE_TYPE__ - The PCR polymerase used for library generation

__LIBRARY_GENERATION_PCR_THERMOCYCLING_PROGRAM__ - The thermocycling program used for library generation.

__LIBRARY_GENERATION_PCR_NUMBER_CYCLES__ - The number of PCR cycles used for library generation.

__LIBRARY_GENERATION_PCR_F_PRIMER_SEQUENCE__ - The sequence of the PCR forward primer used for library generation.

__LIBRARY_GENERATION_PCR_R_PRIMER_SEQUENCE__ - The sequence of the PCR reverse primer used for library generation.

__LIBRARY_GENERATION_PCR_PRIMER_CONC__ - The concentration of the PCR primers used for library generation.

__LIBRARY_GENERATION_PCR_PRODUCT_ISOLATION_PROTOCOL__ - The protocol for isolating PCR products used for library generation.

## MeDIP-Seq

__EXPERIMENT_TYPE:__ (Controlled Vocabulary) 'DNA Methylation'.

__EXPERIMENT_ONTOLOGY_URI:__ (Ontology: OBI) 'http://purl.obolibrary.org/obo/OBI_0000693' or any of its subclasses.

__LIBRARY_STRATEGY:__ (Controlled Vocabulary) 'MeDIP-Seq'.

__MOLECULE_ONTOLOGY_URI:__ (Ontology: SO) 'http://purl.obolibrary.org/obo/SO_0000991' or any of its subclasses.

__MOLECULE:__ (Controlled Vocabulary) 'genomic DNA'.

__EXTRACTION_PROTOCOL__ - The protocol used to isolate the extract material.

__EXTRACTION_PROTOCOL_TYPE_OF_SONICATOR__ - The type of sonicator used for extraction.

__EXTRACTION_PROTOCOL_SONICATION_CYCLES__ - The number of sonication cycles used for extraction.

__MeDIP_PROTOCOL__ - The MeDIP protocol used.

__MeDIP_PROTOCOL_DNA_AMOUNT__ - The amount of DNA used in the MeDIP protocol.

__MeDIP_PROTOCOL_BEAD_TYPE__ - The type of bead used in the MeDIP protocol.

__MeDIP_PROTOCOL_BEAD_AMOUNT__ - The amount of beads used in the MeDIP protocol.

__MeDIP_PROTOCOL_ANTIBODY_AMOUNT__ - The amount of antibody used in the MeDIP protocol.

__MeDIP_ANTIBODY__ - The specific antibody used in the MeDIP protocol.

__MeDIP_ANTIBODY_PROVIDER__ - The name of the company, laboratory or person that provided the antibody.

__MeDIP_ANTIBODY_CATALOG__ - The catalog from which the antibody was purchased.

__MeDIP_ANTIBODY_LOT__ - The lot identifier of the antibody.

## MRE-Seq

__EXPERIMENT_TYPE:__ (Controlled Vocabulary) 'DNA Methylation'.

__EXPERIMENT_ONTOLOGY_URI:__ (Ontology: OBI) 'http://purl.obolibrary.org/obo/OBI_0001861' or any of its subclasses.

__LIBRARY_STRATEGY:__ - (Controlled Vocabulary) 'MRE-Seq'.

__MOLECULE_ONTOLOGY_URI:__ (Ontology: SO) 'http://purl.obolibrary.org/obo/SO_0000991' or any of its subclasses.

__MOLECULE:__ (Controlled Vocabulary) 'genomic DNA'.

__MRE_PROTOCOL__ - The MRE protocol.

__MRE_PROTOCOL_CHROMATIN_AMOUNT__ - The amount of chromatin used in the MRE protocol.

__MRE_PROTOCOL_RESTRICTION_ENZYME__ - The restriction enzyme(s) used in the MRE protocol.

__MRE_PROTOCOL_SIZE_FRACTION__ - The size of the fragments selected in the MRE protocol.

## ChIP-Seq

__EXPERIMENT_TYPE:__ (Controlled Vocabulary) one of ('ChIP-Seq Input','Histone H3K4me1','Histone H3K4me3','Histone H3K9me3','Histone H3K9ac','Histone H3K27me3','Histone H3K36me3', etc.).

__EXPERIMENT_ONTOLOGY_URI:__ (Ontology: OBI) 'http://purl.obolibrary.org/obo/OBI_0000716' or any of its subclasses.

__LIBRARY_STRATEGY:__ (Controlled Vocabulary) 'ChIP-Seq'.

__MOLECULE_ONTOLOGY_URI:__ (Ontology: SO) 'http://purl.obolibrary.org/obo/SO_0000991' or any of its subclasses.

__MOLECULE:__ (Controlled Vocabulary) 'genomic DNA'.

__EXTRACTION_PROTOCOL__ - The protocol used to isolate the extract material.

__EXTRACTION_PROTOCOL_TYPE_OF_SONICATOR__ - The type of sonicator used for extraction.

__EXTRACTION_PROTOCOL_SONICATION_CYCLES__ - The number of sonication cycles used for extraction.

__CHIP_PROTOCOL__ - The ChIP protocol used, or 'Input'.

__CHIP_PROTOCOL_CHROMATIN_AMOUNT__ - The amount of chromatin used in the ChIP protocol.

__CHIP_PROTOCOL_BEAD_TYPE__ - The type of bead used in the ChIP protocol. Leave empty for 'ChIP-Seq Input'.

__CHIP_PROTOCOL_BEAD_AMOUNT__ - The amount of beads used in the ChIP protocol. Leave empty for 'ChIP-Seq Input'.

__CHIP_PROTOCOL_ANTIBODY_AMOUNT__ - The amount of antibody used in the ChIP protocol. Leave empty for 'ChIP-Seq Input'.

__CHIP_ANTIBODY__ - The specific antibody used in the ChIP protocol. Leave empty for 'ChIP-Seq Input'.

__CHIP_ANTIBODY_PROVIDER__ - The name of the company, laboratory or person that provided the antibody. Leave empty for 'ChIP-Seq Input'.

__CHIP_ANTIBODY_CATALOG__ - The catalog from which the antibody was purchased. Leave empty for 'ChIP-Seq Input'.

__CHIP_ANTIBODY_LOT__ - The lot identifier of the antibody. Leave empty for 'ChIP-Seq Input'.

__CHIP_PROTOCOL_CROSSLINK_TIME__ - The timespan in which the chromatin is crosslinked. Leave empty for 'ChIP-Seq Input'.

__LIBRARY_GENERATION_FRAGMENT_SIZE_RANGE__ - The fragment size range of the preparation. Leave empty for 'ChIP-Seq Input'.

## RNA-Seq

__EXPERIMENT_TYPE:__ (Controlled Vocabulary) 'RNA-Seq'.

__EXPERIMENT_ONTOLOGY_URI:__ (Ontology: OBI) 'http://purl.obolibrary.org/obo/OBI_0001271' or any of its subclasses.

__LIBRARY_STRATEGY__ - (Controlled Vocabulary) 'RNA-Seq'.

__MOLECULE_ONTOLOGY_URI:__ (Ontology: SO) 'http://purl.obolibrary.org/obo/SO_0000234' or any of its subclasses.

__MOLECULE:__ (Controlled Vocabulary) 'polyA RNA', 'total RNA', 'nuclear RNA', 'cytoplasmic RNA' or 'small RNA'.

__EXTRACTION_PROTOCOL__ - The protocol used to isolate the extract material.

__EXTRACTION_PROTOCOL_RNA_ENRICHMENT__ - The RNA enrichment method used in the extraction protocol.

__EXTRACTION_PROTOCOL_FRAGMENTATION__ - The fragmentation method used in the extraction protocol.

__RNA_PREPARATION_FRAGMENT_SIZE_RANGE__ - The RNA fragment size range of the preparation, or 'NA' if not applicable.

<strong>RNA_PREPARATION_5'_RNA_ADAPTER_SEQUENCE</strong> - The sequence of the 5’ RNA adapter used in preparation.

<strong>RNA_PREPARATION_3'_RNA_ADAPTER_SEQUENCE</strong> - The sequence of the 3’ RNA adapter used in preparation.

__RNA_PREPARATION_REVERSE_TRANSCRIPTION_PRIMER_SEQUENCE__ - The sequence of the primer for reverse transcription used in preparation.

<strong>RNA_PREPARATION_5'_DEPHOSPHORYLATION</strong> - The protocol for 5’ dephosphorylation used in preparation.

<strong>RNA_PREPARATION_5'_PHOSPHORYLATION</strong> - The protocol for 5’ phosphorylation used in preparation.

<strong>RNA_PREPARATION_3'_RNA_ADAPTER_LIGATION_PROTOCOL</strong> - The protocol for 3’ adapter ligation used in preparation.

<strong>RNA_PREPARATION_5'_RNA_ADAPTER_LIGATION_PROTOCOL</strong> - The protocol for 5’ adapter ligation used in preparation.

__LIBRARY_GENERATION_PCR_TEMPLATE_CONC__ - The PCR template concentration for library generation.

__LIBRARY_GENERATION_PCR_POLYMERASE_TYPE__ - The PCR polymerase used for library generation

__LIBRARY_GENERATION_PCR_THERMOCYCLING_PROGRAM__ - The thermocycling program used for library generation.

__LIBRARY_GENERATION_PCR_NUMBER_CYCLES__ - The number of PCR cycles used for library generation.

__LIBRARY_GENERATION_PCR_F_PRIMER_SEQUENCE__ - The sequence of the PCR forward primer used for library generation.

__LIBRARY_GENERATION_PCR_R_PRIMER_SEQUENCE__ - The sequence of the PCR reverse primer used for library generation.

__LIBRARY_GENERATION_PCR_PRIMER_CONC__ - The concentration of the PCR primers used for library generation.

__LIBRARY_GENERATION_PCR_PRODUCT_ISOLATION_PROTOCOL__ - The protocol for isolating PCR products used for library generation.

__TEMPLATE_TYPE__ - (Controlled Vocabulary) mRNA or cDNA - The type of template, if applicable.

__AMPLIFIED__ - (Controlled Vocabulary) True or False - Is the sample amplified?

__PREPARATION_INITIAL_RNA_QNTY__ - The initial RNA quantity used in preparation.

__PREPARATION_REVERSE_TRANSCRIPTION_PROTOCOL__ - The protocol for reverse transcription used in preparation.

__PREPARATION_PCR_NUMBER_CYCLES__ - The number of PCR cycles used to amplify.

__LIBRARY_GENERATION_PROTOCOL__ - The protocol used to generate the library.

__LIBRARY_GENERATION_FRAGMENTATION__ - The fragmentation method used in the library protocol.

__LIBRARY_GENERATION_FRAGMENT_SIZE_RANGE__ - The fragment size range of the preparation.

<strong>LIBRARY_GENERATION_3'_ADAPTER_SEQUENCE</strong> - The sequence of the 3' adapter used for library generation.

<strong>LIBRARY_GENERATION_5'_ADAPTER_SEQUENCE</strong> - The sequence of the 5' adapter used for library generation.