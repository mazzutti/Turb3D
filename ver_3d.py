import webbrowser
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


def gerar_visualizacao_3d(caminho_npz: str = None, abrir_navegador: bool = True):
    base_dir = Path(__file__).parent
    if caminho_npz is None:
        caminho_npz = base_dir / "modelo_turbiditico_3D.npz"
    else:
        caminho_npz = Path(caminho_npz)

    dados = np.load(str(caminho_npz))
    x = dados["x"]  # (90,)
    y = dados["y"]  # (70,)
    z = dados["z"]  # (35,)

    # Meshgrid com coordenadas reais
    Y, X, Z = np.meshgrid(y, x, z, indexing="ij")
    x_flat = X.flatten()
    y_flat = Y.flatten()
    z_flat = Z.flatten()

    variaveis = ["porosity", "permeability_mD", "facies", "depth"]
    fig = go.Figure()

    cmaps = {
        "porosity": "Viridis",
        "permeability_mD": "Turbo",
        "facies": "Portland",
        "depth": "Cividis",
    }

    # Criar um trace de Volume 3D para cada propriedade
    for i, var in enumerate(variaveis):
        val = dados[var]
        val_flat = val.flatten()
        vmin = float(np.nanmin(val_flat))
        vmax = float(np.nanmax(val_flat))

        fig.add_trace(
            go.Volume(
                x=x_flat,
                y=y_flat,
                z=z_flat,
                value=val_flat,
                isomin=vmin,
                isomax=vmax,
                opacity=0.15,
                surface_count=18,
                colorscale=cmaps.get(var, "Viridis"),
                colorbar=dict(title=var),
                name=var,
                visible=(i == 0),  # Apenas o primeiro visivel inicialmente
            )
        )

    # Botoes para alternar entre as propriedades
    buttons = []
    for i, var in enumerate(variaveis):
        vis = [False] * len(variaveis)
        vis[i] = True
        buttons.append(
            dict(
                label=var,
                method="update",
                args=[{"visible": vis}, {"title": f"Modelo Turbidítico 3D - Propriedade: {var}"}],
            )
        )

    fig.update_layout(
        title=f"Modelo Turbidítico 3D - Propriedade: {variaveis[0]}",
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=0.02,
                y=0.98,
                showactive=True,
                buttons=buttons,
            )
        ],
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Profundidade Z (m)",
            zaxis=dict(autorange="reversed"),  # Geologia: profundidade aumenta para baixo
            aspectratio=dict(x=1.2, y=1.0, z=0.5),
        ),
        margin=dict(l=0, r=0, b=0, t=50),
    )

    saida_html = (base_dir / "visualizacao_3d_interativa.html").resolve()
    fig.write_html(str(saida_html))
    print(f"Arquivo HTML 3D gerado: {saida_html}")

    if abrir_navegador:
        print("Abrindo navegador padrao...")
        webbrowser.open(saida_html.as_uri())


if __name__ == "__main__":
    gerar_visualizacao_3d()
