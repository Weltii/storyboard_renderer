from backend.classes.project import Project


class ProjectHandler:
    current_project: Project = None

    def save_project(self, project: Project = None):
        if not project:
            project = self.current_project
        if project:
            project.save_project()

    def load_project(self, path):
        self.current_project = Project.load_from_path(path)
        return self.current_project

    def create_new_project(self, path):
        self.current_project = Project.generate_new_project(path)
        return self.current_project

    def close_project(self):
        self.current_project = None
