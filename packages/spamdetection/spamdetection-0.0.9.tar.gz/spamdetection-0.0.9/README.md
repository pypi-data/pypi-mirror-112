# Introdução

Este diretório contém um projeto Python para solução do problema prático `02-SMSSpamDetection` do teste de Inteligência Artificial da Nuveo. Neste problema, solicitou-se a criação de um projeto para servir um modelo de classificação de mensagens de texto em _'ham'_ e _'spam'_. O modelo foi criado utilizando o pacote _scikit-learn_ e disponibilizado como um _pipeline_ contendo um passo de pré-processamento utilizando _TF-IDF_, seguido por um modelo de classificação binária utilizando _Random Forest_.

Para a implementação, foi criado um pacote Python de nome `spamdetection`, que implementa a classe `SpamDetector`, contendo métodos `prob_spam()` (que retorna a probabilidade de classificação _'spam'_ determinada pelo modelo) e `is_spam()` (que retorna a classificação). Maiores detalhes sobre o uso do pacote estão disponíveis na seção [Utilização](https://github.com/fabio-a-oliveira/nuveo-teste-ia/tree/main/02-SMSSpamDetection#utilização) e na [documentação](https://fabio-a-oliveira.github.io/nuveo-teste-ia/spamdetection).

Conforme solicitado no desafio, o pacote também é acompanhado de um módulo de testes unitários, contido na pasta [/tests](https://github.com/fabio-a-oliveira/nuveo-teste-ia/tree/main/02-SMSSpamDetection/tests). Maiores detalhes abaixo, na seção [Testes](https://github.com/fabio-a-oliveira/nuveo-teste-ia/tree/main/02-SMSSpamDetection#testes).

Também foi criado um aplicativo web que permite fazer previsões utilizando o modelo. O aplicativo pode ser utilizado visitando https://nuveo-teste-ia.herokuapp.com/. Entretanto, por estar hospedado gratuitamente, somente um visitante é permitido por vez.

# Dependências

Além da biblioteca padrão de Python, os seguintes pacotes são necessários para o uso do pacote _spamdetection_:

* sklearn == 0.24.1
* pywebio == 1.2.3

O pacote foi criado em Python 3.8.5.

Ambos estão especificados em `requirements.txt`. Caso opte por clonar o repositório (não é necessário, veja em [Instalação](https://github.com/fabio-a-oliveira/nuveo-teste-ia/tree/main/02-SMSSpamDetection#instalação)), podem ser instalados com `pip install requirements.txt` à partir da pasta raiz do repositório.

# Instalação

Duas opções estão disponíveis para uso do pacote _spamdetection_:

### 1. Instalar com `pip`

Para cumprimento do desafio, criei o pacote `spamdetection`, que também foi disponibilizado no PyPI. O pacote pode ser instalado à partir da linha de comando com:

```
pip install spamdetection
```

Antes da instalação e uso, recomenda-se a criação de um ambiente virtual dedicado, utilizando sua ferramenta favorita para gestão de ambientes virtuais, e.g.:
* `conda create -n {nome_do_ambiente}` e `source activate {nome_do_ambiente}`, 
* `virtualenv {nome_do_ambiente}` e `activate` ou 
* `python -m venv {endereço_do_ambiente}`

O uso de ambiente virtual é altamente recomendado mas não obrigatório. Caso a versão de `scikit-learn` não seja a 0.24.1, pode haver um mar de _warnings_ desencorajando o uso de um modelo criado em versão diferente do pacote. Testei com a 0.23.2 e não houve degradação de performance.

### 2. Clonar este repositório

Tanto o pacote `spamdetection` quanto este repositório foram criados para que não fosse necessário clonar o repositório localmente (clonar repositório é solução para ___contribuir___, não para ___utilizar___!).

Entretanto, caso queira ter o código localmente, utilize:

```
git clone git@github.com:fabio-a-oliveira/nuveo-teste-ia.git
```

Antes de utilizar, navegue até a pasta raiz do repositório e instale as dependências com:

```
pip install requirements.txt
```

Aqui, recomenda-se também a utilização de ambiente virtual dedicado.


# Utilização

São disponibilizados alguns modos de operação:

### 1. Classe `SpamDetector`

Após instalar o pacote seguindo as instruções em [Instalação](https://github.com/fabio-a-oliveira/nuveo-teste-ia/tree/main/02-SMSSpamDetection#instalação), utilizar o método `SpamDetector()`.

Exemplo de utilização de `prob_spam()`:

```
>>> from spamdetection import SpamDetector
>>> detector = SpamDetector()
>>> detector.prob_spam("These are not the droids you are looking for")
0.02
```

Exemplo de utilização de `is_spam()`:

```
>>> from spamdetection import SpamDetector
>>> detector.is_spam("These are not the droids you are looking for")
False
```

O método `is_spam()` também pode ser chamado com o argumento `mode`, que aceita `1` ou `"aggressive"` (_threshold_ baixo para classificação como _spam_) ou `2` ou `"permissive"` (_threshold_ alto para classificação como _spam_). Caso não seja especificado, o valor padrão é `"permissive"`.

O exemplo abaixo ilustra a diferença:

```
>>> from spamdetection import SpamDetector
>>> detector = SpamDetector()
>>> detector.prob_spam("call 09058094583 urgent")
0.42

>>> detector.is_spam("call 09058094583 urgent", "aggressive")
True

>>> detector.is_spam("call 09058094583 urgent", "permissive")
False
```

Vale ressaltar que o argumento `mode` pode receber também os valores `1` ou `2`, que correspondem aos dois modos de operação solicitados no desafio. Os _thresholds_ para classificação foram escolhidos para atingir zero falsos negativos (modo agressivo) e zero falsos positivos (modo permissivo) no conjunto de testes.

Adicionalmente, ambos os métodos `prob_spam()` e `is_spam()` também aceitam listas de mensagens como argumentos. Neste caso, retornam uma lista com suas respectivas respostas para cada mensagem individual.

Mais detalhes sobre o uso do pacote disponíveis em https://fabio-a-oliveira.github.io/nuveo-teste-ia/spamdetection, particularmente na página da classe [SpamDetector](https://fabio-a-oliveira.github.io/nuveo-teste-ia/spamdetection/SpamDetector.html). 

_N.B._: caso tenha optado por clonar o repositório, o comando `import spamdetection` somente fica disponível à partir da pasta `02-SMSSpamDetection`, a não ser que se adicione a pasta ao PATH do Python.

### 2. Linha de comando

À partir da linha de comando, o pacote `spamdetection` pode ser utilizado de duas maneiras diferentes, dependendo da quantidade de argumentos.

Com nenhum argumento, o comando abaixo abre o aplicativo _web_ https://nuveo-teste-ia.herokuapp.com/ em uma nova página do _browser_:

```
python -m spamdetection
```

Com um ou dois argumentos, o pacote retorna um diagnóstico da mensagem fornecida, conforme exemplos abaixo:

```
python -m spamdetection "call 09058094583 urgent"
>>> Message is classified as 'ham' with probability 0.58

python -m spamdetection "call 09058094583 urgent" aggressive
>>> Message is classified as 'spam' with probability 0.42

python -m spamdetection "call 09058094583 urgent" 2
>>> Message is classified as 'ham' with probability 0.58
```

Assim como nos demais usos, caso não seja fornecido o segundo argumento indicando o modo de operação, o valor padrão é `"permissive"`.

### 3. Aplicação _web_

Visite https://nuveo-teste-ia.herokuapp.com/ e experimente com algumas mensagens para receber de volta suas classificações e probabilidade de _spam_!


# Documentação do API

Além da descrição do uso neste arquivo `README.md`, foi criada a documentação do API utilizando o `pdoc`. A documentação pode ser consultada em https://fabio-a-oliveira.github.io/nuveo-teste-ia/spamdetection.

Optei pelo uso do `pdoc` (ao invés de uma ferramenta mais utilizada como `sphinx`) porque ele é mais simples e tem a vantagem de criar páginas com o botão `view source`, que permite inspecionar o código diretamente na página.

# Testes

Para realização dos testes unitários, foram utilizados os pacotes `unittest` e `unittest.mock` da biblioteca padrão do Python.

Conforme o padrão para testes unitários com `unittest`, cada teste foi criado como um método de um objeto da classe `TestSpamDetector`. Somente um objeto desta classe foi necessário, já que não havia diferenças no _setup_ entre cada teste.

No método `setUp()`, são criados três objetos da classe `SpamDetector` (sem seleção de modo, com modo agressivo e com mode permissiveo). Este método é repetido antes do início de cada teste, de maneira que os testes individuais não precisam criar estes objetos explicitamente.

Foram criados testes para todos os aspectos ligados ao cumprimento com os requisitos do desafio, incluindo as funcionalidades de `prob_spam()` e `is_spam()`, assim como para a performance esperada de `is_spam()` (zero falsos negativos ou falsos positivos no conjunto de testes, de acordo com o modo de operação). 

Também há testes para verificar a correta inicialização de objetos da classe `SpamDetector` e para verificar a capacidade de seus métodos de identificar que foram chamados com argumentos inválidos.

Foram utilizados _mock objects_, do módulo `unittest.mock`, para a realização de testes verificando que o método `is_spam()` acionou corretamente o método `prob_spam()`, assim como para verificar que a inicialização da classe `SpamDetector` é capaz de identificar quando não há um arquivo contendo um modelo válido para a classificação.

Todos os testes podem ser executados através do comando abaixo, à partir da pasta _02-SMSSpamDetection_:

```
python -m unittest -v
```
