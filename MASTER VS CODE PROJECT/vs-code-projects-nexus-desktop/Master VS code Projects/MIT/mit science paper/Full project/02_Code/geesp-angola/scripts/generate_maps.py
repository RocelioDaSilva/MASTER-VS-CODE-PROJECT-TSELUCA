"""
GEESP-Angola: Map Generation Module
Gera mapas raster realistas para demonstração e análise MCDA
"""

import numpy as np
from pathlib import Path
import logging
from typing import Any
from scripts import map_utils

# Optional heavy dependencies (rasterio, scipy)
try:
    import rasterio
    from rasterio.transform import from_origin

    HAS_RASTERIO = True
except Exception:
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
except Exception:
    plt = None
    mpatches = None
    LinearSegmentedColormap = None

try:
    from scipy.ndimage import gaussian_filter, distance_transform_edt

    HAS_SCIPY = True
except Exception:
    HAS_SCIPY = False

    def gaussian_filter(arr, sigma):
        return arr

    def distance_transform_edt(mask):
        # Fallback: compute Euclidean distance to nearest True pixel (vectorized)
        pts = np.array(np.where(mask)).T
        if pts.size == 0:
            return np.full(mask.shape, mask.shape[0] + mask.shape[1], dtype=float)
        y_idx, x_idx = np.indices(mask.shape)
        coords = np.stack([y_idx.ravel(), x_idx.ravel()], axis=1)
        # compute distances to all pts (may be memory heavy but acceptable for demo size)
        dists = np.sqrt(((coords[:, None, :] - pts[None, :, :]) ** 2).sum(axis=2))
        min_d = dists.min(axis=1).reshape(mask.shape)
        return min_d


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MapGenerator:
    """Gera mapas raster para análise MCDA da Huíla"""

    def __init__(self, width=300, height=280, crs="EPSG:32733"):
        """
        Args:
            width (int): Largura em pixels
            height (int): Altura em pixels
            crs (str): Sistema de coordenadas
        """
        self.width = width
        self.height = height
        self.crs = crs

        # Bounds para Huíla (UTM 33S, aproximado)
        # Convertido de graus para metros UTM
        self.west = 500000  # metros
        self.south = 8000000  # metros
        self.east = 530000
        self.north = 8078500

        self.pixel_size_x = (self.east - self.west) / width
        self.pixel_size_y = (self.north - self.south) / height

        # Criar transform para georreferenciamento
        self.transform = from_origin(
            self.west, self.north, self.pixel_size_x, self.pixel_size_y
        )

        logger.info(f"✓ MapGenerator inicializado: {width}x{height} pixels")

    def generate_solar_radiation(self):
        """
        Gera mapa de irradiação solar realista

        Padrão: Irradiação mais alta no norte (Humpata)
        Unidade: kWh/m²/dia
        Intervalo: 5.5 - 6.4
        """
        logger.info("Gerando mapa de Irradiação Solar...")

        # Cria gradiente base (norte-sul)
        y_gradient = np.linspace(6.4, 5.5, self.height)[:, np.newaxis]
        data = np.tile(y_gradient, (1, self.width))

        # Adiciona variação espacial
        x = np.linspace(0, 1, self.width)
        y = np.linspace(0, 1, self.height)
        X, Y = np.meshgrid(x, y)

        # Padrão sinusoidal
        noise = 0.3 * np.sin(X * 3) * np.cos(Y * 4)
        data += noise

        # Suavizar
        data = gaussian_filter(data, sigma=2)

        # Normalizar ao intervalo [5.5, 6.4]
        data = np.clip(data, 5.5, 6.4)

        logger.info(
            f"  Min: {data.min():.2f}, Max: {data.max():.2f}, "
            f"Mean: {data.mean():.2f} kWh/m²/dia"
        )

        return data.astype(np.float32)

    def generate_population_density(self):
        """
        Gera mapa de densidade populacional (luzes noturnas simuladas)

        Padrão: Clusters em torno de centros urbanos
        Unidade: Proxy de luzes noturnas (nanoWatts/cm²/sr)
        Intervalo: 10 - 95
        """
        logger.info("Gerando mapa de Densidade Populacional...")

        # Inicializa
        data = np.zeros((self.height, self.width), dtype=np.float32)

        # Define centros urbanos (aproximado para 3 zonas)
        # Cacula (Zona A)
        cy_a, cx_a = int(0.25 * self.height), int(0.45 * self.width)
        # Humpata (Zona B)
        cy_b, cx_b = int(0.75 * self.height), int(0.65 * self.width)
        # Quilengues (Zona C)
        cy_c, cx_c = int(0.55 * self.height), int(0.30 * self.width)

        centers = [(cy_a, cx_a, 45), (cy_b, cx_b, 60), (cy_c, cx_c, 55)]

        # Cria gaussianas para cada centro
        for cy, cx, intensity in centers:
            y = np.arange(self.height)
            x = np.arange(self.width)
            Y, X = np.meshgrid(x, y)

            # Gaussiana 2D
            gaussian = intensity * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 1500)
            data += gaussian

        # Adiciona ruído de fundo
        noise = np.random.poisson(5, (self.height, self.width)).astype(np.float32)
        data += noise

        # Suavizar
        data = gaussian_filter(data, sigma=3)

        # Normalizar ao intervalo [10, 95]
        data_min, data_max = data.min(), data.max()
        data = (data - data_min) / (data_max - data_min) * 85 + 10

        logger.info(
            f"  Min: {data.min():.1f}, Max: {data.max():.1f}, "
            f"Mean: {data.mean():.1f} nW/cm²/sr"
        )

        return np.clip(data, 10, 95).astype(np.float32)

    def generate_distance_to_grid(self):
        """
        Gera mapa de distância à rede elétrica existente

        Padrão: Redes existentes ao longo de estradas principais
        Unidade: km
        Intervalo: 0 - 45 km
        """
        logger.info("Gerando mapa de Distância à Rede...")

        # Cria "rede elétrica" como linhas retas
        grid_mask = np.zeros((self.height, self.width), dtype=bool)

        # Linha vertical (leste-oeste)
        grid_mask[int(0.3 * self.height), :] = True

        # Linha horizontal (norte-sul)
        grid_mask[:, int(0.4 * self.width)] = True

        # Linhas diagonais
        for i in range(self.height):
            if 0.18 * i < self.width:
                grid_mask[i, int(0.18 * i)] = True

        # Calcular distância euclidiana
        distance = distance_transform_edt(~grid_mask)

        # Converter pixels em km (pixel_size_x ~= 100m)
        distance_km = distance * (self.pixel_size_x / 1000)

        # Normalizar para [0, 45]
        data = np.clip(distance_km, 0, 45).astype(np.float32)

        logger.info(
            f"  Min: {data.min():.2f}, Max: {data.max():.2f}, "
            f"Mean: {data.mean():.2f} km"
        )

        return data

    def generate_slope(self):
        """
        Gera mapa de declividade (simulado)

        Unidade: graus
        Intervalo: 0 - 30
        """
        logger.info("Gerando mapa de Declividade...")

        # Cria um DEM sintético
        x = np.linspace(0, 3, self.width)
        y = np.linspace(0, 3, self.height)
        X, Y = np.meshgrid(x, y)

        # Elevação sintética com trends e ruído
        elevation = (
            2000
            + 200 * np.sin(X)
            + 150 * np.cos(Y)
            + np.random.normal(0, 50, (self.height, self.width))
        )

        # Calcular declividade (aproximada com gradientes)
        dz_dy, dz_dx = np.gradient(elevation)
        slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
        slope_deg = np.degrees(slope_rad)

        data = np.clip(slope_deg, 0, 30).astype(np.float32)

        logger.info(
            f"  Min: {data.min():.2f}, Max: {data.max():.2f}, "
            f"Mean: {data.mean():.2f}°"
        )

        return data

    def generate_ndvi(self):
        """
        Gera mapa de NDVI (Índice de Vegetação)

        Unidade: Adimensional
        Intervalo: -0.2 - 0.7
        """
        logger.info("Gerando mapa de NDVI...")

        # Padrão base
        x = np.linspace(0, 1, self.width)
        y = np.linspace(0, 1, self.height)
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

    def generate_aptitude_map(self, solar, population, distance, slope, ndvi):
        """
        Gera mapa final de aptidão (resultado MCDA)

        Combinação ponderada dos critérios:
        - Solar: 25%
        - Demanda: 25%
        - Acesso: 20%
        - Infraestrutura (declividade): 15%
        - Vegetação (uso do solo): 15%
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

    def save_geotiff(self, data, filename, nodata=-9999):
        """Salva array como GeoTIFF georreferenciado"""

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Preparar perfil do raster
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
            dst.write(data, 1)

        logger.info(f"✓ Salvo GeoTIFF: {output_path}")
        return output_path

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


def generate_all_maps(output_dir="data/processed"):
    """Gera todos os mapas principais"""

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
