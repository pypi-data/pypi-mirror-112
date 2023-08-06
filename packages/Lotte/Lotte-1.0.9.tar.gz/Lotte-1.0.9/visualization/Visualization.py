from yattag import Doc
import json
from os.path import join, splitext, basename, isfile, isdir
from math import ceil
from visualization.CitationSource import CitationSource
from visualization.CitationSourceLink import CitationSourceLink
from visualization.ImportantSegmentLink import ImportantSegmentLink
from visualization.TargetLocationSelection import TargetLocationSelection
from visualization.TargetText import TargetText
from visualization.ImportantSegment import ImportantSegment
from visualization.Info import Info
from visualization.TargetLocation import TargetLocation
from visualization.SourceSegment import SourceSegment
from visualization.TargetTextLocationLink import TargetTextLocationLink
from os import listdir
from pathlib import Path
import re
import copy
from match.Match import Match
from match.MatchSegment import MatchSegment

next_id = 1
KEEP_RANGE = 25


def generate_next_id():
    global next_id
    id_to_return = next_id
    next_id += 1
    return id_to_return


def json_encoder(obj):
    if isinstance(obj, set):
        return list(obj)

    if isinstance(obj, Info):
        return obj.__dict__

    return obj


def json_decoder(json_input):
    if 'source_match_segment' in json_input and 'target_match_segment' in json_input:
        return Match(json_input['source_match_segment'], json_input['target_match_segment'])
    else:
        return MatchSegment(json_input['character_start_pos'], json_input['character_end_pos'])


def generate_info_json(output_folder_path, title, author, year):
    info = Info(title, author, year)

    with open(join(output_folder_path, 'info.json'), 'w', encoding='utf-8') as info_output_file:
        content = json.dumps(info, default=json_encoder)
        info_output_file.write(content)


def get_citation_sources(matches_folder_path, source_content):
    """
    Get a list of CitationSources for all similarity files in the given similarity folder.
    :param matches_folder_path: Path to the folder with the similarity files
    :param source_content: Content of the source file
    :return: A list of CitationSources.
    """

    citation_sources = []
    segment_id_to_target_location_map = {}

    for fileOrFolder in listdir(matches_folder_path):
        matches_file_path = join(matches_folder_path, fileOrFolder)
        citation_sources, segment_id_to_target_location_map = get_citation_sources_from_file(matches_file_path,
                                                                                             citation_sources,
                                                                                             segment_id_to_target_location_map)

    for citation_source in citation_sources:
        text = ''

        for segment in citation_source.source_segments:
            content = source_content[segment.start:segment.end].strip()
            length = len(content.split(' '))
            segment.token_length = length
            segment.text = content
            text += ' ' + content

        citation_source.text = text.strip()

    citation_sources.sort(key=lambda x: x.get_start())
    return citation_sources, segment_id_to_target_location_map


