class BluLupo:
    def __init__(self):
        self.username = 'BluLupo'
        self.name = 'Hersel Giannella'
        self.position = 'Analyst & System Integrator & PythonDev'
        self.web = 'https://hersel.it'
        self.blog = 'https://hersel.it/blog'
        self.linkedin = 'https://linkedin.com/in/hersel-giannella-654580111'
        self.code = {
            'backend': ['Python', 'Flask', 'Django', 'FastAPI', 'PHP'],
            'database': ['PostgreSQL', 'MySQL', 'SQL Server', 'Redis'],
            'devops': ['Docker', 'Linux', 'Proxmox','VMWare','Kubernetes'],
            'frontend': ['HTML', 'CSS', 'JavaScript', 'VueJS', 'Boostrap'],
            'tools': ['GIT', 'GitHub', 'GitLab', 'Nginx'],
            'misc': ['HL7-FHIR', 'Agile', 'Hardware-Expert']
        }
        self.architecture = ['MVC', 'REST-API', 'Headless']

    def __str__(self):
        return f'Name: {self.name}\n'\
                'Position: {self.position}\n'\
                'Website: {self.web}\nBlog: {self.blog}'

if __name__ == '__main__':
    me = BluLupo()
    print(me)