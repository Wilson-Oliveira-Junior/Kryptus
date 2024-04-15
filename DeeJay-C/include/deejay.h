#ifndef __DEEJAY_H__
#define __DEEJAY_H__

#include <glib.h>

typedef enum {
    DJ_ResultStatus_Success,
    DJ_ResultStatus_NotImplemented,
    DJ_ResultStatus_InternalServerError,
    DJ_ResultStatus_LogicalError
} DJ_ResultStatus;

typedef struct DJ_Error {
    DJ_ResultStatus result_status;
    char *message;
} DJ_Error;

typedef enum {
    DJ_Operation_CreatePlaylist,
    DJ_Operation_DeletePlaylist,
    DJ_Operation_ClearPlaylist,
    DJ_Operation_ShowPlaylist,
    DJ_Operation_ConfigureLoop,
    DJ_Operation_QueueSong,
    DJ_Operation_DequeueSong,
    DJ_Operation_ShiftSongPosition,
    DJ_Operation_ShowCurrentSong,
    DJ_Operation_SetSong,
    DJ_Operation_SkipSong,
    DJ_Operation_TimeSkip
} DJ_Operation;

typedef enum {
    DJ_LoopSetting_All,
    DJ_LoopSetting_Single,
    DJ_LoopSetting_None
} DJ_LoopSetting;

typedef struct DJ_RequestMessage {
    DJ_Operation operation;
    void *parameters;
} DJ_RequestMessage;

typedef struct DJ_ResponseMessage {
    DJ_ResultStatus result_status;
    char *result_message;
    DJ_Operation operation;
    void *return_values;
} DJ_ResponseMessage;

typedef struct DJ_DeletePlaylistParameters {
    int playlist_id;
} DJ_DeletePlaylistParameters;

typedef struct DJ_ShowPlaylistParameters {
    int playlist_id;
} DJ_ShowPlaylistParameters;

typedef struct DJ_QueueSongParameters {
    int playlist_id;
    char *artist;
    char *title;
} DJ_QueueSongParameters;

typedef struct DJ_DequeueSongParameters {
    int playlist_id;
    int song_position;
} DJ_DequeueSongParameters;

typedef struct DJ_Playlist {
    GList *song_list;
    int position;
    int timestamp;
    DJ_LoopSetting loop_setting;
} DJ_Playlist;

typedef struct DJ_Deejay {
    GHashTable *playlists;
} DJ_Deejay;

DJ_Deejay *DJ_get_deejay();
void DJ_free_deejay(DJ_Deejay *deejay_instance);
char *DJ_process_request(DJ_Deejay *deejay_instance, char *request);
DJ_Error *DJ_execute_create_playlist(DJ_Deejay *deejay_instance, void *params, void **return_values);
DJ_Error *DJ_execute_delete_playlist(DJ_Deejay *deejay_instance, void *params, void **return_values);
DJ_Error *DJ_execute_show_playlist(DJ_Deejay *deejay_instance, void *params, void **return_values);
DJ_Error *DJ_execute_queue_song(DJ_Deejay *deejay_instance, void *params, void **return_values);
DJ_Error *DJ_execute_dequeue_song(DJ_Deejay *deejay_instance, void *params, void **return_values);

#endif /* __DEEJAY_H__ */
