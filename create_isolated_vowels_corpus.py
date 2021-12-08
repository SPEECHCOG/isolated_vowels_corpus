"""
    Script to create the isolated vowels corpus (MBROLA-based corpus) to compare directly vowels from different
    languages within the same contrast.

    Languages included: Dutch, French, German, Japanese, English

    Vowel repertoires per languages (MBROLA voices): SAMPA standard

    Dutch:
        /Y/, /@/, /O/, /A/, /y/, /e/, /2/, /o/, /a/ (nl1, nl2, nl3)
        /I/, /i/, /E/, /u/ (nl2, nl3)
        /E:/, /9:/, /O:/ (nl3)

    German:
        /@/, /i/, /I/, /Y/, /y:/, /e:/, /E/, /E:/, /2:/, /9/, /u:/, /U/, /o:/, /O/, /a:/, /a/ (de1, de2, de3, de4,
                                                                                               de5, de6, de7)
        /6/ (de6, de7)
        /E^/, /a^/, /o^/ (de1, de2, de3, de5)
        /E~/, /a~/, /o~/ (de1, de2, de3, de4, de5)
        /e~/, /a~/ (de6, de7)
        /o~/, /9~/ (de6)

        de8 voice (Munich dialect) was left out because of large difference with main repertoire

    Japanese:
        /a/, /i/, /u/, /e/, /o/ (jp1, jp2, jp3)
        /u_o/, /i_o/, /a:/, /e:/, /o:/, /u:/, /i:/ (jp2)

    French:
        /i/, /e/, /E/, /a/, /A/, /O/, /o/, /u/, /y/, /2/, /9/, /@/, /e~/, /a~/, /o~/, /9~/ (fr1, fr2, fr3, fr4,
                                                                                            fr5, fr6, fr7)

    English:
        /i/, /A/, /O/, /u/, /I/, /E/, /{/, /V/, /U/, /@/ (us1, us2, us3)

    Language codes: ISO-639-1
    Dutch: nl, German: de, Japanese: jp, French: fr, and English: en

    @date 9.4.2021
"""

__docformat__ = ['reStructuredText']
__all__ = ['create_basic_corpus']

import argparse
import csv
import pathlib
import pickle
import subprocess
import sys
from typing import Union, List, Optional

SPEAKERS_GENDER = {
    'nl1': 'm', 'nl2': 'm', 'nl3': 'f',
    'de1': 'f', 'de2': 'm', 'de3': 'f', 'de4': 'm', 'de5': 'f', 'de6': 'm', 'de7': 'f',
    'jp1': 'm', 'jp2': 'f', 'jp3': 'f',
    'fr1': 'm', 'fr2': 'f', 'fr3': 'm', 'fr4': 'f', 'fr5': 'm', 'fr6': 'm', 'fr7': 'm',
    'us1': 'f', 'us2': 'm', 'us3': 'm'
}


def generate_pitch_contour_pho_line(pitch_type: str, speaker_id: str) -> str:
    # pitch contour for female (_f) and male (_m) voices
    falling_m = [112, 132, 92]
    falling_f = [189, 223, 155]
    rising_m = [112, 132]
    rising_f = [189, 223]

    if SPEAKERS_GENDER[speaker_id] == 'f':
        contour = falling_f if pitch_type == 'f' else rising_f
    else:
        contour = falling_m if pitch_type == 'f' else rising_m

    if pitch_type == 'r':
        pho_line = '(1, {0}) (100, {1})'.format(*contour)
    else:
        pho_line = '(1,  {0}) (20, {1}) (28, {1}) (100, {2})'.format(*contour)

    return pho_line


def create_pho_files(lang: str, vowels: List[str], speakers: List[str], corpus_info: dict,
                     output_path: Union[str, pathlib.Path], vowel_duration: Optional[int] = 500) -> dict:

    for speaker in speakers:
        # keys format: lang_speaker_pitch_sequence. Counting by speaker
        prev_seq = [int(curr_files[-3:]) for curr_files in corpus_info.keys() if speaker in curr_files]
        if len(prev_seq) > 0:
            seq = sorted(prev_seq,reverse=True)[0]
            seq += 1
        else:
            seq = 1
        for vowel in vowels:
            for pitch in ['f', 'r']:  # falling and rising
                title = f'{lang}_{speaker}_{pitch}_{seq:03d}.pho'
                line = f'{vowel} {vowel_duration} {generate_pitch_contour_pho_line(pitch, speaker)}'
                with open(pathlib.Path(output_path).joinpath(title), 'w') as file:
                    file.write(line)
                corpus_info[title.replace('.pho', '')] = {'vowel': vowel, 'details': {'language': lang},
                                                          'vowel_onset': 0, 'vowel_offset': vowel_duration,
                                                          'speaker': speaker}
                seq += 1
    return corpus_info


