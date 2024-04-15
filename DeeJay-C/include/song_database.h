#ifndef __SONG_DATABASE_H__
#define __SONG_DATABASE_H__

/**
 * @brief A song entry in the "database"
 */
typedef struct SongEntry
{
	char *title;
	char *genre;
	char *artist;
	int duration;
} SongEntry;

/**
 * @brief An object that handles "databases" operations
 */
typedef struct DBHandler
{
	int entry_count;
	SongEntry *song_entries;
} DBHandler;

/**
 * @brief get_database_handler initializes and returns a new handler to the database
 *
 * @return DBHandler*
 */
DBHandler *get_database_handler();

/**
 * @brief query_song searches the databases for a song that matches the provided parameters
 *
 * @param handler A handler to the database
 * @param title REQUIRED. The title of the song being queried
 * @param genre OPTIONAL. The genre of the song being queried
 * @param artist OPTIONAL. The artist of the song being queried
 * @return SongEntry*
 */
SongEntry *query_song(DBHandler *handler, const char *title, const char *genre, const char *artist);

/**
 * @brief release_database_handler frees a database handler
 *
 * @param handler The handler that will be freed
 */
void release_database_handler(DBHandler *handler);

#endif /* __SONG_DATABASE_H__ */