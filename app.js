import express from 'express';
import { json } from 'body-parser';

const app = express();
app.use(json());

let books = [
    { id: 1, title: 'Книга 1', author: 'Автор 1' },
    { id: 2, title: 'Книга 2', author: 'Автор 2' }
];

// Получить все книги (GET)
app.get('/books', (req, res) => {
    res.json(books);
});

// Создать новую книгу (POST)
app.post('/books', (req, res) => {
    const newBook = req.body;
    newBook.id = books.length + 1;
    books.push(newBook);
    res.status(201).json(newBook);
});

// Обновить книгу (PUT)
app.put('/books/:id', (req, res) => {
    const bookId = parseInt(req.params.id);
    const book = books.find(b => b.id === bookId);
    if (!book) {
        return res.status(404).json({ error: 'Книга не найдена' });
    }
    Object.assign(book, req.body);
    res.json(book);
});

// Удалить книгу (DELETE)
app.delete('/books/:id', (req, res) => {
    const bookId = parseInt(req.params.id);
    books = books.filter(b => b.id !== bookId);
    res.json({ result: 'Книга уда��ена' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Сервер запущен на порту ${PORT}`);
});


//{
   // "title": "Новая книга",
   // "author": "Новый автор "
//}
