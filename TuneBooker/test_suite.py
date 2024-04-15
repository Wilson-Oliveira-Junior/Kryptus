from distutils.bcppcompiler import BCPPCompiler
from urllib import response

from regex import B, D
from operations import *
import sys
import copy

def run_test_suite(args):
    if args.suite == "basic":
        run_basic_tests(args)
    elif args.suite == "full":
        run_basic_tests(args)
        run_bonus_tests(args)
    else:
        # Should never happen
        print("Invalid test suite")
        sys.exit(1)

# Basic suite
def run_basic_tests(args):
    try:
        run_create_playlist_tests(args)
        run_delete_playlist_tests(args)
        run_queue_song_tests(args)  
        run_dequeue_song_tests(args)    
        run_show_playlist_tests(args)
    except Exception as e:
        print(e)
        sys.exit(1)

# Bonus suite
def run_bonus_tests(args):
    try:
        run_clear_playlist_tests(args)
        run_peek_song_tests(args)
        run_time_skip_tests(args)
        run_configure_loop_tests(args)
        run_shift_song_tests(args)
        run_play_song_tests(args)
        run_skip_song_tests(args)
    except Exception as e:
        print(e)
        sys.exit(1)

###############################################################################
#                               Basic Tests                                   #
###############################################################################
def run_create_playlist_tests(args):
    print("\nRunning create playlist tests...")
    
    try:
        # Case 1: Two playlists should't have the same ID
        pl1_response_dict = create_playlist_operation(args)
        pl1_result_status = get_field_value(pl1_response_dict, Tag.Tag_ResultStatus)
        pl1_result_message = get_field_value(pl1_response_dict, Tag.Tag_ResultMessage)

        assert (pl1_result_status == ResultStatus.ResultStatus_Success.value), "Failed to create playlist 1: {}".format(pl1_result_message)

        pl2_response_dict = create_playlist_operation(args)
        pl2_result_status = get_field_value(pl2_response_dict, Tag.Tag_ResultStatus)
        pl2_result_message = get_field_value(pl2_response_dict, Tag.Tag_ResultMessage)

        assert (pl2_result_status == ResultStatus.ResultStatus_Success.value), "Failed to create playlist 2: {}".format(pl2_result_message)

        pl1_return_values = get_children_field(pl1_response_dict, Tag.Tag_ReturnValues)
        pl1_id = get_field_value(pl1_return_values, Tag.Tag_PlaylistID)

        pl2_return_values = get_children_field(pl2_response_dict, Tag.Tag_ReturnValues)
        pl2_id = get_field_value(pl2_return_values, Tag.Tag_PlaylistID)

        assert (pl1_id != pl2_id), "Both playlists have the same ID"

        print("Case 1: OK")
    
    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

def run_delete_playlist_tests(args):
    print("\nRunning delete playlist tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)
    
    try:
        # Case 1: Deleting a playlist that doesn't exist should return a LogicalError
        # Test this by trying to delete a playlist with negative ID, which would never exist
        dl1_args = copy.deepcopy(args)
        dl1_args.playlist = -1
        dl1_response_dict = delete_playlist_operation(dl1_args)
        dl1_result_status = get_field_value(dl1_response_dict, Tag.Tag_ResultStatus)

        assert (dl1_result_status == ResultStatus.ResultStatus_LogicalError.value), "Deleting a nonexistent playlist did not return a logical error"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

    try:
        # Case 2: Deleting a playlist that exists should work
        dl2_args = copy.deepcopy(args)
        dl2_args.playlist = pl_id
        dl2_response_dict = delete_playlist_operation(dl2_args)
        dl2_result_status = get_field_value(dl2_response_dict, Tag.Tag_ResultStatus)
        dl2_result_message = get_field_value(dl2_response_dict, Tag.Tag_ResultMessage)

        assert (dl2_result_status == ResultStatus.ResultStatus_Success.value), "Deleting an existent playlist did not work: {}".format(dl2_result_message)

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e))

