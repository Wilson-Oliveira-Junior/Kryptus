#!/usr/bin/env python3

import argparse
from operations import *
from test_suite import *

def create_parser():
    tune_booker_parser = argparse.ArgumentParser(description="Your favorite CLI to your personal DeeJay!",
                                                 add_help=True)
    subparsers = tune_booker_parser.add_subparsers()

    # Common parser to make the connection
    connection_parser = argparse.ArgumentParser(add_help=False)
    connection_parser.add_argument("--host", help="Hostname or IP of the DeeJay server", type=str, required=True)
    connection_parser.add_argument("--port", help="Port of the DeeJay server", type=int, required=True)

    # Common parser for all the operations that need a playlist argument
    playlist_operations_parser = argparse.ArgumentParser(add_help=False)
    playlist_operations_parser.add_argument("--playlist", help="The ID of the playlist.", type=int, required=True)

    # Create playlist
    create_playlist_parser = subparsers.add_parser("create", parents=[connection_parser],
                                                   help="Creates a new playlist.",
                                                   description="Creates a new playlist and displays its returned ID.")
    create_playlist_parser.set_defaults(func=create_playlist_operation, test=False)

    # Delete playlist
    delete_playlist_parser = subparsers.add_parser("delete", parents=[connection_parser, playlist_operations_parser],
                                                   help="Deletes a playlist.",
                                                   description="Deletes a playlist with a given ID.")
    delete_playlist_parser.set_defaults(func=delete_playlist_operation, test=False)

    # Clear playlist
    clear_playlist_parser = subparsers.add_parser("clear", parents=[connection_parser, playlist_operations_parser],
                                                  help="Clears all songs from a playlist.",
                                                  description="Clears all songs from a playlist with a given ID.")
    clear_playlist_parser.set_defaults(func=clear_playlist_operation, test=False)

    # Show playlist
    show_playlist_parser = subparsers.add_parser("show", parents=[connection_parser, playlist_operations_parser],
                                                 help="Displays the full song list.",
                                                 description="Displays the full song list of a playlist with a given ID.")
    show_playlist_parser.set_defaults(func=show_playlist_operation, test=False)

    # Configure Loop
    configLoop_parser = subparsers.add_parser("configLoop", parents=[connection_parser, playlist_operations_parser],
                                              help="Loops a playlist, a song or disable it.",
                                              description="Configures either a playlist, a song or none of them to loop.")
    configLoop_parser.add_argument("--setting", help="The loop setting to be applied.", choices=["playlist", "song", "none"], type=str, required=True)
    configLoop_parser.set_defaults(func=config_loop_operation, test=False)

    # Queue song
    queue_song_parser = subparsers.add_parser("queue", parents=[connection_parser, playlist_operations_parser],
                                              help="Queues a new song on a playlist.",
                                              description="Queues a new song on a playlist. " +
                                              "It’s placed at the end by default, but this " +
                                              "behavior can be overridden by the parameters.")
    queue_song_parser.add_argument("--title", help="The title of the new song to be queued.", type=str, required=True)
    queue_song_parser.add_argument("--genre", help="Optional. The genre of the new song to be queued.", type=str, required=False)
    queue_song_parser.add_argument("--artist", help="Optional. The artist of the new song to be queued.", type=str, required=False)
    queue_song_parser.add_argument("--position", help="Optional. The position in the playlist to place the new song.", type=int, required=False)
    queue_song_parser.set_defaults(func=queue_song_operation, test=False)

    # Dequeue song
    dequeue_song_parser = subparsers.add_parser("dequeue", parents=[connection_parser, playlist_operations_parser],
                                                help="Dequeues a song from a playlist.",
                                                description="Dequeues a song from a playlist with a given ID and position.")
    dequeue_song_parser.add_argument("--position", help="The position of the song in the playlist to be dequeued.", type=int, required=True)
    dequeue_song_parser.set_defaults(func=dequeue_song_operation, test=False)

    # Shift song
    shift_song_parser = subparsers.add_parser("shift", parents=[connection_parser, playlist_operations_parser],
                                              help="Moves the position of a song in the playlist.",
                                              description="Moves a song in a playlist to a new position, " +
                                              "shifting down other songs below it.")
    shift_song_parser.add_argument("--position", help="The initial position of the song to be shifted.", type=int, required=True)
    shift_song_parser.add_argument("--new-position", help="The new position of the song after it’s shifted.", type=int, required=True)
    shift_song_parser.set_defaults(func=shift_song_operation, test=False)

    # Peek song
    peek_song_parser = subparsers.add_parser("peek", parents=[connection_parser, playlist_operations_parser],
                                             help="Show current song details.",
                                             description="Retrieves and displays details about the song " +
                                             "that’s currently set to play in a playlist.")
    peek_song_parser.set_defaults(func=peek_song_operation, test=False)

    # Play song
    play_song_parser = subparsers.add_parser("play", parents=[connection_parser, playlist_operations_parser],
                                             help="Change current song.",
                                             description="Stops playing the current song and sets " +
                                             "another song to play within a playlist.")
    play_song_parser.add_argument("--position", help="The position of the other song to be played.", type=int, required=True)
    play_song_parser.set_defaults(func=play_song_operation, test=False)

    # Skip song
    skip_song_parser = subparsers.add_parser("skip", parents=[connection_parser, playlist_operations_parser],
                                             help="Skip current song.",
                                             description="Stops playing the current song and sets the one " +
                                             "in the next position to play within a playlist.")
    skip_song_parser.set_defaults(func=skip_song_operation, test=False)

    # Advance timehelp
    advance_time_parser = subparsers.add_parser("advance", parents=[connection_parser, playlist_operations_parser],
                                                help="Skip some seconds on the current song.",
                                                description="Does a forward time skip on the song being " +
                                                "played within a playlist by the provided amount of time in seconds.")
    advance_time_parser.add_argument("--time", help="The amount of time to advance in seconds.", type=int, required=True)
    advance_time_parser.set_defaults(func=skip_time_operation, direction=1, test=False)

    # Rewind time
    rewind_time_parser = subparsers.add_parser("rewind", parents=[connection_parser, playlist_operations_parser],
                                               help="Rewind some seconds on the current song.",
                                               description="Does a backward time skip on the song being " +
                                               "played within a playlist by the provided amount of time in seconds.")
    rewind_time_parser.add_argument("--time", help="The amount of time to rewind in seconds.", type=int, required=True)
    rewind_time_parser.set_defaults(func=skip_time_operation, direction=-1, test=False)

    # Test suite
    test_suite_parser = subparsers.add_parser("test", parents=[connection_parser],
                                             help="Run a test suite.",
                                             description="Runs the specified test suite and shows the " + 
                                             "results.")
    test_suite_parser.add_argument("--suite", help="The test suite to run.", choices=["basic", "full"], type=str, required=True)
    test_suite_parser.set_defaults(func=run_test_suite, test=True)


    return tune_booker_parser
