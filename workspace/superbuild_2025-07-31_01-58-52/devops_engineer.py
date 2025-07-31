import os

class DevOpsEngineer:
    def __init__(self, name):
        self.name = name
    
    def receive_task(self, task):
        self.task = task
    
    def build(self):
        # Implement build logic here
        print(f"{self.name} is building the project...")
        # Execute build commands, e.g., running shell scripts, Makefiles, etc.
        os.system("make build")
    
    def test(self):
        # Implement test logic here  
        print(f"{self.name} is running tests...")  
        # Execute test commands
        os.system("make test")
    
    def deploy(self):
        # Implement deployment logic here
        print(f"{self.name} is deploying the application...")  
        # Execute deployment commands
        os.system("ansible-playbook deploy.yml")
        
    def execute_task(self):
        print(f"{self.name} received task: {self.task}")
        self.build()
        self.test()
        self.deploy()
        print(f"{self.name} completed the task successfully!")

if __name__ == "__main__":
    engineer = DevOpsEngineer("John")
    engineer.receive_task("Build and deploy the web application")
    engineer.execute_task()
