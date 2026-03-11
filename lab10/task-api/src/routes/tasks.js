const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const { 
  validateCreateTask, 
  validateUpdateTask, 
  validateId 
} = require('../middleware/validation');
const { 
  initializeDataFile, 
  readData, 
  writeData, 
  getNextId 
} = require('../utils/fileOperations');

// Инициализация файла данных при запуске
initializeDataFile();

// GET /api/tasks - получение всех задач с фильтрацией
router.get('/', async (req, res, next) => {
  try {
    const { category, completed, priority, sortBy, page = 1, limit = 10 } = req.query;
    const data = await readData();
    
    let tasks = [...data.tasks];
    
    // TODO: Реализуйте фильтрацию по категории (если передан параметр category)
    if (category) {
      tasks = tasks.filter(task => task.category === category);
    }
    
    // TODO: Реализуйте фильтрацию по статусу выполнения
    // completed может быть 'true' или 'false' (строкой)
    if (completed !== undefined) {
      const isCompleted = completed === 'true';
      tasks = tasks.filter(task => task.completed === isCompleted);
    }
    
    // TODO: Реализуйте фильтрацию по приоритету
    // priority - число от 1 до 5
    if (priority) {
      const priorityNum = parseInt(priority);
      if (!isNaN(priorityNum) && priorityNum >= 1 && priorityNum <= 5) {
        tasks = tasks.filter(task => task.priority === priorityNum);
      }
    }
    
    // TODO: Реализуйте сортировку
    // sortBy может быть: 'dueDate', 'priority', 'createdAt'
    // Для сортировки по убыванию: '-dueDate', '-priority'
    if (sortBy) {
      const sortField = sortBy.startsWith('-') ? sortBy.substring(1) : sortBy;
      const sortOrder = sortBy.startsWith('-') ? -1 : 1;
      
      if (['dueDate', 'priority', 'createdAt'].includes(sortField)) {
        tasks.sort((a, b) => {
          let valA = a[sortField];
          let valB = b[sortField];
          
          // Обработка null значений для dueDate
          if (sortField === 'dueDate') {
            if (!valA && !valB) return 0;
            if (!valA) return 1; // null значения в конец
            if (!valB) return -1;
            valA = new Date(valA).getTime();
            valB = new Date(valB).getTime();
          }
          
          if (valA < valB) return -1 * sortOrder;
          if (valA > valB) return 1 * sortOrder;
          return 0;
        });
      }
    }
    
    // TODO: Добавьте пагинацию
    // Используйте параметры page и limit из query
    const pageNum = parseInt(page);
    const limitNum = parseInt(limit);
    const startIndex = (pageNum - 1) * limitNum;
    const endIndex = pageNum * limitNum;
    
    const paginatedTasks = tasks.slice(startIndex, endIndex);
    
    res.json({
      success: true,
      count: paginatedTasks.length,
      total: tasks.length,
      page: pageNum,
      limit: limitNum,
      totalPages: Math.ceil(tasks.length / limitNum),
      data: paginatedTasks
    });
    
  } catch (error) {
    next(error);
  }
});

// GET /api/tasks/:id - получение задачи по ID
router.get('/:id', validateId, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const data = await readData();
    
    // TODO: Найдите задачу по ID в data.tasks
    // Если задача не найдена, верните 404
    const task = data.tasks.find(t => t.id === taskId);
    
    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    res.json({
      success: true,
      data: task
    });
    
  } catch (error) {
    next(error);
  }
});

// POST /api/tasks - создание новой задачи
router.post('/', validateCreateTask, async (req, res, next) => {
  try {
    const { title, description, category, priority, dueDate } = req.body;
    const data = await readData();
    
    const newTask = {
      id: await getNextId(),
      uuid: uuidv4(),
      title,
      description: description || '',
      category: category || 'personal',
      priority: priority || 3,
      dueDate: dueDate || null,
      completed: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    // TODO: Добавьте новую задачу в массив data.tasks
    data.tasks.push(newTask);
    
    // TODO: Сохраните обновленные данные
    await writeData(data);
    
    res.status(201).json({
      success: true,
      message: 'Задача успешно создана',
      data: newTask
    });
    
  } catch (error) {
    next(error);
  }
});

// PUT /api/tasks/:id - полное обновление задачи
router.put('/:id', validateId, validateUpdateTask, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const updates = req.body;
    const data = await readData();
    
    // TODO: Найдите задачу по ID
    // Если не найдена - 404
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    // TODO: Обновите задачу (все переданные поля)
    // Не забудьте обновить updatedAt
    const updatedTask = {
      ...data.tasks[taskIndex],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    
    data.tasks[taskIndex] = updatedTask;
    
    // TODO: Сохраните обновленные данные
    await writeData(data);
    
    res.json({
      success: true,
      message: 'Задача успешно обновлена',
      data: updatedTask
    });
    
  } catch (error) {
    next(error);
  }
});