def get_citation_sources_from_file(matches_file_path, citation_sources, segment_id_to_target_location_map):
    """
    Get a list of citation sources for the given similarity file.
    :param matches_file_path: The path to the similarity file
    :param citation_sources: A list of already created CitationSources
    :param segment_id_to_target_location_map: A map from a SourceSegment id to a TargetLocation
    :return: Updated list of CitationSources
    """

    if isfile(matches_file_path) and matches_file_path.endswith(".json"):
        filename = splitext(basename(matches_file_path))[0]

        with open(matches_file_path, 'r', encoding='utf-8') as matches_file:
            matches = json.load(matches_file, object_hook=json_decoder)
            matches.sort(key=lambda x: x.source_match_segment.character_start_pos)

            for match in matches:
                source_match_segment = match.source_match_segment
                target_match_segment = match.target_match_segment

                source_match_start = source_match_segment.character_start_pos
                source_match_end = source_match_segment.character_end_pos
                target_match_start = target_match_segment.character_start_pos
                target_match_end = target_match_segment.character_end_pos

                conflicting_sources = []
                conflicting_positions = []

                # Find conflicting sources, i.e. our new source would overlap with one or more existing sources.
                for i in range(0, len(citation_sources)):
                    citation_source = citation_sources[i]
                    if (citation_source.get_start() <= source_match_start < citation_source.get_end() or
                            citation_source.get_start() < source_match_end <= citation_source.get_end() or
                            source_match_start <= citation_source.get_start()
                            and source_match_end >= citation_source.get_end()):
                        conflicting_sources.append(citation_source)
                        conflicting_positions.append(i)

                # In case there are no conflicting sources, we can just create a new CitationSource.
                if len(conflicting_sources) == 0:
                    new_id = generate_next_id()
                    new_segment = SourceSegment.from_frequency(new_id, source_match_start, source_match_end, 1)
                    add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                    target_match_end)

                    new_citation_source = CitationSource.from_segment(generate_next_id(), new_segment)

                    new_citation_source_pos = len(citation_sources)
                    if len(citation_sources) > 0:
                        for i in range(0, len(citation_sources)):
                            if source_match_end <= citation_sources[i].get_start():
                                new_citation_source_pos = i
                                break

                    citation_sources.insert(new_citation_source_pos, new_citation_source)
                else:
                    # It should be noted that new segments are created with a count of 0 and that the count is updated
                    # in a later step.

                    # In case there are conflicting sources, we need to check if the new match starts before the first
                    # conflicting source. If that is the case, then we need to extend the conflicting source with a new
                    # segment.
                    if source_match_start < conflicting_sources[0].get_start():
                        new_id = generate_next_id()
                        new_segment = SourceSegment.from_frequency(new_id, source_match_start,
                                                                   conflicting_sources[0].get_start(), 0)
                        add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                        target_match_end)
                        conflicting_sources[0].add_segment_to_start(new_segment)

                    # We then need to check if the new match ends after the last conflicting source. It that is the
                    # case, we need to extend the conflicting source with a new segment.
                    if source_match_end > conflicting_sources[-1].get_end():
                        new_id = generate_next_id()
                        new_segment = SourceSegment.from_frequency(new_id, conflicting_sources[-1].get_end(),
                                                                   source_match_end, 0)
                        add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                        target_match_end)
                        conflicting_sources[-1].add_segment_to_end(new_segment)

                    new_source = CitationSource(conflicting_sources[0].my_id,
                                                copy.deepcopy(conflicting_sources[0].source_segments))

                    # In case there is more than one conflicting source, we need to extend the new_source with the
                    # existing segments and citation targets from the conflicting sources.
                    for i in range(1, len(conflicting_sources)):
                        next_source = conflicting_sources[i]

                        # We need to make sure that we create a new segment which covers the gap between the
                        # current and the next source.
                        if next_source.get_start() > new_source.get_end():
                            new_id = generate_next_id()
                            new_source.add_segment_to_end(SourceSegment.from_frequency(new_id, new_source.get_end(),
                                                                                       next_source.get_start(), 0))
                            add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                            target_match_end)

                        new_source.source_segments.extend(copy.deepcopy(next_source.source_segments))

                    # We now need to remove the old conflicting sources and add the newly created source
                    for conflicting_position in reversed(conflicting_positions):
                        del citation_sources[conflicting_position]

                    citation_sources.insert(conflicting_positions[0], new_source)

                    # the last step is to update the existing segments to create non overlapping segments and adjust
                    # the frequency of a segment appearing in citations.

                    current_pos = source_match_start
                    segments = new_source.source_segments

                    while current_pos < source_match_end:
                        new_segment = None
                        new_segment_pos = -1

                        for segment_pos in range(0, len(segments)):
                            segment = segments[segment_pos]

                            if current_pos == segment.start:
                                if source_match_end < segment.end:
                                    new_id = generate_next_id()
                                    segment_old_end = segment.end
                                    segment.end = source_match_end

                                    new_segment = SourceSegment.from_frequency(new_id, source_match_end,
                                                                               segment_old_end, segment.frequency)
                                    segment.increment_frequency()
                                    copy_links(segment_id_to_target_location_map, segment.my_id, new_id)
                                    add_to_link_map(segment_id_to_target_location_map, segment.my_id, filename,
                                                    target_match_start, target_match_end)
                                    new_segment_pos = segment_pos + 1
                                    current_pos = source_match_end
                                    break
                                elif source_match_end >= segment.end:
                                    segment.increment_frequency()
                                    add_to_link_map(segment_id_to_target_location_map, segment.my_id, filename,
                                                    target_match_start, target_match_end)
                                    current_pos = segment.end
                                    break

                            elif segment.start < current_pos < segment.end:
                                new_id = generate_next_id()
                                segment_old_end = segment.end
                                segment.end = current_pos

                                new_segment = SourceSegment.from_frequency(new_id, current_pos, segment_old_end,
                                                                           segment.frequency)
                                copy_links(segment_id_to_target_location_map, segment.my_id, new_id)
                                new_segment_pos = segment_pos + 1
                                break
                            elif current_pos == segment.end:
                                if segment_pos < len(segments) - 1:
                                    current_pos = segments[segment_pos + 1].start
                                else:
                                    break
                            elif segment_pos == len(segments) - 1:
                                current_pos += 1

                            if current_pos >= source_match_end:
                                break

                        if new_segment:
                            segments.insert(new_segment_pos, new_segment)

    return citation_sources, segment_id_to_target_location_map


