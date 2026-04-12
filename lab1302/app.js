const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const axios = require('axios');

const app = express();
const port = 3000;

// ✅ Функция для санитизации HTML (добавьте в начало)
const sanitizeHtml = (input) => {
    if (!input) return '';
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;');
};

// ✅ CSP middleware - должна быть здесь (после создания app, перед маршрутами)
app.use((req, res, next) => {
    // Более безопасный CSP (без unsafe-eval)
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    );
    next();
});

// Настройка шаблонизатора EJS
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Инициализация базы данных
const db = new sqlite3.Database('./comments.db');

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    // Добавляем тестовые комментарии
    db.run(`INSERT OR IGNORE INTO comments (id, username, comment) VALUES 
        (1, 'admin', 'Добро пожаловать на сайт!'),
        (2, 'user1', 'Отличный ресурс'),
        (3, 'user2', 'Очень полезная информация')`);
});

// Глобальная переменная для API ключа (hardcoded)
const API_KEY = 'test-api-key-12345';

// Маршруты

// Главная страница с комментариями
app.get('/', (req, res) => {
    db.all(`SELECT * FROM comments ORDER BY created_at DESC`, (err, comments) => {
        if (err) {
            res.status(500).send('Database error');
            return;
        }
        res.render('index', { comments: comments, error: null });
    });
});

// ✅ ИСПРАВЛЕННАЯ страница добавления комментария (с санитизацией)
app.post('/comment', (req, res) => {
    let { username, comment } = req.body;
    
    // ✅ ДОБАВЛЕНА санитизация
    username = sanitizeHtml(username || 'Anonymous');
    comment = sanitizeHtml(comment || '');
    
    db.run(`INSERT INTO comments (username, comment) VALUES (?, ?)`, 
        [username, comment], 
        function(err) {
            if (err) {
                res.status(500).send('Error saving comment');
                return;
            }
            res.redirect('/');
        });
});

// API для получения комментариев (JSON)
app.get('/api/comments', (req, res) => {
    const sort = req.query.sort || 'created_at DESC';
    
    // ✅ Исправлено: allow-list для сортировки
    const allowedSort = [
        'created_at DESC',
        'created_at ASC',
        'username ASC',
        'username DESC'
    ];
    
    if (!allowedSort.includes(sort)) {
        return res.status(400).json({ error: 'Invalid sort parameter' });
    }
    
    db.all(`SELECT * FROM comments ORDER BY ${sort}`, (err, comments) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
            return;
        }
        res.json(comments);
    });
});

// ✅ ИСПРАВЛЕННЫЙ API для поиска (параметризованный запрос)
app.get('/api/search', (req, res) => {
    const search = req.query.q || '';
    
    // ✅ Исправлено: параметризованный запрос
    db.all(`SELECT * FROM comments WHERE comment LIKE ?`, 
        [`%${search}%`], 
        (err, comments) => {
            if (err) {
                res.status(500).json({ error: 'Database error' });
                return;
            }
            res.json(comments);
        });
});

// Эндпоинт с hardcoded секретом (нужно исправить для продакшена)
app.get('/api/config', (req, res) => {
    // TODO: Убрать hardcoded ключ, использовать переменные окружения
    res.json({ 
        api_key: process.env.API_KEY || API_KEY, // лучше использовать переменную окружения
        environment: process.env.NODE_ENV || 'development',
        debug: process.env.NODE_ENV !== 'production'
    });
});

// ✅ ИСПРАВЛЕННЫЙ эндпоинт с axios (с валидацией URL)
app.get('/api/external', async (req, res) => {
    let url = req.query.url || 'https://api.example.com/data';
    
    // ✅ Добавлена валидация URL (только HTTPS, разрешенные домены)
    try {
        const allowedDomains = ['api.example.com', 'jsonplaceholder.typicode.com'];
        const urlObj = new URL(url);
        
        if (!allowedDomains.includes(urlObj.hostname)) {
            return res.status(400).json({ error: 'Domain not allowed' });
        }
        
        if (urlObj.protocol !== 'https:') {
            return res.status(400).json({ error: 'Only HTTPS allowed' });
        }
        
        const response = await axios.get(url, {
            timeout: 5000,
            maxRedirects: 0
        });
        res.json(response.data);
    } catch (error) {
        if (error.code === 'ECONNREFUSED') {
            res.status(500).json({ error: 'External service unavailable' });
        } else {
            res.status(500).json({ error: 'External request failed' });
        }
    }
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});