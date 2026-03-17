const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const tasksRouter = require('./routes/tasks');
const { notFoundHandler, errorHandler } = require('./middleware/errorHandler');

const app = express();

// Безопасность
app.use(helmet());

// CORS
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 минут
  max: 100, // максимум 100 запросов с одного IP
  message: {
    error: 'Слишком много запросов. Попробуйте позже.'
  }
});
app.use('/api/', limiter);

// Парсинг JSON
app.use(express.json());

// Логирование запросов (простое)
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

// Routes
app.use('/api/tasks', tasksRouter);

// TODO: Добавьте корневой маршрут GET / который возвращает информацию об API
// Пример: { name: 'Task Manager API', version: '1.0.0', docs: '/api/tasks' }
app.get('/', (req, res) => {
  res.json({
    name: 'Task Manager API',
    version: '1.0.0',
    description: 'REST API для управления задачами',
    documentation: '/api/tasks',
    endpoints: {
      tasks: '/api/tasks',
      taskById: '/api/tasks/:id',
      stats: '/api/tasks/stats/summary',
      search: '/api/tasks/search/text',
      health: '/health'
    }
  });
});

// TODO: Добавьте маршрут для проверки здоровья GET /health
// Должен возвращать { status: 'healthy', timestamp: new Date().toISOString() }
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Обработка 404
app.use(notFoundHandler);

// Обработка ошибок
app.use(errorHandler);

module.exports = app;