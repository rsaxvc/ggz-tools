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
#define BUFF_SIZE 4096
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


	int bytes_read;
do
	{
	void *buff = XML_GetBuffer(parser, BUFF_SIZE);
	if (buff == NULL)
		{
		printf("Failed to get buffer from eXpat\n");
		break;
		}

	bytes_read = fread( buff, sizeof(char), BUFF_SIZE, fp );
	if ( bytes_read < 0 )
		{
		break;
		}

	if (! XML_ParseBuffer(parser, bytes_read, bytes_read == 0 ) )
		{
	    printf("Error: %s at line:%i col:%i byte:%i\n",
			XML_ErrorString(XML_GetErrorCode(parser)),
			XML_GetCurrentLineNumber( parser ),
			XML_GetCurrentColumnNumber( parser ),
			XML_GetCurrentByteIndex( parser )
			);
		break;
		}
	}while( bytes_read > 0 );

fclose(fp);
XML_ParserFree(parser);

return 0;
}
