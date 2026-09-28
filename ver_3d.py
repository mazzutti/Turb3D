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

        # 1. Fatia Z (Horizontal)
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

        # 2. Fatia X (Vertical Crossline)
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

        # 3. Fatia Y (Vertical Inline)
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

        # 4. Volume 3D Completo (Ativável na legenda)
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
                args=[{"visible": vis}, {"title": f"Modelo Turbidítico 3D - Fatias X, Y, Z ({prop})"}],
            )
        )

    # 1. Slider Z (Profundidade) - atualiza traces [0, 4, 8, 12]
    z_indices = [i * 4 for i in range(len(propriedades))]
    steps_z = []
    for k, z_val in enumerate(z):
        Z_k = np.full_like(X_z, z_val)
        surfs = [dados[p][:, :, k] for p in propriedades]
        steps_z.append(
            dict(
                method="restyle",
                args=[{"z": [Z_k] * len(propriedades), "surfacecolor": surfs}, z_indices],
                label=f"{int(z_val)}m",
            )
        )

    # 2. Slider Y (Inline) - atualiza traces [2, 6, 10, 14]
    y_indices = [i * 4 + 2 for i in range(len(propriedades))]
    idx_y_list = list(range(0, len(y), 2))
    if (len(y) - 1) not in idx_y_list:
        idx_y_list.append(len(y) - 1)

    steps_y = []
    for k in idx_y_list:
        y_val = y[k]
        Y_k = np.full_like(X_y, y_val)
        surfs = [dados[p][k, :, :] for p in propriedades]
        steps_y.append(
            dict(
                method="restyle",
                args=[{"y": [Y_k] * len(propriedades), "surfacecolor": surfs}, y_indices],
                label=f"{int(y_val)}m",
            )
        )

    # 3. Slider X (Crossline) - atualiza traces [1, 5, 9, 13]
    x_indices = [i * 4 + 1 for i in range(len(propriedades))]
    idx_x_list = list(range(0, len(x), 2))
    if (len(x) - 1) not in idx_x_list:
        idx_x_list.append(len(x) - 1)

    steps_x = []
    for j in idx_x_list:
        x_val = x[j]
        X_j = np.full_like(Y_x, x_val)
        surfs = [dados[p][:, j, :] for p in propriedades]
        steps_x.append(
            dict(
                method="restyle",
                args=[{"x": [X_j] * len(propriedades), "surfacecolor": surfs}, x_indices],
                label=f"{int(x_val)}m",
            )
        )

    # Configuração dos 3 Sliders empilhados
    slider_z = dict(
        active=mid_z,
        currentvalue={"prefix": "Fatia Z (Profundidade): ", "font": {"size": 12, "color": "#1f77b4"}},
        pad={"t": 5, "b": 5},
        len=0.88,
        x=0.06,
        y=-0.02,
        steps=steps_z,
    )

    slider_y = dict(
        active=idx_y_list.index(mid_y if mid_y in idx_y_list else idx_y_list[len(idx_y_list) // 2]),
        currentvalue={"prefix": "Fatia Y (Inline): ", "font": {"size": 12, "color": "#2ca02c"}},
        pad={"t": 5, "b": 5},
        len=0.88,
        x=0.06,
        y=-0.12,
        steps=steps_y,
    )

    slider_x = dict(
        active=idx_x_list.index(mid_x if mid_x in idx_x_list else idx_x_list[len(idx_x_list) // 2]),
        currentvalue={"prefix": "Fatia X (Crossline): ", "font": {"size": 12, "color": "#d62728"}},
        pad={"t": 5, "b": 5},
        len=0.88,
        x=0.06,
        y=-0.22,
        steps=steps_x,
    )

    fig.update_layout(
        title=f"Modelo Turbidítico 3D - Fatias X, Y, Z ({propriedades[0]})",
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=0.0,
                y=1.12,
                buttons=dropdown_buttons,
            )
        ],
        sliders=[slider_z, slider_y, slider_x],
        legend=dict(
            title="Camadas e Fatias:",
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
        margin=dict(l=0, r=0, b=160, t=60),
    )

    saida_html = (base_dir / "visualizacao_3d_interativa.html").resolve()
    fig.write_html(str(saida_html))
    print(f"Arquivo HTML 3D gerado com sucesso: {saida_html}")

    if abrir_navegador:
        print("Abrindo navegador padrão...")
        webbrowser.open(saida_html.as_uri())


if __name__ == "__main__":
    gerar_visualizacao_3d()
