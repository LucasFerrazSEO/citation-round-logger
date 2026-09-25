[English](README.md) · **Português (Brasil)**

# citation-round-logger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`citation-round-logger` é uma ferramenta gratuita e de código aberto, em
linha de comando, para registrar "rodadas de citação": rodar o mesmo
prompt em várias IAs (ChatGPT, Claude, Gemini, Perplexity...), anotar se
cada marca do seu conjunto de comparação apareceu na resposta e em que
posição, e depois calcular o share of voice por marca e por IA. Roda
localmente e guarda as rodadas em um arquivo JSON local.

## Sumário

- [Contexto](#contexto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Perguntas frequentes](#perguntas-frequentes)
- [Limitações](#limitações)
- [Método e origem](#método-e-origem)
- [Como contribuir](#como-contribuir)
- [Autor](#autor)
- [Licença](#licença)

## Contexto

O método é simples e manual de propósito: você roda um prompt real (algo
que um cliente perguntaria, como "melhor agência de SEO em Belo
Horizonte") em cada assistente de IA, lê a resposta com atenção e
registra o que apareceu. Depois de várias rodadas ao longo do tempo, o
relatório mostra quem a IA está recomendando de fato. Não é uma
estimativa, é um registro do que você observou.

**Esta ferramenta não consulta nenhuma IA automaticamente.** Não é um
raspador nem usa API de nenhum assistente. É o formato estruturado do
método, para você não perder o registro de rodadas antigas nem depender
de planilha solta.

## Requisitos

Python 3.9 ou mais recente. Só biblioteca padrão, sem dependência
externa.

## Instalação

```bash
git clone https://github.com/LucasFerrazSEO/citation-round-logger.git
cd citation-round-logger
```

## Uso

**1. Rode o prompt manualmente em uma IA**, fora desta ferramenta. Abra o
ChatGPT, o Claude, o Gemini ou a Perplexity e digite a pergunta real que
um cliente faria.

**2. Leia a resposta e registre o que apareceu.** Se sua marca e um
concorrente apareceram, com posição:

```bash
python citation_round_logger.py log --ia chatgpt --prompt "melhor agencia de seo em bh" \
    --marca "Minha Empresa" --posicao 2 --marca "Concorrente X" --posicao 1
```

Cada `--marca` precisa de um `--posicao` correspondente, na mesma ordem.

**3. Se nenhuma marca do seu conjunto apareceu**, registre como ausente:

```bash
python citation_round_logger.py log --ia perplexity --prompt "melhor agencia de seo em bh" \
    --marca "Minha Empresa" --ausente
```

**4. Repita em outra IA, com o mesmo prompt.** É a comparação entre IAs,
no mesmo prompt, que revela o share of voice de verdade.

**5. Depois de várias rodadas, gere o relatório.**

```bash
python citation_round_logger.py report
```

Exemplo real de saída, depois de duas rodadas registradas:

```
=== citation-round-logger: report (2 rodada(s)) ===

-- Concorrente X --
  chatgpt        1/1 rodada(s) (100% share of voice) | posição média 1.0

-- Lucas Ferraz SEO --
  chatgpt        1/1 rodada(s) (100% share of voice) | posição média 2.0
  claude         0/1 rodada(s) (0% share of voice)
```

**6. Filtre o relatório por uma única IA**, se quiser comparar o
desempenho lá especificamente:

```bash
python citation_round_logger.py report --ia chatgpt
```

**7. Use um arquivo de rodadas separado por projeto ou cliente.** O
`--arquivo` vem antes do subcomando:

```bash
python citation_round_logger.py --arquivo cliente-x-rodadas.json log --ia gemini --prompt "..." --marca "..." --posicao 1
```

## Perguntas frequentes

**citation-round-logger é realmente grátis?**
Sim, código aberto sob licença MIT.

**A ferramenta consulta a IA por mim?**
Não. Você roda o prompt manualmente (ou por outra ferramenta ou API
própria) e registra aqui o que observou. Isso é proposital: evita
depender de chave de API paga e mantém com você o controle de qualidade
da leitura da resposta.

**Quantas rodadas preciso para o share of voice fazer sentido?**
Não há um número mínimo garantido, mas uma rodada só (uma resposta, uma
vez) é uma amostra pequena demais para tirar conclusão. Repita ao longo
do tempo, porque a mesma pergunta pode gerar respostas diferentes em
execuções diferentes da mesma IA.

**Os dados ficam salvos onde?**
Em um arquivo JSON local (`rodadas.json` por padrão, ou o nome que você
passar em `--arquivo`). Nenhum dado é enviado para servidor nenhum.

## Limitações

Registro manual: a qualidade do dado depende de quem roda o prompt e lê a
resposta com cuidado. Não normaliza variação de grafia de marca entre
rodadas. Use sempre o mesmo texto exato para a mesma marca, ou o
relatório vai contar como entidades diferentes.

## Método e origem

Formato aberto do método de "rodada de citação" usado internamente para
medir recomendação por IA em [lucasferrazseo.com](https://lucasferrazseo.com),
sem nenhum dado de cliente, só a estrutura do registro.

## Como contribuir

Relatos de erro e sugestões são bem-vindos pelas [Issues do GitHub](https://github.com/LucasFerrazSEO/citation-round-logger/issues).

## Autor

[Lucas Ferraz](https://lucasferraz.com) é especialista em SEO, criação de sites e Generative Engine Optimization e fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
