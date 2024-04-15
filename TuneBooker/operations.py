#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import http.client
import sys
from deejay_types import *
from collections import defaultdict

###############################################################################
#                               Helper functions                              #
###############################################################################

def get_children_field(field_dict, tag):
    return field_dict.get(tag.value, None)

def get_field_value(field_dict, tag):
    return get_children_field(field_dict, tag)[Attribute.Attribute_value.value]

# element tree to python dict, taken from:
# https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update((k, v) for k, v in t.attrib.items())
    return d

def parse_response_message(response_message_str, test=False):
    response_message = ET.fromstring(response_message_str)

    response_dict = etree_to_dict(response_message)

    response_message_dict = get_children_field(response_dict, Tag.Tag_ResponseMessage)

    rs = get_field_value(response_message_dict, Tag.Tag_ResultStatus)
    rm = get_field_value(response_message_dict, Tag.Tag_ResultMessage)
    if rs != ResultStatus.ResultStatus_Success.value and not test:
        print("Result Status is not Success:", rs)
        print(rm)
        sys.exit(1)

    return response_message_dict

def post_request_message(host, port, operation, parameters_list=None, song_query_list=None, test=False):
    # XML root: "RequestMessage"
    request_message = ET.Element(Tag.Tag_RequestMessage.value)

    # "Operation" element
    ET.SubElement(request_message, Tag.Tag_Operation.value, type=Type.Type_Enumeration.value, value=operation)

    # Extra parameters
    if parameters_list:
        parameters = ET.SubElement(request_message, Tag.Tag_Parameters.value)

        for req_tag, req_type, req_value in parameters_list:
            ET.SubElement(parameters, req_tag, type=req_type, value=req_value)

        # "SongQuery" parameters
        if song_query_list:
            song_query = ET.SubElement(parameters, Tag.Tag_SongQuery.value, type=Type.Type_Object.value)

            for req_tag, req_type, req_value in song_query_list:
                ET.SubElement(song_query, req_tag, type=req_type, value=req_value)

    # Transform ElementTree to a string to be sent
    raw_xml_request = ET.tostring(request_message)

    # Actually send the request
    conn = http.client.HTTPConnection(host + ":" + str(port))
    conn.request("POST", "/", body=raw_xml_request,
                 headers={'Content-Type': 'application/xml'})

    # Parse and return the response
    return parse_response_message(conn.getresponse().read().decode('utf-8'), test)

def print_song_information(song):
    genre = get_field_value(song, Tag.Tag_Genre)
    artist = get_field_value(song, Tag.Tag_Artist)
    title = get_field_value(song, Tag.Tag_Title)
    duration = get_field_value(song, Tag.Tag_Duration)
    position = get_field_value(song, Tag.Tag_Position)

    print(" - Position:", position)
    print("   - Title: \t", title)
    print("   - Duration: \t", duration)
    print("   - Artist: \t", artist)
    print("   - Genre: \t", genre)

def print_common_response_information(response_dict):
    status = get_field_value(response_dict, Tag.Tag_ResultStatus)
    message = get_field_value(response_dict, Tag.Tag_ResultMessage)

    try:
        operation = get_field_value(response_dict, Tag.Tag_Operation)
    except Exception as e:
        # Operation field may not be returned if an error occurs
        print("Operation field missing")
        sys.exit(1)

    print("Status: \t", status)
    print("Message: \t", message)
    print("Operation: \t", operation)

###############################################################################
#                             Operation functions                             #
###############################################################################

def create_playlist_operation(args):
    response_dict = post_request_message(args.host, args.port, Operation.Operation_CreatePlaylist.value, test=args.test)
    if args.test:
        return response_dict

    try:
        return_values = get_children_field(response_dict, Tag.Tag_ReturnValues)
        playlist_id = get_field_value(return_values, Tag.Tag_PlaylistID)
    except Exception as e:
        print("Failed to access the playlist ID", e)
        sys.exit(1)

    print_common_response_information(response_dict)
    print("Playlist ID: \t", playlist_id)

    return None

