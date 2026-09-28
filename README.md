# Visualização 3D - Modelo Turbidítico

Visualização tridimensional interativa do modelo geológico `modelo_turbiditico_3D.npz`.  
Compatível com **Windows 10/11**, Linux e macOS.

---

## 1. Instalação no Windows

### Pré-requisitos
- Python 3.10 ou superior instalado no Windows ([python.org](https://www.python.org/downloads/)).  
  *(Ao instalar, marque a caixa **"Add python.exe to PATH"**).*

---

### Passo a passo no Windows (PowerShell)

Abra o **PowerShell** na pasta do projeto e execute:

```powershell
# 1. Liberar execução de scripts para a sessão atual (se necessário)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 2. Criar o ambiente virtual (.venv)
python -m venv .venv

# 3. Ativar o ambiente virtual
.venv\Scripts\Activate.ps1

# 4. Atualizar pip e instalar dependências
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Se preferir usar o Prompt de Comando clássico (CMD):**
> ```cmd
> python -m venv .venv
> .venv\Scripts\activate.bat
> pip install -r requirements.txt
> ```

---

## 2. Como Executar no Windows

### Opção A: Visualizador 3D no Navegador (Recomendado)
Gera volume tridimensional interativo e abre automaticamente no navegador padrão (Edge, Chrome, Firefox, etc.):

```powershell
python ver_3d.py
```

- **Interação:**
  - Botão esquerdo do mouse: Rotação 3D
  - Scroll do mouse: Zoom in / Zoom out
  - Botão direito: Pan (mover câmera)
- **Menu Dropdown (canto superior esquerdo):**
  - Alterna entre as propriedades: `porosity`, `permeability_mD`, `facies` e `depth`.
- **Eixo Z:** Profundidade orientada conforme geologia (aumenta para baixo).

---

### Opção B: Lexcube no JupyterLab
Para utilizar o widget 3D do **Lexcube**:

```powershell
jupyter lab visualizacao_turbiditico_3d.ipynb
```

*(Se o Firewall do Windows exibir um aviso de rede para o Python, clique em "Permitir Acesso").*

1. A página do JupyterLab abrirá no navegador (`http://localhost:8888`).
2. Clique no botão **Run All** (ícone ▶▶ na barra de ferramentas).
3. O cubo 3D do Lexcube será renderizado na saída da célula com sliders interativos de fatia.

---

## 3. Estrutura dos Arquivos

- `modelo_turbiditico_3D.npz`: Arquivo de dados tridimensionais (eixos `x`, `y`, `z` e matrizes `porosity`, `permeability_mD`, `facies`, `depth`).
- `ver_3d.py`: Script autônomo com Plotly que gera e abre o visualizador 3D no navegador.
- `visualizar_lexcube.py`: Módulo auxiliar para carregar o modelo no formato do Lexcube.
- `visualizacao_turbiditico_3d.ipynb`: Notebook Jupyter configurado para o Lexcube.
- `requirements.txt`: Dependências do projeto.
