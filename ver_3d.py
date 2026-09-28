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
                name="Fatia Z",
                legendgroup=prop,
                cmin=vmin,
                cmax=vmax,
                colorbar=dict(title=prop, x=0.86, y=0.58, len=0.52),
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
                name="Fatia X",
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
                name="Fatia Y",
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
                name="Volume 3D",
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
                label=f"Propriedade: {prop}",
                method="update",
                args=[{"visible": vis}],
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

    # Sliders empilhados com coordenadas Y positivas na faixa dedicada inferior [0.0, 0.24]
    slider_z = dict(
        active=mid_z,
        currentvalue={"prefix": "Fatia Z (Profundidade): ", "font": {"size": 12, "color": "#1f77b4"}},
        pad={"t": 4, "b": 4},
        len=0.80,
        x=0.04,
        y=0.17,
        steps=steps_z,
    )

    slider_y = dict(
        active=idx_y_list.index(mid_y if mid_y in idx_y_list else idx_y_list[len(idx_y_list) // 2]),
        currentvalue={"prefix": "Fatia Y (Inline): ", "font": {"size": 12, "color": "#2ca02c"}},
        pad={"t": 4, "b": 4},
        len=0.80,
        x=0.04,
        y=0.09,
        steps=steps_y,
    )

    slider_x = dict(
        active=idx_x_list.index(mid_x if mid_x in idx_x_list else idx_x_list[len(idx_x_list) // 2]),
        currentvalue={"prefix": "Fatia X (Crossline): ", "font": {"size": 12, "color": "#d62728"}},
        pad={"t": 4, "b": 4},
        len=0.80,
        x=0.04,
        y=0.01,
        steps=steps_x,
    )

    fig.update_layout(
        height=980,
        title=dict(
            text="Modelo Turbidítico 3D — Fatias Ortogonais Interativas",
            font=dict(size=20),
            x=0.02,
            y=0.985,
            xanchor="left",
            yanchor="top",
        ),
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=0.02,
                y=0.935,
                xanchor="left",
                yanchor="middle",
                buttons=dropdown_buttons,
            )
        ],
        sliders=[slider_z, slider_y, slider_x],
        legend=dict(
            orientation="h",
            x=0.32,
            y=0.935,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12),
        ),
        # Delimitar dominio da cena 3D para NUNCA encavalar nos sliders, titulo ou colorbar
        scene=dict(
            domain=dict(x=[0.02, 0.83], y=[0.26, 0.89]),
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Profundidade Z (m)",
            zaxis=dict(autorange="reversed"),  # Geologia: profundidade aumenta para baixo
            aspectratio=dict(x=1.2, y=1.0, z=0.5),
        ),
        margin=dict(l=30, r=30, b=30, t=50),
    )

    # Gerar HTML com margens de pagina e container elegante
    plot_div = fig.to_html(include_plotlyjs=True, full_html=False)

    template_html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Modelo Turbidítico 3D - Fatias Interativas</title>
  <style>
    * {{
      box-sizing: border-box;
    }}
    html, body {{
      margin: 0;
      padding: 0;
      background-color: #edf2f7;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .page-wrapper {{
      padding: 25px 35px 50px 35px;
      min-height: 100vh;
    }}
    .card-container {{
      max-width: 1550px;
      margin: 0 auto;
      background-color: #ffffff;
      border-radius: 14px;
      box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
      padding: 20px 20px 30px 20px;
      overflow: visible;
    }}
  </style>
</head>
<body>
  <div class="page-wrapper">
    <div class="card-container">
      {plot_div}
    </div>
  </div>
</body>
</html>
"""

    saida_html = (base_dir / "visualizacao_3d_interativa.html").resolve()
    with open(saida_html, "w", encoding="utf-8") as f:
        f.write(template_html)

    print(f"Arquivo HTML 3D gerado com sucesso: {saida_html}")

    if abrir_navegador:
        print("Abrindo navegador padrão...")
        webbrowser.open(saida_html.as_uri())


if __name__ == "__main__":
    gerar_visualizacao_3d()
