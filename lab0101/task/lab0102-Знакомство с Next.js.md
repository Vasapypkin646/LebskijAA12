# **Лабораторная работа 1. Часть 2: Знакомство с Next.js**

## **Тема:** Создание многостраничного веб-приложения с серверным рендерингом

### **Цель работы:**
Практическое знакомство с Next.js — мета-фреймворком для React. Освоение концепций серверного рендеринга (SSG), файловой маршрутизации и деплоя.

---

## **Задание: Сайт-портфолио с блогом**

Разработайте простое многостраничное приложение на Next.js с использованием TypeScript.

### **1. Настройка проекта**

Откройте терминал в Ubuntu и выполните:

```bash
# Создание проекта Next.js с TypeScript
npx create-next-app@latest portfolio-site --typescript --tailwind --app
cd portfolio-site

# Установка зависимостей (если create-next-app не установил автоматически)
npm install

# Установка дополнительных зависимостей
npm install date-fns
```

Проверьте структуру проекта:

```bash
tree -L 2
```

Должна быть следующая структура:
```
portfolio-site/
├── app/
│   ├── layout.tsx
│   └── page.tsx
├── public/
├── package.json
└── tailwind.config.js
```

### **2. Базовое приложение**

**Файл: `app/layout.tsx`** (уже создан, проверьте содержимое):

```tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Мое портфолио',
  description: 'Сайт-портфолио разработчика',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <header className="bg-gray-800 text-white p-4">
          <nav className="container mx-auto">
            <ul className="flex gap-6">
              <li><a href="/" className="hover:text-blue-300">Главная</a></li>
              <li><a href="/about" className="hover:text-blue-300">Обо мне</a></li>
              <li><a href="/blog" className="hover:text-blue-300">Блог</a></li>
              <li><a href="/projects" className="hover:text-blue-300">Проекты</a></li>
            </ul>
          </nav>
        </header>
        <main className="container mx-auto p-4">
          {children}
        </main>
        <footer className="bg-gray-800 text-white p-4 text-center">
          <p>© Мое портфолио. Все права защищены.</p>
        </footer>
      </body>
    </html>
  )
}
```

**Файл: `app/page.tsx`** (главная страница):

```tsx
export default function HomePage() {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold mb-4">Добро пожаловать в мое портфолио</h1>
      <p className="text-lg text-gray-600 mb-8">
        Я веб-разработчик, специализирующийся на современных технологиях
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Next.js</h2>
          <p className="text-gray-600">Серверный рендеринг и статическая генерация</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">React</h2>
          <p className="text-gray-600">Компонентный подход и хуки</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">TypeScript</h2>
          <p className="text-gray-600">Статическая типизация для надежности</p>
        </div>
      </div>
    </div>
  )
}
```

### **3. Задания для самостоятельного выполнения**

#### **A. Создайте страницу "Обо мне"** (обязательно)

Создайте файл: `app/about/page.tsx`

```tsx
export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Обо мне</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
        <h2 className="text-xl font-semibold mb-3">Навыки</h2>
        <ul className="list-disc pl-5 space-y-1">
          {/* TODO: Добавьте минимум 5 своих навыков */}
        </ul>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-3">Опыт работы</h2>
        <div className="space-y-4">
          {/* TODO: Добавьте минимум 2 пункта опыта работы */}
        </div>
      </div>
    </div>
  )
}
```

#### **B. Создайте страницу "Блог" со статической генерацией** (обязательно)

Сначала создайте тип для статей и массив данных:

**Файл: `app/blog/data.ts`**

```typescript
export interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  content: string
  date: string
  author: string
}

export const blogPosts: BlogPost[] = [
  {
    id: 1,
    title: 'Введение в Next.js',
    slug: 'introduction-to-nextjs',
    excerpt: 'Основы Next.js и преимущества серверного рендеринга',
    content: 'Полный текст статьи о Next.js...',
    date: '2026-01-15',
    author: 'Иван Иванов'
  },
  // TODO: Добавьте еще минимум 2 статьи самостоятельно
]
```

