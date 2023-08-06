import argparse
from argparse import ArgumentParser
from cli.Match import Match
from cli.MatchSegment import MatchSegment
from lotte.Lotte import Lotte
import json
from visualization import Visualization
import time
from os.path import join, isfile, splitext, basename
from os import listdir
import multiprocessing
from datetime import datetime
from pathlib import Path
from visualization.CitationSource import CitationSource
from visualization.CitationSourceLink import CitationSourceLink
from visualization.ImportantSegment import ImportantSegment
from visualization.ImportantSegmentLink import ImportantSegmentLink
from visualization.SourceSegment import SourceSegment
from visualization.TargetLocation import TargetLocation
from visualization.TargetLocationSelection import TargetLocationSelection
from visualization.TargetText import TargetText
from visualization.TargetTextLocationLink import TargetTextLocationLink


class IntCheckAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        if option_string == '--min-match-length':
            if int(values) < 3:
                parser.error("Minimum value for {0} is 3".format(option_string))
        elif option_string == '--look-back-limit':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--look-ahead-limit':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--max-merge-distance':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--max-merge-ellipsis-distance':
            if int(values) < 0:
                parser.error("{0} must be positive".format(option_string))
        elif option_string == '--max-num-processes':
            if int(values) <= 0:
                parser.error("{0} must be greater 0".format(option_string))

        setattr(namespace, self.dest, values)


def __json_encoder(obj):
    if isinstance(obj, MatchSegment):
        result_dict = obj.__dict__

        if not result_dict['text']:
            del result_dict['text']

        return result_dict

    return obj.__dict__


def __json_encoder_visualization(obj):
    if isinstance(obj, set):
        return list(obj)

    if isinstance(obj, (TargetText, CitationSourceLink, TargetLocationSelection, TargetTextLocationLink,
                        ImportantSegmentLink)):
        return obj.__dict__

    if isinstance(obj, CitationSource):
        result_dict = obj.__dict__

        if len(result_dict['text']) > 40:
            text = result_dict['text']
            result_dict['text'] = text[0:20] + ' [\u2026] ' + text[-20:]

        return result_dict

    if isinstance(obj, TargetLocation):
        result_dict = obj.__dict__

        if 'start' in result_dict:
            del result_dict['start']

        if 'end' in result_dict:
            del result_dict['end']

        if len(result_dict['text']) > 40:
            text = result_dict['text']
            result_dict['text'] = text[0:20] + ' [\u2026] ' + text[-20:]

        return result_dict

    if isinstance(obj, ImportantSegment):
        result_dict = obj.__dict__

        if len(result_dict['text']) > 40:
            text = result_dict['text']
            result_dict['text'] = text[0:20] + ' [\u2026] ' + text[-20:]

        return result_dict
    elif isinstance(obj, SourceSegment):
        result_dict = obj.__dict__

        if 'citation_targets' in result_dict:
            del result_dict['citation_targets']

        if 'text' in result_dict:
            del result_dict['text']

        return result_dict

    return obj


def __run_compare(source_file_path, target_path, export_text, output_type, min_match_length, look_ahead_limit,
                  look_back_limit, max_merge_distance, max_merge_ellipsis_distance, output_folder_path,
                  num_of_processes):

    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_file_content = source_file.read()

    if isfile(target_path) and target_path.endswith(".txt"):

        with open(target_path, 'r', encoding='utf-8') as target_file:
            target_file_content = target_file.read()

        filename = splitext(basename(target_path))[0]

        __process_file(source_file_content, target_file_content, export_text, output_type, min_match_length,
                       look_ahead_limit, look_back_limit, max_merge_distance, max_merge_ellipsis_distance,
                       output_folder_path, filename)
    else:
        pool = multiprocessing.Pool(num_of_processes)

        for file_or_folder in listdir(target_path):
            full_path = join(target_path, file_or_folder)

            if isfile(full_path) and full_path.endswith(".txt"):
                with open(full_path, 'r', encoding='utf-8') as target_file:
                    target_file_content = target_file.read()

                filename = splitext(basename(full_path))[0]
                pool.apply_async(__process_file, args=(source_file_content, target_file_content, export_text,
                                                       output_type, min_match_length, look_ahead_limit,
                                                       look_back_limit, max_merge_distance,
                                                       max_merge_ellipsis_distance, output_folder_path,
                                                       filename))

        pool.close()
        pool.join()


