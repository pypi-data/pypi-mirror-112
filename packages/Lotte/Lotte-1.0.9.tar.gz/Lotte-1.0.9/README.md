# Readme

## Overview
Lotte is a tool to find quotations in two texts, called source and target. If known, the source text should be the one that is quoted by the target text. This allows the algorithm to handle things like ellipsis in quotations, e.g.
~~~
0	52	This is a long Text and the long test goes on and on
0	45	This is a long Text [...] test goes on and on
~~~

## Installation
~~~
pip install Lotte
~~~

## Usage
There are two ways to use the algorithm. The following two sections describe the use of the algorithm in code and from the command line.

### In code
The algorithm can be found in the package `lotte`. To use it create a `Lotte` object which expects the following arguments:
- The length of the shortest match (default: 5)
- The number of tokens to skip when looking backwards (default: 10)
- The number of tokens to skip when looking ahead (default: 3)
- The maximum distance in tokens between to matches considered for merging (default: 2)
- The maximum distance in tokens between two matches considered for merging where the target text contains an ellipsis between the matches (default: 10)


Then call the `compare` method on the object which expects two texts to be compared.
The method returns a list with the following structure: `List[Match]`. `Match` stores two `MatchSegments`. One for the source text and one for the target text. `MatchSegment` stores the `character_start_pos` and `character_end_pos` for the matching segments in the source and target text.

### Command line
The `lotte compare` command provides a command line interface to the algorithm.

~~~
usage: LotteCLI.py compare [-h] [--text ] [--no-text]
                           [--output-type {json,text}]
                           [--output-folder-path OUTPUT_FOLDER_PATH]
                           [--min-match-length MIN_MATCH_LENGTH]
                           [--look-back-limit LOOK_BACK_LIMIT]
                           [--look-ahead-limit LOOK_AHEAD_LIMIT]
                           [--max-merge-distance MAX_MERGE_DISTANCE]
                           [--max-merge-ellipsis-distance MAX_MERGE_ELLIPSIS_DISTANCE]
                           [--create-dated-subfolder]
                           [--no-create-dated-subfolder]
                           [--max-num-processes MAX_NUM_PROCESSES]
                           source-file-path target-path

Lotte compare allows the user to find quotations in two texts, a source text
and a target text. If known, the source text should be the one that is quoted
by the target text. This allows the algorithm to handle things like ellipsis
in quotations.

positional arguments:
  source-file-path      Path to the source text file
  target-path           Path to the target text file or folder

optional arguments:
  -h, --help            show this help message and exit
  --text                Include matched text in the returned data structure
  --no-text             Don't include matched text in the returned data
                        structure
  --output-type {json,text}
                        The output type
  --output-folder-path OUTPUT_FOLDER_PATH
                        The output folder path. If this option is set the
                        output will be saved to a file created in the
                        specified folder.
  --min-match-length MIN_MATCH_LENGTH
                        The length of the shortest match (>= 3, default: 5)
  --look-back-limit LOOK_BACK_LIMIT
                        The number of tokens to skip when looking backwards
                        (>= 0, default: 10), (Very rarely needed)
  --look-ahead-limit LOOK_AHEAD_LIMIT
                        The number of tokens to skip when looking ahead (>= 0,
                        default: 3)
  --max-merge-distance MAX_MERGE_DISTANCE
                        The maximum distance in tokens between two matches
                        considered for merging (>= 0, default: 2)
  --max-merge-ellipsis-distance MAX_MERGE_ELLIPSIS_DISTANCE
                        The maximum distance in tokens between two matches
                        considered for merging where the target text contains
                        an ellipsis between the matches (>= 0, default: 10)
  --create-dated-subfolder
                        Create a subfolder named with the current date to
                        store the results
  --no-create-dated-subfolder
                        Don't create a subfolder named with the current date
                        to store the results
  --max-num-processes MAX_NUM_PROCESSES
                        Maximum number of processes to use for parallel
                        processing.
~~~

By default, the result is returned as a json structure: `List[Match]`. `Match` stores two `MatchSegments`. One for the source text and one for the target text. `MatchSegment` stores the `character_start_pos` and `character_end_pos` for the matching segments in the source and target text.
For example,

~~~
[
  {
    "source_match_segment": {
      "character_start_pos": 0,
      "character_end_pos": 52,
      "text": "This is a long Text and the long test goes on and on"
    },
    "target_match_segment": {
      "character_start_pos": 0,
      "character_end_pos": 45,
      "text": "This is a long Text [...] test goes on and on"
    }
  }
]
~~~

Alternatively, the result can be printed in a human-readable text format, e.g.:

~~~
0	52	This is a long Text and the long test goes on and on
0	45	This is a long Text [...] test goes on and on 
~~~

In case the matching text is not needed, the option --no-text allows to exclude the text from the output.

## Visualization
The package `visualization` contains code to create the content for a web page to visualize the result of the algorithm.
For the website, see [LotteVizEx](/../../../../lottevizex/).

### Usage
~~~
usage: LotteCLI.py visualize [-h] [--title TITLE] [--author AUTHOR]
                             [--year YEAR]
                             source-file-path target-folder-path
                             matches-folder-path output-folder-path

Lotte visualize allows the user to create the files needed for a website that
visualizes the lotte algorithm results.

positional arguments:
  source-file-path     Path to the source text file
  target-folder-path   Path to the target texts folder path
  matches-folder-path  Path to the folder with the match files
  output-folder-path   Path to the output folder

optional arguments:
  -h, --help           show this help message and exit
  --title TITLE        Title of the work
  --author AUTHOR      Author of the work
  --year YEAR          Year of the work
~~~

## Technical Background
See [Verfahren zur Entdeckung und Charakterisierung von Schlüsselstellen (Poster)](https://doi.org/10.5281/zenodo.4737131)

## Acknowledgement
The algorithm is inspired by _sim_text_ by Dick Grune [^1]
and _Similarity texter: A text-comparison web tool based on the “sim_text” algorithm_ by Sofia Kalaidopoulou (2016) [^2]

[^1]: https://dickgrune.com/Programs/similarity_tester/ (Stand: 12.04.2021)

[^2]: https://people.f4.htw-berlin.de/~weberwu/simtexter/522789_Sofia-Kalaidopoulou_bachelor-thesis.pdf (Stand: 12.04.2021)
