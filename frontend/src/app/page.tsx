export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Dashboard Educativo
        </h1>
        <p className="text-gray-600 mb-8">
          Frontend Context-Aware funcionando correctamente
        </p>
        <div className="space-y-4">
          <div className="flex items-center justify-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
            <span className="text-gray-700">Next.js 13.5.6 funcionando</span>
          </div>
          <div className="flex items-center justify-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
            <span className="text-gray-700">TypeScript 5.1.6 configurado</span>
          </div>
          <div className="flex items-center justify-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
            <span className="text-gray-700">Tailwind CSS 3.3.3 activo</span>
          </div>
          <div className="flex items-center justify-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
            <span className="text-gray-700">React Query v4 integrado</span>
          </div>
        </div>
        <div className="mt-8 space-x-4">
          <a 
            href="/login" 
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Ir a Login
          </a>
          <a 
            href="/dashboard" 
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Ir a Dashboard
          </a>
        </div>
      </div>
    </div>
  );
}