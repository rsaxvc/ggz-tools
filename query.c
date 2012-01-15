#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>

static int cb_find_return_count(void*ptr_to_retn, int num_cols, char ** c1, char ** c2)
{
(*(int*)ptr_to_retn)++;
return 0;
}

int find_count_by_loc( sqlite3 * ppDb,double minlat, double maxlat, double minlon, double maxlon )
{
int sz;
const char * pstr = "SELECT gc_code FROM geocaches_r, geocaches WHERE lat >= %f AND lat <= %f AND lon >= %f AND lon <= %f AND geocaches_r.id == geocaches.id";
char * buffer;
int retn = 0;
sz = snprintf( NULL, 0, pstr, minlat, maxlat, minlon, maxlon );
buffer = malloc( sz + 1 );
sprintf( buffer, pstr, minlat, maxlat, minlon, maxlon );
sqlite3_exec( ppDb, buffer, cb_find_return_count, &retn, NULL );
free( buffer );
return retn;
}

int main( int numArgs, char * args[] )
{
int sd;
sqlite3 * ppDb;

double minLat = -45;
double maxLat = +45;
double minLon = -45;
double maxLon = +45;

sd = sqlite3_open( "out.db", &ppDb );
if( SQLITE_OK == sd )
    {
    int count;
    printf("Opened DB\n");
    if( numArgs == 5 )
        {
        minLat = atof(args[1]);
        maxLat = atof(args[2]);
        minLon = atof(args[3]);
        maxLon = atof(args[4]);
        }
    else
        {
        printf("Usage: %s minLat maxLat minLon maxLon\n", args[0] );
        printf("Assuming " );
        }
    printf("minLat=%f maxLat=%f minLon=%f maxLon=%f\n", minLat, maxLat, minLon, maxLon );

    count = find_count_by_loc(ppDb, minLat, maxLat, minLon, maxLon );
    printf("Found %i\n",count);
    }
else
    {
    printf("Error opening db:%i\n",sd);
    }
sqlite3_close( ppDb );
}
