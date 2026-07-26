%{
#include "parser.tab.h"
#include <stdio.h>
%}

%option noyywrap
%option yylineno

%%

":"                         { return TK_DOS_PUNTOS; }
"-"                         { return TK_GUION; }
\n                          { return TK_NEWLINE; }
\r                          { /* Ignorar retorno de carro de Windows */ }
[ \t]+                      { /* Ignorar espacios horizontales */ }

"networks"                  { return TK_NETWORKS; }
"driver"                    { return TK_DRIVER; }
"ipam"                      { return TK_IPAM; }
"config"                    { return TK_CONFIG; }
"subnet"                    { return TK_SUBNET; }
"gateway"                   { return TK_GATEWAY; }
"labels"                    { return TK_LABELS; }
"driver_opts"               { return TK_DRIVER_OPTS; }
"true"|"false"              { return TK_BOOLEAN; }

[0-9a-fA-F:\.]+(\/[0-9]+)?  { return TK_IP_RANGO; }
\"[^\"]*\"                  { return TK_TEXTO; }
[a-zA-Z0-9_\-\.]+           { return TK_TEXTO; }

.                           { /* Ignorar caracteres desconocidos */ }

%%