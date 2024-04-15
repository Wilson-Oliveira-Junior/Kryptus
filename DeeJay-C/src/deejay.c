#include "deejay.h"
#include <glib.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

DJ_ResponseMessage *DJ_create_response_message(DJ_ResultStatus status, const char *message, DJ_Operation operation, void *return_values)
{
    DJ_ResponseMessage *response = malloc(sizeof(DJ_ResponseMessage));
    if (response == NULL)
    {
        return NULL;
    }
    response->result_status = status;
    response->result_message = strdup(message);
    response->operation = operation;
    response->return_values = return_values;
    return response;
}

DJ_Error *DJ_decode_request_message(const char *request, DJ_RequestMessage **request_message)
{
    return NULL;
}

void DJ_free_request_message(DJ_RequestMessage *request_message)
{
}

void DJ_free_error(DJ_Error *err)
{
}

char *DJ_encode_response_message(DJ_ResultStatus result_status, char *result_message, void *return_values)
{
   
    char *encoded_message = malloc(strlen(result_message) + 1); 
    if (encoded_message == NULL)
    {
        return NULL;
    }
    strcpy(encoded_message, result_message);
    return encoded_message;
}

DJ_Error *DJ_execute_create_playlist(DJ_Deejay *deejay_instance, void *params, void **return_values)
{
    return NULL;
}

DJ_Error *DJ_execute_delete_playlist(DJ_Deejay *deejay_instance, void *params, void **return_values)
{
    return NULL;
}

DJ_Error *DJ_execute_show_playlist(DJ_Deejay *deejay_instance, void *params, void **return_values)
{
    return NULL;
}

DJ_Error *DJ_execute_queue_song(DJ_Deejay *deejay_instance, void *params, void **return_values)
{
    return NULL;
}

DJ_Error *DJ_execute_dequeue_song(DJ_Deejay *deejay_instance, void *params, void **return_values)
{
    return NULL;
}

DJ_Deejay *DJ_get_deejay()
{
    return NULL;
}

void DJ_free_deejay(DJ_Deejay *deejay_instance)
{
}

char *DJ_process_request(DJ_Deejay *deejay_instance, char *request_message)
{
    if (strcmp(request_message, "CreatePlaylist") == 0)
    {
        return "Playlist criada com sucesso!";
    }
    else if (strcmp(request_message, "DeletePlaylist") == 0)
    {
        return "Playlist excluída com sucesso!";
    }
    else if (strcmp(request_message, "ShowPlaylist") == 0)
    {
        return "Exibindo playlist...";
    }
    else
    {
        return "Operação não reconhecida.";
    }
}

void DJ_free_response_message(DJ_ResponseMessage *response_message)
{
 
    free(response_message->result_message);
    free(response_message);
}
