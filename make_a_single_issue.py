#!/usr/bin/env python3
"""
Script para generar issues en GitHub con un template personalizable
"""

import requests
import json
from string import Template

def generate_issue(
    github_token: str,
    repo_owner: str,
    repo_name: str,
    assignee: str,
    section_number: int,
    section_title: str,
    name: str
) -> dict:
    """
    Genera un issue en GitHub usando un template con variables reemplazables
    
    Args:
        github_token: Token de acceso personal de GitHub
        repo_owner: Dueño del repositorio
        repo_name: Nombre del repositorio
        assignee: Usuario asignado al issue
        section_number: Número de la sección
        section_title: Título de la sección
        name: Usuario a mencionar en el issue
    
    Returns:
        dict: Respuesta de la API de GitHub
    """
    
    # Template con marcadores de posición
    issue_template = Template("""# Instrucciones para el resumen de la sección ${section_number} del curso de pandas

Hola @${assignee},

Por favor, realiza un resumen de la **sección ${section_number}: _${section_title}_** del curso de **pandas** disponible en la plataforma **Kaggle**.

## Instrucciones

- Trabaja en el branch:  
${CODE_BLOCK}
doc/${name}−seccion−${section_number}
${CODE_BLOCK}
- El archivo HTML generado debe llamarse:  
${CODE_BLOCK}
${section_number}_${formatted_title}.html
${CODE_BLOCK}
y debe estar ubicado dentro de la carpeta:  
${CODE_BLOCK}
pandas-summary
${CODE_BLOCK}
- Al finalizar, realiza un commit con el siguiente mensaje:  
${CODE_BLOCK}
Resumen de la sección $section_number: ${section_title} del curso de pandas.
${CODE_BLOCK}
- Crea un Pull Request con el siguiente título:  
${CODE_BLOCK}
Doc: resumen sección ${section_number}
${CODE_BLOCK}
- En la descripción del PR incluye:  
${CODE_BLOCK}
Este PR resume la sección $section_number: $section_title del curso de pandas.
${CODE_BLOCK}
Gracias.""")    

    # Formatear el título para el nombre de archivo
    formatted_title = section_title.replace(' ', '_') 

    # Reemplazar los marcadores de posición
    issue_body = issue_template.substitute(
        CODE_BLOCK='```',
        section_number=section_number,
        section_title=section_title,
        name=name,
        assignee=assignee,
        formatted_title=formatted_title
    )

    # Mostrar preview en terminal
    # print("\n" + "="*50)
    # print("VISTA PREVIA DEL ISSUE A CREAR:")
    # print("="*50)
    # print(issue_body)
    # print("="*50 + "\n")
    # return 

    # Configurar la solicitud a la API de GitHub
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "title": f"Doc: resumen seccion {section_number}",        
        "body": issue_body,
        "assignees": [assignee],
        "labels": ["documentation"]
    }
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al crear el issue: {e}")
        return None

def main():
    """Función principal para ejecutar el script"""
    print("Generador de Issues para GitHub\n" + "="*30 + "\n")
    
    # Configuración básica
    github_token = input("Ingresa tu token de GitHub: ").strip()
    # repo_owner = input("Dueño del repositorio (usuario/organización): ").strip()
    # repo_name = input("Nombre del repositorio: ").strip()
    
    # Datos del issue
    # print("\nDatos del issue:")
    # assignee = input("Usuario a asignar (sin @): ").strip()
    # section_number = input("Número de la sección: ").strip()
    # section_title = input("Título de la sección: ").strip()
    # name = input("Nombre del usuario @{assignee}: ").strip()
    
    repo_owner = 'GracieTics'
    repo_name = 'integrador-zapotecas-2b'

    assignee = 'GracieTics'
    section_number = 6
    section_title = 'Renaming and Combining'
    name = 'Gracie'

    # Generar el issue
    print("\nGenerando issue...")
    result = generate_issue(
        github_token=github_token,
        repo_owner=repo_owner,
        repo_name=repo_name,
        assignee=assignee,
        section_number=section_number,
        section_title=section_title,
        name=name
    )
    
    if result:
        print("\n¡Issue creado exitosamente!")
        print(f"Título: {result['title']}")
        print(f"URL: {result['html_url']}")
    else:
        print("\nNo se pudo crear el issue")

if __name__ == "__main__":
    main()