def run_queue_song_tests(args):
    print("\nRunning queue song tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)
    
    try:
        # Case 1: Queing a song just by the title
        qs1_args = copy.deepcopy(args)
        qs1_args.playlist = pl_id
        qs1_args.title = "All Star"
        qs1_args.genre = None
        qs1_args.artist = None
        qs1_args.position = None
        qs1_response_dict = queue_song_operation(qs1_args)
        qs1_result_status = get_field_value(qs1_response_dict, Tag.Tag_ResultStatus)
        qs1_result_message = get_field_value(qs1_response_dict, Tag.Tag_ResultMessage)

        assert (qs1_result_status == ResultStatus.ResultStatus_Success.value), "Queueing a song by title did not work: {}".format(qs1_result_message)

        qs1_return_values = get_children_field(qs1_response_dict, Tag.Tag_ReturnValues)
        qs1_queued_song = get_children_field(qs1_return_values, Tag.Tag_Song)
        qs1_title = get_field_value(qs1_queued_song, Tag.Tag_Title)
        qs1_genre = get_field_value(qs1_queued_song, Tag.Tag_Genre)
        qs1_artist = get_field_value(qs1_queued_song, Tag.Tag_Artist)
        qs1_duration = get_field_value(qs1_queued_song, Tag.Tag_Duration)
        qs1_position = get_field_value(qs1_queued_song, Tag.Tag_Position)

        assert (qs1_title.lower() == "All Star".lower()), "Wrong song title"
        assert (qs1_genre.lower() == "Pop".lower()), "Wrong song genre"
        assert (qs1_artist.lower() == "Smash Mouth".lower()), "Wrong song artist"
        assert (qs1_duration == "200373"), "Wrong song duration"
        assert (qs1_position == "1"), "Wrong song position"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

    try:
        # Case 2: Queing a song with all parameters 
        qs2_args = copy.deepcopy(args)
        qs2_args.playlist = pl_id
        qs2_args.title = "gas GAS gAs"
        qs2_args.genre = "EuroBEAT"
        qs2_args.artist = "MANUEL caramori"
        qs2_args.position = 1
        qs2_response_dict = queue_song_operation(qs2_args)
        qs2_result_status = get_field_value(qs2_response_dict, Tag.Tag_ResultStatus)
        qs2_result_message = get_field_value(qs2_response_dict, Tag.Tag_ResultMessage)

        assert (qs2_result_status == ResultStatus.ResultStatus_Success.value), "Queueing a song with all parameters did not work: {}".format(qs2_result_message)

        qs2_return_values = get_children_field(qs2_response_dict, Tag.Tag_ReturnValues)
        qs2_queued_song = get_children_field(qs2_return_values, Tag.Tag_Song)
        qs2_title = get_field_value(qs2_queued_song, Tag.Tag_Title)
        qs2_genre = get_field_value(qs2_queued_song, Tag.Tag_Genre)
        qs2_artist = get_field_value(qs2_queued_song, Tag.Tag_Artist)
        qs2_duration = get_field_value(qs2_queued_song, Tag.Tag_Duration)
        qs2_position = get_field_value(qs2_queued_song, Tag.Tag_Position)

        assert (qs2_title.lower() == "gas GAS gAs".lower()), "Wrong song title"
        assert (qs2_genre.lower() == "EuroBEAT".lower()), "Wrong song genre"
        assert (qs2_artist.lower() == "MANUEL caramori".lower()), "Wrong song artist"
        assert (qs2_duration == "196000"), "Wrong song duration"
        assert (qs2_position == "1"), "Wrong song position"

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e))

def run_dequeue_song_tests(args):
    print("\nRunning dequeue song tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    qs3_args = copy.deepcopy(qs1_args)
    qs3_args.title = "Dragostea Din Tei"
    queue_song_operation(qs3_args)

    qs4_args = copy.deepcopy(qs1_args)
    qs4_args.title = "Fly me to the Moon"
    queue_song_operation(qs4_args)

    qs5_args = copy.deepcopy(qs1_args)
    qs5_args.title = "Suicide Mission"
    queue_song_operation(qs5_args)

    try:
        # Case 1: Dequeue the last song
        ds1_args = copy.deepcopy(args)
        ds1_args.playlist = pl_id
        ds1_args.position = 5
        ds1_response_dict = dequeue_song_operation(ds1_args)
        ds1_result_status = get_field_value(ds1_response_dict, Tag.Tag_ResultStatus)
        ds1_result_message = get_field_value(ds1_response_dict, Tag.Tag_ResultMessage)

        assert (ds1_result_status == ResultStatus.ResultStatus_Success.value), "Dequeing the last song of the playlist did not work: {}".format(ds1_result_message)

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

    try:
        # Case 2: Dequeue the first song
        ds2_args = copy.deepcopy(args)
        ds2_args.playlist = pl_id
        ds2_args.position = 1
        ds2_response_dict = dequeue_song_operation(ds2_args)
        ds2_result_status = get_field_value(ds2_response_dict, Tag.Tag_ResultStatus)
        ds2_result_message = get_field_value(ds2_response_dict, Tag.Tag_ResultMessage)

        assert (ds2_result_status == ResultStatus.ResultStatus_Success.value), "Dequeing the first song of the playlist did not work: {}".format(ds2_result_message)

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e))

    try:
        # Case 3: Dequeue the middle song
        ds3_args = copy.deepcopy(args)
        ds3_args.playlist = pl_id
        ds3_args.position = 2
        ds3_response_dict = dequeue_song_operation(ds3_args)
        ds3_result_status = get_field_value(ds3_response_dict, Tag.Tag_ResultStatus)
        ds3_result_message = get_field_value(ds3_response_dict, Tag.Tag_ResultMessage)

        assert (ds3_result_status == ResultStatus.ResultStatus_Success.value), "Dequeing the middle song of the playlist did not work: {}".format(ds3_result_message)

        print("Case 3: OK")

    except Exception as e:
        raise Exception("Case 3 failed: {}".format(e))

