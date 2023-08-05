# sgrna_designer
> Python library to design sgRNAs for CRISPR tiling screens


The primary function of this package is `design_sgrna_tiling_library`, in which you can input a list of
ensembl transcript IDs, specify a region of interest (e.g. three_prime_UTR) and get all sgRNAs
tiling those transcript regions.

## Install

`pip install git+https://github.com/gpp-rnd/sgrna_designer.git#egg=sgrna_designer`

## An example

In this example we'll design sgRNAs tiling the 3' UTR of PDL1 (CD274) and BRAF

**Note**: You must also have [pandas installed](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
to run this tutorial

```
from sgrna_designer.design import design_sgrna_tiling_library

target_transcripts = ['ENST00000381577', 'ENST00000644969'] # [PDL1, BRAF]
```

Note the design function is agnostic to CRISPR enzyme and pam preferences, so you must specifiy the
following parameters in a design run:
* region: broad region you are trying to target (e.g. UTR)
* region: more specific region you are trying to target (e.g. three_prime_UTR)
* expand_3prime: amount to expand region in 3' direction
* expand_5prime: amount to expand region in 5' direction
* context_len: length of context sequence
* pam_start: position of PAM start relative to the context sequence
* pam_len: length of PAM
* sgrna_start: position of sgRNA relative to context sequence
* sgrna_len: length of sgRNA sequence
* pams: PAMs to target
* sg_positions: positions within the sgRNA to annotate and target
(e.g. [4,8] for nucleotides 4 and 8 of the sgRNA for a base editing window)

```
sgrna_designs = design_sgrna_tiling_library(target_transcripts, region_parent='UTR',
                                            region='three_prime_UTR', expand_3prime=30,
                                            expand_5prime=30, context_len=30, pam_start=-6,
                                            pam_len=3, sgrna_start=4, sgrna_len=20,
                                            pams=['AGG', 'CGG', 'TGG', 'GGG'],
                                            sg_positions=[4, 8], flag_seqs=['TTTT', 'CGTCTC', 'GAGACG'],
                                            flag_seqs_start=['TCTC', 'AGACG'], flag_seqs_end=['GAGAC'])
sgrna_designs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>context_sequence</th>
      <th>pam_sequence</th>
      <th>sgrna_sequence</th>
      <th>sgrna_global_start</th>
      <th>sgrna_global_4</th>
      <th>sgrna_global_8</th>
      <th>sgrna_strand</th>
      <th>object_type</th>
      <th>transcript_strand</th>
      <th>transcript_id</th>
      <th>chromosome</th>
      <th>region_id</th>
      <th>region_start</th>
      <th>region_end</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CATTGGAACTTCTGATCTTCAAGCAGGGAT</td>
      <td>AGG</td>
      <td>GGAACTTCTGATCTTCAAGC</td>
      <td>5467872</td>
      <td>5467875</td>
      <td>5467879</td>
      <td>1</td>
      <td>three_prime_UTR</td>
      <td>1</td>
      <td>ENST00000381577</td>
      <td>9</td>
      <td>ENST00000381577</td>
      <td>5467863</td>
      <td>5470554</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ATTGGAACTTCTGATCTTCAAGCAGGGATT</td>
      <td>GGG</td>
      <td>GAACTTCTGATCTTCAAGCA</td>
      <td>5467873</td>
      <td>5467876</td>
      <td>5467880</td>
      <td>1</td>
      <td>three_prime_UTR</td>
      <td>1</td>
      <td>ENST00000381577</td>
      <td>9</td>
      <td>ENST00000381577</td>
      <td>5467863</td>
      <td>5470554</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CTTCAAGCAGGGATTCTCAACCTGTGGTTT</td>
      <td>TGG</td>
      <td>AAGCAGGGATTCTCAACCTG</td>
      <td>5467888</td>
      <td>5467891</td>
      <td>5467895</td>
      <td>1</td>
      <td>three_prime_UTR</td>
      <td>1</td>
      <td>ENST00000381577</td>
      <td>9</td>
      <td>ENST00000381577</td>
      <td>5467863</td>
      <td>5470554</td>
    </tr>
    <tr>
      <th>3</th>
      <td>GCAGGGATTCTCAACCTGTGGTTTAGGGGT</td>
      <td>AGG</td>
      <td>GGATTCTCAACCTGTGGTTT</td>
      <td>5467894</td>
      <td>5467897</td>
      <td>5467901</td>
      <td>1</td>
      <td>three_prime_UTR</td>
      <td>1</td>
      <td>ENST00000381577</td>
      <td>9</td>
      <td>ENST00000381577</td>
      <td>5467863</td>
      <td>5470554</td>
    </tr>
    <tr>
      <th>4</th>
      <td>CAGGGATTCTCAACCTGTGGTTTAGGGGTT</td>
      <td>GGG</td>
      <td>GATTCTCAACCTGTGGTTTA</td>
      <td>5467895</td>
      <td>5467898</td>
      <td>5467902</td>
      <td>1</td>
      <td>three_prime_UTR</td>
      <td>1</td>
      <td>ENST00000381577</td>
      <td>9</td>
      <td>ENST00000381577</td>
      <td>5467863</td>
      <td>5470554</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>845</th>
      <td>GCTCAGGTCCCTTCATTTGTACTTTGGAGT</td>
      <td>TGG</td>
      <td>AGGTCCCTTCATTTGTACTT</td>
      <td>140719570</td>
      <td>140719567</td>
      <td>140719563</td>
      <td>-1</td>
      <td>three_prime_UTR</td>
      <td>-1</td>
      <td>ENST00000644969</td>
      <td>7</td>
      <td>ENST00000644969</td>
      <td>140719337</td>
      <td>140726493</td>
    </tr>
    <tr>
      <th>846</th>
      <td>TATAACAGAAAATATTGTTCAGTTTGGATA</td>
      <td>TGG</td>
      <td>ACAGAAAATATTGTTCAGTT</td>
      <td>140719522</td>
      <td>140719519</td>
      <td>140719515</td>
      <td>-1</td>
      <td>three_prime_UTR</td>
      <td>-1</td>
      <td>ENST00000644969</td>
      <td>7</td>
      <td>ENST00000644969</td>
      <td>140719337</td>
      <td>140726493</td>
    </tr>
    <tr>
      <th>847</th>
      <td>ATTGTTCAGTTTGGATAGAAAGCATGGAGA</td>
      <td>TGG</td>
      <td>TTCAGTTTGGATAGAAAGCA</td>
      <td>140719509</td>
      <td>140719506</td>
      <td>140719502</td>
      <td>-1</td>
      <td>three_prime_UTR</td>
      <td>-1</td>
      <td>ENST00000644969</td>
      <td>7</td>
      <td>ENST00000644969</td>
      <td>140719337</td>
      <td>140726493</td>
    </tr>
    <tr>
      <th>848</th>
      <td>TATTTAAAAACTGTATTATATAAAAGGCAA</td>
      <td>AGG</td>
      <td>TAAAAACTGTATTATATAAA</td>
      <td>140719426</td>
      <td>140719423</td>
      <td>140719419</td>
      <td>-1</td>
      <td>three_prime_UTR</td>
      <td>-1</td>
      <td>ENST00000644969</td>
      <td>7</td>
      <td>ENST00000644969</td>
      <td>140719337</td>
      <td>140726493</td>
    </tr>
    <tr>
      <th>849</th>
      <td>CTGCTATAATAAAGATTGACTGCATGGAGA</td>
      <td>TGG</td>
      <td>TATAATAAAGATTGACTGCA</td>
      <td>140719360</td>
      <td>140719357</td>
      <td>140719353</td>
      <td>-1</td>
      <td>three_prime_UTR</td>
      <td>-1</td>
      <td>ENST00000644969</td>
      <td>7</td>
      <td>ENST00000644969</td>
      <td>140719337</td>
      <td>140726493</td>
    </tr>
  </tbody>
</table>
<p>850 rows × 14 columns</p>
</div>