def add_to_link_map(link_map, new_id, filename, target_match_start, target_match_end):
    if new_id in link_map:
        link_map[new_id].append((filename, target_match_start, target_match_end))
    else:
        new_list = [(filename, target_match_start, target_match_end)]
        link_map[new_id] = new_list


def copy_links(link_map, old_id, new_id):
    link_map[new_id] = copy.deepcopy(link_map[old_id])


def add_important_segments(citation_sources):
    """
    Generate and add important segments for the given CitationSources.
    :param citation_sources: CitationSources for which to generate and add the important segments
    """

    pattern = re.compile("[A-Za-zäöüß]")
    # stopwords = ['der', 'die', 'das', 'daß', 'ein', 'eine', 'einer', 'eines', 'und', 'vor', 'von', 'da', 'vom', 'in',
    #              'mit', 'was', 'es', 'um', 'doch', 'auch', 'ihn']
    stopwords = []

    for citation_source in citation_sources:
        source_segment_ids = []
        last_frequency = -1
        frequency_sum = 0
        token_length = -1
        text = ''
        count = 0

        important_segments = []
        segment_pos = 0

        while segment_pos < len(citation_source.source_segments):
            segment = citation_source.source_segments[segment_pos]
            next_segment = None

            if segment_pos + 1 < len(citation_source.source_segments):
                next_segment = citation_source.source_segments[segment_pos + 1]

            if last_frequency == -1:
                source_segment_ids = [segment.my_id]
                last_frequency = segment.frequency
                frequency_sum = segment.frequency
                token_length = segment.token_length
                text = segment.text
                count = 1
                segment_pos += 1
            else:
                diff_last = abs(last_frequency - segment.frequency)
                diff_next = None

                if next_segment:
                    diff_next = abs(segment.frequency - next_segment.frequency)

                if (not diff_next or token_length <= 3 or (diff_next and diff_last <= diff_next)) and diff_last <= 2:
                    source_segment_ids.append(segment.my_id)
                    frequency_sum += segment.frequency
                    token_length += segment.token_length
                    text += ' ' + segment.text
                    count += 1
                    segment_pos += 1
                elif diff_next and diff_next < diff_last and diff_next <= 2:
                    text = re.sub(r'^[\W]+', '', text)
                    important_segments.append(ImportantSegment(generate_next_id(), source_segment_ids,
                                                               round(frequency_sum / count, 1), token_length, text))
                    source_segment_ids = [segment.my_id, next_segment.my_id]
                    last_frequency = segment.frequency
                    frequency_sum = segment.frequency + next_segment.frequency
                    token_length = segment.token_length + next_segment.token_length
                    text = segment.text + ' ' + next_segment.text
                    count = 2
                    segment_pos += 2
                else:
                    text = re.sub(r'^[\W]+', '', text)
                    important_segments.append(ImportantSegment(generate_next_id(), source_segment_ids,
                                                               round(frequency_sum / count, 1), token_length, text))
                    source_segment_ids = [segment.my_id]
                    last_frequency = segment.frequency
                    frequency_sum = segment.frequency
                    token_length = segment.token_length
                    text = segment.text
                    count = 1
                    segment_pos += 1

        text = re.sub(r'^[\W]+', '', text)

        important_segments.append(ImportantSegment(generate_next_id(), source_segment_ids,
                                                   round(frequency_sum / count, 1), token_length, text))

        # for important_segment in important_segments:
        #     if important_segment.token_length <= 2:
        #         if important_segment.text:
        #             start = 0
        #             end = 0
        #             for ct in citation_sources:
        #                 for ss in ct.source_segments:
        #                     if ss.my_id == important_segment.source_segment_ids[0]:
        #                         start = ss.start
        #
        #                     if ss.my_id == important_segment.source_segment_ids[-1]:
        #                         end = ss.end
        #                         break
        #
        #                 if start and end:
        #                     break
        #
        #             print('\n' + important_segment.text + '\n' + source_text[start - 30:end + 30])

        important_segments.sort(key=lambda x: x.frequency, reverse=True)
        important_segments = [x for x in important_segments if x.text and pattern.search(x.text)
                              and not x.text.lower() in stopwords]

        citation_source.important_segments = important_segments[:10]


