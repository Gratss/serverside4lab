const express = require('express');
const app = express();
app.use(express.json());

let books = [];

// Получение списка всех книг
app.get('/books', (req, res) => {
    res.json(books);
});

// Получение книги по ID
app.get('/books/:id', (req, res) => {
    const book = books.find(b => b.id === parseInt(req.params.id));
    if (!book) return res.status(404).send('Книга не найдена');
    res.json(book);
});

// Добавление новой книги
app.post('/books', (req, res) => {
    const newBook = {
        id: books.length + 1,
        title: req.body.title,
        author: req.body.author,
        year: req.body.year
    };
    books.push(newBook);
    res.status(201).json(newBook);
});

// Обновление книги по ID
app.put('/books/:id', (req, res) => {
    const book = books.find(b => b.id === parseInt(req.params.id));
    if (!book) return res.status(404).send('Книга не найдена');

    book.title = req.body.title;
    book.author = req.body.author;
    book.year = req.body.year;
    res.json(book);
});

// Удаление книги по ID
app.delete('/books/:id', (req, res) => {
    books = books.filter(b => b.id !== parseInt(req.params.id));
    res.status(204).send();
});

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});


//{
  //  "title": "Название книги",
  //  "author": "Автор книги",
  //  "year": 2024
//}