// PATCH /api/tasks/:id/complete - отметка задачи как выполненной
router.patch('/:id/complete', validateId, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const data = await readData();
    
    // TODO: Найдите задачу по ID
    // Если не найдена - 404
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    // TODO: Обновите статус задачи на completed: true
    // Обновите updatedAt
    data.tasks[taskIndex].completed = true;
    data.tasks[taskIndex].updatedAt = new Date().toISOString();
    
    // TODO: Сохраните обновленные данные
    await writeData(data);
    
    res.json({
      success: true,
      message: 'Задача отмечена как выполненная',
      data: data.tasks[taskIndex]
    });
    
  } catch (error) {
    next(error);
  }
});

// DELETE /api/tasks/:id - удаление задачи
router.delete('/:id', validateId, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const data = await readData();
    
    // TODO: Найдите индекс задачи по ID
    // Если не найдена - 404
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    // TODO: Удалите задачу из массива
    data.tasks.splice(taskIndex, 1);
    
    // TODO: Сохраните обновленные данные
    await writeData(data);
    
    res.json({
      success: true,
      message: 'Задача успешно удалена'
    });
    
  } catch (error) {
    next(error);
  }
});

// GET /api/tasks/stats - статистика по задачам
router.get('/stats/summary', async (req, res, next) => {
  try {
    const data = await readData();
    const tasks = data.tasks;
    
    const stats = {
      total: 0,
      completed: 0,
      pending: 0,
      overdue: 0,
      byCategory: {},
      byPriority: {
        1: 0, 2: 0, 3: 0, 4: 0, 5: 0
      }
    };
    
    // TODO: Реализуйте подсчет статистики:
    // 1. Общее количество задач
    stats.total = tasks.length;
    
    const now = new Date();
    
    tasks.forEach(task => {
      // 2. Количество выполненных задач
      if (task.completed) {
        stats.completed++;
      } else {
        // 3. Количество невыполненных задач
        stats.pending++;
        
        // 4. Количество просроченных задач (dueDate < сегодня и completed = false)
        if (task.dueDate) {
          const dueDate = new Date(task.dueDate);
          if (dueDate < now) {
            stats.overdue++;
          }
        }
      }
      
      // 5. Распределение задач по категориям
      const category = task.category || 'other';
      stats.byCategory[category] = (stats.byCategory[category] || 0) + 1;
      
      // 6. Распределение задач по приоритетам
      if (task.priority >= 1 && task.priority <= 5) {
        stats.byPriority[task.priority]++;
      }
    });
    
    res.json({
      success: true,
      data: stats
    });
    
  } catch (error) {
    next(error);
  }
});

// GET /api/tasks/search - поиск задач
router.get('/search/text', async (req, res, next) => {
  try {
    const { q } = req.query;
    
    if (!q || q.trim().length < 2) {
      return res.status(400).json({
        success: false,
        error: 'Поисковый запрос должен содержать минимум 2 символа'
      });
    }
    
    const data = await readData();
    const searchTerm = q.toLowerCase().trim();
    
    // TODO: Реализуйте поиск задач
    // Искать в полях title и description
    // Поиск должен быть регистронезависимым
    // Верните задачи, содержащие поисковый запрос
    const results = data.tasks.filter(task => {
      const titleMatch = task.title.toLowerCase().includes(searchTerm);
      const descriptionMatch = task.description.toLowerCase().includes(searchTerm);
      return titleMatch || descriptionMatch;
    });
    
    res.json({
      success: true,
      count: results.length,
      data: results
    });
    
  } catch (error) {
    next(error);
  }
});

module.exports = router;