def run_show_playlist_tests(args):
    print("\nRunning show playlist tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    try:
        # Case 1: Show empty playlist
        sp1_args = copy.deepcopy(args)
        sp1_args.playlist = pl_id
        sp1_response_dict = show_playlist_operation(sp1_args)
        sp1_result_status = get_field_value(sp1_response_dict, Tag.Tag_ResultStatus)
        sp1_result_message = get_field_value(sp1_response_dict, Tag.Tag_ResultMessage)

        assert (sp1_result_status == ResultStatus.ResultStatus_Success.value), "Showing empty playlist did not work: {}".format(sp1_result_message)

        sp1_return_values = get_children_field(sp1_response_dict, Tag.Tag_ReturnValues)
        sp1_playlist_position = get_field_value(sp1_return_values, Tag.Tag_PlaylistPosition)
        sp1_timestamp = get_field_value(sp1_return_values, Tag.Tag_Timestamp)
        sp1_loop_setting = get_field_value(sp1_return_values, Tag.Tag_LoopSetting)
        
        sp1_song_list = get_children_field(sp1_return_values, Tag.Tag_SongList)
        sp1_song_list_size = get_children_field(sp1_song_list, Attribute.Attribute_count)

        assert (sp1_playlist_position == "0"), "The default playlist position should be 0"
        assert (sp1_timestamp == "0"), "The default playlist timestamp should be 0"
        assert (sp1_loop_setting == LoopSetting.LoopSetting_None.value), "The default playlist loop setting should be None"
        assert (sp1_song_list_size == "0"), "The playlist should be empty"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

    # Setup
    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    qs3_args = copy.deepcopy(qs1_args)
    qs3_args.title = "Dragostea Din Tei"
    queue_song_operation(qs3_args)

    try:
        # Case 2: Show playlist with three songs
        sp2_args = copy.deepcopy(args)
        sp2_args.playlist = pl_id
        sp2_response_dict = show_playlist_operation(sp2_args)
        sp2_result_status = get_field_value(sp2_response_dict, Tag.Tag_ResultStatus)
        sp2_result_message = get_field_value(sp2_response_dict, Tag.Tag_ResultMessage)

        assert (sp2_result_status == ResultStatus.ResultStatus_Success.value), "Showing filled playlist did not work: {}".format(sp2_result_message)

        sp2_return_values = get_children_field(sp2_response_dict, Tag.Tag_ReturnValues)
        sp2_playlist_position = get_field_value(sp2_return_values, Tag.Tag_PlaylistPosition)
        sp2_timestamp = get_field_value(sp2_return_values, Tag.Tag_Timestamp)
        sp2_loop_setting = get_field_value(sp2_return_values, Tag.Tag_LoopSetting)
        
        sp2_song_list = get_children_field(sp2_return_values, Tag.Tag_SongList)
        sp2_song_list_size = get_children_field(sp2_song_list, Attribute.Attribute_count)
        sp2_songs = get_children_field(sp2_song_list, Tag.Tag_Song)

        assert (sp2_playlist_position == "1"), "The filled playlist should be playing the first song"
        assert (sp2_timestamp == "0"), "The default playlist timestamp should be 0"
        assert (sp2_loop_setting == LoopSetting.LoopSetting_None.value), "The default playlist loop setting should be None"
        assert (sp2_song_list_size == "3"), "The playlist should have 3 songs"

        sp2_song1_title = get_field_value(sp2_songs[0], Tag.Tag_Title)
        sp2_song1_genre = get_field_value(sp2_songs[0], Tag.Tag_Genre)
        sp2_song1_artist = get_field_value(sp2_songs[0], Tag.Tag_Artist)
        sp2_song1_duration = get_field_value(sp2_songs[0], Tag.Tag_Duration)
        sp2_song1_position = get_field_value(sp2_songs[0], Tag.Tag_Position)
        assert (sp2_song1_title.lower() == "never gonna give you up".lower()), "Song 1 has wrong title"
        assert (sp2_song1_genre.lower() == "pop".lower()), "Song 1 has wrong genre"
        assert (sp2_song1_artist.lower() == "rick ashtley".lower()), "Song 1 has wrong artist"
        assert (sp2_song1_duration == "212827"), "Song 1 has wrong duration"
        assert (sp2_song1_position == "1"), "Song 1 position should be 1"

        sp2_song2_title = get_field_value(sp2_songs[1], Tag.Tag_Title)
        sp2_song2_genre = get_field_value(sp2_songs[1], Tag.Tag_Genre)
        sp2_song2_artist = get_field_value(sp2_songs[1], Tag.Tag_Artist)
        sp2_song2_duration = get_field_value(sp2_songs[1], Tag.Tag_Duration)
        sp2_song2_position = get_field_value(sp2_songs[1], Tag.Tag_Position)
        assert (sp2_song2_title.lower() == "shooting stars".lower()), "Song 2 has wrong title"
        assert (sp2_song2_genre.lower() == "alternative".lower()), "Song 2 has wrong genre"
        assert (sp2_song2_artist.lower() == "bag raiders".lower()), "Song 2 has wrong artist"
        assert (sp2_song2_duration == "235813"), "Song 2 has wrong duration"
        assert (sp2_song2_position == "2"), "Song 2 position should be 2"

        sp2_song3_title = get_field_value(sp2_songs[2], Tag.Tag_Title)
        sp2_song3_genre = get_field_value(sp2_songs[2], Tag.Tag_Genre)
        sp2_song3_artist = get_field_value(sp2_songs[2], Tag.Tag_Artist)
        sp2_song3_duration = get_field_value(sp2_songs[2], Tag.Tag_Duration)
        sp2_song3_position = get_field_value(sp2_songs[2], Tag.Tag_Position)
        assert (sp2_song3_title.lower() == "dragostea din tei".lower()), "Song 3 has wrong title"
        assert (sp2_song3_genre.lower() == "dance".lower()), "Song 3 has wrong genre"
        assert (sp2_song3_artist.lower() == "o-zone".lower()), "Song 3 has wrong artist"
        assert (sp2_song3_duration == "217120"), "Song 3 has wrong duration"
        assert (sp2_song3_position == "3"), "Song 3 position should be 3"

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e))