def generate_target_texts(similarity_folder_path, target_folder_path):
    target_texts = []
    target_location_id_to_source_location_map = {}

    for fileOrFolder in listdir(similarity_folder_path):
        similarity_file_path = join(similarity_folder_path, fileOrFolder)
        if isdir(similarity_file_path) or not similarity_file_path.endswith(".json"):
            continue

        target_text, temp_target_location_id_to_source_location_map = get_target_text_from_file(similarity_file_path,
                                                                                                target_folder_path)
        target_texts.append(target_text)

        target_location_id_to_source_location_map.update(temp_target_location_id_to_source_location_map)

    return target_texts, target_location_id_to_source_location_map


def get_target_text_from_file(matches_file_path, target_folder_path):
    filename = splitext(basename(matches_file_path))[0]
    target_text_id = generate_next_id()

    with open(matches_file_path, 'r', encoding='utf-8') as match_file:
        matches = json.load(match_file, object_hook=json_decoder)
        matches.sort(key=lambda x: x.source_match_segment.character_start_pos)

    with open(join(target_folder_path, filename + '.txt'), 'r', encoding='utf-8') as target_file:
        target_content = target_file.read()

    target_locations = []
    target_location_id_to_source_location_map = {}

    for match in matches:
        source_match_segment = match.source_match_segment
        target_match_segment = match.target_match_segment
        source_character_start_pos = source_match_segment.character_start_pos
        source_character_end_pos = source_match_segment.character_end_pos
        target_character_start_pos = target_match_segment.character_start_pos
        target_character_end_pos = target_match_segment.character_end_pos

        text = target_content[target_character_start_pos:target_character_end_pos]

        new_id = generate_next_id()
        target_locations.append(TargetLocation(new_id, target_character_start_pos, target_character_end_pos, text))
        target_location_id_to_source_location_map[new_id] = (source_character_start_pos, source_character_end_pos)

    target_locations.sort(key=lambda x: x.start)

    return TargetText(target_text_id, filename, target_locations), target_location_id_to_source_location_map


def generate_target_text_location_links(citation_sources, target_texts, target_location_id_to_source_location_map):
    target_text_location_links = []

    for target_text in target_texts:
        new_target_text_location_links = generate_target_text_location_links_for_target_text(citation_sources,
                                                                                             target_text,
                                                                                             target_location_id_to_source_location_map)
        target_text_location_links.extend(new_target_text_location_links)

    return target_text_location_links


def generate_target_text_location_links_for_target_text(citation_sources, target_text,
                                                        target_location_id_to_source_location_map):
    target_text_location_links = []

    for target_location in target_text.target_locations:
        target_location_id = target_location.my_id
        source_character_start_pos, source_character_end_pos = target_location_id_to_source_location_map[
            target_location_id]

        source_segment_start_id = None
        source_segment_end_id = None

        for citation_source in citation_sources:
            for source_segment in citation_source.source_segments:
                if source_segment.start == source_character_start_pos:
                    source_segment_start_id = source_segment.my_id

                if source_segment_start_id and source_segment.end == source_character_end_pos:
                    source_segment_end_id = source_segment.my_id

                if source_segment_start_id and source_segment_end_id:
                    break

            if source_segment_start_id and source_segment_end_id:
                break

        if not (source_segment_start_id and source_segment_end_id):
            raise Exception('This should never happen!')

        target_text_location_link = TargetTextLocationLink(target_text.my_id, target_location_id,
                                                           source_segment_start_id, source_segment_end_id)
        target_text_location_links.append(target_text_location_link)

    return target_text_location_links


