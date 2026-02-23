# CLAUDE.md

Este arquivo orienta o Claude Code (claude.ai/code) ao trabalhar neste repositório.

## Visão geral

**Calcmed** é uma calculadora farmacológica de medicamentos para profissionais de saúde, escrita em Python com interface desktop nativa via PySide6 (Qt). Toda a interface e documentação estão em português (pt-BR).

## Como executar

```bash
# Instalar dependências (atenção: o arquivo se chama "requiriments.txt", não "requirements.txt")
pip install -r requiriments.txt

# Executar
python calc.py
```

## Arquitetura

Toda a aplicação está em `calc.py`. Estrutura de classes:

| Classe | Função |
|---|---|
| `MainWindow` | Janela principal (`QMainWindow`): barra de cabeçalho, `QTabWidget`, rodapé |
| `DoseTab` | Aba 1 — entradas de cálculo de dose mínima/máxima + dois `DoseCard` |
| `EquivTab` | Aba 2 — entradas de equivalência entre medicamentos + dois `EquivCard` |
| `DoseCard` | Card de resultado com total diário e quebra por frequência |
| `EquivCard` | Card de resultado com gotas/mL/princípio ativo de um medicamento |

Os cálculos são disparados em tempo real via sinal `valueChanged` do PySide6, conectados aos métodos `_recalc()`. Não há botão "Calcular".

A constante `STYLESHEET` (final do arquivo) controla todo o tema visual — cabeçalho azul (`#1E40AF`), fundo cinza claro e cards brancos. Altere-a para mudar a aparência.

## Restrições importantes

- **Precisão médica é crítica.** Não modifique as fórmulas em `_recalc()` sem verificar a correção matemática e farmacológica.
- **Não renomeie `requiriments.txt`** — nome mantido intencionalmente por razões históricas.
- Compatibilidade com Python 3.8+ deve ser mantida.
- Não há testes automatizados — valide alterações manualmente executando o app com valores conhecidos.
