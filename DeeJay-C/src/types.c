#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libxml/xmlwriter.h>
#include <libxml/parser.h>
#include <libxml/tree.h>

typedef enum {
    ResultStatus_Success,
    ResultStatus_InternalServerError,
    ResultStatus_HTTPError,
    ResultStatus_InvalidMessage,
    ResultStatus_NotImplemented,
    ResultStatus_LogicalError,
    ResultStatus_Unknown
} ResultStatus;

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
    Operation_TimeSkip,
    Operation_Unknown
} Operation;

typedef enum {
    LoopSetting_None,
    LoopSetting_Playlist,
    LoopSetting_Song,
    LoopSetting_Unknown
} LoopSetting;

typedef struct {
    ResultStatus result_status;
    char *message;
} Error;

typedef struct {
    Operation operation;
    void *parameters;
} RequestMessage;

typedef struct {
    ResultStatus result_status;
    char *message;
    void *return_values;
} ResponseMessage;

typedef struct {
    int playlist_id;
} CreatePlaylistReturnValues;

typedef struct {
    int playlist_id;
} DeletePlaylistReturnValues;

typedef struct {
    char *song_id_str;
    char *song_name;
} QueueSongReturnValues;

typedef struct {
    char *song_id_str;
    char *song_name;
} DequeueSongReturnValues;

RequestMessage *decode_request_message(const char *request_xml) {
    xmlDocPtr doc = xmlParseMemory(request_xml, strlen(request_xml));
    if (doc == NULL) {
        return NULL;
    }

    xmlNodePtr root = xmlDocGetRootElement(doc);
    if (root == NULL) {
        xmlFreeDoc(doc);
        return NULL;
    }

    RequestMessage *request_message = (RequestMessage *)malloc(sizeof(RequestMessage));
    if (request_message == NULL) {
        xmlFreeDoc(doc);
        return NULL;
    }

    xmlFreeDoc(doc);
    return request_message;
}

void free_request_message(RequestMessage *request_message) {
    if (request_message == NULL) {
        return;
    }

    free(request_message);
}

ResponseMessage *encode_response_message(ResultStatus result_status, const char *message, void *return_values) {
    ResponseMessage *response_message = (ResponseMessage *)malloc(sizeof(ResponseMessage));
    if (response_message == NULL) {
        return NULL;
    }

    response_message->result_status = result_status;
    response_message->message = strdup(message);
    response_message->return_values = return_values;

    return response_message;
}

void free_response_message(ResponseMessage *response_message) {
    if (response_message == NULL) {
        return;
    }

    if (response_message->message != NULL) {
        free(response_message->message);
    }

    free(response_message);
}

int encode_create_playlist_return_values(xmlTextWriterPtr writer, void *return_values) {
    if (writer == NULL || return_values == NULL) {
        return -1;
    }

    CreatePlaylistReturnValues *ret_values = (CreatePlaylistReturnValues *)return_values;

    if (xmlTextWriterStartElement(writer, BAD_CAST "ReturnValues") < 0) {
        return -1;
    }

    if (xmlTextWriterStartElement(writer, BAD_CAST "PlaylistID") < 0) {
        return -1;
    }

    if (xmlTextWriterWriteAttribute(writer, BAD_CAST "type", BAD_CAST "Integer") < 0) {
        return -1;
    }

    char playlist_id_str[20];
    snprintf(playlist_id_str, sizeof(playlist_id_str), "%d", ret_values->playlist_id);

    if (xmlTextWriterWriteAttribute(writer, BAD_CAST "value", BAD_CAST playlist_id_str) < 0) {
        return -1;
    }

    if (xmlTextWriterEndElement(writer) < 0) {
        return -1;
    }

    if (xmlTextWriterEndElement(writer) < 0) {
        return -1;
    }

    return 0;
}

