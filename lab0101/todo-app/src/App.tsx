import { useState } from 'react';

// Тип для задачи
interface Task {
  id: number;
  text: string;
  completed: boolean;
}

function App() {
  // Состояние для списка задач
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Изучить React', completed: true },
    { id: 2, text: 'Написать To-Do приложение', completed: false }
  ]);

  // Состояние для новой задачи
  const [newTask, setNewTask] = useState('');

  // Функция добавления задачи
  const addTask = () => {
    if (newTask.trim() === '') return;
    
    const task: Task = {
      id: Date.now(),
      text: newTask,
      completed: false
    };
    
    setTasks([...tasks, task]);
    setNewTask('');
  };

  // Функция удаления задачи (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО)
  const removeTask = (id: number) => {
    // TODO: Реализуйте удаление задачи по ID
    // Подсказка: используйте метод filter для создания нового массива
    const task1: Task[] = tasks.filter(task => task.id != id);
                         
    setTasks(task1);
  };

  // Функция переключения статуса задачи (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО)
  const toggleTask = (id: number) => {
    // TODO: Реализуйте переключение статуса completed
    // Подсказка: используйте метод map для обновления массива
    const task2 = tasks.map(task => {
      if(task.id === id){
        return {...task,               
        completed: !task.completed
        }
      }
      return task;
      } );
    
    console.log(task2);
    setTasks(task2);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
          📝 Список задач
        </h1>
        
        {/* Форма добавления задачи */}
        <div className="flex gap-2 mb-6">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addTask()}
            placeholder="Введите новую задачу..."
            className="flex-grow px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={addTask}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
          >
            Добавить
          </button>
        </div>

        {/* Список задач */}
        <div className="space-y-3">
          {tasks.map(task => (
            <div 
              key={task.id} 
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
            >
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                  className="h-5 w-5 text-blue-600"
                />
                <span className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                  {task.text}
                </span>
              </div>
              
              {/* Кнопка удаления (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО) */}
              <button
                onClick={() => removeTask(task.id)}
                className="text-red-500 hover:text-red-700"
              >Удалить
                {/* TODO: Добавьте иконку удаления или текст "Удалить" */}
              </button>
            </div>
          ))}
          {/* После map */}
          {tasks.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>Список задач пуст</p>
              <p className="text-sm">Добавьте первую задачу!</p>
            </div>
          )}
        </div>

        {/* Статистика (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО) */}
        <div className="mt-6 pt-4 border-t">
          <p className="text-gray-600">
            Всего задач: {tasks.length}
          </p>
          <p className="text-gray-600">
            Выполненных  задач: {tasks.filter(task => task.completed).length}
          </p>
          {/* TODO: Добавьте отображение количества выполненных задач */}
        </div>
      </div>
    </div>
  );
}

export default App;
