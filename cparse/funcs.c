#include "funcs.h"
#include <stdio.h>
#include "parser.h"
#include "UNI_pub.h"

void handle_cache( parser *p, const unichar_t * unused )
{
}

void handle_code( parser *p, const unichar_t * code )
{
printf("Got code\n");
}

void handle_lon( parser * p, const unichar_t * lon )
{
printf("Got lon\n");
}

void handle_lat( parser * p, const unichar_t * lat )
{
printf("Got lat\n");
}

void handle_name( parser * p, const unichar_t * name )
{
printf("Got name\n");
}

void handle_awesomeness( parser * p, const unichar_t * awesomeness )
{
printf("awesomeness:%s\n",awesomeness);
}

void handle_difficulty( parser * p, const unichar_t * difficulty )
{
printf("difficulty:%s\n",difficulty);
}

void handle_size( parser * p, const unichar_t * size )
{
printf("size:%s\n",size);
}

void handle_terrain( parser * p, const unichar_t * terrain )
{
printf("terrain:%s\n",terrain);
}

void handle_type( parser * p, const unichar_t * type )
{
printf("type:%s\n",type);
}

void handle_file_pos( parser * p, const unichar_t * fpos )
{
printf("pos:%s\n",fpos);
}

void handle_file_len( parser * p, const unichar_t * flen )
{
printf("len:%s\n",flen);
}
