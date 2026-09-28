# Visualização 3D - Modelo Turbidítico (Plotly)

Visualização tridimensional volumétrica e por **fatias ortogonais interativas com 3 sliders (X, Y, Z)** do modelo geológico `modelo_turbiditico_3D.npz`.  
Abre diretamente no navegador padrão sem necessidade de Jupyter. Compatível com **Windows 10/11**, Linux e macOS.

---

## 1. Instalação no Windows

### Pré-requisitos
- Python 3.10 ou superior instalado ([python.org](https://www.python.org/downloads/)).  
  *(Na instalação, marcar a opção **"Add python.exe to PATH"**).*

---

### Passo a passo (PowerShell)

Abra o **PowerShell** na pasta do projeto e execute:

```powershell
# 1. Habilitar execução de scripts para a sessão atual (caso bloqueado)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# 4. Instalar dependências leves (numpy e plotly)
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Se preferir o Prompt de Comando clássico (CMD):**
> ```cmd
> python -m venv .venv
> .venv\Scripts\activate.bat
> pip install -r requirements.txt
> ```

---

## 2. Como Executar

Com o ambiente ativado, execute:

```powershell
python ver_3d.py
```

O script irá:
1. Carregar os dados geológicos de `modelo_turbiditico_3D.npz`.
2. Gerar o arquivo interativo `visualizacao_3d_interativa.html`.
3. Abrir automaticamente a aba no seu navegador padrão (Edge, Chrome, Firefox).

---

## 3. Controles Interativos no Navegador

- **3 Sliders Independentes de Fatias (abaixo do gráfico 3D):**
  - **Slider Z (Azul - Profundidade):** Desliza entre as 35 camadas geológicas (1850 m a 2200 m).
  - **Slider Y (Verde - Inline):** Desliza o plano vertical ao longo do eixo Y (0 m a 7000 m).
  - **Slider X (Vermelho - Crossline):** Desliza o plano vertical ao longo do eixo X (0 m a 9000 m).
- **Menu Dropdown (canto superior esquerdo):**  
  Alterna instantaneamente a propriedade exibida em todas as fatias:
  - `porosity` (Porosidade)
  - `permeability_mD` (Permeabilidade em mD)
  - `facies` (Fácies sedimentares)
  - `depth` (Profundidade)
- **Legenda Interativa (canto direito):**
  - Clique em qualquer fatia (`Fatia Z`, `Fatia X`, `Fatia Y`) para ocultá-la ou exibi-la.
  - Clique em **"Volume 3D Completo"** para ativar a nuvem volumétrica com transparência junto com as fatias.
- **Navegação 3D:**
  - **Botão esquerdo do mouse (arrastar):** Rotação 3D em torno do volume.
  - **Scroll do mouse:** Zoom in / Zoom out.
  - **Botão direito do mouse:** Pan (deslocar a câmera).
- **Eixo Z:** Profundidade orientada conforme convenção geológica (profundidade aumenta para baixo).

---

## 4. Estrutura dos Arquivos

- `modelo_turbiditico_3D.npz`: Arquivo de dados tridimensionais (eixos `x`, `y`, `z` e matrizes de propriedades).
- `ver_3d.py`: Script Python com Plotly que gera e abre a visualização por fatias X, Y, Z e volume 3D.
- `requirements.txt`: Dependências mínimas (`numpy`, `plotly`).
- `visualizacao_3d_interativa.html`: Arquivo HTML gerado pelo script.
