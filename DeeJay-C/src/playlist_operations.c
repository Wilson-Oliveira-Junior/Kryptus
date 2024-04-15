// playlist_operations.c

#include "playlist_operations.h"

PlaylistParameters *decode_create_playlist_parameters(xmlNodePtr node) {
    PlaylistParameters *parameters = (PlaylistParameters *)malloc(sizeof(PlaylistParameters));
    if (parameters == NULL) {
        return NULL;
    }

    // Implement the logic to decode parameters from the XML node

    return parameters;
}

PlaylistParameters *decode_delete_playlist_parameters(xmlNodePtr node) {
    PlaylistParameters *parameters = (PlaylistParameters *)malloc(sizeof(PlaylistParameters));
    if (parameters == NULL) {
        return NULL;
    }

    // Implement the logic to decode parameters from the XML node

    return parameters;
}

PlaylistParameters *decode_show_playlist_parameters(xmlNodePtr node) {
    PlaylistParameters *parameters = (PlaylistParameters *)malloc(sizeof(PlaylistParameters));
    if (parameters == NULL) {
        return NULL;
    }

    // Implement the logic to decode parameters from the XML node

    return parameters;
}

PlaylistParameters *decode_configure_loop_parameters(xmlNodePtr node) {
    PlaylistParameters *parameters = (PlaylistParameters *)malloc(sizeof(PlaylistParameters));
    if (parameters == NULL) {
        return NULL;
    }

    // Implement the logic to decode parameters from the XML node

    return parameters;
}

PlaylistParameters *decode_queue_song_parameters(xmlNodePtr node) {
    PlaylistParameters *parameters = (PlaylistParameters *)malloc(sizeof(PlaylistParameters));
    if (parameters == NULL) {
        return NULL;
    }

    // Implement the logic to decode parameters from the XML node

    return parameters;
}

PlaylistParameters *decode_dequeue_song_parameters(xmlNodePtr node) {
    PlaylistParameters *parameters = (PlaylistParameters *)malloc(sizeof(PlaylistParameters));
    if (parameters == NULL) {
        return NULL;
    }

    // Implement the logic to decode parameters from the XML node

    return parameters;
}
