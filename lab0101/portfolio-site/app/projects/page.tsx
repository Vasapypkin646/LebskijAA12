import ProjectCard from '../components/ProjectCard'

// TODO: Создайте массив с данными о проектах
interface Project {
  title: string;
  description: string;
  technologies: string[];
  link: string;
};

const projects: Project[] = [
  {
    title: 'Интернет-магазин',
    description: 'Полнофункциональный интернет-магазин с корзиной и оплатой',
    technologies: ['Next.js', 'TypeScript', 'Stripe'],
    link: 'https://example.com'
  },
  // TODO: Добавьте еще минимум 2 проекта
  {
    title: 'Игровой-интернет-магазин',
    description: 'Полнофункциональный игровой-интернет-магазин с корзиной и оплатой',
    technologies: ['Next.js', 'TypeScript', 'Stripe'],
    link: 'https://example2.com'
  },
  {
    title: 'Корпоративный сайт',
    description: 'Корпоративный сайт фитнес-клуба с расписанием занятий и онлайн-записью',
    technologies: ['Next.js', 'TypeScript', 'Tailwind CSS', 'Prisma', 'PostgreSQL'],
    link: 'https://example3.com'
  }
]

export default function ProjectsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Мои проекты</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* TODO: Используйте компонент ProjectCard для отображения проектов */}
        {projects.map((projects, index) => (
          <ProjectCard
            key = {index}
            title = {projects.title}
            description = {projects.description}
            technologies = {projects.technologies}
            link = {projects.link}
            
          />
        ))
        }
        
      </div>
    </div>
  )
}