all: query

query: query.c
	gcc query.c -lsqlite3 -g -O1 -o query
