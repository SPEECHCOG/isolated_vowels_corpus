# Isolated Vowels Corpus
This repository contains the isolated vowel corpus (IVC) of vowels 
synthesised with MBROLA voices.

This corpus was generate using the pitch contours and durations from 
Marean et al. (1992). MBROLA voices used to synthesise the vowels 
can be found in their [repository](https://github.com/numediart/MBROLA-voices).

## Vowels repertoire

Vowels in SAMPA standard

* en: ['A', 'i', 'I', 'E', 'u', '{']
* nl: ['I', 'i', 'E', 'u']
* de: ['2:', 'I', 'E', 'a:', 'a', 'u:', 'y:', '6']
* fr: ['u', 'y', 'a', 'a~', 'i']
* jp: ['a', 'u', 'i', 'a:']

## Folder structure

Audio and phonetic transcription files can be found in the corpus folder

```
corpus
├── corpus_info.csv
├── pho
|	├── de_de1_f_001.pho
|	├── ...
|	└── nl_nl3_r_008.pho
└── wav
 	├── de_de1_f_001.wav
	├── ...
	└── nl_nl3_r_008.wav
```

Files name has the following format
`<language>_<voice>_<f/r>_seq.<pho/wav>` where f/r are indications of
the pitch contour (falling, rising).

## Generate the corpus
The code used to generate this code is available in `create_isolated_vowels_corpus.py`.
You will need to download [MBROLA](https://github.com/numediart/MBROLA) 
and [MBROLA voices](https://github.com/numediart/MBROLA-voices).

Which can be executed as:

```
python create_isolated_vowels_corpus.py --mbrola_path path_MBROLA_executable --mbrola_voices_path path_MBROLA_voices --output_corpus_path path_corpus --output_info path_corpus_info_file
```

The parameter `output_info` state the path of the binary file where 
to save the meta-data of the corpus. The file `corpus_info.pickle` 
contains the current version of the corpus meta-data.

# Citing this work

María Andrea Cruz Blandón, Alejandrina Cristia, Okko Räsänen. 
Evaluation of computational models of infant language development 
against robust empirical data from meta-analyses: what, why, and how?

# References
\Marean, G. C., Werner, L. A., & Kuhl, P. K. (1992). 
Vowel categorization by very young infants. Developmental 
Psychology, 28(3), 396–405. https://doi.org/10.1037/0012-1649.28.3.396

# Contact
If you find any issue please report it on the 
[issues section](https://github.com/SPEECHCOG/isolated_vowels_corpus/issues) 
in this repository. Further comments can be sent to 
`maria <dot> cruzblandon <at> tuni <dot> fi`
