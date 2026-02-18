export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Обо мне</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
        <h2 className="text-xl font-semibold mb-3 text-gray-600">Навыки</h2>
        <ul className="list-disc pl-5 space-y-1">
          {/* TODO: Добавьте минимум 5 своих навыков */}
          <li className="text-base font-semibold mb-3 text-gray-500">HTML/CSS</li>
          <li className="text-base font-semibold mb-3 text-gray-500">JavaScript</li>
          <li className="text-base font-semibold mb-3 text-gray-500">Git</li>
          <li className="text-base font-semibold mb-3 text-gray-500">React</li>
          <li className="text-base font-semibold mb-3 text-gray-500">Next.js</li>
        </ul>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-3 text-gray-600">Опыт работы</h2>
        <div className="space-y-4">
          {/* TODO: Добавьте минимум 2 пункта опыта работы */}
          <p className="text-base font-semibold mb-3 text-gray-500">Microsoft</p>
          <p className="text-base font-semibold mb-3 text-gray-500">Apple</p>
          <p className="text-base font-semibold mb-3 text-gray-500">Android</p>
        </div>
      </div>
    </div>
  )
}
