"""
GEESP-Angola: Map Generation Module
Gera mapas raster realistas para demonstração e análise MCDA
"""

import numpy as np
from pathlib import Path
from typing import Any, Dict
from ..geospatial import operations as map_utils
from utils.constants import MapGenerationConstants
from utils.logging import setup_logging

# Optional heavy dependencies (rasterio, scipy)
try:
    import rasterio
    from rasterio.transform import from_origin

    HAS_RASTERIO = True
except ImportError:
    rasterio = None
    from_origin = None
    HAS_RASTERIO = False

plt: Any = None
mpatches: Any = None
LinearSegmentedColormap: Any = None
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.colors import LinearSegmentedColormap
except ImportError:
    plt = None
    mpatches = None
    LinearSegmentedColormap = None

try:
    from scipy.ndimage import gaussian_filter, distance_transform_edt

    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

    def gaussian_filter(arr: "np.ndarray", sigma: float) -> "np.ndarray":
        """Pure-numpy separable 2-D Gaussian blur (scipy fallback)."""
        if sigma <= 0:
            return arr
        radius = max(1, int(3 * sigma + 0.5))
        x = np.arange(-radius, radius + 1, dtype=np.float64)
        kernel = np.exp(-0.5 * (x / sigma) ** 2)
        kernel /= kernel.sum()

        def _convolve1d(row):
            return np.convolve(row, kernel, mode="same")

        result = np.apply_along_axis(_convolve1d, 0, arr.astype(np.float64))
        result = np.apply_along_axis(_convolve1d, 1, result)
        return result.astype(arr.dtype)

    def distance_transform_edt(mask):
        # Fallback: tiled Euclidean distance to avoid O(H*W * N_pts) memory explosion.
        # Processes the grid in tiles of at most TILE x TILE pixels so that the
        # temporary (n_pixels_tile, n_true_pixels) array stays within ~50 MB.
        pts = np.array(np.where(mask)).T  # shape (N, 2)
        if pts.size == 0:
            return np.full(mask.shape, float(mask.shape[0] + mask.shape[1]))
        result = np.empty(mask.shape, dtype=np.float32)
        TILE = 256
        H, W = mask.shape
        y_idx, x_idx = np.indices((H, W))
        coords_all = np.stack([y_idx.ravel(), x_idx.ravel()], axis=1)  # (H*W, 2)
        n = H * W
        for start in range(0, n, TILE * TILE):
            end = min(start + TILE * TILE, n)
            chunk = coords_all[start:end]  # (chunk_size, 2)
            dists = np.sqrt(((chunk[:, None, :] - pts[None, :, :]) ** 2).sum(axis=2))
            result.ravel()[start:end] = dists.min(axis=1)
        return result

logger = setup_logging(__name__)

if not HAS_SCIPY:
    logger.warning("scipy not installed — map generation will use tiled fallbacks (reduced quality)")


