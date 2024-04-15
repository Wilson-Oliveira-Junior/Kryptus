#ifndef __TYPES_H__
#define __TYPES_H__
#include "playlist_operations.h"
#include <libxml/parser.h>
#include <libxml/xmlwriter.h>

typedef enum {
    Operation_CreatePlaylist,
    Operation_DeletePlaylist,
    Operation_ClearPlaylist,
    Operation_ShowPlaylist,
    Operation_ConfigureLoop,
    Operation_QueueSong,
    Operation_DequeueSong,
    Operation_ShiftSongPosition,
    Operation_ShowCurrentSong,
    Operation_SetSong,
    Operation_SkipSong,
    Operation_TimeSkip
} Operation;

typedef enum {
    ResultStatus_Success,
    ResultStatus_InternalServerError,
    ResultStatus_HTTPError,
    ResultStatus_InvalidMessage,
    ResultStatus_NotImplemented,
    ResultStatus_LogicalError
} ResultStatus;

typedef enum {
    LoopSetting_None,
    LoopSetting_Playlist,
    LoopSetting_Song
} LoopSetting;

typedef struct RequestMessage {
    Operation operation;
    void *parameters;
} RequestMessage;

typedef struct PlaylistParameters {
    char name[50];
    int playlist_id;
    int num_songs;
} PlaylistParameters;

typedef struct OperationRequest {
    char *request_message;
    char *response_message;
} OperationRequest;

typedef struct ResponseMessage {
    ResultStatus result_status;
    char *result_message;
    Operation operation;
    void *return_values;
} ResponseMessage;

typedef struct Error {
    ResultStatus result_status;
    char *message;
} Error;

typedef struct CreatePlaylistParameters {
    // Define os parâmetros da criação da lista de reprodução
} CreatePlaylistParameters;

typedef struct DeletePlaylistParameters {
    int playlist_id;
} DeletePlaylistParameters;

typedef struct ShowPlaylistParameters {
    char *playlist_name_or_id;
} ShowPlaylistParameters;

typedef struct QueueSongParameters {
    char *playlist_name_or_id;
    char *song_artist;
    char *song_title;
    int song_duration_seconds;
} QueueSongParameters;

typedef struct DequeueSongParameters {
    char *playlist_name_or_id;
    int song_position;
} DequeueSongParameters;

const char *result_status_to_str(ResultStatus result_status);
ResultStatus str_to_result_status(const char *result_status_str);

const char *operation_to_str(Operation operation);
const char *loop_setting_to_str(LoopSetting loop_setting);
LoopSetting str_to_loop_setting(const char *loop_setting_str);
Operation str_to_operation(const char *operation_str);

Error *new_error(ResultStatus result_status, const char *message);
Error *wrap_error(Error *wrapped_error, const char *message);

Error *decode_request_message(const char *request_xml, RequestMessage **request_message);
char *encode_response_message_simple(ResponseMessage *response_message);
char *encode_response_message(ResultStatus result_status, char *result_message, Operation operation, void *return_values);

int encode_create_playlist_return_values(xmlTextWriterPtr writer, void *return_values);
int encode_delete_playlist_return_values(xmlTextWriterPtr writer, void *return_values);
int encode_show_playlist_return_values(xmlTextWriterPtr writer, void *return_values);
int encode_queue_song_return_values(xmlTextWriterPtr writer, void *return_values);
int encode_dequeue_song_return_values(xmlTextWriterPtr writer, void *return_values);

#endif /* __TYPES_H__ */
