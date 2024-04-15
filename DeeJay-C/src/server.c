#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <microhttpd.h>


#include "playlist_operations.h"
#include "types.h" 
#include "deejay.h"

#define PORT 8888
#define POST_BUFFER_SIZE 1024 * 1024 /* 1 Mb */


/**
 * send_response builds a response from the provided message and status code, then sends it back
 * through the connection
 */
int send_response(struct MHD_Connection *connection, const char *message, int status_code)
{
	int ret;
	struct MHD_Response *response;

	response = MHD_create_response_from_buffer(strlen(message),
											   (void *)message,
											   MHD_RESPMEM_MUST_COPY);
	if (response == NULL)
	{
		return MHD_NO;
	}

	MHD_add_response_header(response, MHD_HTTP_HEADER_CONTENT_TYPE, "application/xml");
	ret = MHD_queue_response(connection, status_code, response);
	MHD_destroy_response(response);

	return ret;
}


/**
 * request_completed will be called at the end, just before closing the connection. We use it to
 * free our resources.
 */
void request_completed(void *cls,
					   struct MHD_Connection *connection,
					   void **con_cls,
					   enum MHD_RequestTerminationCode toe)
{

	OperationRequest *op_req = (OperationRequest *)*con_cls;

	if (op_req == NULL)
	{
		return;
	}

	if (op_req->request_message != NULL)
	{
		free(op_req->request_message);
	}

	if (op_req->response_message != NULL)
	{
		free(op_req->response_message);
	}

	free(op_req);
	*con_cls = NULL;
}


/**
 * handle_connection will handle new connections to the server. The library will call this 3 times,
 * one time with only the headers, a second time with upload_data, and a third final time to queue
 * the response
 */
int handle_connection(void *cls,
                                   struct MHD_Connection *connection,
                                   const char *url,
                                   const char *method,
                                   const char *version,
                                   const char *upload_data,
                                   size_t *upload_data_size,
                                   void **con_cls)
{

	DJ_Deejay *deejay_instance = NULL;
	OperationRequest *op_req = NULL;

	char *http_error_str = NULL;
	char *internal_server_error_str = NULL;

	// Only accept the POST method
	if (strcmp(method, MHD_HTTP_METHOD_POST) != 0)
	{
		http_error_str = encode_response_message(ResultStatus_HTTPError,
												 "HTTP Error: Only the POST method is supported",
												 DJ_Operation_ShowCurrentSong, // Escolha uma operação apropriada
												 NULL);

		return send_response(connection, http_error_str, MHD_HTTP_BAD_REQUEST);
	}

	if (*con_cls == NULL)
	{
		// First iteration, set everything up

		// Initialize Connection Info
		op_req = (OperationRequest *)malloc(sizeof(OperationRequest));
		op_req->request_message = NULL;
		op_req->response_message = NULL;

		*con_cls = (void *)op_req;
		return MHD_YES;
	}

	op_req = (OperationRequest *)*con_cls;

	if (*upload_data_size != 0)
	{
		// Second iteration, process upload data

		// Copy the request to the connection info
		op_req->request_message = (char *)malloc(*upload_data_size + 1);
		op_req->request_message[0] = '\0';
		strcpy(op_req->request_message, upload_data);

		deejay_instance = DJ_get_deejay();


		op_req->response_message = DJ_process_request(deejay_instance, op_req->request_message); // Corrigido para DJ_process_request
		if (op_req->response_message == NULL)
		{
			internal_server_error_str = encode_response_message(ResultStatus_InternalServerError,
																"An internal server error ocurred",
																DJ_Operation_ShowCurrentSong, // Escolha uma operação apropriada
																NULL);
			return send_response(connection,
								 internal_server_error_str,
								 MHD_HTTP_INTERNAL_SERVER_ERROR);
		}

		// Finished processing data
		*upload_data_size = 0;

		return MHD_YES;
	}

	// Third and final iteration, queue a response for the user
	return send_response(connection, op_req->response_message, MHD_HTTP_OK);
}

int main(int argc, char *argv[])
{
	struct MHD_Daemon *daemon;

	daemon = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION, PORT, NULL, NULL, (MHD_AccessHandlerCallback) &handle_connection, NULL, MHD_OPTION_END);

	if (daemon == NULL)
	{
		fprintf(stderr, "Failed to start daemon.\n");
		return 1;
	};

	getchar();
	MHD_stop_daemon(daemon);

	DJ_free_deejay(DJ_get_deejay());
	return 0;
}
