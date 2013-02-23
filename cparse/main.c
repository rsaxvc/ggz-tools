#include <expat.h>
#include <stdio.h>
#include <string.h>

#include "hash.h"

#define STACK_SIZE 1024
static char tag_stack[STACK_SIZE];
static unsigned short tag_stack_idx[STACK_SIZE];
static unsigned short tag_stack_head;

static char element_buffer[1024];
static size_t element_buffer_usage;

void start_element(void *data, const char *element, const char **attribute)
{
size_t stored_stack_idx = tag_stack_head;

tag_stack[tag_stack_head++]='/';
strcpy( tag_stack + tag_stack_head, element );
tag_stack_head += strlen( element );
tag_stack_idx[tag_stack_head] = stored_stack_idx;

printf("SE:%s Stack:%s Head:%i\n",element,tag_stack,tag_stack_head);
}

void end_element(void *data, const char *el)
{
const struct ggz_handler_map * ptr;

ptr = in_word_set ( tag_stack, tag_stack_head );

if( ptr != NULL )
	{
	printf("Found handler\n");
	}
element_buffer_usage = 0;
tag_stack_head = tag_stack_idx[tag_stack_head];
tag_stack[tag_stack_head] = '\0';

printf("EL:%s Stack:%s Head:%i\n",el,tag_stack, tag_stack_head);
}

void handle_data(void *data, const char *content, int length)
{
memcpy( element_buffer + element_buffer_usage, content, length );
element_buffer_usage += length;
element_buffer[element_buffer_usage]='\0';
}

int main( int num_args, const char * args[] )
{
size_t file_size;
char buff[1024];
FILE           *fp;

if( num_args != 2 )
	{
	printf("usage: %s input.xml\n", args[0] );
	return 1;
	}

fp = fopen(args[1], "r");
if (fp == NULL) {
    printf("Failed to open file\n");
    return 1;
	}

XML_Parser      parser = XML_ParserCreate(NULL);
XML_SetElementHandler(parser, start_element, end_element);
XML_SetCharacterDataHandler(parser, handle_data);

tag_stack_head = 0;
tag_stack_idx[tag_stack_head] = tag_stack_head;

do
	{
	file_size = fread(buff, sizeof(char), sizeof(buff), fp);

	/* parse the xml */
	if (XML_Parse(parser, buff, file_size, XML_TRUE) == XML_STATUS_ERROR)
		{
	    printf("Error: %s\n", XML_ErrorString(XML_GetErrorCode(parser)));
		}
	}while( file_size == sizeof( buff ) );


fclose(fp);
XML_ParserFree(parser);

return 0;
}