###############################################################################
#                               Bonus Tests                                   #
###############################################################################
def run_clear_playlist_tests(args):
    print("\nRunning clear playlist tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    qs3_args = copy.deepcopy(qs1_args)
    qs3_args.title = "Dragostea Din Tei"
    queue_song_operation(qs3_args)

    qs4_args = copy.deepcopy(qs1_args)
    qs4_args.title = "Fly me to the Moon"
    queue_song_operation(qs4_args)

    qs5_args = copy.deepcopy(qs1_args)
    qs5_args.title = "Suicide Mission"
    queue_song_operation(qs5_args)

    try:
        # Case 1: Clear playlist with 3 songs
        cp1_args = copy.deepcopy(args)
        cp1_args.playlist = pl_id
        cp1_response_dict = clear_playlist_operation(cp1_args)
        cp1_result_status = get_field_value(cp1_response_dict, Tag.Tag_ResultStatus)
        cp1_result_message = get_field_value(cp1_response_dict, Tag.Tag_ResultMessage)

        assert (cp1_result_status == ResultStatus.ResultStatus_Success.value), "Clearing filled playlist did not work: {}".format(cp1_result_message)

        sp_args = copy.deepcopy(cp1_args)
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_song_list = get_children_field(sp_return_values, Tag.Tag_SongList)

        assert (sp_song_list == None), "Cleared playlist should not return a SongList"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))    

