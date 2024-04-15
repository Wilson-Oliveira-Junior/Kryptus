#ifndef PLAYLIST_OPERATIONS_H
#define PLAYLIST_OPERATIONS_H

#include "types.h"

PlaylistParameters *decode_create_playlist_parameters(xmlNodePtr node);
PlaylistParameters *decode_delete_playlist_parameters(xmlNodePtr node);
PlaylistParameters *decode_show_playlist_parameters(xmlNodePtr node);
PlaylistParameters *decode_configure_loop_parameters(xmlNodePtr node);
PlaylistParameters *decode_queue_song_parameters(xmlNodePtr node);
PlaylistParameters *decode_dequeue_song_parameters(xmlNodePtr node);

#endif /* PLAYLIST_OPERATIONS_H */
