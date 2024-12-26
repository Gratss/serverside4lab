const express = require('express');
const morgan = require('morgan');
const winston = require('winston');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Настройка логирования с использованием Winston
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'logs/app.log' }),
        new winston.transports.File({ filename: 'logs/trace.log', level: 'debug' })
    ],
});

// Middleware для логирования HTTP-запросов
app.use(morgan('combined', {
    stream: {
        write: (message) => logger.info(message.trim())
    }
}));

// Middleware для обработки тела запроса
app.use(bodyParser.json());

// Обработчик для корневого маршрута
app.get('/', (req, res) => {
    res.send('Добро пожаловать на главную страницу!');
});

// Логирование времени выполнения методов
const logExecutionTime = (req, res, next) => {
    const start = Date.now();
    res.on('finish', () => {
        const duration = Date.now() - start;
        logger.info(`Время выполнения ${req.method} ${req.originalUrl}: ${duration} мс`);
    });
    next();
};

app.use(logExecutionTime);

// Пример контроллера
app.get('/example', (req, res) => {
    logger.info('Запрос к /example');
    res.send('Hello, World!');
});

// Глобальный обработчик ошибок
app.use((err, req, res, next) => {
    logger.error('Ошибка: ', err);
    res.status(500).send('Что-то пошло не так!');
});

// Запуск сервера
app.listen(port, () => {
    logger.info(`Сервер запущен на http://localhost:${port}`);
});