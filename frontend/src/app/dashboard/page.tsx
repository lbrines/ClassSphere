export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Dashboard Educativo
              </h1>
              <p className="text-gray-600 mb-8">
                Bienvenido al Dashboard Context-Aware
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Cursos
                  </h3>
                  <p className="text-gray-600">Gestiona tus cursos</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Estudiantes
                  </h3>
                  <p className="text-gray-600">Administra estudiantes</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Métricas
                  </h3>
                  <p className="text-gray-600">Visualiza estadísticas</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}