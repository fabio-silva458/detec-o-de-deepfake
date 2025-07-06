const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="flex flex-col items-center space-y-4">
        <div className="spinner"></div>
        <p className="text-gray-500 text-sm">Carregando...</p>
      </div>
    </div>
  )
}

export default LoadingSpinner 