def generate_citation_source_links(citation_sources, target_texts, segment_id_to_target_location_map):
    citation_source_links = []

    for citation_source in citation_sources:
        citation_source_link = generate_citation_source_links_for_citation_source(citation_source, target_texts,
                                                                                  segment_id_to_target_location_map)
        citation_source_links.append(citation_source_link)

    return citation_source_links


def generate_citation_source_links_for_citation_source(citation_source, target_texts,
                                                       segment_id_to_target_location_map):
    target_location_selections = []

    for source_segment in citation_source.source_segments:
        triple_list = segment_id_to_target_location_map[source_segment.my_id]

        for (filename, target_match_start, target_match_end) in triple_list:
            target_text_id = get_target_text_id(filename, target_texts)
            existing_target_location_selection = None

            for tls in target_location_selections:
                if tls.target_text_id == target_text_id:
                    existing_target_location_selection = tls
                    break

            if existing_target_location_selection:
                target_location_id = get_target_location_id(target_texts, target_text_id, target_match_start,
                                                            target_match_end)
                existing_target_location_selection.add_target_location_id(target_location_id)
            else:
                target_location_id = get_target_location_id(target_texts, target_text_id, target_match_start,
                                                            target_match_end)
                target_location_selection = TargetLocationSelection(target_text_id, target_location_id)
                target_location_selections.append(target_location_selection)

    return CitationSourceLink(citation_source.my_id, target_location_selections)


def generate_important_segment_links(citation_sources, target_texts, link_map):
    important_segment_links = []

    for citation_source in citation_sources:
        for important_segment in citation_source.important_segments:
            target_location_selections = []

            for source_segment_id in important_segment.source_segment_ids:
                triple_list = link_map[source_segment_id]

                for (filename, target_match_start, target_match_end) in triple_list:
                    target_text_id = get_target_text_id(filename, target_texts)
                    target_location_id = get_target_location_id(target_texts, target_text_id, target_match_start,
                                                                target_match_end)

                    found = False
                    for existing_target_location_selection in target_location_selections:
                        if existing_target_location_selection.target_text_id == target_text_id:
                            existing_target_location_selection.add_target_location_id(target_location_id)
                            found = True
                            break

                    if not found:
                        target_location_selections.append(TargetLocationSelection(target_text_id, target_location_id))

            important_segment_link = ImportantSegmentLink(important_segment.my_id, target_location_selections)
            important_segment_links.append(important_segment_link)

    return important_segment_links


def get_target_text_id(filename, target_texts):
    for target_text in target_texts:
        if target_text.filename == filename:
            return target_text.my_id

    raise Exception('This should never happen')


def get_target_location_id(target_texts, target_text_id, target_match_start, target_match_end):
    for target_text in target_texts:
        if target_text.my_id == target_text_id:
            for target_location in target_text.target_locations:
                if target_location.start == target_match_start and target_location.end == target_match_end:
                    return target_location.my_id

    raise Exception('This should never happen!')


def calculate_max_target_texts_count(citation_source_links):
    max_citation_sources = 0

    for citation_source_link in citation_source_links:
        max_citation_sources = max(max_citation_sources, len(citation_source_link.target_location_selections))

    return max_citation_sources


def calculate_max_segment_frequency(citation_sources):
    max_segment_frequency = 0

    for citation_source in citation_sources:
        for source_segment in citation_source.source_segments:
            max_segment_frequency = max(max_segment_frequency, source_segment.frequency)

    return max_segment_frequency


