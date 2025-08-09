# 🤟 Tradutor de Libras (LIBRAS Translator)

Um projeto de reconhecimento de gestos em tempo real para tradução da Língua Brasileira de Sinais (LIBRAS) usando visão computacional e aprendizado de máquina.

## 📋 Sobre o Projeto

Este projeto utiliza OpenCV e MediaPipe para capturar e analisar movimentos das mãos através da webcam, identificando letras do alfabeto em LIBRAS. O sistema é capaz de reconhecer tanto gestos estáticos quanto dinâmicos (que envolvem movimento).

### ⚠️ Status do Projeto

**🚧 PROJETO EM DESENVOLVIMENTO 🚧**

Este projeto ainda está em fase de desenvolvimento e não está completo. Funcionalidades implementadas e limitações:

#### ✅ Funcionalidades Implementadas:
- Captura de vídeo em tempo real via webcam
- Detecção e rastreamento de landmarks das mãos usando MediaPipe
- Reconhecimento de letras estáticas do alfabeto LIBRAS
- Reconhecimento de letras dinâmicas (J, H, Z, X) que requerem movimento
- Sistema de coleta e armazenamento de dados de treinamento
- Interface visual com feedback em tempo real

#### ❌ Limita��ões Atuais:
- Conjunto limitado de letras reconhecidas
- Precisão pode variar dependendo da iluminação e posicionamento
- Não possui interface gráfica amigável
- Falta de reconhecimento de palavras completas
- Ausência de tradução de frases
- Não possui sistema de calibração personalizada

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **OpenCV** - Processamento de imagem e vídeo
- **MediaPipe** - Detecção de landmarks das mãos
- **NumPy** - Operações matemáticas e processamento de arrays
- **JSON** - Armazenamento de dados de landmarks

## 📦 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd tradutor-de-libras
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### Executar o Reconhecimento em Tempo Real:
```bash
python camera.py
```

### Controles:
- **'q'** - Sair do programa
- **'s'** - Salvar landmarks da mão atual (para treinamento)

### Testar Movimentos Específicos:
```bash
python test_movements.py
```

## 📁 Estrutura do Projeto

```
tradutor-de-libras/
├── camera.py                 # Script principal de captura e reconhecimento
├── gestures.py              # Lógica de detecção de gestos e movimentos
├── test_movements.py        # Testes para movimentos específicos
├── configuracao_avancada.py # Configurações avançadas do sistema
├── requirements.txt         # Dependências do projeto
├── landmarks/              # Dados de treinamento salvos
│   └── all_landmarks.json  # Landmarks coletados para cada letra
├── shape_predictor_68_face_landmarks.dat # Modelo para detecção facial
└── README.md               # Este arquivo
```

## 🎯 Funcionalidades Detalhadas

### Reconhecimento Estático
- Identifica letras baseadas na posição dos dedos
- Utiliza normalização de landmarks para maior precisão
- Compara com banco de dados de gestos pré-coletados

### Reconhecimento Dinâmico
- **Letra J**: Movimento em gancho para baixo e esquerda
- **Letra H**: Movimento horizontal da direita para esquerda
- **Letra Z**: Movimento em zigue-zague
- **Letra X**: Movimento de gancho pequeno

### Sistema de Coleta de Dados
- Permite salvar novos exemplos de gestos
- Armazena landmarks em formato JSON
- Suporte para múltiplas amostras por letra

## 🔮 Próximos Passos

- [ ] Expandir o alfabeto completo de LIBRAS
- [ ] Implementar reconhecimento de números
- [ ] Adicionar suporte para palavras e frases
- [ ] Criar interface gráfica mais amigável
- [ ] Melhorar precisão com mais dados de treinamento
- [ ] Implementar sistema de calibração personalizada
- [ ] Adicionar suporte para múltiplas mãos simultaneamente
- [ ] Criar sistema de tradução bidirecional (texto para LIBRAS)

## 🤝 Contribuindo

Este projeto está aberto para contribuições! Se você quiser ajudar:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

João Pedro Henriques Balbino - joaopedrohbalbino@gmail.com

**Nota**: Este é um projeto educacional/experimental em desenvolvimento. Para uso em produção, são necessários mais testes e melhorias na precisão do reconhecimento.