**Файл: `app/blog/page.tsx`**

```tsx
import Link from 'next/link'
import { blogPosts } from './data'

export default function BlogPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Блог</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {blogPosts.map((post) => (
          <div key={post.id} className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-2">
              <Link 
                href={`/blog/${post.slug}`}
                className="hover:text-blue-600"
              >
                {post.title}
              </Link>
            </h2>
            <p className="text-gray-600 mb-3">{post.excerpt}</p>
            <div className="flex justify-between text-sm text-gray-500">
              <span>{post.date}</span>
              <span>{post.author}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

#### **C. Создайте динамические страницы статей блога** (обязательно)

Создайте структуру для динамических маршрутов:

**Файл: `app/blog/[slug]/page.tsx`**

```tsx
import { notFound } from 'next/navigation'
import { blogPosts } from '../data'

// Функция для генерации статических путей
export async function generateStaticParams() {
  return blogPosts.map((post) => ({
    slug: post.slug,
  }))
}

export default function BlogPostPage({
  params,
}: {
  params: { slug: string }
}) {
  // TODO: Найдите статью по slug из параметров
  // Если статья не найдена, вызовите notFound()
  
  const post = blogPosts.find(p => p.slug === params.slug)
  
  if (!post) {
    notFound()
  }

  return (
    <article className="max-w-3xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{post.title}</h1>
        <div className="flex justify-between text-gray-600">
          <span>{post.date}</span>
          <span>Автор: {post.author}</span>
        </div>
      </header>
      
      <div className="prose max-w-none">
        <p className="text-lg mb-4">{post.excerpt}</p>
        {/* TODO: Добавьте отображение полного содержания статьи */}
      </div>
      
      <div className="mt-8 pt-4 border-t">
        <Link 
          href="/blog"
          className="text-blue-600 hover:text-blue-800"
        >
          ← Вернуться к списку статей
        </Link>
      </div>
    </article>
  )
}
```

**Файл: `app/blog/[slug]/not-found.tsx`** (опционально, для обработки 404):

```tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold mb-4">Статья не найдена</h1>
      <p className="text-gray-600 mb-8">Запрошенная статья не существует или была удалена</p>
      <Link 
        href="/blog"
        className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
      >
        Вернуться к блогу
      </Link>
    </div>
  )
}
```

#### **D. Создайте страницу "Проекты" с использованием компонентов** (дополнительно)

Создайте компонент карточки проекта:

**Файл: `app/components/ProjectCard.tsx`**

```tsx
interface ProjectCardProps {
  title: string
  description: string
  technologies: string[]
  link?: string
}

export default function ProjectCard({ 
  title, 
  description, 
  technologies,
  link 
}: ProjectCardProps) {
  return (
    <div className="border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>
      <div className="mb-4">
        <span className="text-sm font-medium">Технологии: </span>
        {/* TODO: Отобразите технологии в виде тегов */}
      </div>
      {link && (
        <a 
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block text-blue-600 hover:text-blue-800"
        >
          Посмотреть проект →
        </a>
      )}
    </div>
  )
}
```

**Файл: `app/projects/page.tsx`**

```tsx
import ProjectCard from '../components/ProjectCard'

// TODO: Создайте массив с данными о проектах
const projects = [
  {
    title: 'Интернет-магазин',
    description: 'Полнофункциональный интернет-магазин с корзиной и оплатой',
    technologies: ['Next.js', 'TypeScript', 'Stripe'],
    link: 'https://example.com'
  },
  // TODO: Добавьте еще минимум 2 проекта
]

export default function ProjectsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Мои проекты</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* TODO: Используйте компонент ProjectCard для отображения проектов */}
      </div>
    </div>
  )
}
```

### **4. Сборка и деплой**

#### **A. Локальная сборка и проверка**

```bash
# Запуск в режиме разработки
npm run dev

