from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# creating Table class
class Table(declarative_base()):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, default="default value")
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


# main Algorithm
class TaskManager(object):

    def __init__(self):

        self.engine = create_engine("sqlite:///todo.db?check_same_thread=False")
        Table.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)()
        self.choicemaker = {
            1: self.today, 2: self.weeks_task,
            3: self.all_tasks, 4: self.missed_tasks,
            5: self.adding_task, 6: self.delete_task
        }

    def adding_task(self):
        print("\nEnter task")
        new_task = input()
        print("Enter deadline")
        deadline_time = input()
        new_row = Table(task=new_task, deadline=datetime.strptime(deadline_time, "%Y-%m-%d"))
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!\n")

    def today(self):
        today = datetime.today()
        rows = self.session.query(Table).filter(Table.deadline == today.date()).all()
        today = datetime.strftime(datetime.today(), "%d %b:")
        if len(rows) == 0:
            print("\nToday", today, "\nNothing to do!\n")
        else:
            print("\nToday", today)
            n = 0
            for index in range(len(rows)):
                print(str(index + 1) + ". " + str(rows[n]))
                n += 1
            print("")

    def weeks_task(self):

        print()
        for date in (datetime.today() + timedelta(n) for n in range(7)):
            day = date.day
            day_name = date.strftime("%A")
            month = date.strftime('%b')
            tasks = self.session.query(Table).filter(Table.deadline == date.date()).all()
            print(f"{day_name} {day} {month}:")
            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task.task}")
            else:
                print("Nothing to do!")
            print()

    def all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print()
        for index, row in enumerate(rows, 1):
            print(f"{index}. {row.task}.", datetime.strftime(row.deadline, "%d %b"))
        print()

    def missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print("\nMissed tasks:")
        if len(rows) != 0:
            for index, row in enumerate(rows, 1):
                print(f"{index}. {row.task}.", datetime.strftime(row.deadline, "%d %b"))
            print()
        else:
            print("Nothing is missed")
            print()

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("\nChoose the number of the task you want to delete:")
        if len(rows) == 0:
            print("Nothing to delete\n")
        else:
            for index, row in enumerate(rows, 1):
                print(f"{index}. {row.task}.", datetime.strftime(row.deadline, "%d %b"))
            x = int(input())
            specific_row = rows[x - 1]
            self.session.delete(specific_row)
            self.session.commit()
            print("The task has been deleted!\n")

    def menu(self):

        while True:
            print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
            choice = int(input())
            if choice == 0:
                exit("\nBye!")
            self.choicemaker.get(choice, None)()


if __name__ == "__main__":
    Start = TaskManager()
    Start.menu()