class MapGenerator:
    """Gera mapas raster para análise MCDA da Huíla"""

    def __init__(self, width: int = None, height: int = None, crs: str = None) -> None:
        """Initialize map generator.
        
        Args:
            width: Width in pixels (default from MapGenerationConstants)
            height: Height in pixels (default from MapGenerationConstants)
            crs: Coordinate reference system (default from MapGenerationConstants)
        """
        if width is None:
            width = MapGenerationConstants.MAP_WIDTH_PIXELS
        if height is None:
            height = MapGenerationConstants.MAP_HEIGHT_PIXELS
        if crs is None:
            crs = MapGenerationConstants.MAP_CRS
        
        self.width = width
        self.height = height
        self.crs = crs

        # Bounds para Huíla (UTM 33S, aproximado)
        # Convertido de graus para metros UTM
        self.west = MapGenerationConstants.MAP_WEST_UTM
        self.south = MapGenerationConstants.MAP_SOUTH_UTM
        self.east = MapGenerationConstants.MAP_EAST_UTM
        self.north = MapGenerationConstants.MAP_NORTH_UTM

        self.pixel_size_x = (self.east - self.west) / width
        self.pixel_size_y = (self.north - self.south) / height

        # Criar transform para georreferenciamento
        # Only build a real geo-transform when rasterio is available
        if HAS_RASTERIO and from_origin is not None:
            self.transform = from_origin(
                self.west, self.north, self.pixel_size_x, self.pixel_size_y
            )
        else:
            self.transform = None  # GeoTIFF export disabled without rasterio
            logger.warning("rasterio not available — GeoTIFF export disabled")

        logger.info(f"✓ MapGenerator inicializado: {width}x{height} pixels")

    def generate_solar_radiation(self) -> np.ndarray:
        """Generate realistic solar irradiance map.
        
        Returns:
            Solar irradiance array in kWh/m²/day
        """
        logger.info("Gerando mapa de Irradiação Solar...")

        # Cria gradiente base (norte-sul)
        y_gradient = np.linspace(
            MapGenerationConstants.SOLAR_MAX,
            MapGenerationConstants.SOLAR_MIN,
            self.height
        )[:, np.newaxis]
        data = np.tile(y_gradient, (1, self.width))

        # Adiciona variação espacial
        x = np.linspace(0, 1, self.width)
        y = np.linspace(0, 1, self.height)
        X, Y = np.meshgrid(x, y)

        # Padrão sinusoidal
        noise = (
            MapGenerationConstants.SOLAR_NOISE_AMP
            * np.sin(X * MapGenerationConstants.SOLAR_SINE_MULT)
            * np.cos(Y * MapGenerationConstants.SOLAR_COSINE_MULT)
        )
        data += noise

        # Suavizar
        data = gaussian_filter(data, sigma=MapGenerationConstants.SOLAR_GAUSSIAN_SIGMA)

        # Normalizar ao intervalo definido
        data = np.clip(
            data,
            MapGenerationConstants.SOLAR_MIN,
            MapGenerationConstants.SOLAR_MAX
        )

        logger.info(
            f"  Min: {data.min():.2f}, Max: {data.max():.2f}, "
            f"Mean: {data.mean():.2f} kWh/m²/dia"
        )

        return data.astype(np.float32)

    def generate_population_density(self) -> np.ndarray:
        """Generate realistic population density map.
        
        Returns:
            Population density array (people/km²)
            
        Note:
            Gera mapa de densidade populacional (luzes noturnas simuladas).
            Padrão: Clusters em torno de centros urbanos.
            Unidade: Proxy de luzes noturnas (nanoWatts/cm²/sr).
            Intervalo: definido em MapGenerationConstants.
        """
        logger.info("Gerando mapa de Densidade Populacional...")

        # Inicializa
        data = np.zeros((self.height, self.width), dtype=np.float32)

        # Define centros urbanos (aproximado para 3 zonas)
        # Caçula (Zona A)
        cy_a = int(MapGenerationConstants.POP_CENTER_1_Y * self.height)
        cx_a = int(MapGenerationConstants.POP_CENTER_1_X * self.width)
        # Humpata (Zona B)
        cy_b = int(MapGenerationConstants.POP_CENTER_2_Y * self.height)
        cx_b = int(MapGenerationConstants.POP_CENTER_2_X * self.width)
        # Quilengues (Zona C)
        cy_c = int(MapGenerationConstants.POP_CENTER_3_Y * self.height)
        cx_c = int(MapGenerationConstants.POP_CENTER_3_X * self.width)

        centers = [
            (cy_a, cx_a, MapGenerationConstants.POP_INTENSITY_1),
            (cy_b, cx_b, MapGenerationConstants.POP_INTENSITY_2),
            (cy_c, cx_c, MapGenerationConstants.POP_INTENSITY_3),
        ]

        # Cria gaussianas para cada centro
        yy, xx = np.indices((self.height, self.width))
        for cy, cx, intensity in centers:
            # Gaussiana 2D
            gaussian = intensity * np.exp(
                -((xx - cx) ** 2 + (yy - cy) ** 2)
                / MapGenerationConstants.POP_GAUSSIAN_CENTER
            )
            data += gaussian

        # Adiciona ruído de fundo
        noise = np.random.poisson(
            MapGenerationConstants.POP_POISSON_LAMBDA, (self.height, self.width)
        ).astype(np.float32)
        data += noise

        # Suavizar
        data = gaussian_filter(data, sigma=MapGenerationConstants.POP_GAUSSIAN_SIGMA)

        # Normalizar ao intervalo [POP_MIN, POP_MAX]
        data_min, data_max = data.min(), data.max()
        if data_max > data_min:
            data = (
                (data - data_min) / (data_max - data_min)
                * MapGenerationConstants.POP_SCALE_RANGE
                + MapGenerationConstants.POP_MIN
            )
        else:
            data = np.full_like(data, MapGenerationConstants.POP_MIN, dtype=np.float32)
        logger.info(
            f"  Min: {data.min():.1f}, Max: {data.max():.1f}, "
            f"Mean: {data.mean():.1f} nW/cm²/sr"
        )

        return np.clip(
            data, MapGenerationConstants.POP_MIN, MapGenerationConstants.POP_MAX
        ).astype(np.float32)

    def generate_distance_to_grid(self) -> np.ndarray:
        """Generate distance to electrical grid map.
        
        Returns:
            Distance array in kilometers
            
        Note:
            Gera mapa de distância à rede elétrica existente.
            Padrão: Redes existentes ao longo de estradas principais.
            Unidade: km.
            Intervalo: definido em MapGenerationConstants.
        """
        logger.info("Gerando mapa de Distância à Rede...")

        # Cria "rede elétrica" como linhas retas
        grid_mask = np.zeros((self.height, self.width), dtype=bool)

        # Linha vertical (leste-oeste)
        grid_mask[int(MapGenerationConstants.DISTANCE_GRID_ROW_FRAC * self.height), :] = True

        # Linha horizontal (norte-sul)
        grid_mask[:, int(MapGenerationConstants.DISTANCE_GRID_COL_FRAC * self.width)] = True

        # Linhas diagonais
        for i in range(self.height):
            if MapGenerationConstants.DISTANCE_DIAGONAL_SLOPE * i < self.width:
                grid_mask[i, int(MapGenerationConstants.DISTANCE_DIAGONAL_SLOPE * i)] = True

        # Calcular distância euclidiana
        distance = distance_transform_edt(~grid_mask)

        # Converter pixels em km (pixel_size_x ~= 100m)
        distance_km = distance * (self.pixel_size_x / 1000)

        # Normalizar para intervalo definido
        data = np.clip(
            distance_km,
            MapGenerationConstants.DISTANCE_MIN,
            MapGenerationConstants.DISTANCE_MAX,
        ).astype(np.float32)

        logger.info(
            f"  Min: {data.min():.2f}, Max: {data.max():.2f}, "
            f"Mean: {data.mean():.2f} km"
        )

        return data

    def generate_slope(self) -> np.ndarray:
        """Generate terrain slope map.
        
        Returns:
            Slope array in degrees
            
        Note:
            Gera mapa de declividade (simulado).
            Unidade: graus.
            Intervalo: definido em MapGenerationConstants.
        """
        logger.info("Gerando mapa de Declividade...")

        # Cria um DEM sintético
        x = np.linspace(0, MapGenerationConstants.SLOPE_X_RANGE, self.width)
        y = np.linspace(0, MapGenerationConstants.SLOPE_Y_RANGE, self.height)
        X, Y = np.meshgrid(x, y)

        # Elevação sintética com trends e ruído
        noise = np.random.normal(
            0, MapGenerationConstants.SLOPE_NOISE_STD, (self.height, self.width)
        )
        noise = gaussian_filter(noise, sigma=4)

        elevation = (
            MapGenerationConstants.SLOPE_ELEVATION_BASE
            + MapGenerationConstants.SLOPE_SINE_AMP * np.sin(X)
            + MapGenerationConstants.SLOPE_COSINE_AMP * np.cos(Y)
            + 0.35 * noise
        )
        elevation = gaussian_filter(elevation, sigma=2)

        # Calcular declividade com espaçamento geográfico para evitar saturação artificial
        dz_dy, dz_dx = np.gradient(elevation, self.pixel_size_y, self.pixel_size_x)
        slope_rad = np.arctan(np.hypot(dz_dx, dz_dy))
        slope_deg = np.degrees(slope_rad)

        data = np.clip(
            slope_deg, MapGenerationConstants.SLOPE_MIN, MapGenerationConstants.SLOPE_MAX
        ).astype(np.float32)

        logger.info(
            f"  Min: {data.min():.2f}, Max: {data.max():.2f}, "
            f"Mean: {data.mean():.2f}°"
        )

        return data

    def generate_ndvi(self) -> np.ndarray:
        """Generate vegetation index map.
        
        Returns:
            NDVI array with values in range [-1.0, 1.0]
            
        Note:
            Gera mapa de NDVI (Índice de Vegetação).
            Unidade: Adimensional.
            Intervalo: definido em MapGenerationConstants.
        """
        logger.info("Gerando mapa de NDVI...")

        # Padrão base
        x = np.linspace(0, MapGenerationConstants.NDVI_X_RANGE, self.width)
        y = np.linspace(0, MapGenerationConstants.NDVI_Y_RANGE, self.height)
        X, Y = np.meshgrid(x, y)

        # NDVI mais alto ao norte (zona verde)
        data = 0.3 + 0.35 * (1 - Y) + 0.1 * np.sin(X * 4) * np.cos(Y * 3)

        # Suavizar
        data = gaussian_filter(data, sigma=2)

        # Clipes
        data = np.clip(data, -0.2, 0.7).astype(np.float32)

        logger.info(
            f"  Min: {data.min():.3f}, Max: {data.max():.3f}, "
            f"Mean: {data.mean():.3f}"
        )

        return data

    def generate_aptitude_map(self, solar: np.ndarray, population: np.ndarray, distance: np.ndarray, slope: np.ndarray, ndvi: np.ndarray) -> np.ndarray:
        """Generate MCDA aptitude map.
        
        Combine multiple criteria with weights:
        - Solar: 25%, Population: 25%, Distance: 20%, Slope: 15%, NDVI: 15%
        
        Args:
            solar: Solar irradiance array
            population: Population density array
            distance: Distance to grid array
            slope: Terrain slope array
            ndvi: Vegetation index array
            
        Returns:
            Aptitude map with values in [0, 1]
        """
        logger.info("Gerando mapa de Aptidão Integrada...")

        # Delegate to shared utility to ensure consistent normalization & weights
        aptitude = map_utils.compute_aptitude(
            solar, population, distance, slope, ndvi
        )

        logger.info(
            f"  Min: {aptitude.min():.3f}, Max: {aptitude.max():.3f}, "
            f"Mean: {aptitude.mean():.3f}"
        )

        return aptitude

    def save_geotiff(self, data: np.ndarray, filename: str, nodata: float = None) -> bool:
        """Save array as georeferenced GeoTIFF.
        
        Args:
            data: Raster data array
            filename: Output filename
            nodata: No data value for raster
            
        Returns:
            True if successful, False otherwise
        """
        if not HAS_RASTERIO or rasterio is None or self.transform is None:
            logger.warning(
                f"rasterio unavailable — skipping GeoTIFF export for {filename}"
            )
            return False

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Preparar perfil do raster
        if nodata is None:
            from utils.constants import GeoConstants
            nodata = GeoConstants.NODATA_VALUE

        profile = {
            "driver": "GTiff",
            "height": data.shape[0],
            "width": data.shape[1],
            "count": 1,
            "dtype": rasterio.float32,
            "crs": self.crs,
            "transform": self.transform,
            "nodata": nodata,
            "compress": "lzw",
        }

        # Salvar
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(data.astype(np.float32), 1)

        logger.info(f"✓ Salvo GeoTIFF: {output_path}")
        return True

    def create_visualization(
        self, data, title, cmap, output_path=None, vmin=None, vmax=None
    ):
        """Cria visualização PNG do mapa"""

        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)

        # Plotar raster
        im = ax.imshow(
            data, cmap=cmap, vmin=vmin, vmax=vmax, origin="upper", aspect="auto"
        )

        # Customizar
        ax.set_title(title, fontsize=16, fontweight="bold", pad=20)
        ax.set_xlabel("Longitude (UTM)", fontsize=12)
        ax.set_ylabel("Latitude (UTM)", fontsize=12)

        # Colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        # Grid
        ax.grid(True, alpha=0.3, linestyle="--")

        plt.tight_layout()

        # Salvar
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            logger.info(f"✓ Salvo PNG: {output_path}")

        plt.close()
        return fig