int encode_delete_playlist_return_values(xmlTextWriterPtr writer, void *return_values)
{
    int rc = -1;
    DeletePlaylistReturnValues *ret_values = (DeletePlaylistReturnValues *)return_values;

    if (ret_values == NULL)
    {
        fprintf(stderr, "Expected return values but got none\n");
        return -1;
    }

    // Start ReturnValues element
    rc = xmlTextWriterStartElement(writer, (xmlChar *)"ReturnValues");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to start XML element\n");
        return rc;
    }

    // Start PlaylistID element
    rc = xmlTextWriterStartElement(writer, (xmlChar *)"PlaylistID");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to start XML element\n");
        return rc;
    }

    // Add attribute type
    rc = xmlTextWriterWriteAttribute(writer, (xmlChar *)"type", (xmlChar *)"Integer");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to write type attribute\n");
        return rc;
    }

    // Add attribute value (assuming PlaylistID is an integer)
    char playlist_id_str[20]; // Assuming a reasonable length for the string representation of the integer
    snprintf(playlist_id_str, sizeof(playlist_id_str), "%d", ret_values->playlist_id);
    rc = xmlTextWriterWriteAttribute(writer, (xmlChar *)"value", (xmlChar *)playlist_id_str);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to write value attribute\n");
        return rc;
    }

    // End PlaylistID element
    rc = xmlTextWriterEndElement(writer);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to end XML element\n");
        return rc;
    }

    // End ReturnValues element
    rc = xmlTextWriterEndElement(writer);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to end XML element\n");
        return rc;
    }

    return rc;
}

int encode_queue_song_return_values(xmlTextWriterPtr writer, void *return_values)
{
    int rc = -1;
    QueueSongReturnValues *ret_values = (QueueSongReturnValues *)return_values;

    // Start ReturnValues element
    rc = xmlTextWriterStartElement(writer, (xmlChar *)"ReturnValues");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to start XML element\n");
        return rc;
    }

    // Start Song element
    rc = xmlTextWriterStartElement(writer, (xmlChar *)"Song");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to start XML element\n");
        return rc;
    }

    // Add SongID attribute
    rc = xmlTextWriterWriteAttribute(writer, (xmlChar *)"SongID", (xmlChar *)ret_values->song_id_str);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to write attribute\n");
        return rc;
    }

    // Add SongName attribute
    rc = xmlTextWriterWriteAttribute(writer, (xmlChar *)"SongName", (xmlChar *)ret_values->song_name);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to write attribute\n");
        return rc;
    }

    // End Song element
    rc = xmlTextWriterEndElement(writer);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to end XML element\n");
        return rc;
    }

    // End ReturnValues element
    rc = xmlTextWriterEndElement(writer);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to end XML element\n");
        return rc;
    }

    return rc;
}

int encode_dequeue_song_return_values(xmlTextWriterPtr writer, void *return_values)
{
    int rc = -1;
    DequeueSongReturnValues *ret_values = (DequeueSongReturnValues *)return_values;

    // Start ReturnValues element
    rc = xmlTextWriterStartElement(writer, (xmlChar *)"ReturnValues");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to start XML element\n");
        return rc;
    }

    // Start Song element
    rc = xmlTextWriterStartElement(writer, (xmlChar *)"Song");
    if (rc < 0)
    {
        fprintf(stderr, "Failed to start XML element\n");
        return rc;
    }

    // Add SongID attribute
    rc = xmlTextWriterWriteAttribute(writer, (xmlChar *)"SongID", (xmlChar *)ret_values->song_id_str);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to write attribute\n");
        return rc;
    }

    // Add SongName attribute
    rc = xmlTextWriterWriteAttribute(writer, (xmlChar *)"SongName", (xmlChar *)ret_values->song_name);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to write attribute\n");
        return rc;
    }

    // End Song element
    rc = xmlTextWriterEndElement(writer);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to end XML element\n");
        return rc;
    }

    // End ReturnValues element
    rc = xmlTextWriterEndElement(writer);
    if (rc < 0)
    {
        fprintf(stderr, "Failed to end XML element\n");
        return rc;
    }

    return rc;
}