def run_peek_song_tests(args):
    print("\nRunning peek song tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    qs3_args = copy.deepcopy(qs1_args)
    qs3_args.title = "Dragostea Din Tei"
    queue_song_operation(qs3_args)

    qs4_args = copy.deepcopy(qs1_args)
    qs4_args.title = "Fly me to the Moon"
    queue_song_operation(qs4_args)

    qs5_args = copy.deepcopy(qs1_args)
    qs5_args.title = "Suicide Mission"
    queue_song_operation(qs5_args)

    try:
        # Case 1: Peek song that's playing (should be the first one in this case)
        ps1_args = copy.deepcopy(args)
        ps1_args.playlist = pl_id
        ps1_response_dict = peek_song_operation(ps1_args)
        ps1_result_status = get_field_value(ps1_response_dict, Tag.Tag_ResultStatus)
        ps1_result_message = get_field_value(ps1_response_dict, Tag.Tag_ResultMessage)

        assert (ps1_result_status == ResultStatus.ResultStatus_Success.value), "Peeking into a filled playlist did not work: {}".format(ps1_result_message)

        ps1_return_values = get_children_field(ps1_response_dict, Tag.Tag_ReturnValues)
        ps1_song = get_children_field(ps1_return_values, Tag.Tag_Song)

        assert (ps1_song != None), "Peeking into a filled playlist should have returned a Song"

        ps1_song_title = get_field_value(ps1_song, Tag.Tag_Title)
        ps1_song_genre = get_field_value(ps1_song, Tag.Tag_Genre)
        ps1_song_artist = get_field_value(ps1_song, Tag.Tag_Artist)
        ps1_song_duration = get_field_value(ps1_song, Tag.Tag_Duration)
        ps1_song_position = get_field_value(ps1_song, Tag.Tag_Position)
        assert (ps1_song_title.lower() == "never gonna give you up".lower()), "Peeked song has wrong title"
        assert (ps1_song_genre.lower() == "pop".lower()), "Peeked song has wrong genre"
        assert (ps1_song_artist.lower() == "rick ashtley".lower()), "Peeked song has wrong artist"
        assert (ps1_song_duration == "212827"), "Peeked song has wrong duration"
        assert (ps1_song_position == "1"), "Peeked song position should be 1"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e)) 

def run_time_skip_tests(args):
    print("\nRunning time skip tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    try:
        # Case 1: Time skip forwards by 60 seconds
        ts1_args = copy.deepcopy(args)
        ts1_args.playlist = pl_id
        ts1_args.time = 60
        ts1_args.direction = 1
        ts1_response_dict = skip_time_operation(ts1_args)
        ts1_result_status = get_field_value(ts1_response_dict, Tag.Tag_ResultStatus)
        ts1_result_message = get_field_value(ts1_response_dict, Tag.Tag_ResultMessage)

        assert (ts1_result_status == ResultStatus.ResultStatus_Success.value), "Time skipping forwards by 60 seconds did not work: {}".format(ts1_result_message)

        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_timestamp == "60000"), "Timestamp should have advanced by 60000 milliseconds"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e)) 

    try:
        # Case 2: Time skip backwards by 30 seconds
        ts2_args = copy.deepcopy(args)
        ts2_args.playlist = pl_id
        ts2_args.time = 30
        ts2_args.direction = -1
        ts2_response_dict = skip_time_operation(ts2_args)
        ts2_result_status = get_field_value(ts2_response_dict, Tag.Tag_ResultStatus)
        ts2_result_message = get_field_value(ts2_response_dict, Tag.Tag_ResultMessage)

        assert (ts2_result_status == ResultStatus.ResultStatus_Success.value), "Time skipping backwards by 60 seconds did not work: {}".format(ts2_result_message)

        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_timestamp == "30000"), "Timestamp should have rewinded by 30000 milliseconds"

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e)) 

    try:
        # Case 3: Time skip forwards by 300 seconds will end the current song and start the next one from timestamp 0
        ts3_args = copy.deepcopy(args)
        ts3_args.playlist = pl_id
        ts3_args.time = 300
        ts3_args.direction = 1
        ts3_response_dict = skip_time_operation(ts3_args)
        ts3_result_status = get_field_value(ts3_response_dict, Tag.Tag_ResultStatus)
        ts3_result_message = get_field_value(ts3_response_dict, Tag.Tag_ResultMessage)

        assert (ts3_result_status == ResultStatus.ResultStatus_Success.value), "Time skipping forwards by 300 seconds did not work: {}".format(ts3_result_message)

        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_playlist_position = get_field_value(sp_return_values, Tag.Tag_PlaylistPosition)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_playlist_position == "2"), "Playlist position should be at the second song"
        assert (sp_timestamp == "0"), "Timestamp should be 0, the start of the second song"

        print("Case 3: OK")

    except Exception as e:
        raise Exception("Case 3 failed: {}".format(e)) 

    try:
        # Case 4: Time skip backwards by 10 seconds should not modify the timestamp 0, or change the song
        ts4_args = copy.deepcopy(args)
        ts4_args.playlist = pl_id
        ts4_args.time = 10
        ts4_args.direction = -1
        ts4_response_dict = skip_time_operation(ts4_args)
        ts4_result_status = get_field_value(ts4_response_dict, Tag.Tag_ResultStatus)
        ts4_result_message = get_field_value(ts4_response_dict, Tag.Tag_ResultMessage)

        assert (ts4_result_status == ResultStatus.ResultStatus_Success.value), "Time skipping backwards by 10 seconds did not work: {}".format(ts4_result_message)

        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_playlist_position = get_field_value(sp_return_values, Tag.Tag_PlaylistPosition)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_playlist_position == "2"), "Playlist position should still be 2, time skipping backwards doesn't change the song"
        assert (sp_timestamp == "0"), "Timestamp should be unchanged and still 0"

        print("Case 4: OK")

    except Exception as e:
        raise Exception("Case 4 failed: {}".format(e)) 

