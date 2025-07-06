import { Link } from 'react-router-dom'
import { Shield, Search, BarChart3, Zap, Users, Award } from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: Search,
      title: 'Detecção Avançada',
      description: 'Analise imagens e vídeos com tecnologia de machine learning de ponta'
    },
    {
      icon: Zap,
      title: 'Processamento Rápido',
      description: 'Resultados em segundos com nossa arquitetura otimizada'
    },
    {
      icon: Shield,
      title: 'Segurança Garantida',
      description: 'Seus arquivos são processados localmente com total privacidade'
    },
    {
      icon: BarChart3,
      title: 'Análise Detalhada',
      description: 'Relatórios completos com métricas e visualizações'
    }
  ]

  const stats = [
    { label: 'Análises Realizadas', value: '10,000+' },
    { label: 'Taxa de Precisão', value: '95%' },
    { label: 'Usuários Ativos', value: '1,000+' },
    { label: 'Tempo Médio', value: '< 5s' }
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center mb-8">
            <Shield className="h-20 w-20 text-primary-600" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Sistema de Detecção de{' '}
            <span className="text-primary-600">Deepfake</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Tecnologia avançada de machine learning para identificar deepfakes em imagens e vídeos. 
            Proteja-se da desinformação digital com precisão e velocidade.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/detection"
              className="btn btn-primary px-8 py-3 text-lg"
            >
              Começar Análise
            </Link>
            <Link
              to="/about"
              className="btn btn-secondary px-8 py-3 text-lg"
            >
              Saiba Mais
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">
                {stat.value}
              </div>
              <div className="text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Por que escolher nosso sistema?
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Nossa plataforma oferece a mais avançada tecnologia de detecção de deepfake, 
            combinando precisão, velocidade e facilidade de uso.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div key={index} className="card text-center">
                <div className="flex justify-center mb-4">
                  <Icon className="h-12 w-12 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            )
          })}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 rounded-lg p-8 text-center text-white">
        <h2 className="text-3xl font-bold mb-4">
          Pronto para começar?
        </h2>
        <p className="text-primary-100 mb-8 max-w-2xl mx-auto">
          Faça upload de uma imagem ou vídeo e descubra se é um deepfake em segundos. 
          Nossa tecnologia está pronta para proteger você da desinformação.
        </p>
        <Link
          to="/detection"
          className="btn bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 text-lg"
        >
          Analisar Agora
        </Link>
      </section>

      {/* How it works */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Como funciona?
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Nosso processo é simples e eficiente, garantindo resultados precisos em tempo recorde.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">1</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Upload do Arquivo
            </h3>
            <p className="text-gray-600">
              Faça upload de uma imagem ou vídeo que deseja analisar
            </p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">2</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Análise Automática
            </h3>
            <p className="text-gray-600">
              Nosso algoritmo analisa o arquivo usando IA avançada
            </p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">3</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Resultado Detalhado
            </h3>
            <p className="text-gray-600">
              Receba um relatório completo com a probabilidade de ser deepfake
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home 