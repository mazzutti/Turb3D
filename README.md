# Visualização 3D - Modelo Turbidítico (Plotly)

Visualização tridimensional volumétrica e por **fatias ortogonais interativas com 3 sliders (X, Y, Z)** do modelo geológico `modelo_turbiditico_3D.npz`.  
Pronto para execução local no **Windows 10/11**, Linux, macOS e publicação no **GitHub Pages**.

🌐 **Visualização Online (GitHub Pages):** [https://mazzutti.github.io/Turb3D/](https://mazzutti.github.io/Turb3D/)

---

## 1. Publicação no GitHub Pages

O repositório já está preparado com o arquivo `index.html` e um workflow automatizado em `.github/workflows/deploy.yml`.

### Como ativar o GitHub Pages no repositório:
1. No seu repositório no GitHub, clique na aba **Settings** (Configurações).
2. No menu lateral esquerdo, clique em **Pages**.
3. Em **Build and deployment > Source**:
   - Selecione **GitHub Actions** (recomendado — publica automaticamente em qualquer push para a branch `main`).
   - *Ou alternativa direta:* Selecione **Deploy from a branch** > Branch: `main` > Pasta: `/ (root)` > clique em **Save**.
4. Em poucos segundos, a visualização estará acessível publicamente em:  
   👉 **`https://mazzutti.github.io/Turb3D/`**

---

## 2. Clonar o Repositório

Abra o **PowerShell**, **Terminal** ou **Prompt de Comando (CMD)** e execute:

```bash
# Clonar o repositório
git clone https://github.com/mazzutti/Turb3D.git

# Entrar na pasta do projeto
cd Turb3D
```

---

## 3. Instalação no Windows

### Pré-requisitos
- Python 3.10 ou superior instalado ([python.org](https://www.python.org/downloads/)).  
  *(Na instalação, marcar a opção **"Add python.exe to PATH"**).*
- Git instalado ([git-scm.com](https://git-scm.com/)).

---

### Passo a passo (PowerShell)

Dentro da pasta `Turb3D`, execute:

```powershell
# 1. Habilitar execução de scripts para a sessão atual (caso bloqueado)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 2. Criar ambiente virtual (.venv)
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

## 4. Como Executar Localmente

Com o ambiente ativado, execute:

```powershell
python ver_3d.py
```

O script irá:
1. Carregar os dados geológicos de `modelo_turbiditico_3D.npz`.
2. Gerar/atualizar o arquivo `index.html` otimizado para web.
3. Abrir automaticamente a aba no seu navegador padrão (Edge, Chrome, Firefox).

> **Dica para gerar sem abrir navegador:**  
> `python ver_3d.py --no-browser`

---

## 5. Controles Interativos no Navegador

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
- **Legenda Interativa (canto superior):**
  - Clique em qualquer fatia (`Fatia Z`, `Fatia X`, `Fatia Y`) para ocultá-la ou exibi-la.
  - Clique em **"Volume 3D"** para ativar a nuvem volumétrica com transparência junto com as fatias.
- **Navegação 3D:**
  - **Botão esquerdo do mouse (arrastar):** Rotação 3D em torno do volume.
  - **Scroll do mouse:** Zoom in / Zoom out.
  - **Botão direito do mouse:** Pan (deslocar a câmera).
- **Eixo Z:** Profundidade orientada conforme convenção geológica (profundidade aumenta para baixo).

---

## 6. Estrutura dos Arquivos

- `index.html`: Arquivo principal servido pelo GitHub Pages.
- `modelo_turbiditico_3D.npz`: Arquivo de dados tridimensionais (eixos `x`, `y`, `z` e matrizes de propriedades).
- `ver_3d.py`: Script Python com Plotly que gera e abre a visualização por fatias X, Y, Z e volume 3D.
- `requirements.txt`: Dependências mínimas (`numpy`, `plotly`).
- `.github/workflows/deploy.yml`: Workflow do GitHub Actions para publicação contínua no GitHub Pages.
- `.gitignore`: Configuração para ignorar arquivos temporários e caches.