def run_configure_loop_tests(args):
    print("\nRunning configure loop tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    try:
        # Case 1: Configure loop on the current song, skip through all of it and it should restart
        cl1_args = copy.deepcopy(args)
        cl1_args.playlist = pl_id
        cl1_args.setting = LoopSetting.LoopSetting_Song.value
        cl1_response_dict = config_loop_operation(cl1_args)
        cl1_result_status = get_field_value(cl1_response_dict, Tag.Tag_ResultStatus)
        cl1_result_message = get_field_value(cl1_response_dict, Tag.Tag_ResultMessage)

        assert (cl1_result_status == ResultStatus.ResultStatus_Success.value), "Configure song loop did not work: {}".format(cl1_result_message)

        ts_args = copy.deepcopy(args)
        ts_args.playlist = pl_id
        ts_args.time = 300
        ts_args.direction = 1
        skip_time_operation(ts_args)
        
        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_playlist_position = get_field_value(sp_return_values, Tag.Tag_PlaylistPosition)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_playlist_position == "1"), "Playlist position should still be 1"
        assert (sp_timestamp == "0"), "Timestamp should be 0"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

    try:
        # Case 2: Configure loop on the playlist, skip through both songs until the end.
        cl2_args = copy.deepcopy(args)
        cl2_args.playlist = pl_id
        cl2_args.setting = LoopSetting.LoopSetting_Playlist.value
        cl2_response_dict = config_loop_operation(cl2_args)
        cl2_result_status = get_field_value(cl2_response_dict, Tag.Tag_ResultStatus)
        cl2_result_message = get_field_value(cl2_response_dict, Tag.Tag_ResultMessage)

        assert (cl2_result_status == ResultStatus.ResultStatus_Success.value), "Configure playlist loop did not work: {}".format(cl2_result_message)

        ts_args = copy.deepcopy(args)
        ts_args.playlist = pl_id
        ts_args.time = 300
        ts_args.direction = 1
        skip_time_operation(ts_args)
        
        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_playlist_position = get_field_value(sp_return_values, Tag.Tag_PlaylistPosition)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_playlist_position == "2"), "Playlist position should be 2"
        assert (sp_timestamp == "0"), "Timestamp should be 0"

        skip_time_operation(ts_args)
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        sp_playlist_position = get_field_value(sp_return_values, Tag.Tag_PlaylistPosition)
        sp_timestamp = get_field_value(sp_return_values, Tag.Tag_Timestamp)

        assert (sp_playlist_position == "1"), "Playlist position should be 1"
        assert (sp_timestamp == "0"), "Timestamp should be 0"

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e))

