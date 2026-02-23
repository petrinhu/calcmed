# Histórico de Alterações

Todas as mudanças notáveis neste projeto estão documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [2.0.0] - 2026-02-23

### Alterado
- Interface migrada de Streamlit (web) para PySide6 (Qt), agora como aplicativo desktop nativo.
- Navegação por abas (`QTabWidget`) no lugar do menu lateral do Streamlit.
- Cálculo em tempo real via sinais `valueChanged` do Qt, sem botão "Calcular".
- Tema visual moderno: cabeçalho azul, fundo cinza claro, cards brancos.

### Removido
- Dependências `streamlit` e `pywebview`.
- Arquivo `main_desktop.py` (wrapper do Streamlit, não mais necessário).

### Adicionado
- Dependência `PySide6`.
- Arquivos `.gitignore`, `CLAUDE.md`, `agents.md`, `CONTRIBUTING.md`.

---

## [1.0.0] - 2025

### Adicionado
- Cálculo de dose mínima e máxima em mg/kg/dia, com saída em mg, mL e gotas para frequências de 1×, 2×, 3× e 4× ao dia.
- Cálculo de equivalência entre dois medicamentos em solução com diferentes concentrações e gotas/mL.
- Interface web com Streamlit.
