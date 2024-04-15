#include "song_database.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// XXX: For the purposes of this assignment, this small list of 10 songs will server as our database
static SongEntry song_entries[] = {
	{"never gonna give you up", "pop", "rick ashtley", 212827},
	{"all star", "pop", "smash mouth", 200373},
	{"shooting stars", "alternative", "bag raiders", 235813},
	{"baby", "pop", "justin bieber", 214240},
	{"dragostea din tei", "dance", "o-zone", 217120},
	{"running in the 90's", "eurobeat", "max coveri", 283000},
	{"gas gas gas", "eurobeat", "manuel caramori", 196000},
	{"deja vu", "eurobeat", "dave rodgers", 260000},
	{"fly me to the moon", "jazz", "frank sinatra", 147000},
	{"suicide mission", "ost", "jack wall", 285000}};

DBHandler *get_database_handler()
{
	DBHandler *db_handler = NULL;
	db_handler = (DBHandler *)malloc(sizeof(DBHandler));

	db_handler->song_entries = song_entries;
	db_handler->entry_count = 10;

	return db_handler;
}

SongEntry *query_song(DBHandler *handler, const char *title, const char *genre, const char *artist)
{
	int i;
	int match_pos = -1;

	for (i = 0; i < handler->entry_count; i++)
	{
		if (strcasecmp(handler->song_entries[i].title, title) == 0)
		{
			if (genre != NULL && strcasecmp(handler->song_entries[i].genre, genre) != 0)
			{
				continue;
			}
			if (artist != NULL && strcasecmp(handler->song_entries[i].artist, artist) != 0)
			{
				continue;
			}
			match_pos = i;
		}
	}

	if (match_pos < 0)
	{
		return NULL;
	}
	else
	{
		return &(handler->song_entries[match_pos]);
	}
}

void release_database_handler(DBHandler *handler)
{
	free(handler);
}