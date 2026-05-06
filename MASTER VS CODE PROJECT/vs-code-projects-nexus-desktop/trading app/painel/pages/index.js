import { useState } from 'react';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchType, setSearchType] = useState('offers'); // 'offers' ou 'demands'
  const [error, setError] = useState('');

  const search = async () => {
    if (!query.trim()) {
      setError('Digite um termo para buscar');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const endpoint = searchType === 'offers' ? '/api/search' : '/api/search-demands';
      const res = await fetch(`${endpoint}?q=${encodeURIComponent(query)}`);
      
      if (!res.ok) {
        throw new Error('Erro ao buscar resultados');
      }
      
      const data = await res.json();
      setResults(data);
      
      if (data.length === 0) {
        setError(`Nenhuma ${searchType === 'offers' ? 'oferta' : 'demanda'} encontrada para "${query}"`);
      }
    } catch (err) {
      setError('Erro ao conectar com o servidor. Verifique a URL da API.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      search();
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleString('pt-BR');
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>🏪 Intermediário de Vendas</h1>
        <p>Busque ofertas e demandas de produtos compartilhados no WhatsApp</p>
      </header>

      <main className={styles.main}>
        <div className={styles.searchBox}>
          <div className={styles.searchControls}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Digite o produto que procura..."
              className={styles.input}
            />
            <button onClick={search} disabled={loading} className={styles.button}>
              {loading ? '🔍 Buscando...' : '🔍 Buscar'}
            </button>
          </div>

          <div className={styles.filterButtons}>
            <button
              className={`${styles.filterBtn} ${searchType === 'offers' ? styles.active : ''}`}
              onClick={() => {
                setSearchType('offers');
                setResults([]);
                setError('');
              }}
            >
              📤 Ofertas
            </button>
            <button
              className={`${styles.filterBtn} ${searchType === 'demands' ? styles.active : ''}`}
              onClick={() => {
                setSearchType('demands');
                setResults([]);
                setError('');
              }}
            >
              📥 Demandas
            </button>
          </div>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.results}>
          {results.map((item, i) => (
            <div key={i} className={styles.resultItem}>
              <div className={styles.resultHeader}>
                <span className={styles.resultNumber}>#{i + 1}</span>
                <span className={styles.groupName}>📍 {item.groupName}</span>
                <span className={styles.date}>{formatDate(item.timestamp)}</span>
              </div>
              <div className={styles.resultContent}>
                <p>{item.content}</p>
              </div>
            </div>
          ))}
        </div>

        {results.length > 0 && (
          <div className={styles.info}>
            ✅ {results.length} resultado{results.length > 1 ? 's' : ''} encontrado{results.length > 1 ? 's' : ''}
          </div>
        )}
      </main>

      <footer className={styles.footer}>
        <p>💡 Dica: Use comandos no WhatsApp para buscar: <code>!buscar [produto]</code></p>
      </footer>
    </div>
  );
}