def run_shift_song_tests(args):
    print("\nRunning shift song tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    qs3_args = copy.deepcopy(qs1_args)
    qs3_args.title = "Dragostea Din Tei"
    queue_song_operation(qs3_args)

    qs4_args = copy.deepcopy(qs1_args)
    qs4_args.title = "Fly me to the Moon"
    queue_song_operation(qs4_args)

    qs5_args = copy.deepcopy(qs1_args)
    qs5_args.title = "Suicide Mission"
    queue_song_operation(qs5_args)

    try:
        # Case 1: Shift second song to the fourth position
        ss1_args = copy.deepcopy(args)
        ss1_args.playlist = pl_id
        ss1_args.position = 2
        ss1_args.new_position = 4
        ss1_response_dict = shift_song_operation(ss1_args)
        ss1_result_status = get_field_value(ss1_response_dict, Tag.Tag_ResultStatus)
        ss1_result_message = get_field_value(ss1_response_dict, Tag.Tag_ResultMessage)

        assert (ss1_result_status == ResultStatus.ResultStatus_Success.value), "Shift Song did not work: {}".format(ss1_result_message)
        
        sp_args = copy.deepcopy(args)
        sp_args.playlist = pl_id
        sp_response_dict = show_playlist_operation(sp_args)
        sp_return_values = get_children_field(sp_response_dict, Tag.Tag_ReturnValues)
        
        sp_song_list = get_children_field(sp_return_values, Tag.Tag_SongList)
        sp_songs = get_children_field(sp_song_list, Tag.Tag_Song)

        sp_song1_title = get_field_value(sp_songs[0], Tag.Tag_Title)
        sp_song1_position = get_field_value(sp_songs[0], Tag.Tag_Position)

        sp_song2_title = get_field_value(sp_songs[1], Tag.Tag_Title)
        sp_song2_position = get_field_value(sp_songs[1], Tag.Tag_Position)

        sp_song3_title = get_field_value(sp_songs[2], Tag.Tag_Title)
        sp_song3_position = get_field_value(sp_songs[2], Tag.Tag_Position)

        sp_song4_title = get_field_value(sp_songs[3], Tag.Tag_Title)
        sp_song4_position = get_field_value(sp_songs[3], Tag.Tag_Position)

        sp_song5_title = get_field_value(sp_songs[4], Tag.Tag_Title)
        sp_song5_position = get_field_value(sp_songs[4], Tag.Tag_Position)

        assert (sp_song1_title == "Never Gonna Give You Up".lower()), "First song has wrong title"
        assert (sp_song1_position == "1"), "Song position should be 1"

        assert (sp_song2_title == "Dragostea Din Tei".lower()), "Second song has wrong title"
        assert (sp_song2_position == "2"), "Song position should be 2"

        assert (sp_song3_title == "Fly me to the Moon".lower()), "Third song has wrong title"
        assert (sp_song3_position == "3"), "Song position should be 3"

        assert (sp_song4_title == "Shooting Stars".lower()), "Fourth song has wrong title"
        assert (sp_song4_position == "4"), "Song position should be 4"

        assert (sp_song5_title == "Suicide Mission".lower()), "Fifth song has wrong title"
        assert (sp_song5_position == "5"), "Song position should be 5"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

def run_play_song_tests(args):
    print("\nRunning play song tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    try:
        # Case 1: Play the second song, then peek. The song returned should be the second one that was queued.
        ps1_args = copy.deepcopy(args)
        ps1_args.playlist = pl_id
        ps1_args.position = 2
        ps1_response_dict = play_song_operation(ps1_args)
        ps1_result_status = get_field_value(ps1_response_dict, Tag.Tag_ResultStatus)
        ps1_result_message = get_field_value(ps1_response_dict, Tag.Tag_ResultMessage)

        assert (ps1_result_status == ResultStatus.ResultStatus_Success.value), "Play song did not work: {}".format(ps1_result_message)
        
        p_args = copy.deepcopy(args)
        p_args.playlist = pl_id
        p_response_dict = peek_song_operation(p_args)
        p_return_values = get_children_field(p_response_dict, Tag.Tag_ReturnValues)
        p_song = get_children_field(p_return_values, Tag.Tag_Song)

        p_song_title = get_field_value(p_song, Tag.Tag_Title)
        p_song_genre = get_field_value(p_song, Tag.Tag_Genre)
        p_song_artist = get_field_value(p_song, Tag.Tag_Artist)
        p_song_duration = get_field_value(p_song, Tag.Tag_Duration)
        p_song_position = get_field_value(p_song, Tag.Tag_Position)
        assert (p_song_title.lower() == "Shooting Stars".lower()), "Peeked song has wrong title"
        assert (p_song_genre.lower() == "alternative".lower()), "Peeked song has wrong genre"
        assert (p_song_artist.lower() == "bag raiders".lower()), "Peeked song has wrong artist"
        assert (p_song_duration == "235813"), "Peeked song has wrong duration"
        assert (p_song_position == "2"), "Peeked song position should be 2"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

def run_skip_song_tests(args):
    print("\nRunning skip song tests...")

    # Setup
    pl_response_dict = create_playlist_operation(args)
    pl_return_values = get_children_field(pl_response_dict, Tag.Tag_ReturnValues)
    pl_id = get_field_value(pl_return_values, Tag.Tag_PlaylistID)

    qs1_args = copy.deepcopy(args)
    qs1_args.playlist = pl_id
    qs1_args.title = "Never Gonna Give You Up"
    qs1_args.genre = None
    qs1_args.artist = None
    qs1_args.position = None
    queue_song_operation(qs1_args)

    qs2_args = copy.deepcopy(qs1_args)
    qs2_args.title = "Shooting Stars"
    queue_song_operation(qs2_args)

    try:
        # Case 1: Skip the first song, then peek song should return the second song
        ss1_args = copy.deepcopy(args)
        ss1_args.playlist = pl_id
        ss1_response_dict = skip_song_operation(ss1_args)
        ss1_result_status = get_field_value(ss1_response_dict, Tag.Tag_ResultStatus)
        ss1_result_message = get_field_value(ss1_response_dict, Tag.Tag_ResultMessage)

        assert (ss1_result_status == ResultStatus.ResultStatus_Success.value), "Skip song did not work: {}".format(ss1_result_message)
        
        p_args = copy.deepcopy(args)
        p_args.playlist = pl_id
        p_response_dict = peek_song_operation(p_args)
        p_return_values = get_children_field(p_response_dict, Tag.Tag_ReturnValues)
        p_song = get_children_field(p_return_values, Tag.Tag_Song)

        p_song_title = get_field_value(p_song, Tag.Tag_Title)
        p_song_genre = get_field_value(p_song, Tag.Tag_Genre)
        p_song_artist = get_field_value(p_song, Tag.Tag_Artist)
        p_song_duration = get_field_value(p_song, Tag.Tag_Duration)
        p_song_position = get_field_value(p_song, Tag.Tag_Position)
        assert (p_song_title.lower() == "Shooting Stars".lower()), "Peeked song has wrong title"
        assert (p_song_genre.lower() == "alternative".lower()), "Peeked song has wrong genre"
        assert (p_song_artist.lower() == "bag raiders".lower()), "Peeked song has wrong artist"
        assert (p_song_duration == "235813"), "Peeked song has wrong duration"
        assert (p_song_position == "2"), "Peeked song position should be 2"

        print("Case 1: OK")

    except Exception as e:
        raise Exception("Case 1 failed: {}".format(e))

    try:
        # Case 2: Try to skip the second song, but since it's the last one the peeked song should not change
        ss2_args = copy.deepcopy(args)
        ss2_args.playlist = pl_id
        ss2_response_dict = skip_song_operation(ss2_args)
        ss2_result_status = get_field_value(ss2_response_dict, Tag.Tag_ResultStatus)
        ss2_result_message = get_field_value(ss2_response_dict, Tag.Tag_ResultMessage)

        assert (ss2_result_status == ResultStatus.ResultStatus_Success.value), "Skip song did not work: {}".format(ss2_result_message)
        
        p_args = copy.deepcopy(args)
        p_args.playlist = pl_id
        p_response_dict = peek_song_operation(p_args)
        p_return_values = get_children_field(p_response_dict, Tag.Tag_ReturnValues)
        p_song = get_children_field(p_return_values, Tag.Tag_Song)

        p_song_title = get_field_value(p_song, Tag.Tag_Title)
        p_song_genre = get_field_value(p_song, Tag.Tag_Genre)
        p_song_artist = get_field_value(p_song, Tag.Tag_Artist)
        p_song_duration = get_field_value(p_song, Tag.Tag_Duration)
        p_song_position = get_field_value(p_song, Tag.Tag_Position)
        assert (p_song_title.lower() == "Shooting Stars".lower()), "Peeked song has wrong title"
        assert (p_song_genre.lower() == "alternative".lower()), "Peeked song has wrong genre"
        assert (p_song_artist.lower() == "bag raiders".lower()), "Peeked song has wrong artist"
        assert (p_song_duration == "235813"), "Peeked song has wrong duration"
        assert (p_song_position == "2"), "Peeked song position should still be 2"

        print("Case 2: OK")

    except Exception as e:
        raise Exception("Case 2 failed: {}".format(e))