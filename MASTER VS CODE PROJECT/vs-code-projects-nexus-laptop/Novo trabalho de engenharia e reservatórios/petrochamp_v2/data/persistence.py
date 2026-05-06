"""
Sistema de cache e gerenciamento de projetos
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import OrderedDict
import pickle

from ..core.models import EORProject, ProjectStatistics

logger = logging.getLogger(__name__)


class ResultsCache:
    """Cache inteligente para resultados computacionais"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Inicializa cache
        
        Args:
            max_size: Tamanho máximo do cache
            ttl_seconds: Tempo de vida em segundos
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, base_key: str, args: tuple, kwargs: dict) -> str:
        """Gera chave única para cache"""
        args_str = json.dumps(args, default=str, sort_keys=True)
        kwargs_str = json.dumps(kwargs, default=str, sort_keys=True)
        combined = f"{base_key}:{args_str}:{kwargs_str}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, key: str, compute_func: Optional[Callable] = None, 
            *args, **kwargs) -> Any:
        """
        Obtém resultado do cache ou computa novo
        
        Args:
            key: Chave base para cache
            compute_func: Função para computar se não em cache
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
        
        Returns:
            Resultado do cache ou computado
        """
        cache_key = self._generate_key(key, args, kwargs)
        
        # Verificar se existe no cache e se ainda é válido
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            age = datetime.now() - cached['timestamp']
            
            if age.total_seconds() < self.ttl_seconds:
                self.hits += 1
                logger.debug(f"Cache hit para {key}")
                return cached['value']
            else:
                # Expirou
                del self.cache[cache_key]
                logger.debug(f"Cache expirado para {key}")
        
        # Não estava em cache
        self.misses += 1
        
        if compute_func is None:
            return None
        
        try:
            result = compute_func(*args, **kwargs)
            self._add_to_cache(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Erro ao computar resultado: {e}")
            return None
    
    def _add_to_cache(self, key: str, value: Any) -> None:
        """Adiciona valor ao cache"""
        # Evictar se necessário
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now()
        }
    
    def _evict_oldest(self) -> None:
        """Remove entrada mais antiga"""
        if self.cache:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            logger.debug(f"Cache evictado: {oldest_key}")
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache limpo")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache),
            'max_size': self.max_size,
            'usage_percent': len(self.cache) / self.max_size * 100
        }


