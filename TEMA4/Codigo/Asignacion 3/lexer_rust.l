%{
#include <stdio.h>
%}

%option noyywrap

%%

fn          { printf("TOKEN: TK_FN, Lexema: %s\n", yytext); }
let         { printf("TOKEN: TK_LET, Lexema: %s\n", yytext); }
mut         { printf("TOKEN: TK_MUT, Lexema: %s\n", yytext); }
i32         { printf("TOKEN: TK_I32, Lexema: %s\n", yytext); }
"println!"  { printf("TOKEN: TK_PRINTLN, Lexema: %s\n", yytext); }

[a-zA-Z_][a-zA-Z0-9_]* { printf("TOKEN: TK_IDENTIFICADOR, Lexema: %s\n", yytext); }
[0-9]+                 { printf("TOKEN: TK_NUMERO, Lexema: %s\n", yytext); }
\"[^\"]*\"             { printf("TOKEN: TK_CADENA, Lexema: %s\n", yytext); }

[{}():;=]   { printf("TOKEN: TK_SIMBOLO, Lexema: %s\n", yytext); }

"//".* { /* Ignorar comentarios */ }
[ \t\n]+    { /* Ignorar espacios, tabulaciones y saltos de linea */ }

.           { printf("ERROR LÉXICO: Carácter no reconocido: %s\n", yytext); }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error al abrir el archivo");
            return 1;
        }
        yyin = file;
    }
    yylex();
    return 0;
}