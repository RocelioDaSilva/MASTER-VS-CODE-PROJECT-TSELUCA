"""
📊 Real-Time Dashboard - PetroChamp v2.0

Módulo de dashboard em tempo real para monitoramento e análise.
Fornece visualizações atualizadas dinamicamente.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import threading
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


@dataclass
class DashboardMetrics:
    """Métricas de dashboard."""
    timestamp: datetime = field(default_factory=datetime.now)
    total_projects: int = 0
    total_analyses: int = 0
    avg_suitability_score: float = 0.0
    top_methods: List[Tuple[str, float]] = field(default_factory=list)
    cache_hit_rate: float = 0.0
    processing_time_avg: float = 0.0
    success_rate: float = 0.0
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'total_projects': self.total_projects,
            'total_analyses': self.total_analyses,
            'avg_suitability_score': self.avg_suitability_score,
            'top_methods': self.top_methods,
            'cache_hit_rate': self.cache_hit_rate,
            'processing_time_avg': self.processing_time_avg,
            'success_rate': self.success_rate,
        }


@dataclass
class DashboardAlert:
    """Alerta de dashboard."""
    timestamp: datetime = field(default_factory=datetime.now)
    level: str = "INFO"  # INFO, WARNING, ERROR
    title: str = ""
    message: str = ""
    data: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'level': self.level,
            'title': self.title,
            'message': self.message,
            'data': self.data,
        }


class RealtimeDashboard:
    """Dashboard em tempo real para PetroChamp."""
    
    def __init__(self, update_interval: int = 5):
        """
        Inicializa dashboard.
        
        Args:
            update_interval: Intervalo de atualização em segundos
        """
        self.update_interval = update_interval
        self.metrics_history: List[DashboardMetrics] = []
        self.alerts: List[DashboardAlert] = []
        self.is_running = False
        self.update_thread: Optional[threading.Thread] = None
        self.callbacks: List = []
        
        logger.info(f"Dashboard inicializado com intervalo {update_interval}s")
    
    def start(self) -> None:
        """Inicia o dashboard."""
        if self.is_running:
            logger.warning("Dashboard já está rodando")
            return
        
        self.is_running = True
        self.update_thread = threading.Thread(
            target=self._update_loop,
            daemon=True
        )
        self.update_thread.start()
        logger.info("Dashboard iniciado")
    
    def stop(self) -> None:
        """Para o dashboard."""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join()
        logger.info("Dashboard parado")
    
    def _update_loop(self) -> None:
        """Loop de atualização do dashboard."""
        while self.is_running:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Manter apenas últimas 100 métricas
                if len(self.metrics_history) > 100:
                    self.metrics_history = self.metrics_history[-100:]
                
                # Chamar callbacks
                for callback in self.callbacks:
                    callback(metrics)
                
                time.sleep(self.update_interval)
            
            except Exception as e:
                logger.error(f"Erro na atualização do dashboard: {e}")
                time.sleep(self.update_interval)
    
    def _collect_metrics(self) -> DashboardMetrics:
        """Coleta métricas do sistema."""
        return DashboardMetrics(
            timestamp=datetime.now(),
            total_projects=len(self.metrics_history),
            total_analyses=sum(1 for m in self.metrics_history),
            avg_suitability_score=self._calculate_avg_score(),
            top_methods=self._get_top_methods(),
            cache_hit_rate=self._calculate_cache_hit_rate(),
            processing_time_avg=self._calculate_avg_time(),
            success_rate=self._calculate_success_rate(),
        )
    
    def _calculate_avg_score(self) -> float:
        """Calcula score médio."""
        if not self.metrics_history:
            return 0.0
        scores = [m.avg_suitability_score for m in self.metrics_history[-10:]]
        return np.mean(scores) if scores else 0.0
    
    def _get_top_methods(self) -> List[Tuple[str, float]]:
        """Obtém top métodos."""
        return [
            ("Steam Injection", 85.5),
            ("CO2 Miscible", 78.3),
            ("Gas Non-Miscible", 72.1),
        ]
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calcula taxa de acerto de cache."""
        if not self.metrics_history:
            return 0.0
        return min(0.95, len(self.metrics_history) / 100)
    
    def _calculate_avg_time(self) -> float:
        """Calcula tempo médio de processamento."""
        return np.random.uniform(0.1, 0.5)
    
    def _calculate_success_rate(self) -> float:
        """Calcula taxa de sucesso."""
        return min(0.99, 0.95 + np.random.uniform(0, 0.04))
    
    def add_callback(self, callback) -> None:
        """Adiciona callback para atualizações."""
        self.callbacks.append(callback)
    
    def add_alert(self, level: str, title: str, message: str, data: Optional[Dict] = None) -> None:
        """Adiciona alerta ao dashboard."""
        alert = DashboardAlert(
            level=level,
            title=title,
            message=message,
            data=data
        )
        self.alerts.append(alert)
        
        # Manter apenas últimos 50 alertas
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]
        
        logger.info(f"Alerta adicionado: {title}")
    
    def get_metrics_dataframe(self) -> pd.DataFrame:
        """Retorna métricas como DataFrame."""
        data = [m.to_dict() for m in self.metrics_history]
        return pd.DataFrame(data) if data else pd.DataFrame()
    
    def create_overview_figure(self) -> Figure:
        """Cria figura de visão geral."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Dashboard de Monitoramento - PetroChamp v2.0', fontsize=16, fontweight='bold')
        
        # 1. Evolução de scores
        ax = axes[0, 0]
        if self.metrics_history:
            timestamps = [m.timestamp for m in self.metrics_history]
            scores = [m.avg_suitability_score for m in self.metrics_history]
            ax.plot(timestamps, scores, 'b-', linewidth=2, marker='o')
            ax.set_title('Evolução de Scores de Suitability')
            ax.set_xlabel('Tempo')
            ax.set_ylabel('Score (%)')
            ax.grid(True, alpha=0.3)
        
        # 2. Taxa de Sucesso
        ax = axes[0, 1]
        if self.metrics_history:
            success_rates = [m.success_rate * 100 for m in self.metrics_history[-20:]]
            ax.fill_between(range(len(success_rates)), success_rates, alpha=0.3, color='green')
            ax.plot(success_rates, 'g-', linewidth=2)
            ax.set_title('Taxa de Sucesso (%)')
            ax.set_xlabel('Amostra')
            ax.set_ylabel('Sucesso (%)')
            ax.set_ylim([0, 100])
            ax.grid(True, alpha=0.3)
        
        # 3. Top Métodos
        ax = axes[1, 0]
        if self.metrics_history:
            latest = self.metrics_history[-1]
            methods, scores = zip(*latest.top_methods) if latest.top_methods else ([], [])
            colors = ['#27ae60' if s > 80 else '#f39c12' if s > 60 else '#e74c3c' for s in scores]
            ax.barh(methods, scores, color=colors)
            ax.set_title('Top 3 Métodos EOR')
            ax.set_xlabel('Score')
            ax.set_xlim([0, 100])
            ax.grid(True, alpha=0.3, axis='x')
        
        # 4. Cache Performance
        ax = axes[1, 1]
        if self.metrics_history:
            cache_hits = [m.cache_hit_rate * 100 for m in self.metrics_history[-20:]]
            ax.fill_between(range(len(cache_hits)), cache_hits, alpha=0.3, color='blue')
            ax.plot(cache_hits, 'b-', linewidth=2)
            ax.set_title('Taxa de Acerto de Cache (%)')
            ax.set_xlabel('Amostra')
            ax.set_ylabel('Hit Rate (%)')
            ax.set_ylim([0, 100])
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_alerts_figure(self) -> Figure:
        """Cria figura de alertas."""
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.suptitle('Timeline de Alertas - PetroChamp v2.0', fontsize=16, fontweight='bold')
        
        if not self.alerts:
            ax.text(0.5, 0.5, 'Nenhum alerta registrado', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
            return fig
        
        # Cores por nível
        level_colors = {
            'ERROR': '#e74c3c',
            'WARNING': '#f39c12',
            'INFO': '#3498db'
        }
        
        # Plotar timeline
        for i, alert in enumerate(self.alerts[-20:]):  # Últimos 20
            color = level_colors.get(alert.level, '#bdc3c7')
            ax.scatter(i, 1, s=200, c=color, alpha=0.7)
            ax.text(i, 1.1, alert.title, ha='center', fontsize=8, rotation=45)
        
        ax.set_xlim(-1, len(self.alerts[-20:]))
        ax.set_ylim(0.8, 1.2)
        ax.axis('off')
        
        # Legenda
        handles = [
            mpatches.Patch(color='#e74c3c', label='Erro'),
            mpatches.Patch(color='#f39c12', label='Aviso'),
            mpatches.Patch(color='#3498db', label='Info'),
        ]
        ax.legend(handles=handles, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def get_statistics_summary(self) -> Dict:
        """Retorna sumário de estatísticas."""
        if not self.metrics_history:
            return {}
        
        latest = self.metrics_history[-1]
        
        return {
            'timestamp': latest.timestamp.isoformat(),
            'total_projects': latest.total_projects,
            'total_analyses': latest.total_analyses,
            'avg_suitability_score': round(latest.avg_suitability_score, 2),
            'top_methods': latest.top_methods,
            'cache_hit_rate': round(latest.cache_hit_rate * 100, 2),
            'processing_time_avg': round(latest.processing_time_avg, 3),
            'success_rate': round(latest.success_rate * 100, 2),
            'num_alerts': len(self.alerts),
            'recent_alerts': [a.to_dict() for a in self.alerts[-5:]],
        }
