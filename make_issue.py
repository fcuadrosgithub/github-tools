import requests
import json
from typing import List, Dict

class GitHubIssueCreator:
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_issue(
        self,
        repo_owner: str,
        repo_name: str,
        student_github: str,
        section_number: str,
        section_title: str,
        student_name: str,
        team_number: int
    ) -> bool:
        """
        Crea un issue en GitHub con las instrucciones para el resumen de una sección
        
        Args:
            repo_owner: Dueño del repositorio (organización o usuario)
            repo_name: Nombre del repositorio del equipo
            student_github: Nombre de usuario de GitHub del estudiante (con @)
            section_number: Número de la sección (ej. "3")
            section_title: Título de la sección (ej. "Summary Functions and Maps")
            student_name: Nombre del estudiante para el branch
            team_number: Número del equipo (para referencia)
        
        Returns:
            bool: True si el issue se creó correctamente
        """
        # Generar los campos personalizados
        branch_name = f"doc/{student_name}-seccion-{section_number}"
        html_filename = f"{section_number}_{section_title.replace(' ', '_')}.html"
        commit_message = f"Resumen de la sección {section_number}: {section_title} del curso de pandas"
        pr_title = f"Doc: resumen sección {section_number}"
        pr_description = f"Este PR resume la sección {section_number}: {section_title} del curso de pandas."
        
        # Crear el cuerpo del issue
        issue_body = f"""# Instrucciones para el resumen de la sección {section_number} del curso de pandas
            Hola {student_github} ,

            Por favor, realiza un resumen de la **sección {section_number}: _{section_title}_** del curso de **pandas** disponible en la plataforma **Kaggle**.

            ## Instrucciones

            - Trabaja en el branch:  
            {branch_name}
            - El archivo HTML generado debe llamarse:  
            {html_filename}
            y debe estar ubicado dentro de la carpeta:  
            pandas-summary
            - Al finalizar, realiza un commit con el siguiente mensaje:  
            {commit_message}
            - Crea un Pull Request con el siguiente título:  
            {pr_title}
            - En la descripción del PR incluye:  
            {pr_description}

            Gracias.
            """
      
        # Datos para la API de GitHub
        issue_data = {
            "title": f"Resumen sección {section_number}: {section_title} (Equipo {team_number})",
            "body": issue_body,
            "assignees": [student_github.replace("@", "")]
        }
      
        # URL de la API
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
        
        # Enviar la solicitud
        response = requests.post(url, headers=self.headers, data=json.dumps(issue_data))
        
        if response.status_code == 201:
            print(f"Issue creado exitosamente para {student_github} en {repo_name}")
            return True
        else:
            print(f"Error al crear issue para {student_github}: {response.content}")
            return False


def main():
    # Configuración inicial
    github_token = input("Ingresa tu token de acceso personal de GitHub: ")
    issue_creator = GitHubIssueCreator(github_token)
    
    # Obtener información de los equipos y estudiantes
    teams = []
    num_teams = int(input("¿Cuántos equipos hay? "))
    
    for i in range(num_teams):
        team_number = i + 1
        repo_name = input(f"Nombre del repositorio para el equipo {team_number}: ")
        num_members = int(input(f"¿Cuántos miembros tiene el equipo {team_number}? "))
        
        members = []
        for j in range(num_members):
            student_name = input(f"Nombre del estudiante {j+1} (solo nombre, ej. Alberto): ")
            github_username = input(f"Usuario de GitHub de {student_name} (con @, ej. @JoseAlbertoLunaA57): ")
            members.append({
                "name": student_name,
                "github": github_username
            })
        
        teams.append({
            "number": team_number,
            "repo": repo_name,
            "members": members
        })
    
    # Obtener información de las secciones
    sections = []
    num_sections = int(input("¿Cuántas secciones necesitan resumen? "))
    
    for i in range(num_sections):
        section_number = input(f"Número de la sección {i+1} (ej. 3): ")
        section_title = input(f"Título de la sección {i+1} (ej. Summary Functions and Maps): ")
        sections.append({
            "number": section_number,
            "title": section_title
        })
    
    # Asignar secciones a estudiantes (round-robin)
    print("\nAsignando secciones a estudiantes...")
    
    repo_owner = input("¿Quién es el dueño de los repositorios? (usuario u organización): ")
    
    for section in sections:
        for team in teams:
            for member in team["members"]:
                # Crear issue para este estudiante
                success = issue_creator.create_issue(
                    repo_owner=repo_owner,
                    repo_name=team["repo"],
                    student_github=member["github"],
                    section_number=section["number"],
                    section_title=section["title"],
                    student_name=member["name"],
                    team_number=team["number"]
                )
                
                if not success:
                    print(f"Hubo un problema con {member['github']} - Sección {section['number']}")
                
                # Pausa para evitar rate limiting
                import time
                time.sleep(2)


if __name__ == "__main__":
    print("Script para crear issues de resumen en GitHub")
    print("-------------------------------------------\n")
    main()