def __process_file(source_file_content, target_file_content, export_text, output_type, min_match_length,
                   look_ahead_limit, look_back_limit, max_merge_distance, max_merge_ellipsis_distance,
                   output_folder_path, filename):

    lotte = Lotte(min_match_length, look_back_limit, look_ahead_limit, max_merge_distance, max_merge_ellipsis_distance)
    matches = lotte.compare(source_file_content, target_file_content)

    output_matches = []

    for match in matches:
        source_match_segment = match.source_match_segment
        target_match_segment = match.target_match_segment

        source_output_match_segment = MatchSegment(source_match_segment.character_start_pos,
                                                   source_match_segment.character_end_pos)

        target_output_match_segment = MatchSegment(target_match_segment.character_start_pos,
                                                   target_match_segment.character_end_pos)

        if export_text:
            source_text = source_file_content[source_match_segment.character_start_pos:
                                              source_match_segment.character_end_pos]
            target_text = target_file_content[target_match_segment.character_start_pos:
                                              target_match_segment.character_end_pos]

            source_output_match_segment.text = source_text
            target_output_match_segment.text = target_text

        output_match = Match(source_output_match_segment, target_output_match_segment)
        output_matches.append(output_match)

    if output_type == 'json':
        result = json.dumps(output_matches, default=__json_encoder)
        file_ending = 'json'
    else:
        result = ''

        for match in output_matches:
            match_literature = match.source_match_segment
            match_scientific = match.target_match_segment

            result += f'\n\n{match_literature.character_start_pos}\t{match_literature.character_end_pos}'

            if export_text:
                result += f'\t{match_literature.text}'

            result += f'\n{match_scientific.character_start_pos}\t{match_scientific.character_end_pos}'

            if export_text:
                result += f'\t{match_scientific.text}'

        result = result.strip()
        file_ending = 'txt'

    if output_folder_path:
        filename = f'{filename}.{file_ending}'
        with open(join(output_folder_path, filename), 'w', encoding='utf-8') as output_file:
            output_file.write(result)

    else:
        print('Ergebnisse:')
        print(result)


def __run_visualize(source_file_path, target_folder_path, matches_folder_path, output_folder_path, title, author, year,
                    censor):
    Visualization.generate_info_json(output_folder_path, title, author, year)

    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_content = source_file.read()

    citation_sources, segment_id_to_target_location_map = Visualization.get_citation_sources(matches_folder_path,
                                                                                             source_content)

    Visualization.add_important_segments(citation_sources)

    target_texts, target_location_id_to_source_location_map = Visualization.generate_target_texts(matches_folder_path,
                                                                                                  target_folder_path)
    target_text_location_links = \
        Visualization.generate_target_text_location_links(citation_sources, target_texts,
                                                          target_location_id_to_source_location_map)

    citation_source_links = Visualization.generate_citation_source_links(citation_sources, target_texts,
                                                                         segment_id_to_target_location_map)
    important_segment_links = Visualization.generate_important_segment_links(citation_sources, target_texts,
                                                                             segment_id_to_target_location_map)

    max_target_texts_count = Visualization.calculate_max_target_texts_count(citation_source_links)
    max_segment_frequency = Visualization.calculate_max_segment_frequency(citation_sources)

    start_time = time.time()
    Visualization.generate_source_html(source_content, citation_sources, output_folder_path, max_target_texts_count,
                                       max_segment_frequency, citation_source_links)

    print(f"\n--- Generate source html, {time.time() - start_time: .2f} seconds ---")

    start_time = time.time()
    Visualization.generate_target_html(target_texts, target_folder_path, output_folder_path, censor)

    print(f"\n--- Generate target html, {time.time() - start_time: .2f} seconds ---")

    with open(join(output_folder_path, 'target_texts.json'), 'w', encoding='utf-8') as target_works_output_file:
        content = json.dumps(target_texts, default=__json_encoder_visualization)
        target_works_output_file.write(content)

    with open(join(output_folder_path, 'citation_sources.json'), 'w', encoding='utf-8') as segments_output_file:
        content = json.dumps(list(citation_sources), default=__json_encoder_visualization)
        segments_output_file.write(content)

    with open(join(output_folder_path, 'target_text_location_links.json'), 'w', encoding='utf-8') as \
            target_text_location_links_output_file:
        content = json.dumps(target_text_location_links, default=__json_encoder_visualization)
        target_text_location_links_output_file.write(content)

    with open(join(output_folder_path, 'citation_source_links.json'), 'w', encoding='utf-8') as \
            citation_source_links_output_file:
        content = json.dumps(citation_source_links, default=__json_encoder_visualization)
        citation_source_links_output_file.write(content)

    with open(join(output_folder_path, 'important_segment_links.json'), 'w', encoding='utf-8') as \
            important_segment_links_output_file:
        content = json.dumps(important_segment_links, default=__json_encoder_visualization)
        important_segment_links_output_file.write(content)


