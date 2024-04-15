#!/usr/bin/env python3

from enum import Enum

class Operation(Enum):
    Operation_ClearPlaylist = "ClearPlaylist"
    Operation_ConfigureLoop = "ConfigureLoop"
    Operation_CreatePlaylist = "CreatePlaylist"
    Operation_DeletePlaylist = "DeletePlaylist"
    Operation_DequeueSong = "DequeueSong"
    Operation_QueueSong = "QueueSong"
    Operation_SetSong = "SetSong"
    Operation_ShiftSongPosition = "ShiftSongPosition"
    Operation_ShowCurrentSong = "ShowCurrentSong"
    Operation_ShowPlaylist = "ShowPlaylist"
    Operation_SkipSong = "SkipSong"
    Operation_TimeSkip = "TimeSkip"

class ResultStatus(Enum):
    ResultStatus_HTTPError = "HTTPError"
    ResultStatus_InternalServerError = "InternalServerError"
    ResultStatus_InvalidMessage = "InvalidMessage"
    ResultStatus_LogicalError = "LogicalError"
    ResultStatus_NotImplemented = "NotImplemented"
    ResultStatus_Success = "Success"

class LoopSetting(Enum):
    LoopSetting_None = "None"
    LoopSetting_Playlist = "Playlist"
    LoopSetting_Song = "Song"

class Tag(Enum):
    Tag_Artist = "Artist"
    Tag_Duration = "Duration"
    Tag_Genre = "Genre"
    Tag_LoopSetting = "LoopSetting"
    Tag_NewPosition = "NewPosition"
    Tag_Operation = "Operation"
    Tag_Parameters = "Parameters"
    Tag_PlaylistID = "PlaylistID"
    Tag_PlaylistPosition = "PlaylistPosition"
    Tag_Position = "Position"
    Tag_RequestMessage = "RequestMessage"
    Tag_ResponseMessage = "ResponseMessage"
    Tag_ResultMessage = "ResultMessage"
    Tag_ResultStatus = "ResultStatus"
    Tag_ReturnValues = "ReturnValues"
    Tag_Song = "Song"
    Tag_SongList = "SongList"
    Tag_SongQuery = "SongQuery"
    Tag_TimeInterval = "TimeInterval"
    Tag_Timestamp = "Timestamp"
    Tag_Title = "Title"

class Type(Enum):
    Type_Enumeration = "Enumeration"
    Type_Integer = "Integer"
    Type_Object = "Object"
    Type_String = "String"

class Attribute(Enum):
    Attribute_elem = "elem"
    Attribute_count = "count"
    Attribute_type = "type"
    Attribute_value = "value"
