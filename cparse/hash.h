#include "parser.h"
#include "UNI_pub.h"

typedef void(*ggz_handler)(parser *, const unichar_t * tag);

struct ggz_handler_map
	{
	const unichar_t * name;
	ggz_handler handler;
	};

const struct ggz_handler_map *
in_word_set (register const char *str, register unsigned int len);

