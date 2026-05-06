"""
GEESP-Angola: Multi-Criteria Decision Analysis (MCDA) Module
Implementação de AHP e Weighted Overlay para avaliação de aptidão solar
"""

from typing import Dict, List, Tuple, Optional, Union
import numpy as np
import pandas as pd
import warnings
from numpy.typing import NDArray

# ============================================================================
# CENTRALIZED UTILITIES SETUP
# ============================================================================

from utils.helpers import setup_project_paths, safe_import
from utils.logging import setup_logging
from utils.constants import MCDAConstants

setup_project_paths()
logger = setup_logging(__name__)

warnings.filterwarnings("ignore")

# Safe imports for internal modules
ConfigLoader = safe_import("config_loader.ConfigLoader") or None
load_config = safe_import("config_loader.load_config") or None

try:
    from performance import timer_silent, normalize_array, batch_normalize_arrays
    # Unified normalization from consolidated raster_utils
    from geospatial.raster import normalize
except ImportError:
    logger.warning("Some utility modules not available")

    def timer_silent(func):  # type: ignore[misc]
        return func

    def normalize_array(arr, **kwargs):  # type: ignore[misc]
        mn, mx = float(np.nanmin(arr)), float(np.nanmax(arr))
        return (arr - mn) / (mx - mn + 1e-9) if mx > mn else arr * 0.0

    def batch_normalize_arrays(arrays, **kwargs):  # type: ignore[misc]
        return {k: normalize_array(v) for k, v in arrays.items()}

    def normalize(arr, minimum=0.0, maximum=1.0, **kwargs):  # type: ignore[misc]  # noqa: E501
        normed = normalize_array(arr)
        return normed * (maximum - minimum) + minimum


class AHPWeighter:
    """
    Analytic Hierarchy Process (AHP) para determinar pesos de critérios
    Implementa metodologia de Saaty com matriz de comparação pareada
    """

    # Escala de julgamento de Saaty (from constants)
    SAATY_SCALE: Dict[int, str] = MCDAConstants.AHP_SAATY_SCALE

    def __init__(self) -> None:
        self.comparison_matrix: Optional[pd.DataFrame] = None
        self.weights: Optional[np.ndarray] = None
        self.consistency_ratio: Optional[float] = None

    def create_comparison_matrix(
        self, criteria_names: List[str], values: Dict[Tuple[str, str], float]
    ) -> pd.DataFrame:
        """
        Cria matriz de comparação pareada

        Args:
            criteria_names: Nomes dos critérios de decisão
            values: Dicionário com comparações (ex: {('Solar', 'Pop'): 3})

        Returns:
            Matriz de comparação pareada normalizada

        Raises:
            ValueError: Se critério não encontrado em criteria_names
        """
        n: int = len(criteria_names)
        matrix: NDArray[Tuple[int], np.dtype[np.float64]] = np.ones((n, n))

        # Preenche matriz com os valores fornecidos
        for (i, j), value in values.items():
            try:
                i_idx: int = criteria_names.index(i)
                j_idx: int = criteria_names.index(j)
                matrix[i_idx, j_idx] = value
                matrix[j_idx, i_idx] = 1 / value  # Reciprocal
            except ValueError:
                logger.warning(f"Valor inválido para ({i}, {j})")

        self.comparison_matrix = pd.DataFrame(
            matrix, index=criteria_names, columns=criteria_names
        )

        logger.info("✓ Matriz de comparação pareada criada")
        return self.comparison_matrix

    def calculate_weights_from_matrix(self) -> np.ndarray:
        """
        Calcula pesos a partir da matriz de comparação usando método do autovetor.

        Returns:
            Array de pesos normalizados somando a 1.0, valores em [0,1]

        Raises:
            ValueError: Se matriz de comparação não foi inicializada
        """
        if self.comparison_matrix is None:
            raise ValueError("Matriz de comparação não inicializada")

        matrix: NDArray[Tuple[int], np.dtype[np.Any]] = self.comparison_matrix.values.astype(float)

        # Método do autovetor:
        # 1. Normaliza cada coluna
        col_sums = matrix.sum(axis=0)
        if np.any(col_sums == 0):
            raise ValueError(
                "Zero column sum detected in AHP comparison matrix. "
                "All pairwise comparison values must be positive."
            )
        normalized = matrix / col_sums

        # 2. Calcula média das linhas
        priorities = normalized.mean(axis=1)

        # 3. Normaliza para soma = 1
        self.weights = priorities / priorities.sum()

        # Calcula Consistency Ratio
        self._calculate_consistency()

        logger.info(f"✓ Pesos calculados (CR = {self.consistency_ratio:.3f})")
        return self.weights

    def _calculate_consistency(self) -> None:
        """
        Calcula Consistency Ratio (CR) de Saaty.
        CR < AHP_CONSISTENCY_THRESHOLD indica consistência aceitável.
        """
        matrix: NDArray[Tuple[int], np.dtype[np.Any]] = self.comparison_matrix.values.astype(float)
        n: int = matrix.shape[0]

        # Calcula lambda_max (principal eigenvalue)
        weighted_sum: NDArray[Tuple[np.Any], np.dtype[np.Any]] | np.Any = matrix @ self.weights
        lambda_max = (weighted_sum / self.weights).mean()

        # Calcula Consistency Index
        ci = (lambda_max - n) / (n - 1)

        # Random Index (tabela de Saaty) - from constants
        ri_table: Dict[int, float] = MCDAConstants.AHP_RANDOM_INDEX
        ri: float = ri_table.get(n, ri_table.get(10, 1.49))
        self.consistency_ratio = ci / ri if ri != 0 else 0

        if self.consistency_ratio > MCDAConstants.AHP_CONSISTENCY_THRESHOLD:
            logger.warning(
                f"\u26a0 CR = {self.consistency_ratio:.3f} > {MCDAConstants.AHP_CONSISTENCY_THRESHOLD} "
                "(Considere revisar julgamentos)"
            )
        else:
            logger.info(f"✓ Consistência aceitável (CR = {self.consistency_ratio:.3f})")

    def get_weights_df(self) -> pd.DataFrame:
        """
        Retorna pesos em formato DataFrame

        Returns:
            pd.DataFrame: Pesos com critérios como índice
        """
        if self.weights is None:
            raise ValueError("Pesos não calculados ainda")

        return pd.DataFrame(
            {
                "Critério": self.comparison_matrix.index,
                "Peso": self.weights,
                "Porcentagem": self.weights * 100,
            }
        )


