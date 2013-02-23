#include "parser.h"
#include "UNI_pub.h"

void handle_cache( parser *p, const unichar_t * unused );

void handle_code( parser *p, const unichar_t * code );
void handle_lon( parser * p, const unichar_t * lon );
void handle_lat( parser * p, const unichar_t * lat );
void handle_name( parser * p, const unichar_t * name );

void handle_awesomeness( parser * p, const unichar_t * awesomeness );
void handle_difficulty( parser * p, const unichar_t * difficulty );
void handle_size( parser * p, const unichar_t * size );
void handle_terrain( parser * p, const unichar_t * terrain );

void handle_type( parser * p, const unichar_t * type );

void handle_file_pos( parser * p, const unichar_t * fpos );
void handle_file_len( parser * p, const unichar_t * flen );
