**English** · [Português (Brasil)](README.pt-BR.md)

# citation-round-logger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`citation-round-logger` is a free, open source command-line tool for
logging "citation rounds": you run the same prompt in several AI
assistants (ChatGPT, Claude, Gemini, Perplexity...), note whether each
brand in your comparison set appeared in the answer and in which
position, and then calculate share of voice per brand and per AI. It runs
locally and stores the rounds in a local JSON file. The tool prints its
report in Brazilian Portuguese.

## Contents

- [Background](#background)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

The method is simple and manual on purpose. You run a real prompt
(something a customer would ask, such as "melhor agência de SEO em Belo
Horizonte") in each AI assistant, read the answer carefully and record
what appeared. After several rounds over time, the report shows who the
AI is actually recommending. It is not an estimate, it is a record of
what you observed.

**This tool does not query any AI automatically.** It is not a scraper
and it does not use any assistant's API. It is the structured format of
the method, so you do not lose the record of past rounds or depend on a
loose spreadsheet.

## Requirements

Python 3.9 or newer. Standard library only, no external dependencies.

## Installation

```bash
git clone https://github.com/LucasFerrazSEO/citation-round-logger.git
cd citation-round-logger
```

## Usage

**1. Run the prompt manually in an AI assistant**, outside this tool.
Open ChatGPT, Claude, Gemini or Perplexity and type the real question a
customer would ask.

**2. Read the answer and log what appeared.** If your brand and a
competitor appeared, with their positions:

```bash
python citation_round_logger.py log --ia chatgpt --prompt "melhor agencia de seo em bh" \
    --marca "Minha Empresa" --posicao 2 --marca "Concorrente X" --posicao 1
```

Each `--marca` needs a matching `--posicao`, in the same order.

**3. If no brand from your set appeared**, log it as absent:

```bash
python citation_round_logger.py log --ia perplexity --prompt "melhor agencia de seo em bh" \
    --marca "Minha Empresa" --ausente
```

**4. Repeat in another AI with the same prompt.** Comparing AIs on the
same prompt is what shows the real share of voice.

**5. After several rounds, generate the report.**

```bash
python citation_round_logger.py report
```

A real output example, after two logged rounds:

```
=== citation-round-logger: report (2 rodada(s)) ===

-- Concorrente X --
  chatgpt        1/1 rodada(s) (100% share of voice) | posição média 1.0

-- Lucas Ferraz SEO --
  chatgpt        1/1 rodada(s) (100% share of voice) | posição média 2.0
  claude         0/1 rodada(s) (0% share of voice)
```

**6. Filter the report by a single AI** if you want to compare
performance there specifically:

```bash
python citation_round_logger.py report --ia chatgpt
```

**7. Use a separate rounds file per project or client.** `--arquivo` goes
before the subcommand:

```bash
python citation_round_logger.py --arquivo cliente-x-rodadas.json log --ia gemini --prompt "..." --marca "..." --posicao 1
```

## FAQ

**Is citation-round-logger really free?**
Yes. It is open source under the MIT license.

**Does the tool query the AI for me?**
No. You run the prompt manually (or through another tool or your own API
setup) and log here what you observed. This is on purpose: it avoids
depending on a paid API key and keeps the quality control of reading the
answer with you.

**How many rounds do I need for share of voice to make sense?**
There is no guaranteed minimum, but a single round (one answer, one time)
is too small a sample to draw a conclusion. Repeat over time, because the
same question can produce different answers in different runs of the
same AI.

**Where is the data stored?**
In a local JSON file (`rodadas.json` by default, or the name you pass in
`--arquivo`). No data is sent to any server.

## Limitations

Logging is manual: data quality depends on whoever runs the prompt and
reads the answer carefully. Brand spelling variations across rounds are
not normalized. Always use the exact same text for the same brand, or the
report will count them as different entities.

## Methodology

This is the open format of the "citation round" method used internally
to measure AI recommendations at
[lucasferrazseo.com](https://lucasferrazseo.com), with no client data,
only the structure of the record.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/citation-round-logger/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
