import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, FlatList, ActivityIndicator, Alert, ScrollView } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';
import moment from 'moment';
import 'moment/locale/pt-br';

moment.locale('pt-br');

// 🌐 URLs da API (escolha uma)
const API_URLS = [
  'https://SEU_PAINEL.vercel.app/api',  // ← USE ESTA para qualquer lugar (online)
  'http://localhost:3000/api',           // Emulador local
  'http://10.0.2.2:3000/api',            // Emulador Android
  'http://192.168.1.100:3000/api',       // IP local (mude o IP)
];

const API_BASE_URL = API_URLS[0]; // Mude o índice: 0=online, 1-3=local

export default function App() {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('offers'); // 'offers' ou 'demands'
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [favorites, setFavorites] = useState([]);
  const [showFavorites, setShowFavorites] = useState(false);
  const [history, setHistory] = useState([]);

  const search = async () => {
    if (!query.trim()) {
      Alert.alert('Aviso', 'Digite algo para buscar');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const endpoint = searchType === 'offers' ? '/search' : '/search-demands';
      const response = await axios.get(`${API_BASE_URL}${endpoint}`, {
        params: { q: query },
        timeout: 10000
      });

      if (response.data && response.data.length > 0) {
        setResults(response.data);
        // Adicionar ao histórico
        setHistory(prev => {
          const newHistory = [{ query, type: searchType, time: new Date() }, ...prev];
          return newHistory.slice(0, 20); // Guardar últimas 20 buscas
        });
      } else {
        setError('Nenhum resultado encontrado');
      }
    } catch (err) {
      console.error('Erro:', err);
      if (err.message === 'Network Error' || err.code === 'ECONNABORTED') {
        setError('❌ Sem conexão ao servidor.\n\nVerifique:\n• URL da API está correta?\n• Servidor está online?');
      } else {
        setError(`❌ Erro: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleFavorite = (item) => {
    const isFavorited = favorites.some(fav => fav.text === item.text);
    if (isFavorited) {
      setFavorites(favorites.filter(fav => fav.text !== item.text));
    } else {
      setFavorites([...favorites, item]);
    }
  };

  const isFavorited = (item) => {
    return favorites.some(fav => fav.text === item.text);
  };

  const handleKeyPress = (e) => {
    if (e.nativeEvent.key === 'Enter') {
      search();
    }
  };

  const formatDate = (dateString) => {
    try {
      return moment(dateString).format('DD/MM HH:mm');
    } catch {
      return 'Data inválida';
    }
  };

  const ResultItem = ({ item }) => (
    <View style={styles.resultItem}>
      <View style={styles.resultItemHeader}>
        <Text style={styles.resultText}>{item.text}</Text>
        <TouchableOpacity 
          onPress={() => toggleFavorite(item)}
          style={styles.favoriteBtn}
        >
          <Text style={styles.favoriteBtnText}>
            {isFavorited(item) ? '❤️' : '🤍'}
          </Text>
        </TouchableOpacity>
      </View>
      <View style={styles.resultMeta}>
        <Text style={styles.resultGroup}>{item.group}</Text>
        <Text style={styles.resultDate}>{formatDate(item.timestamp)}</Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🔍 Buscador Pessoal</Text>
        <Text style={styles.headerSubtitle}>Suas ofertas, em qualquer lugar</Text>
      </View>

      {/* Search Box */}
      <View style={styles.searchBox}>
        <TextInput
          style={styles.input}
          placeholder="Buscar ofertas ou demandas..."
          placeholderTextColor="#999"
          value={query}
          onChangeText={setQuery}
          onKeyPress={handleKeyPress}
          editable={!loading}
        />
        <TouchableOpacity
          style={[styles.searchButton, loading && styles.searchButtonDisabled]}
          onPress={search}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" size="small" />
          ) : (
            <Text style={styles.searchButtonText}>🔍</Text>
          )}
        </TouchableOpacity>
      </View>

      {/* Filter Buttons */}
      <View style={styles.filterContainer}>
        <TouchableOpacity
          style={[styles.filterBtn, searchType === 'offers' && styles.filterBtnActive]}
          onPress={() => setSearchType('offers')}
        >
          <Text style={[styles.filterBtnText, searchType === 'offers' && styles.filterBtnTextActive]}>
            💰 Ofertas
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.filterBtn, searchType === 'demands' && styles.filterBtnActive]}
          onPress={() => setSearchType('demands')}
        >
          <Text style={[styles.filterBtnText, searchType === 'demands' && styles.filterBtnTextActive]}>
            📦 Demandas
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.filterBtn, showFavorites && styles.filterBtnActive]}
          onPress={() => setShowFavorites(!showFavorites)}
        >
          <Text style={[styles.filterBtnText, showFavorites && styles.filterBtnTextActive]}>
            ❤️ ({favorites.length})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Error Message */}
      {error ? (
        <View style={styles.errorBox}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      ) : null}

      {/* Results */}
      {showFavorites ? (
        <>
          {favorites.length > 0 && (
            <View style={styles.resultsHeader}>
              <Text style={styles.resultsCount}>❤️ {favorites.length} favorito{favorites.length !== 1 ? 's' : ''}</Text>
            </View>
          )}
          <FlatList
            data={favorites}
            renderItem={ResultItem}
            keyExtractor={(item, index) => `fav-${index}`}
            style={styles.resultsList}
            contentContainerStyle={styles.resultsContainer}
            ListEmptyComponent={
              <View style={styles.emptyState}>
                <Text style={styles.emptyStateText}>Nenhum favorito ainda</Text>
                <Text style={styles.emptyStateSubtext}>Toque no ❤️ dos resultados para salvar</Text>
              </View>
            }
          />
        </>
      ) : (
        <>
          {results.length > 0 && (
            <View style={styles.resultsHeader}>
              <Text style={styles.resultsCount}>📊 {results.length} resultado{results.length !== 1 ? 's' : ''}</Text>
            </View>
          )}
          <FlatList
            data={results}
            renderItem={ResultItem}
            keyExtractor={(item, index) => index.toString()}
            style={styles.resultsList}
            contentContainerStyle={styles.resultsContainer}
            ListEmptyComponent={
              !loading && results.length === 0 && !error ? (
                <View style={styles.emptyState}>
                  <Text style={styles.emptyStateText}>👋 Bem-vindo!</Text>
                  <Text style={styles.emptyStateSubtext}>Busque por produtos ou preços</Text>
                  {history.length > 0 && (
                    <View style={styles.historyContainer}>
                      <Text style={styles.historyTitle}>📜 Últimas buscas:</Text>
                      {history.slice(0, 5).map((h, i) => (
                        <TouchableOpacity 
                          key={i} 
                          onPress={() => {
                            setQuery(h.query);
                            setSearchType(h.type);
                          }}
                          style={styles.historyItem}
                        >
                          <Text style={styles.historyText}>• {h.query}</Text>
                        </TouchableOpacity>
                      ))}
                    </View>
                  )}
                </View>
              ) : null
            }
          />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    paddingTop: 40,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    marginTop: 4,
  },
  searchBox: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    gap: 10,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    color: '#333',
  },
  searchButton: {
    backgroundColor: '#667eea',
    borderRadius: 8,
    paddingHorizontal: 15,
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchButtonDisabled: {
    opacity: 0.6,
  },
  searchButtonText: {
    fontSize: 18,
  },
  filterContainer: {
    flexDirection: 'row',
    paddingHorizontal: 15,
    paddingVertical: 10,
    gap: 10,
    backgroundColor: '#fff',
  },
  filterBtn: {
    flex: 1,
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
    alignItems: 'center',
  },
  filterBtnActive: {
    backgroundColor: '#667eea',
    borderColor: '#667eea',
  },
  filterBtnText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
  filterBtnTextActive: {
    color: '#fff',
  },
  errorBox: {
    marginHorizontal: 15,
    marginTop: 10,
    padding: 12,
    backgroundColor: '#ffe6e6',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#ff6b6b',
  },
  errorText: {
    color: '#cc0000',
    fontSize: 13,
    lineHeight: 18,
  },
  resultsHeader: {
    paddingHorizontal: 15,
    paddingTop: 15,
    paddingBottom: 5,
  },
  resultsCount: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
  resultsList: {
    flex: 1,
  },
  resultsContainer: {
    paddingHorizontal: 15,
    paddingBottom: 20,
  },
  resultItem: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 12,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#667eea',
    elevation: 2,
  },
  resultItemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  resultText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
    flex: 1,
  },
  favoriteBtn: {
    marginLeft: 10,
    paddingHorizontal: 5,
  },
  favoriteBtnText: {
    fontSize: 18,
  },
  resultMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  resultGroup: {
    fontSize: 11,
    color: '#999',
    fontWeight: '600',
  },
  resultDate: {
    fontSize: 11,
    color: '#999',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyStateText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  emptyStateSubtext: {
    fontSize: 13,
    color: '#999',
    textAlign: 'center',
    paddingHorizontal: 30,
  },
  historyContainer: {
    marginTop: 30,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    padding: 12,
    width: '80%',
  },
  historyTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 10,
  },
  historyItem: {
    paddingVertical: 6,
    paddingHorizontal: 8,
  },
  historyText: {
    fontSize: 12,
    color: '#667eea',
  },
};
