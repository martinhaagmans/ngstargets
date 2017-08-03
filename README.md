# Targets for NGS-pipeline
********************************

**These files exist for every capture:**

    - list with genes/targets on the capture
    - BED-file  with regions of interest (exonplus20)
    - BED-file  with annotated regions of interest
    - BED-file with transcription region for genes of interest
    - picard interval lists for target regions


**These files exist for every typeA-panel:**

    - list with genes/targets in the panel
    - BED-file with regions of interest extracted from the capture's annotated region of interest BED-file

```
├── AGPPVM
│   ├── AGP
│   │   ├── AGPv5_exonplus20.bed
│   │   └── AGPv5_genes.txt
│   ├── AGPPVMv1_exonplus20.annotated
│   ├── AGPPVMv1_exonplus20.bed
│   ├── AGPPVMv1_genes.txt
│   ├── AGPPVMv1_target.picard.interval_list
│   ├── PP
│   │   ├── PPv4_exonplus20.bed
│   │   └── PPv4_genes.txt
│   └── VM
│       ├── VMv4_exonplus20.bed
│       └── VMv4_genes.txt
├── BH
│   ├── ALBI
│   │   ├── ALBIv1_exonplus20.bed
│   │   └── ALBIv1_genes.txt
│   ├── BHv3_exonplus20.annotated
│   ├── BHv3_exonplus20.bed
│   ├── BHv3_genes.txt
│   ├── BHv3_target.picard.interval_list
│   └── corepanels
│       ├── CRDtypeAv2.bed
│       ├── CRDtypeAv2_genes.txt
│       ├── LCAtypeAv1.bed
│       ├── LCAtypeAv1_genes.txt
│       ├── RPtypeAv2.bed
│       └── RPtypeAv2_genes.txt
├── CAP
│   ├── CAPv1_exonplus20.annotated
│   ├── CAPv1_exonplus20.bed
│   ├── CAPv1_generegions.bed
│   ├── CAPv1_genes.txt
│   ├── CAPv1_target.picard.interval_list
│   ├── CAPv1_tiled.picard.interval_list
│   └── corepanels
│       ├── OVRv1.bed
│       └── OVRv1.txt
├── CHC
│   ├── CHCv1_exonplus20.annotated
│   ├── CHCv1_exonplus20.bed
│   ├── CHCv1_genes.txt
│   ├── CHCv1_target.picard.interval_list
│   └── HT
│       ├── HTv1_exonplus20.bed
│       └── HTv1_genes.txt
├── CM
│   ├── CMv15_exonplus20.annotated
│   ├── CMv15_exonplus20.bed
│   ├── CMv15_genes.txt
│   └── CMv15_target.picard.interval_list
├── COWSO
│   ├── COW
│   │   ├── COWv2_exonplus20.bed
│   │   └── COWv2_genes.txt
│   ├── COWSOv1_exonplus20.annotated
│   ├── COWSOv1_exonplus20.bed
│   ├── COWSOv1_genes.txt
│   ├── COWSOv1_target.picard.interval_list
│   └── SO
│       ├── SOv2_exonplus20.bed
│       ├── SOv2_genes.txt
│       └── SOv2_mozaiekposities.txt
├── DL
│   ├── DLv2_exonplus20.annotated
│   ├── DLv2_exonplus20.bed
│   ├── DLv2_genes.txt
│   └── DLv2_target.picard.interval_list
├── LYMPH
│   ├── LYMPHv4_exonplus20.annotated
│   ├── LYMPHv4_exonplus20.bed
│   ├── LYMPHv4_genes.txt
│   └── LYMPHv4_target.picard.interval_list
├── MBS
│   ├── MBSv4_exonplus20.annotated
│   ├── MBSv4_exonplus20.bed
│   ├── MBSv4_genes.txt
│   └── MBSv4_target.picard.interval_list
├── NEURO
│   ├── ALS
│   │   ├── ALSv1_exonplus20.bed
│   │   ├── ALSv1_genes.txt
│   │   └── corepanels
│   │       ├── ALStypeAv2.bed
│   │       └── ALStypeAv2_genes.txt
│   ├── CMT
│   │   ├── CMTv4_exonplus20.bed
│   │   ├── CMTv4_genes.txt
│   │   └── corepanels
│   │       ├── CMTtypeAv3.bed
│   │       └── CMTtypeAv3_genes.txt
│   ├── LIMBG
│   │   ├── LIMBGv1_exonplus20.bed
│   │   └── LIMBGv1_genes.txt
│   ├── NEUROv4_exonplus20.annotated
│   ├── NEUROv4_exonplus20.bed
│   ├── NEUROv4_genes.txt
│   ├── NEUROv4_target.picard.interval_list
│   └── PCH
│       ├── corepanels
│       │   ├── PCHtypeAv2.bed
│       │   └── PCHtypeAv2_genes.txt
│       ├── PCHv1_exonplus20.bed
│       └── PCHv1_genes.txt
├── ngstargets.py
├── PCO
│   ├── corepanels
│   │   ├── BMUTtypeAv1.bed
│   │   └── BMUTtypeAv1.txt
│   ├── PCOv2_exonplus20.annotated
│   ├── PCOv2_exonplus20.bed
│   ├── PCOv2_genes.txt
│   └── PCOv2_target.picard.interval_list
├── README.md
├── SCD
│   ├── LQT
│   │   ├── LQTv1_exonplus20.bed
│   │   └── LQTv1_genes.txt
│   ├── SCDv6_exonplus20.annotated
│   ├── SCDv6_exonplus20.bed
│   ├── SCDv6_genes.txt
│   └── SCDv6_target.picard.interval_list
└── varia
    ├── capinfo.sqlite
    └── OVRv1.txt

31 directories, 95 files
```