def main():

    compare_description = "Lotte compare allows the user to find quotations in two texts, a source text and a target " \
                          "text. If known, the source text should be the one that is quoted by the target text. " \
                          "This allows the algorithm to handle things like ellipsis in quotations."

    argument_parser = ArgumentParser(description="Lotte is a tool to find quotations in texts and to visualize the"
                                                 " matching segments.")

    subparsers = argument_parser.add_subparsers(dest='command')
    subparsers.required = True
    parser_compare = subparsers.add_parser('compare', help=compare_description, description=compare_description)

    parser_compare.add_argument("source_file_path", nargs=1, metavar="source-file-path",
                                help="Path to the source text file")
    parser_compare.add_argument("target_path", nargs=1, metavar="target-path",
                                help="Path to the target text file or folder")
    parser_compare.add_argument('--text', dest="export_text", default=True, action='store_true',
                                help="Include matched text in the returned data structure")
    parser_compare.add_argument('--no-text', dest='export_text', action='store_false',
                                help="Don't include matched text in the returned data structure")
    parser_compare.add_argument('--output-type', choices=['json', 'text'], dest="output_type", default="json",
                                help="The output type")
    parser_compare.add_argument('--output-folder-path', dest="output_folder_path",
                                help="The output folder path. If this option is set the output will be saved to a file"
                                     " created in the specified folder.")
    parser_compare.add_argument('--min-match-length', dest="min_match_length", action=IntCheckAction,
                                default=5, type=int, help="The length of the shortest match (>= 3, default: 5)")

    parser_compare.add_argument('--look-back-limit', dest="look_back_limit", action=IntCheckAction,
                                default=10, type=int, help="The number of tokens to skip when looking backwards"
                                                           " (>= 0, default: 10), (Very rarely needed)")
    parser_compare.add_argument('--look-ahead-limit', dest="look_ahead_limit", action=IntCheckAction,
                                default=3, type=int, help="The number of tokens to skip when looking ahead"
                                                          " (>= 0, default: 3)")
    parser_compare.add_argument('--max-merge-distance', dest="max_merge_distance", action=IntCheckAction,
                                default=2, type=int, help="The maximum distance in tokens between two matches"
                                                          " considered for merging (>= 0, default: 2)")
    parser_compare.add_argument('--max-merge-ellipsis-distance', dest="max_merge_ellipsis_distance",
                                action=IntCheckAction, default=10, type=int,
                                help="The maximum distance in tokens between two matches considered for merging where"
                                     " the target text contains an ellipsis between the matches (>= 0, default: 10)")
    parser_compare.add_argument('--create-dated-subfolder', dest="created_dated_subfolder", default=False,
                                action='store_true',
                                help="Create a subfolder named with the current date to store the results")
    parser_compare.add_argument('--no-create-dated-subfolder', dest="created_dated_subfolder",
                                action='store_false',
                                help="Don't create a subfolder named with the current date to store the results")
    parser_compare.add_argument('--max-num-processes', dest="max_num_processes", action=IntCheckAction, default=1,
                                type=int, help="Maximum number of processes to use for parallel processing.")

    parser_visualize = subparsers.add_parser('visualize',
                                             help="Lotte visualize allows the user to create the files needed"
                                                  " for a website that visualizes the lotte algorithm results.",
                                             description="Lotte visualize allows the user to create the files needed"
                                                         " for a website that visualizes the lotte algorithm results.")

    parser_visualize.add_argument("source_file_path", nargs=1, metavar="source-file-path",
                                  help="Path to the source text file")
    parser_visualize.add_argument("target_folder_path", nargs=1, metavar="target-folder-path",
                                  help="Path to the target texts folder path")
    parser_visualize.add_argument("matches_folder_path", nargs=1, metavar="matches-folder-path",
                                  help="Path to the folder with the match files")
    parser_visualize.add_argument("output_folder_path", nargs=1, metavar="output-folder-path",
                                  help="Path to the output folder")
    parser_visualize.add_argument("--title", dest="title", help="Title of the work", default="NN")
    parser_visualize.add_argument("--author", dest="author", help="Author of the work", default="NN")
    parser_visualize.add_argument("--year", dest="year", help="Year of the work", default="0", type=int)
    parser_visualize.add_argument('--censor', dest="censor", default=False, action='store_true',
                                  help="Censor scholarly works to prevent copyright violations.")

    args = argument_parser.parse_args()

    if args.command == 'compare':
        source_path = args.source_file_path[0]
        target_path = args.target_path[0]
        export_text = args.export_text
        output_type = args.output_type
        output_folder_path = args.output_folder_path
        min_match_length = args.min_match_length
        look_ahead_limit = args.look_ahead_limit
        look_back_limit = args.look_back_limit
        max_merge_distance = args.max_merge_distance
        max_merge_ellipsis_distance = args.max_merge_ellipsis_distance
        created_dated_subfolder = args.created_dated_subfolder
        max_num_processes = args.max_num_processes

        if output_folder_path and created_dated_subfolder:
            now = datetime.now()
            date_time_string = now.strftime("%Y_%m_%d_%H_%M_%S")
            output_folder_path = join(args.output_folder_path, date_time_string)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        __run_compare(source_path, target_path, export_text, output_type, min_match_length, look_ahead_limit,
                      look_back_limit, max_merge_distance, max_merge_ellipsis_distance, output_folder_path,
                      max_num_processes)

        end_time = time.time()
        print(f'\n--- Runtime: {end_time - start_time: .2f} seconds ---')
    elif args.command == 'visualize':
        source_file_path = args.source_file_path[0]
        target_folder_path = args.target_folder_path[0]
        matches_folder_path = args.matches_folder_path[0]
        output_folder_path = args.output_folder_path[0]
        title = args.title
        author = args.author
        year = args.year
        censor = args.censor

        start_time = time.time()
        __run_visualize(source_file_path, target_folder_path, matches_folder_path, output_folder_path, title, author,
                        year, censor)
        end_time = time.time()
        print(f'\n--- Runtime: {end_time - start_time: .2f} seconds ---')


if __name__ == '__main__':
    main()
