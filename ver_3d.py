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

    # Malhas para fatias e volume
    X_z, Y_z = np.meshgrid(x, y)
    Y_x, Z_x = np.meshgrid(y, z, indexing="ij")
    X_y, Z_y = np.meshgrid(x, z, indexing="ij")
    Y_vol, X_vol, Z_vol = np.meshgrid(y, x, z, indexing="ij")

    mid_z = len(z) // 2
    mid_x = len(x) // 2
    mid_y = len(y) // 2

    propriedades = ["porosity", "permeability_mD", "facies", "depth"]
    cmaps = {
        "porosity": "Viridis",
        "permeability_mD": "Turbo",
        "facies": "Portland",
        "depth": "Cividis",
    }

    fig = go.Figure()

    # Cada propriedade recebe 4 traces:
    # 0: Fatia Z (Profundidade / Horizontal)
    # 1: Fatia X (Crossline / Vertical)
    # 2: Fatia Y (Inline / Vertical)
    # 3: Volume 3D (Nuvem volumétrica)
    for i, prop in enumerate(propriedades):
        val = dados[prop]
        vmin, vmax = float(np.nanmin(val)), float(np.nanmax(val))
        ativo = (i == 0)

        # 1. Fatia Z (Plano Horizontal)
        fig.add_trace(
            go.Surface(
                x=X_z,
                y=Y_z,
                z=np.full_like(X_z, z[mid_z]),
                surfacecolor=val[:, :, mid_z],
                colorscale=cmaps[prop],
                name="Fatia Z (Profundidade)",
                legendgroup=prop,
                cmin=vmin,
                cmax=vmax,
                colorbar=dict(title=prop, x=1.02),
                visible=ativo,
                showscale=True,
            )
        )

        # 2. Fatia X (Plano Vertical Crossline)
        fig.add_trace(
            go.Surface(
                x=np.full_like(Y_x, x[mid_x]),
                y=Y_x,
                z=Z_x,
                surfacecolor=val[:, mid_x, :],
                colorscale=cmaps[prop],
                name="Fatia X (Crossline)",
                legendgroup=prop,
                cmin=vmin,
                cmax=vmax,
                visible=ativo,
                showscale=False,
            )
        )

        # 3. Fatia Y (Plano Vertical Inline)
        fig.add_trace(
            go.Surface(
                x=X_y,
                y=np.full_like(X_y, y[mid_y]),
                z=Z_y,
                surfacecolor=val[mid_y, :, :],
                colorscale=cmaps[prop],
                name="Fatia Y (Inline)",
                legendgroup=prop,
                cmin=vmin,
                cmax=vmax,
                visible=ativo,
                showscale=False,
            )
        )

        # 4. Volume 3D (Disponível na legenda com 1 clique)
        fig.add_trace(
            go.Volume(
                x=X_vol.flatten(),
                y=Y_vol.flatten(),
                z=Z_vol.flatten(),
                value=val.flatten(),
                isomin=vmin,
                isomax=vmax,
                opacity=0.10,
                surface_count=15,
                colorscale=cmaps[prop],
                name="Volume 3D Completo",
                legendgroup=prop,
                visible=("legendonly" if ativo else False),
                showscale=False,
            )
        )

    # Menu Dropdown para alternar propriedades
    dropdown_buttons = []
    for i, prop in enumerate(propriedades):
        vis = [False] * (len(propriedades) * 4)
        vis[i * 4] = True
        vis[i * 4 + 1] = True
        vis[i * 4 + 2] = True
        vis[i * 4 + 3] = "legendonly"
        dropdown_buttons.append(
            dict(
                label=prop,
                method="update",
                args=[{"visible": vis}, {"title": f"Modelo Turbidítico 3D - Fatias e Volume ({prop})"}],
            )
        )

    # Slider interativo para navegar pelas 35 camadas em Z
    z_indices = [i * 4 for i in range(len(propriedades))]
    steps = []
    for k, z_val in enumerate(z):
        Z_k = np.full_like(X_z, z_val)
        surfs = [dados[p][:, :, k] for p in propriedades]
        step = dict(
            method="restyle",
            args=[{"z": [Z_k] * len(propriedades), "surfacecolor": surfs}, z_indices],
            label=f"{int(z_val)}m",
        )
        steps.append(step)

    sliders = [
        dict(
            active=mid_z,
            currentvalue={"prefix": "Fatia Z (Profundidade): "},
            pad={"t": 45, "b": 15},
            steps=steps,
        )
    ]

    fig.update_layout(
        title=f"Modelo Turbidítico 3D - Fatias e Volume ({propriedades[0]})",
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=0.0,
                y=1.12,
                buttons=dropdown_buttons,
            )
        ],
        sliders=sliders,
        legend=dict(
            title="Camadas e Fatias (clique p/ ocultar/exibir):",
            orientation="v",
            x=1.12,
            y=0.8,
        ),
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Profundidade Z (m)",
            zaxis=dict(autorange="reversed"),  # Geologia: profundidade aumenta para baixo
            aspectratio=dict(x=1.2, y=1.0, z=0.5),
        ),
        margin=dict(l=0, r=0, b=0, t=60),
    )

    saida_html = (base_dir / "visualizacao_3d_interativa.html").resolve()
    fig.write_html(str(saida_html))
    print(f"Arquivo HTML 3D gerado com sucesso: {saida_html}")

    if abrir_navegador:
        print("Abrindo navegador padrão...")
        webbrowser.open(saida_html.as_uri())


if __name__ == "__main__":
    gerar_visualizacao_3d()