def generate_all_maps(output_dir: str = "data/processed") -> Dict[str, np.ndarray]:
    """Generate all map layers for GEESP-Angola.
    
    Gera todos os mapas principais (All standard map layers).
    
    Args:
        output_dir: Output directory for saved maps
        
    Returns:
        Dictionary mapping map names to numpy arrays with keys:
        'solar', 'population', 'distance', 'slope', 'ndvi', 'aptitude'
    """
    logger.info("=" * 80)
    logger.info("GEESP-Angola Map Generation Pipeline")
    logger.info("=" * 80)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Inicializar gerador
    gen = MapGenerator(width=300, height=280)

    # 1. IRRADIAÇÃO SOLAR
    logger.info("\n1️⃣ Irradiação Solar")
    solar = gen.generate_solar_radiation()
    gen.save_geotiff(solar, output_dir / "mapa_irradiacao.tif")
    gen.create_visualization(
        solar,
        "Irradiação Solar - Huíla, Angola",
        cmap="YlOrRd",
        output_path=output_dir / "mapa_irradiacao.png",
        vmin=5.5,
        vmax=6.4,
    )

    # 2. DENSIDADE POPULACIONAL (Luzes Noturnas)
    logger.info("\n2️⃣ Densidade Populacional")
    population = gen.generate_population_density()
    gen.save_geotiff(population, output_dir / "mapa_populacao.tif")
    gen.create_visualization(
        population,
        "Densidade Populacional (Luzes Noturnas) - Huíla",
        cmap="twilight_shifted",
        output_path=output_dir / "mapa_populacao.png",
        vmin=10,
        vmax=95,
    )

    # 3. DISTÂNCIA À REDE ELÉTRICA
    logger.info("\n3️⃣ Distância à Rede Elétrica")
    distance = gen.generate_distance_to_grid()
    gen.save_geotiff(distance, output_dir / "mapa_distanciarede.tif")
    gen.create_visualization(
        distance,
        "Distância à Rede Elétrica Existente",
        cmap="RdYlGn_r",
        output_path=output_dir / "mapa_distanciarede.png",
        vmin=0,
        vmax=45,
    )

    # 4. DECLIVIDADE
    logger.info("\n4️⃣ Declividade")
    slope = gen.generate_slope()
    gen.save_geotiff(slope, output_dir / "mapa_declividade.tif")
    gen.create_visualization(
        slope,
        "Declividade do Terreno",
        cmap="RdYlGn_r",
        output_path=output_dir / "mapa_declividade.png",
        vmin=0,
        vmax=30,
    )

    # 5. NDVI (Vegetação)
    logger.info("\n5️⃣ NDVI (Índice de Vegetação)")
    ndvi = gen.generate_ndvi()
    gen.save_geotiff(ndvi, output_dir / "mapa_ndvi.tif")
    gen.create_visualization(
        ndvi,
        "NDVI - Índice de Vegetação por Diferença Normalizada",
        cmap="RdYlGn",
        output_path=output_dir / "mapa_ndvi.png",
        vmin=-0.2,
        vmax=0.7,
    )

    # 6. APTIDÃO INTEGRADA (Resultado MCDA)
    logger.info("\n6️⃣ Mapa de Aptidão Integrada")
    aptitude = gen.generate_aptitude_map(solar, population, distance, slope, ndvi)
    gen.save_geotiff(aptitude, output_dir / "mapa_aptidao_integrada.tif")
    gen.create_visualization(
        aptitude,
        "Mapa de Aptidão Integrada para Sistemas Solares Comunitários",
        cmap="RdYlGn",
        output_path=output_dir / "mapa_aptidao_integrada.png",
        vmin=0,
        vmax=1,
    )

    logger.info("\n" + "=" * 80)
    logger.info("✅ Geração de mapas concluída!")
    logger.info(f"📁 Arquivos salvos em: {output_dir}")
    logger.info("=" * 80)

    return {
        "solar": solar,
        "population": population,
        "distance": distance,
        "slope": slope,
        "ndvi": ndvi,
        "aptitude": aptitude,
    }


