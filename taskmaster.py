import tkinter
import tkinter.messagebox
import pickle

root = tkinter.Tk()
root.title("TaskMaster")


# Adds a task to the listbox from the entry widget
def add_task():
    task = task_entry.get()
    if task != "":
        tasks_listbox.insert(tkinter.END, task)
        task_entry.delete(0, tkinter.END)
    else:
        tkinter.messagebox.showwarning(title="Error", message="Enter a task first")


# Deletes selected task
def delete_task():
    try:
        task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(task_index)
    except:
        tkinter.messagebox.showwarning(title="Error", message="Select a task first")


# Loads tasks that are saved in tasks.dat
# Deletes previous tasks in the listbox so it doesn't load on top of them
def load_tasks():
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        tasks_listbox.delete(0, tkinter.END)
        for task in tasks:
            tasks_listbox.insert(tkinter.END, task)
    except:
        tkinter.messagebox.showwarning(title="Error", message="Save a task list first")


# Saves tasks to tasks.dat
def save_tasks():
    tasks = tasks_listbox.get(0, tasks_listbox.size())
    pickle.dump(tasks, open("tasks.dat", "wb"))


# GUI

# Makes a frame to put the listbox and scrollbar together
tasks_frame = tkinter.Frame(root)
tasks_frame.pack()

tasks_listbox = tkinter.Listbox(tasks_frame, height=20, width=50)
tasks_listbox.pack(side=tkinter.LEFT)

tasks_scrollbar = tkinter.Scrollbar(tasks_frame)
tasks_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Lets the listbox be controlled by the scrollbar
tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
tasks_scrollbar.config(command=tasks_listbox.yview)

task_entry = tkinter.Entry(root, width=50)
task_entry.pack()

add_task_button = tkinter.Button(root, text="Add task", width=48, command=add_task)
add_task_button.pack()

delete_task_button = tkinter.Button(
    root, text="Delete task", width=48, command=delete_task
)
delete_task_button.pack()

load_tasks_button = tkinter.Button(
    root, text="Load tasks", width=48, command=load_tasks
)
load_tasks_button.pack()

save_tasks_button = tkinter.Button(
    root, text="Save tasks", width=48, command=save_tasks
)
save_tasks_button.pack()


root.mainloop()
