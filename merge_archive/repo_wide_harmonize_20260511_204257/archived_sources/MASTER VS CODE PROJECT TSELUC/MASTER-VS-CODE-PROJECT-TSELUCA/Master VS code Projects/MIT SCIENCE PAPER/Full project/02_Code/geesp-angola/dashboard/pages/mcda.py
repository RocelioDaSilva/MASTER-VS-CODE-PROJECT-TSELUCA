def render():
    import streamlit as st
    import numpy as np
    import pandas as pd
    import plotly.express as px
    import matplotlib.pyplot as plt
    import io
    from pathlib import Path

    st.markdown("# 🎯 Análise Multicritério (MCDA)")

    # Sidebar: Configurar pesos
    st.sidebar.markdown("## ⚙️ Configurar Pesos")

    default_weights = {
        "Irradiação Solar": 25,
        "Demanda (Luzes Noturnas)": 25,
        "Acesso (Distância Rede)": 20,
        "Infraestrutura": 15,
        "Uso do Solo": 15,
    }

    weights = {}
    for criterion, default in default_weights.items():
        weights[criterion] = st.sidebar.slider(
            f"{criterion}", 0, 100, default, help="Ajuste o peso relativo deste critério"
        )

    total = sum(weights.values()) or 1
    weights_normalized = {k: v / total * 100 for k, v in weights.items()}

    st.markdown("### 📊 Pesos Dos Critérios (Normalizados)")
    weights_df = pd.DataFrame({"Critério": list(weights_normalized.keys()), "Peso (%)": list(weights_normalized.values())})

    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(weights_df, x="Critério", y="Peso (%)", color="Peso (%)", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(weights_df, use_container_width=True)

    st.markdown("### 🔎 Filtros & Camadas")
    layer_options = {
        "Irradiação Solar": "mapa_irradiacao",
        "Demanda (Luzes Noturnas)": "mapa_populacao",
        "Acesso (Distância Rede)": "mapa_distanciarede",
        "Infraestrutura (Declividade)": "mapa_declividade",
        "Uso do Solo (NDVI)": "mapa_ndvi",
    }

    st.divider()

    # Execute MCDA
    if st.button("▶️ Executar Análise MCDA", use_container_width=True):
        st.info("Analisando... ⏳")
        with st.spinner("Processando dados..."):
            data_dir = Path(__file__).parent.parent.parent / "data" / "processed"
            map_keys = {k: v for k, v in layer_options.items()}

            # Optional helpers
            try:
                from scripts import utils as scripts_utils
            except Exception:
                try:
                    import utils as scripts_utils
                except Exception:
                    scripts_utils = None

            try:
                from scripts.raster_utils import normalize_rasters_dict
            except Exception:
                try:
                    from raster_utils import normalize_rasters_dict
                except Exception:
                    normalize_rasters_dict = None

            # Load rasters
            loaded = {}
            for crit, fname in map_keys.items():
                p = data_dir / f"{fname}.npy"
                try:
                    if scripts_utils:
                        arr, _meta = scripts_utils.load_raster(str(p))
                    else:
                        arr = np.load(p)
                    loaded[crit] = np.array(arr, dtype=float)
                except Exception:
                    continue

            if not loaded:
                st.error("Nenhum mapa disponível em data/processed para executar MCDA.")
                return

            # Normalize
            if normalize_rasters_dict:
                normed = normalize_rasters_dict(loaded, minimum=0.0, maximum=1.0)
            else:
                normed = {}
                for k, a in loaded.items():
                    valid = np.isfinite(a)
                    if valid.any():
                        amin = float(np.nanmin(a))
                        amax = float(np.nanmax(a))
                        denom = (amax - amin) if (amax - amin) != 0 else 1.0
                        norm = (a - amin) / denom
                        normed[k] = np.nan_to_num(norm)
                    else:
                        normed[k] = np.zeros_like(a)

            # Weighted overlay
            frac_weights = {k: (weights.get(k, 0) / total) for k in weights.keys()}
            overlay = None
            for crit, arr in normed.items():
                w = frac_weights.get(crit, 0.0)
                overlay = arr * w if overlay is None else overlay + arr * w

            overlay = np.nan_to_num(np.asarray(overlay))

            out_npy = data_dir / "mapa_aptidao_integrada.npy"
            np.save(out_npy, overlay)
            try:
                if scripts_utils:
                    scripts_utils.save_raster(overlay, str(data_dir / "mapa_aptidao_integrada.tif"))
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Não foi possível salvar GeoTIFF: {e}")

            fig, ax = plt.subplots(figsize=(6, 4))
            im = ax.imshow(overlay, cmap="viridis")
            ax.set_title("Mapa de Aptidão Integrada (MCDA)")
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            plt.close(fig)
            buf.seek(0)

            col1, col2 = st.columns([2, 1])
            with col1:
                st.success("✓ Análise concluída com sucesso!")
                st.metric("Pixels válidos", f"{np.isfinite(overlay).sum()}")
                st.image(buf.getvalue(), use_column_width=True)
                st.download_button(label="📥 Baixar overlay (.npy)", data=open(out_npy, "rb").read(), file_name="mapa_aptidao_integrada.npy", mime="application/octet-stream")
            with col2:
                st.dataframe(pd.DataFrame({"Critério": list(normed.keys()), "Validos": [int(np.isfinite(v).sum()) for v in normed.values()]}))

    # Sensitivity analysis (lightweight)
    if st.button("▶️ Executar Sensibilidade para critério selecionado"):
        deltas = list(range(-20, 21, 5))
        results = []
        base_weights = {k: weights[k] / total for k in weights.keys()}
        for d in deltas:
            adj = base_weights.copy()
            key_name = list(layer_options.keys())[0]
            adj[key_name] = max(0.0, adj.get(key_name, 0.0) * (1 + d / 100.0))
            s = sum(adj.values())
            normed_w = {k: v / s for k, v in adj.items()} if s != 0 else {k: 0.0 for k in adj.keys()}

            o = None
            for crit_name, arr in normed.items():
                w = normed_w.get(crit_name, 0.0)
                o = arr * w if o is None else o + arr * w
            mean_val = float(np.nanmean(o)) if o is not None else 0.0
            results.append({"delta": d, "mean": mean_val})

        df = pd.DataFrame(results)
        fig2 = px.line(df, x="delta", y="mean", title=f"Sensibilidade")
        st.plotly_chart(fig2, use_container_width=True)
