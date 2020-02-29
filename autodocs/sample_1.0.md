

## Cell Line 

The metadata specification for Cell Line samples is as defined below.

<strong>BATCH</strong>:The batch from which the cell line is derived. Primarily applicable to initial H1 cell line batches. NA if not applicable.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>DIFFERENTIATION_METHOD</strong>:The protocol used to differentiation the cell line. At most 1 instance(s) are allowed.

<strong>DIFFERENTIATION_STAGE</strong>:The stage in cell differentiation to which the cell line belongs.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>LINE</strong>:The name of the cell line.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>LINEAGE</strong>:The developmental lineage to which the cell line belongs.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>MEDIUM</strong>:The medium in which the cell line has been grown.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>PASSAGE</strong>:The number of times the cell line has been re-plated and allowed to grow back to confluency or to some maximum density if using suspension cultures.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>SEX</strong>:'Male', 'Female', 'Unknown', or 'Mixed' for pooled samples.  This attribute is <strong>required</strong>. Allowed values are: "Female", "Male", "Mixed", "Unknown". At most 1 instance(s) are allowed.


## Primary Cell 

The metadata specification for Primary Cell samples is as defined below.

Additionally, the metadata must also satify requirements for following specifications: <strong>donor</strong>

<strong>CELL_TYPE</strong>:The type of cell.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>MARKERS</strong>:Markers used to isolate and identify the cell type.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>ORIGIN_SAMPLE</strong>:Description of the origin tissue from which sample was extracted.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>ORIGIN_SAMPLE_ONTOLOGY_URI</strong>:(Ontology: UBERON) links to the tissue from which sample was extracted.  This attribute is <strong>required</strong>.

<strong>PASSAGE_IF_EXPANDED</strong>:If the primary cell has been expanded, the number of times the primary cell has been re-plated and allowed to grow back to confluency or to some maximum density if using suspension cultures. NA if no expansion.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.


## Primary Cell Culture 

The metadata specification for Primary Cell Culture samples is as defined below.

Additionally, the metadata must also satify requirements for following specifications: <strong>donor</strong>

<strong>CELL_TYPE</strong>:.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>CULTURE_CONDITIONS</strong>:The conditions under which the primary cell was cultured.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>MARKERS</strong>:Markers used to isolate and identify the cell type.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>ORIGIN_SAMPLE</strong>:Description of the origin tissue from which sample was extracted.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>ORIGIN_SAMPLE_ONTOLOGY_URI</strong>:(Ontology: UBERON) links to the tissue from which sample was extracted.  This attribute is <strong>required</strong>.

<strong>PASSAGE_IF_EXPANDED</strong>:If the primary cell culture has been expanded, the number of times the primary cell culture has been re-plated and allowed to grow back to confluency or to some maximum density if using suspension cultures. NA if no expansion.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.


## Primary Tissue 

The metadata specification for Primary Tissue samples is as defined below.

Additionally, the metadata must also satify requirements for following specifications: <strong>donor</strong>

<strong>COLLECTION_METHOD</strong>:The protocol for collecting the primary tissue.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>TISSUE_DEPOT</strong>:Details about the anatomical location from which the primary tissue was collected.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>TISSUE_TYPE</strong>:The type of tissue.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.


## donor 

The metadata specification for donor samples is as defined below.

<strong>DONOR_AGE</strong>:The age of the donor that provided the cells/tissues. NA if not available. If over 90 years enter as 90+. If entering a range of ages use the format “{age}-{age}”.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>DONOR_AGE_UNIT</strong>:<strong>_undef_</strong>.  This attribute is <strong>required</strong>. Allowed values are: "day", "month", "week", "year". At most 1 instance(s) are allowed.

<strong>DONOR_ETHNICITY</strong>:The ethnicity of the donor that provided the primary cell. NA if not available. If dealing with small/vulnerable populations consider identifiability issues.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>DONOR_HEALTH_STATUS</strong>:The health status of the donor that provided the primary cell. NA if not available.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>DONOR_HEALTH_STATUS_ONTOLOGY_URI</strong>:(Ontology: NCIM) Links to the health status of the donor that provided the primary cell. The NCImetathesaurus term C0277545 'Disease type AND/OR category unknown' should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 'None'. Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_CURIEs (if available) or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

<strong>DONOR_ID</strong>:An identifying designation for the donor that provided the cells/tissues.  This attribute is <strong>required</strong>. At most 1 instance(s) are allowed.

<strong>DONOR_LIFE_STAGE</strong>:__malformed-schema__.  This attribute is <strong>required</strong>.

<strong>DONOR_SEX</strong>:'Male', 'Female', 'Unknown', or 'Mixed' for pooled samples.  This attribute is <strong>required</strong>. Allowed values are: "Female", "Male", "Mixed", "Unknown". At most 1 instance(s) are allowed.

