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
  {
    id: 2,
    title: 'Введение в Django',
    slug: 'introduction-to-django',
    excerpt: 'Основы Python и преимущества Django',
    content: 'Полный текст статьи о Django...',
    date: '2026-02-13',
    author: 'Вася Пупкин'
  },
  {
    id: 3,
    title: 'Введение в Flask',
    slug: 'introduction-to-flask',
    excerpt: 'Основы Python и преимущества Flask',
    content: 'Полный текст статьи о Flask...',
    date: '2026-02-13',
    author: 'Вася Пупкин'
  }
  
]