if __name__ == "__main__":
    maps = generate_all_maps()

    # Estatísticas finais
    print("\n📊 RESUMO DOS MAPAS GERADOS:\n")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ Mapa                     │ Min    │ Max    │ Média      │")
    print("├─────────────────────────────────────────────────────────┤")
    print(
        f"│ Irradiação (kWh/m²/dia)  │{maps['solar'].min():6.2f} │{maps['solar'].max():6.2f} │{maps['solar'].mean():8.3f}     │"
    )
    print(
        f"│ População (nW/cm²/sr)    │{maps['population'].min():6.1f} │{maps['population'].max():6.1f} │{maps['population'].mean():8.2f}     │"
    )
    print(
        f"│ Distância Rede (km)      │{maps['distance'].min():6.2f} │{maps['distance'].max():6.2f} │{maps['distance'].mean():8.2f}     │"
    )
    print(
        f"│ Declividade (°)          │{maps['slope'].min():6.2f} │{maps['slope'].max():6.2f} │{maps['slope'].mean():8.2f}     │"
    )
    print(
        f"│ NDVI                     │{maps['ndvi'].min():6.3f} │{maps['ndvi'].max():6.3f} │{maps['ndvi'].mean():8.4f}    │"
    )
    print(
        f"│ Aptidão Final [0-1]      │{maps['aptitude'].min():6.3f} │{maps['aptitude'].max():6.3f} │{maps['aptitude'].mean():8.4f}    │"
    )
    print("└─────────────────────────────────────────────────────────┘")