def delete_playlist_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_DeletePlaylist.value, parameters, test=args.test)
    if args.test:
        return response_dict


    print_common_response_information(response_dict)

    return None

def clear_playlist_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_ClearPlaylist.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None

def show_playlist_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_ShowPlaylist.value, parameters, test=args.test)
    if args.test:
        return response_dict

    try:
        return_values = get_children_field(response_dict, Tag.Tag_ReturnValues)

        playlist_position = get_field_value(return_values, Tag.Tag_PlaylistPosition)
        current_song_timestamp = get_field_value(return_values, Tag.Tag_Timestamp)
        loop_setting = get_field_value(return_values, Tag.Tag_LoopSetting)

        song_list = get_children_field(return_values, Tag.Tag_SongList)
        song_list_size = get_children_field(song_list, Attribute.Attribute_count)
        songs = get_children_field(song_list, Tag.Tag_Song)
    except Exception as e:
        print("Failed to access some playlist information", e)
        sys.exit(1)

    print_common_response_information(response_dict)
    print("Playlist Info:")
    print(" - Position: \t ", playlist_position)
    print(" - Timestamp: \t ", current_song_timestamp)
    print(" - Loop Set.: \t ", loop_setting)
    print("Song List:")
    print(" - Count: \t", song_list_size)
    for song in songs:
        print_song_information(song)

    return response_dict

def config_loop_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))
    parameters.append((Tag.Tag_LoopSetting.value, Type.Type_Enumeration.value, args.setting))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_ConfigureLoop.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None

def queue_song_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    song_query_list = []
    song_query_list.append((Tag.Tag_Title.value, Type.Type_String.value, args.title))
    if args.genre:
        song_query_list.append((Tag.Tag_Genre.value, Type.Type_String.value, args.genre))
    if args.artist:
        song_query_list.append((Tag.Tag_Artist.value, Type.Type_String.value, args.artist))
    if args.position:
        song_query_list.append((Tag.Tag_Position.value, Type.Type_Integer.value, str(args.position)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_QueueSong.value, parameters, song_query_list, test=args.test)
    if args.test:
        return response_dict

    try:
        return_values = get_children_field(response_dict, Tag.Tag_ReturnValues)
        song = get_children_field(return_values, Tag.Tag_Song)
    except Exception as e:
        print("Failed to access returned song information", e)
        sys.exit(1)

    print_common_response_information(response_dict)
    print("Song:")
    print_song_information(song)


    return None

def dequeue_song_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))
    parameters.append((Tag.Tag_Position.value, Type.Type_Integer.value, str(args.position)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_DequeueSong.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None

def shift_song_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))
    parameters.append((Tag.Tag_Position.value, Type.Type_Integer.value, str(args.position)))
    parameters.append((Tag.Tag_NewPosition.value, Type.Type_Integer.value, str(args.new_position)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_ShiftSongPosition.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None

def peek_song_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_ShowCurrentSong.value, parameters, test=args.test)
    if args.test:
        return response_dict

    try:
        return_values = get_children_field(response_dict, Tag.Tag_ReturnValues)
        song = get_children_field(return_values, Tag.Tag_Song)
    except Exception as e:
        print("Failed to access returned song information", e)
        sys.exit(1)

    print_common_response_information(response_dict)
    print("Song:")
    print_song_information(song)

    return None

def play_song_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))
    parameters.append((Tag.Tag_Position.value, Type.Type_Integer.value, str(args.position)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_SetSong.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None

def skip_song_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_SkipSong.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None

def skip_time_operation(args):
    parameters = []
    parameters.append((Tag.Tag_PlaylistID.value, Type.Type_Integer.value, str(args.playlist)))

    # depending on the direction, change the time argument from
    # positive to negative
    parameters.append((Tag.Tag_TimeInterval.value, Type.Type_Integer.value, str(args.direction * args.time * 1000)))

    response_dict = post_request_message(args.host, args.port, Operation.Operation_TimeSkip.value, parameters, test=args.test)
    if args.test:
        return response_dict

    print_common_response_information(response_dict)

    return None