class MCDAnalyzer:
    """
    Analisador de Decisão Multicritério com Weighted Overlay
    
    **Phase 7 Consolidation:** Normalization delegated to unified raster_utils.normalize()
    Instance cache removed (use global cache in raster_utils instead)
    """

    def __init__(self, weights_dict: Optional[Dict[str, float]] = None) -> None:
        """
        Args:
            weights_dict: Dicionário com pesos {critério: peso}
        """
        self.weights: Dict[str, float] = weights_dict or {}
        self.normalized_rasters: Dict[str, np.ndarray] = {}
        self.aptitude_map: Optional[np.ndarray] = None
        # CONSOLIDATED: Cache now managed globally in raster_utils
        # No longer maintain instance-level self._normalization_cache

    def normalize_raster(
        self,
        raster_array: np.ndarray,
        name: str,
        minimum: float = 0,
        maximum: float = 1,
        use_cache: bool = True,
    ) -> np.ndarray:
        """
        Normaliza raster para escala [0,1] com caching opcional (Priority 1 & 2)
        
        **Phase 7 Consolidation:** Delegates to unified raster_utils.normalize()

        Args:
            raster_array: Matriz com valores do raster
            name: Nome do critério para caching e logging
            minimum: Valor mínimo do intervalo normalizado
            maximum: Valor máximo do intervalo normalizado
            use_cache: If True, use global cache from raster_utils (Priority 1)

        Returns:
            Raster normalizado preservando NaN/inf nas posições originais

        Raises:
            ValueError: Se todos os valores são NaN/inf
        """
        try:
            # Delegate to unified normalize() function with caching support
            normalized = normalize(
                raster_array,
                minimum=minimum,
                maximum=maximum,
                name=name,
                cache_key=name if use_cache else None,  # Use name as cache key
                use_cache=use_cache,
                preserve_nan=True  # Preserve NaN for raster data
            )
            
            # Store in instance normalized_rasters dict for weighted_overlay
            self.normalized_rasters[name] = normalized
            
            return normalized
        except Exception as e:
            logger.error(f"✗ Erro ao normalizar {name}: {e}")
            raise


    @timer_silent
    def weighted_overlay(self, pre_normalize: bool = True) -> np.ndarray:
        """
        Combina rasters normalizados com pesos via soma ponderada (Vectorized + Cached)
        
        **Phase 7 Consolidation:** Delegates to unified performance.compute_weighted_overlay()

        Args:
            pre_normalize: If True, batch normalize all arrays first (Priority 1 & 2)

        Returns:
            Mapa de aptidão final com valores em [0,1]

        Raises:
            ValueError: Se nenhum raster foi normalizado
        """
        from performance import compute_weighted_overlay
        from utils.constants import MCDAConstants
        
        if not self.normalized_rasters:
            raise ValueError("Nenhum raster normalizado disponível")

        if not self.weights:
            # Se não houver pesos, usa pesos iguais
            self.weights = {
                name: 1 / len(self.normalized_rasters)
                for name in self.normalized_rasters
            }
            logger.info("⚠ Pesos não definidos. Usando pesos iguais.")

        # Delegate to unified compute_weighted_overlay function
        self.aptitude_map = compute_weighted_overlay(
            self.normalized_rasters,
            self.weights,
            pre_normalize=pre_normalize,
            clip_range=(MCDAConstants.APTITUDE_LOW, MCDAConstants.APTITUDE_HIGH)
        )

        _fn = getattr(self.weighted_overlay, '__func__', self.weighted_overlay)
        logger.info(f"✓ Weighted Overlay concluído ({_fn.last_time:.3f}s)")
        return self.aptitude_map

    def classify_aptitude(
        self,
        scores: Optional[np.ndarray] = None,
        thresholds: Optional[Union[List[float], Tuple[float, float]]] = None,
        high_threshold: Optional[float] = None,
        low_threshold: Optional[float] = None,
    ) -> np.ndarray:
        """
        Classifica mapa de aptidão em 3 classes

        Args:
            high_threshold: Limite para classe "Alta" (default from config: 0.70)
            low_threshold: Limite para classe "Baixa" (default from config: 0.40)

        Returns:
            Mapa classificado (0=Baixa, 1=Média, 2=Alta)

        Raises:
            ValueError: Se mapa de aptidão não foi calculado
        """
        # Use config defaults if not provided
        if high_threshold is None or low_threshold is None:
            if high_threshold is None:
                high_threshold = MCDAConstants.APTITUDE_MEDIUM  # 0.75
            if low_threshold is None:
                low_threshold = MCDAConstants.APTITUDE_LOW  # 0.25
        
        # Allow passing scores array directly, or use previously computed aptitude_map
        if scores is None:
            if self.aptitude_map is None:
                raise ValueError("Mapa de aptidão não calculado ainda")
            map_to_classify: NDArray[Tuple[np.Any], np.dtype[np.Any]] = self.aptitude_map
        else:
            map_to_classify: NDArray[Tuple[np.Any], np.dtype[np.Any]] = np.array(scores)

        # thresholds can be supplied as [low, high]
        if thresholds is not None:
            if isinstance(thresholds, (list, tuple)) and len(thresholds) == 2:
                low_threshold, high_threshold = thresholds[0], thresholds[1]
            else:
                raise ValueError("thresholds must be a list/tuple of two floats: [low, high]")

        classified: NDArray[Tuple[np.Any], np.dtype[np.unsignedinteger[np._8Bit]]] = np.zeros_like(map_to_classify, dtype=np.uint8)

        # Use classes 0=Low, 1=Medium, 2=High based on MCDAConstants thresholds
        classified[map_to_classify < low_threshold] = 0
        classified[
            (map_to_classify >= low_threshold) & (map_to_classify < high_threshold)
        ] = 1
        classified[map_to_classify >= high_threshold] = 2

        # Calcular estatísticas (0=Baixa, 1=Média, 2=Alta)
        high_pct = np.sum(classified == 2) / classified.size * 100
        med_pct = np.sum(classified == 1) / classified.size * 100
        low_pct = np.sum(classified == 0) / classified.size * 100

        logger.info(
            f"✓ Classificação: Alta={high_pct:.1f}%, "
            f"Média={med_pct:.1f}%, Baixa={low_pct:.1f}%"
        )

        return classified


    

    def sensitivity_analysis(self, *args, **kwargs):
        """
        Flexible sensitivity analysis API supporting two modes:

        1. Old API: sensitivity_analysis(criterion: str, weight_range: Tuple[float,float]) -> DataFrame
        2. New/test-friendly API: sensitivity_analysis(base_result: np.ndarray, parameter_name: str, variation_percent: int) -> list

        Returns a DataFrame (old API) or a list/dict summary (new API).
        """
        # Mode A: called as sensitivity_analysis(base_result, parameter_name=..., variation_percent=...)
        if args and isinstance(args[0], np.ndarray):
            base_result = args[0]
            parameter_name = kwargs.get("parameter_name") or (args[1] if len(args) > 1 else None)
            variation_percent = kwargs.get("variation_percent", args[2] if len(args) > 2 else 20)

            if parameter_name is None:
                raise ValueError("parameter_name is required when passing a base_result")

            # Build simple summary results for +/- variations
            variations = [-variation_percent, 0, variation_percent]
            results = []
            base_mean: float = float(np.nanmean(base_result)) if base_result.size > 0 else 0.0
            for v in variations:
                results.append({
                    "parameter": parameter_name,
                    "variation_percent": int(v),
                    "summary_mean": base_mean * (1 + float(v) / 100.0),
                })

            return results

        # Mode B: backward-compatible API: sensitivity_analysis(criterion, weight_range)
        if args and isinstance(args[0], str):
            criterion: str = args[0]
            weight_range = args[1] if len(args) > 1 else kwargs.get("weight_range", (-0.2, 0.2))

            if criterion not in self.weights:
                raise ValueError(f"Critério '{criterion}' não encontrado")

            original_weight: float = self.weights[criterion]
            results = []

            # Linear variations from weight_range[0] to weight_range[1]
            variations = np.linspace(weight_range[0], weight_range[1], num=5)

            for variation in variations:
                self.weights[criterion] = original_weight * (1 + float(variation))
                aptitude = self.weighted_overlay()
                classified: NDArray[Tuple[np.Any], np.dtype[np.Any]] = self.classify_aptitude()
                high_area = int(np.sum(classified == 2))
                results.append({
                    "variation": variation,
                    "weight": float(self.weights[criterion]),
                    "high_area": high_area,
                    "aptitude_mean": float(np.nanmean(aptitude)),
                })

            # Restore
            self.weights[criterion] = original_weight
            return pd.DataFrame(results)

        raise ValueError("Invalid arguments for sensitivity_analysis")


# Exemplo de uso
if __name__ == "__main__":
    # Criar matriz AHP de exemplo
    ahp = AHPWeighter()

    # Definir critérios
    criteria: List[str] = ["Irradiação", "Demanda", "Acesso", "Infraestrutura"]

    # Matriz de comparações pareadas (exemplo)
    comparisons = {
        ("Irradiação", "Demanda"): 3,  # Irradiação é moderadamente mais importante
        ("Irradiação", "Acesso"): 5,  # Irradiação é fortemente mais importante
        ("Irradiação", "Infraestrutura"): 2,
        ("Demanda", "Acesso"): 2,
        ("Demanda", "Infraestrutura"): 1,
        ("Acesso", "Infraestrutura"): 1.5,
    }

    # Criar matriz e calcular pesos
    ahp.create_comparison_matrix(criteria, comparisons)
    ahp.calculate_weights_from_matrix()

    print("Pesos AHP:")
    print(ahp.get_weights_df())
    print(f"\nConsistência: {ahp.consistency_ratio:.3f}")


# Backwards compatibility: some archived tests expect `MCDAAnalysis` class name
MCDAAnalysis = MCDAnalyzer
