%{
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

extern int yylex();
extern int yyparse();
extern FILE *yyin;
extern void yyrestart(FILE *input_file);

extern int yylineno;
extern char *yytext;

void yyerror(const char *s) {
    fprintf(stderr, "[!] Error en la línea %d: %s (cerca de '%s')\n", yylineno, s, yytext);
}
%}

/* Mantenemos rigurosamente TODOS los tokens del léxico original */
%token TK_NETWORKS TK_DRIVER TK_IPAM TK_CONFIG TK_SUBNET TK_GATEWAY
%token TK_LABELS TK_DRIVER_OPTS TK_BOOLEAN TK_IP_RANGO 
%token TK_TEXTO TK_DOS_PUNTOS TK_GUION TK_NEWLINE

%%

/* La raíz acepta saltos iniciales, la palabra clave networks y el flujo secuencial */
inicio:
    saltos_opcionales TK_NETWORKS TK_DOS_PUNTOS saltos_linea flujo_yaml final_opcional
    ;

flujo_yaml:
    /* vacío */
    | flujo_yaml componente
    ;

/* El parser valida estrictamente las combinaciones válidas del archivo sin enredarse en jerarquías invisibles */
componente:
    TK_TEXTO TK_DOS_PUNTOS saltos_linea             /* Declaración de red o subsección */
    | TK_DRIVER TK_DOS_PUNTOS TK_TEXTO saltos_linea /* driver: texto */
    | TK_IPAM TK_DOS_PUNTOS saltos_linea           /* ipam: */
    | TK_CONFIG TK_DOS_PUNTOS saltos_linea         /* config: */
    | TK_LABELS TK_DOS_PUNTOS saltos_linea         /* labels: */
    | TK_DRIVER_OPTS TK_DOS_PUNTOS saltos_linea    /* driver_opts: */
    | TK_GUION TK_SUBNET TK_DOS_PUNTOS TK_IP_RANGO saltos_linea /* - subnet: IP */
    | TK_GATEWAY TK_DOS_PUNTOS TK_IP_RANGO saltos_linea         /* gateway: IP */
    | TK_TEXTO TK_DOS_PUNTOS TK_TEXTO saltos_linea  /* propiedad clave: valor */
    | TK_TEXTO TK_DOS_PUNTOS TK_BOOLEAN saltos_linea/* propiedad clave: booleano */
    | TK_NEWLINE
    ;

saltos_linea:
    TK_NEWLINE
    | saltos_linea TK_NEWLINE
    ;

saltos_opcionales:
    /* vacío */
    | saltos_linea
    ;

final_opcional:
    /* vacío */
    | saltos_linea
    ;

%%

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Uso: ./parser_c <archivo.yml>\n");
        return 1;
    }
    
    FILE *file = fopen(argv[1], "r");
    if (!file) {
        printf("No se pudo abrir el archivo %s\n", argv[1]);
        return 1;
    }
    
    printf("--- Evaluando %s ---\n", argv[1]);
    
    yyin = file;
    if (yyparse() == 0) {
        printf("=> AST: ¡Análisis en C Exitoso!\n");
    } else {
        printf("\n[!] Análisis abortado.\n");
        fclose(file);
        return 1;
    }

    int iteraciones = 10000;
    printf("Iniciando bucle de estrés de %d iteraciones...\n", iteraciones);
    
    struct timeval start, end;
    gettimeofday(&start, NULL);

    for(int i = 0; i < iteraciones; i++) {
        fseek(file, 0, SEEK_SET);
        yyrestart(file);
        yyparse();
    }
    
    gettimeofday(&end, NULL);
    
    long seconds = (end.tv_sec - start.tv_sec);
    long micros = ((seconds * 1000000) + end.tv_usec) - (start.tv_usec);
    double total_ms = (double)micros / 1000.0;
    
    printf("--> Tiempo total de ejecución (C Nativo): %.2f ms\n\n", total_ms);
    
    fclose(file);
    return 0;
}