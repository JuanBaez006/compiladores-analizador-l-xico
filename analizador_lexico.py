import re

# Definición de los tipos de tokens
class TokenType:
    L_CORCHETE = "L_CORCHETE"
    R_CORCHETE = "R_CORCHETE"
    L_LLAVE = "L_LLAVE"
    R_LLAVE = "R_LLAVE"
    COMA = "COMA"
    DOS_PUNTOS = "DOS_PUNTOS"
    LITERAL_CADENA = "STRING"
    LITERAL_NUM = "NUMBER"
    PR_TRUE = "PR_TRUE"
    PR_FALSE = "PR_FALSE"
    PR_NULL = "PR_NULL"
    EOF_TOKEN = "EOF"
    ERROR = "ERROR"

# Expresiones regulares para cada tipo de token
token_regex = {
    TokenType.L_CORCHETE: r'\[',
    TokenType.R_CORCHETE: r'\]',
    TokenType.L_LLAVE: r'\{',
    TokenType.R_LLAVE: r'\}',
    TokenType.COMA: r',',
    TokenType.DOS_PUNTOS: r':',
    TokenType.LITERAL_CADENA: r'"(.*?)"',
    TokenType.LITERAL_NUM: r'-?\d+(\.\d+)?([eE][-+]?\d+)?',
    TokenType.PR_TRUE: r'true',
    TokenType.PR_FALSE: r'false',
    TokenType.PR_NULL: r'null',
}

# Función para obtener el siguiente token del texto fuente
def get_next_token(text):
    for token_type, regex in token_regex.items():
        match = re.match(regex, text)
        if match:
            lexeme = match.group(0)
            return (token_type, lexeme)
    return (TokenType.ERROR, text[0])

# Función para escribir el tipo de token en un archivo de texto con sangrías
def write_token_type_to_file(token, output_file, indent_level):
    token_type, _ = token
    indent = "\t" * indent_level
    if token_type == TokenType.L_CORCHETE:
        output_file.write(indent + "L_CORCHETE\n")
    elif token_type == TokenType.R_CORCHETE:
        output_file.write(indent + "R_CORCHETE\n")
    elif token_type == TokenType.L_LLAVE:
        output_file.write(indent + "L_LLAVE\n")
    elif token_type == TokenType.R_LLAVE:
        output_file.write(indent + "R_LLAVE\n")
    else:
        output_file.write(indent + token_type + "\n")

# Función principal
def main():
    # Leer el archivo fuente
    try:
        with open('fuente.json', 'r') as file:
            source_text = file.read()
    except FileNotFoundError:
        print("Error: Archivo fuente no encontrado.")
        return

    # Abrir el archivo de salida
    try:
        output_file = open("output.txt", "w")
    except PermissionError:
        print("Error: No se puede crear el archivo de salida.")
        return

    # Lista para seguir el nivel de anidamiento
    indent_level = 0

    # Analizar y escribir cada tipo de token en el archivo
    while source_text:
        token = get_next_token(source_text.strip())
        if token[0] != TokenType.ERROR:
            write_token_type_to_file(token, output_file, indent_level)
            if token[0] == TokenType.L_CORCHETE or token[0] == TokenType.L_LLAVE:
                indent_level += 1
            elif token[0] == TokenType.R_CORCHETE or token[0] == TokenType.R_LLAVE:
                indent_level -= 1
        else:
            print("ERROR: Token no reconocido")
        source_text = source_text[len(token[1]):].strip()

    # Escribir EOF al final
    output_file.write(TokenType.EOF_TOKEN + "\n")
    output_file.close()

if __name__ == "__main__":
    main()