def synthesise_pho_files(dir_pho_files: Union[str, pathlib.Path], mbrola_exe_path: Union[str, pathlib.Path],
                         voices_path: Union[str, pathlib.Path], output_path: Union[str, pathlib.Path]) -> None:
    pho_files = list(pathlib.Path(dir_pho_files).iterdir())

    mbrola_exe_path = pathlib.Path(mbrola_exe_path)
    voices_path = pathlib.Path(voices_path)
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    for pho_file in pho_files:
        name = pho_file.resolve().stem
        voice = name.split('_')[1]  # lang_speaker_pitch_sequence
        wav_file = pathlib.Path(output_path).joinpath(f'{name}.wav')
        # command = f'{mbrola_exe} {voice_path.joinpath(voice)} {pho_file} {wav_file}'
        command = [mbrola_exe_path, voices_path.joinpath(voice), pho_file, wav_file]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(pho_file)


def create_corpus_info_csv_file(output_corpus_path: Union[str, pathlib.Path], corpus_info: dict) -> None:
    header = ['filename', 'vowel', 'vowel_onset', 'vowel_offset', 'mbrola_voice', 'language']
    lines = []
    for filename in sorted(corpus_info.keys()):
        lines.append([filename, corpus_info[filename]['vowel'], corpus_info[filename]['vowel_onset'],
                      corpus_info[filename]['vowel_offset'], filename.split('_')[1],
                      corpus_info[filename]['details']['language']])
    with open(pathlib.Path(output_corpus_path).joinpath('corpus_info.csv'), 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)
        writer.writerows(lines)


def create_basic_corpus(output_corpus_path: Union[str, pathlib.Path],
                        output_corpus_info_path: Union[str, pathlib.Path],
                        mbrola_path: Union[str, pathlib.Path],
                        mbrola_voices_path: Union[str, pathlib.Path]) -> None:
    vowels = {
        'en': [['A', 'i', 'I', 'E', 'u', '{']],
        'nl': [['I', 'i', 'E', 'u']],
        'de': [['2:', 'I', 'E', 'a:', 'a', 'u:', 'y:'], ['6']],
        'fr': [['u', 'y', 'a', 'a~', 'i']],
        'jp': [['a', 'u', 'i'], ['a:']]
    }
    speakers = {
        'en': [['us1', 'us2', 'us3']],
        'nl': [['nl2', 'nl3']],
        'de': [['de1', 'de2', 'de3', 'de4', 'de5', 'de6', 'de7'], ['de6', 'de7']],
        'fr': [['fr1', 'fr2', 'fr3', 'fr4', 'fr5', 'fr6', 'fr7']],
        'jp': [['jp1', 'jp2', 'jp3'], ['jp2']]
    }

    corpus_info = {}

    languages = list(vowels.keys())
    pho_folder = pathlib.Path(output_corpus_path).joinpath('pho')
    pho_folder.mkdir(parents=True, exist_ok=True)

    for language in languages:
        for config_idx in range(len(vowels[language])):
            corpus_info = create_pho_files(language, vowels[language][config_idx], speakers[language][config_idx],
                                           corpus_info, pho_folder)

    wav_folder = pathlib.Path(output_corpus_path).joinpath('wav')
    wav_folder.mkdir(parents=True, exist_ok=True)

    synthesise_pho_files(pho_folder, mbrola_path, mbrola_voices_path, wav_folder)

    pathlib.Path(output_corpus_info_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_corpus_info_path, 'wb') as data_file:
        pickle.dump(corpus_info, data_file)

    create_corpus_info_csv_file(output_corpus_path, corpus_info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to create Isolated vowels corpus with MBROLA. \nUsage: python'
                                                 'create_isolated_vowels_corpus.py '
                                                 '--mbrola_path path_MBROLA_executable '
                                                 '--mbrola_voices_path path_MBROLA_voices '
                                                 '--output_corpus_path path_corpus '
                                                 '--output_info path_corpus_info_file')

    parser.add_argument('--mbrola_path', type=str, required=True)
    parser.add_argument('--mbrola_voices_path', type=str, required=True)
    parser.add_argument('--output_corpus_path', type=str, required=True)
    parser.add_argument('--output_info', type=str, required=True)

    args = parser.parse_args()

    create_basic_corpus(args.output_corpus_path, args.output_info, args.mbrola_path, args.mbrola_voices_path)

    sys.exit(0)
