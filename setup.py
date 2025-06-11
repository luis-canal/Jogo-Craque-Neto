import PyInstaller.__main__
import os
import shutil
import platform

nome_executavel = 'JogoDoCraqueNeto'
icone_caminho = 'recursos/assets/icone.ico'

# Limpa builds anteriores
for pasta in ['build', 'dist', '__pycache__']:
    if os.path.exists(pasta):
        shutil.rmtree(pasta)

# Verifica arquivos essenciais
if not os.path.exists('main.py'):
    raise FileNotFoundError("Arquivo 'main.py' não encontrado.")

if not os.path.exists(icone_caminho):
    raise FileNotFoundError(f"Ícone não encontrado em '{icone_caminho}'")

# Define separador de caminhos
separador = ';' if platform.system() == 'Windows' else ':'

# Executa o PyInstaller
PyInstaller.__main__.run([
    'main.py',
    f'--name={nome_executavel}',
    '--onefile',
    '--noconsole',
    f'--icon={icone_caminho}',
    f'--add-data=recursos/assets{separador}recursos/assets',
    f'--add-data=log.dat{separador}.',
    f'--add-data=README.md{separador}.',
    f'--add-data=recursos/funcoes.py{separador}recursos',
    f'--add-data=recursos/funcaoUtil.py{separador}recursos',
])

extensao = '.exe' if platform.system() == 'Windows' else ''
print(f"\n✅ Executável gerado com sucesso em: dist/{nome_executavel}{extensao}\n")