# Проверка доступных страниц:
# http://localhost:3000 - Главная
# http://localhost:3000/about - Обо мне
# http://localhost:3000/blog - Блог
# http://localhost:3000/blog/introduction-to-nextjs - Статья
# http://localhost:3000/projects - Проекты

# Сборка проекта
npm run build

# Проверка собранного проекта
npm run start
```

#### **B. Деплой на Vercel** (дополнительно)

1. Создайте аккаунт на [vercel.com](https://vercel.com) (можно через GitHub)
2. Установите Vercel CLI:
```bash
npm install -g vercel
```

3. Залогиньтесь и запустите деплой:
```bash
vercel login
vercel
```

4. Следуйте инструкциям в терминале
5. После деплоя получите ссылку на ваше приложение

### **5. Что должно быть в отчёте:**

1. **Исходный код:**
   - Все созданные файлы с вашими дополнениями
   - Особое внимание на динамические маршруты и типы TypeScript

2. **Скриншоты:**
   - Все созданные страницы (главная, о себе, блог, статьи, проекты)
   - Консоль с результатом сборки (`npm run build`)
   - Страница 404 для несуществующей статьи

3. **Ответы на вопросы:**
   - Что такое SSG (Static Site Generation) и как он реализован в вашем проекте?
   - Как работает файловая маршрутизация в Next.js?
   - Какие преимущества даёт использование `generateStaticParams`?
   - В чём разница между `npm run dev` и `npm run build`?

4. **Ссылка на деплой** (если делали):
   - URL работающего приложения на Vercel

### **6. Критерии оценивания:**

#### **Обязательные требования (минимум для зачета):**
- **Страница "Обо мне":** Создана, содержит информацию о навыках и опыте
- **Страница "Блог":** Отображает список статей, использует данные из массива
- **Динамические страницы статей:** Реализован динамический маршрут `[slug]`
- **Навигация:** Все страницы доступны через меню навигации
- **Проект собирается без ошибок:** `npm run build` выполняется успешно

#### **Дополнительные критерии (для повышения оценки):**
- **Страница "Проекты":** Реализована с использованием компонента ProjectCard
- **Качество TypeScript кода:** Правильно типизированы пропсы, состояния, параметры
- **Обработка ошибок:** Реализована страница 404 для несуществующих статей
- **Деплой:** Приложение развернуто на Vercel и доступно по ссылке
- **Дополнительный функционал:** Любые улучшения сверх требований

#### **Неприемлемые ошибки:**
- Ошибки TypeScript при сборке
- Неработающие ссылки между страницами
- Отсутствие обязательных страниц
- Критические ошибки в работе приложения

### **7. Полезные команды для Ubuntu:**

```bash
# Проверка версий
node --version
npm --version

# Очистка кэша Next.js (если проблемы со сборкой)
rm -rf .next
npm run dev

# Проверка структуры проекта
find . -name "*.tsx" -o -name "*.ts" | sort
```

### **8. Структура готового проекта:**

```
portfolio-site/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── about/
│   │   └── page.tsx
│   ├── blog/
│   │   ├── page.tsx
│   │   ├── data.ts
│   │   └── [slug]/
│   │       ├── page.tsx
│   │       └── not-found.tsx
│   ├── projects/
│   │   └── page.tsx
│   └── components/
│       └── ProjectCard.tsx
├── public/
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

### **9. Советы по выполнению:**

1. **Начинайте с простого:** Сначала создайте базовые страницы, затем добавляйте сложности
2. **Проверяйте типы:** TypeScript поможет избежать многих ошибок
3. **Используйте автодополнение:** VS Code отлично работает с Next.js и TypeScript
4. **Тестируйте навигацию:** Переходите по всем ссылкам, проверяйте корректность
5. **Читайте ошибки:** Next.js дает подробные сообщения об ошибках

**Примечание:** В задании предоставлено ~70% кода. Ваша задача — понять архитектуру Next.js и дописать недостающие части, следуя принципам реактивности и типобезопасности.
