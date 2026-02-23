# Agentes

Este arquivo orienta agentes de IA (ex.: Claude via GitHub Actions) ao operar neste repositório.

## Contexto

**Calcmed** é uma calculadora farmacológica de medicamentos para profissionais de saúde, escrita em Python com interface desktop nativa via PySide6 (Qt). Toda a interface e documentação estão em português (pt-BR).

## Como executar e testar

Não há suíte de testes automatizados. A verificação é feita manualmente:

```bash
pip install -r requiriments.txt
python calc.py
```

Valide qualquer alteração de cálculo testando com valores de entrada conhecidos e conferindo os resultados esperados.

## Restrições importantes

- **Precisão médica é crítica.** Qualquer alteração em uma fórmula dentro de `calc.py` deve ser matematicamente correta e farmacologicamente embasada. Em caso de dúvida, não altere a fórmula — registre a questão em um comentário ou na descrição do PR.
- **Não renomeie `requiriments.txt`** — nome mantido intencionalmente por razões históricas.
- Compatibilidade com **Python 3.8+** deve ser mantida.
- Toda a lógica da aplicação está em `calc.py`.

## Diretrizes para pull requests

- Descreva explicitamente qualquer alteração de fórmula ou cálculo.
- A interface deve permanecer em português (pt-BR).
- Não adicione dependências sem justificativa clara na descrição do PR.