def generate_source_html(source_content, citation_sources, output_folder_path, max_target_texts_count,
                         max_segment_frequency, citation_source_links):
    doc, tag, text = Doc().tagtext()

    content = ''
    citation_source_start_pos = 0
    segments = []

    for char_pos in range(0, len(source_content)):
        finished = False
        for citation_source_pos in range(citation_source_start_pos, len(citation_sources)):
            citation_source = citation_sources[citation_source_pos]

            for segment_pos in range(0, len(citation_source.source_segments)):
                segment = citation_source.source_segments[segment_pos]

                if char_pos < segment.start:
                    finished = True
                    break

                if segment.start == char_pos:
                    citation_source_start_pos = citation_source_pos

                    if segment_pos == 0:
                        with tag('span', klass='text_standard'):
                            doc.asis(content)
                        segments.clear()
                    else:
                        segments.append(('asis', content))

                    content = ''
                    finished = True
                    break
                elif segment.end == char_pos or (segment_pos == len(citation_source.source_segments) - 1 and char_pos == len(source_content) - 1):
                    citation_count = calculate_target_text_count(citation_source, citation_source_links)
                    segment_frequency = segment.frequency
                    citation_count_percentage = int((ceil((citation_count / max_target_texts_count) * 10.0) / 10.0) * 10)
                    segment_frequency_percentage = int((ceil((segment_frequency / max_segment_frequency) * 10.0) / 10.0) * 10)
                    klass_background = f'source_segment_background_o{citation_count_percentage}'
                    klass_font = f'source_segment_font_s{segment_frequency_percentage}'
                    klass = f'source_segment {klass_background} {klass_font}'
                    tag_id = f'sourceSegment_{citation_source.my_id}_{segment.my_id}'
                    segments.append(('span', content, klass, tag_id, segment.token_length))
                    content = ''
                    finished = True

                    if segment_pos == len(citation_source.source_segments) - 1:
                        citation_source_start_pos += 1
                        with tag('span', klass='citation_source_container', id=str(citation_source.my_id)):
                            for segment in segments:
                                if segment[0] == 'asis':
                                    if segment[1]:
                                        with tag('span', klass='text_standard'):
                                            doc.asis(segment[1])
                                else:
                                    with tag('span', ('data-token-count', segment[4]), klass=segment[2], id=segment[3]):
                                        doc.asis(segment[1])
                    break

            if finished:
                break

        if source_content[char_pos] == '\n':
            content += '<br>'
        else:
            content += source_content[char_pos]

    if len(content) > 0:
        with tag('span', klass='text_standard'):
            doc.asis(content)

    with open(join(output_folder_path, 'source' + '.html'), 'w', encoding='utf-8') as output_file:
        output_file.write(doc.getvalue())


def calculate_target_text_count(citation_source, citation_source_links):
    for citation_source_link in citation_source_links:
        if citation_source_link.citation_source_id == citation_source.my_id:
            return len(citation_source_link.target_location_selections)

    return None


def generate_target_html(target_texts, target_folder_path, output_folder_path, censor):
    Path(join(output_folder_path, 'target')).mkdir(parents=True, exist_ok=True)

    for target_text in target_texts:
        filename = target_text.filename

        with open(join(target_folder_path, filename + '.txt'), 'r', encoding='utf-8') as target_file_path:
            target_content = target_file_path.read()

        doc, tag, text = Doc().tagtext()

        content = ''
        location_start_pos = 0
        for char_pos in range(0, len(target_content)):
            for location_pos in range(location_start_pos, len(target_text.target_locations)):
                location = target_text.target_locations[location_pos]

                if char_pos < location.start:
                    break

                if location.start == char_pos:
                    location_start_pos = location_pos
                    if censor:
                        if len(content) < KEEP_RANGE * 2:
                            doc.asis(content)
                        else:
                            start = 0

                            if location_pos > 0:
                                start = KEEP_RANGE

                            content_replaced = re.sub("[A-Za-z0-9ÄÖÜäüöß]", "x", content[start:-KEEP_RANGE])
                            doc.asis(content[0:start])
                            with tag('span', klass='censored'):
                                doc.asis(content_replaced)
                            doc.asis(content[-KEEP_RANGE:])
                    else:
                        doc.asis(content)
                    content = ''
                    break
                elif location.end == char_pos:
                    with tag('span', klass='target_location', id=str(location.my_id)):
                        doc.asis(content)
                    content = ''
                    break

            if target_content[char_pos] == '\n':
                content += '<br>'
            else:
                content += target_content[char_pos]

        if len(content) > 0:
            if censor:
                if len(content) < KEEP_RANGE:
                    doc.asis(content)
                else:
                    doc.asis(content[0:KEEP_RANGE])
                    content = re.sub("[A-Za-z0-9ÄÖÜäüöß]", "x", content[KEEP_RANGE:])
                    with tag('span', klass='censored'):
                        doc.asis(content)
            else:
                doc.asis(content)

        with open(join(output_folder_path, 'target/' + filename + '.html'), 'w', encoding='utf-8') as output_file:
            output_file.write(doc.getvalue())
