# Files for NGS-pipeline
********************************

**General**

    - VCF-file with 18 very common SNP´s used to identify samples by gennotyping them with NGS and an alternative method
    - Database wiht all captures, pakketten and panels.

**For every capture:**

    - BED-file  with regions of interest _target.bed 
    - BED-file  with annotated regions of interest _target.annotated
    - picard interval lists for target regions _target.interval_list

**For every pakket:**

    - BED-file with transcription region for genes of interest _genes.bed
    - BED-file with regions of interest extracted from the capture's annotated region of interest BED-file

**For every panel:**

    - BED-file with regions of interest extracted from the capture's annotated region of interest BED-file