class ProjectManager:
    """Gerenciador de projetos com persistência"""
    
    def __init__(self, storage_path: str = "./projects"):
        """
        Inicializa gerenciador
        
        Args:
            storage_path: Caminho para armazenar projetos
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.projects: Dict[str, EORProject] = {}
        self.current_project: Optional[EORProject] = None
        self.history: List[str] = []  # IDs de projetos
        
        self._load_project_index()
    
    def create_project(self, name: str, description: str = "") -> EORProject:
        """Cria novo projeto"""
        project = EORProject(name=name, description=description)
        self.projects[project.id] = project
        self.history.append(project.id)
        
        logger.info(f"Projeto criado: {name} ({project.id})")
        return project
    
    def open_project(self, project_id: str) -> Optional[EORProject]:
        """Abre projeto existente"""
        # Primeiro verificar em memória
        if project_id in self.projects:
            self.current_project = self.projects[project_id]
            logger.info(f"Projeto aberto: {self.current_project.name}")
            return self.current_project
        
        # Tentar carregar do arquivo
        project = self._load_project_from_file(project_id)
        if project:
            self.projects[project_id] = project
            self.current_project = project
            return project
        
        logger.warning(f"Projeto não encontrado: {project_id}")
        return None
    
    def save_project(self, project: Optional[EORProject] = None, 
                    auto_backup: bool = True) -> bool:
        """Salva projeto"""
        target = project or self.current_project
        if not target:
            logger.warning("Nenhum projeto para salvar")
            return False
        
        target.modified_at = datetime.now()
        
        # Salvar no armazenamento
        filepath = self.storage_path / f"{target.id}.json"
        success = target.save_to_file(str(filepath))
        
        if success and auto_backup:
            self._create_backup(target.id)
        
        return success
    
    def delete_project(self, project_id: str) -> bool:
        """Deleta projeto"""
        try:
            # Remover de memória
            if project_id in self.projects:
                del self.projects[project_id]
            
            # Remover arquivo
            filepath = self.storage_path / f"{project_id}.json"
            if filepath.exists():
                filepath.unlink()
            
            # Remover histórico
            if project_id in self.history:
                self.history.remove(project_id)
            
            logger.info(f"Projeto deletado: {project_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar projeto: {e}")
            return False
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """Lista todos os projetos"""
        projects_info = []
        
        for project in self.projects.values():
            projects_info.append({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at.isoformat(),
                'modified_at': project.modified_at.isoformat(),
                'is_current': project.id == (self.current_project.id if self.current_project else None)
            })
        
        return sorted(projects_info, key=lambda x: x['modified_at'], reverse=True)
    
    def get_statistics(self) -> ProjectStatistics:
        """Calcula estatísticas dos projetos"""
        stats = ProjectStatistics()
        stats.total_projects = len(self.projects)
        
        best_scores = []
        all_methods = []
        all_npv = []
        all_irr = []
        
        for project in self.projects.values():
            if project.screening_results:
                stats.projects_with_results += 1
                best = project.get_best_method()
                if best:
                    best_scores.append(best.suitability_score)
                    all_methods.extend([r.method_name for r in project.screening_results])
            
            for econ in project.economic_analyses:
                all_npv.append(econ.npv)
                all_irr.append(econ.irr)
        
        # Calcular médias
        if best_scores:
            stats.avg_best_score = sum(best_scores) / len(best_scores)
        
        if all_methods:
            # Método mais recomendado
            from collections import Counter
            method_counts = Counter(all_methods)
            stats.most_recommended_method = method_counts.most_common(1)[0][0] if method_counts else ""
        
        if all_npv:
            stats.avg_npv = sum(all_npv) / len(all_npv)
        
        if all_irr:
            stats.avg_irr = sum(all_irr) / len(all_irr)
        
        return stats
    
    def export_project(self, project_id: str, output_path: str, 
                      include_results: bool = True) -> bool:
        """Exporta projeto em múltiplos formatos"""
        project = self.projects.get(project_id) or self._load_project_from_file(project_id)
        
        if not project:
            logger.error(f"Projeto não encontrado: {project_id}")
            return False
        
        try:
            output_file = Path(output_path)
            
            # Determinar formato pela extensão
            if output_path.endswith('.json'):
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(project.to_dict(include_results), f, indent=2, default=str)
            
            elif output_path.endswith('.pkl'):
                with open(output_path, 'wb') as f:
                    pickle.dump(project, f)
            
            else:
                logger.error("Formato não suportado. Use .json ou .pkl")
                return False
            
            logger.info(f"Projeto exportado: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao exportar projeto: {e}")
            return False
    
    def import_project(self, input_path: str) -> Optional[EORProject]:
        """Importa projeto de arquivo"""
        try:
            if input_path.endswith('.json'):
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                project = EORProject.from_dict(data)
            
            elif input_path.endswith('.pkl'):
                with open(input_path, 'rb') as f:
                    project = pickle.load(f)
            
            else:
                logger.error("Formato não suportado")
                return None
            
            # Adicionar ao gerenciador
            self.projects[project.id] = project
            self.history.append(project.id)
            
            logger.info(f"Projeto importado: {project.name}")
            return project
        
        except Exception as e:
            logger.error(f"Erro ao importar projeto: {e}")
            return None
    
    def _load_project_from_file(self, project_id: str) -> Optional[EORProject]:
        """Carrega projeto de arquivo"""
        filepath = self.storage_path / f"{project_id}.json"
        if filepath.exists():
            return EORProject.load_from_file(str(filepath))
        return None
    
    def _load_project_index(self) -> None:
        """Carrega índice de projetos"""
        # Procurar arquivos JSON no storage
        for filepath in self.storage_path.glob("*.json"):
            try:
                project = EORProject.load_from_file(str(filepath))
                if project:
                    self.projects[project.id] = project
                    if project.id not in self.history:
                        self.history.append(project.id)
            except Exception as e:
                logger.warning(f"Erro ao carregar projeto {filepath}: {e}")
    
    def _create_backup(self, project_id: str) -> bool:
        """Cria backup de projeto"""
        try:
            project = self.projects.get(project_id)
            if not project:
                return False
            
            backup_dir = self.storage_path / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"{project_id}_backup_{timestamp}.json"
            
            project.save_to_file(str(backup_path))
            logger.info(f"Backup criado: {backup_path}")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return False
    
    def restore_from_backup(self, project_id: str, backup_timestamp: str) -> Optional[EORProject]:
        """Restaura projeto de backup"""
        try:
            backup_path = self.storage_path / "backups" / f"{project_id}_backup_{backup_timestamp}.json"
            
            if not backup_path.exists():
                logger.error(f"Backup não encontrado: {backup_path}")
                return None
            
            project = EORProject.load_from_file(str(backup_path))
            self.projects[project_id] = project
            self.current_project = project
            
            logger.info(f"Projeto restaurado de backup: {project.name}")
            return project
        
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {e}")
            return None
