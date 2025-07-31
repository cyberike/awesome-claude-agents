class DevOpsEngineer:
    def __init__(self):
        self.name = 'DevOps Engineer'
        self.tasks = []

    def receive_task(self, task):
        self.tasks.append(task)

    def build(self):
        output = ''
        for task in self.tasks:
            output += f'Executing task: {task}\n'
        print(output)

if __name__ == '__main__':
    engineer = DevOpsEngineer()
    engineer.receive_task('Build infrastructure')
    engineer.receive_task('Deploy application') 
    engineer.build()