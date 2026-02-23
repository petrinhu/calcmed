import sys
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QDoubleSpinBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QRadioButton,
    QTabWidget, QVBoxLayout, QWidget,
)


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def _spinbox(min_val: float, max_val: float, default: float,
             step: float, decimals: int = 2) -> QDoubleSpinBox:
    sb = QDoubleSpinBox()
    sb.setMinimum(min_val)
    sb.setMaximum(max_val)
    sb.setValue(default)
    sb.setSingleStep(step)
    sb.setDecimals(decimals)
    sb.setAlignment(Qt.AlignmentFlag.AlignRight)
    return sb


def _sep() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setObjectName("sep")
    return line


# ---------------------------------------------------------------------------
# Cards de resultado
# ---------------------------------------------------------------------------

class DoseCard(QFrame):
    """Exibe os resultados de dose mínima ou máxima."""

    def __init__(self, title: str, color: str) -> None:
        super().__init__()
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {color};")
        layout.addWidget(title_lbl)

        self._total = QLabel()
        self._total.setObjectName("totalVal")
        layout.addWidget(self._total)

        layout.addWidget(_sep())

        self._freq = QLabel()
        self._freq.setObjectName("freqVal")
        layout.addWidget(self._freq)
        layout.addStretch()

    def update(self, mg: float, ml: float, g: float,
               ml1: float, ml2: float, ml3: float, ml4: float,
               g1: float, g2: float, g3: float, g4: float) -> None:
        self._total.setText(f"{mg} mg/dia  ·  {ml} mL/dia  ·  {g} gotas/dia")
        self._freq.setText(
            f"1×/dia  →  {g1} gotas   ({ml1} mL)\n"
            f"2×/dia  →  {g2} gotas   ({ml2} mL)\n"
            f"3×/dia  →  {g3} gotas   ({ml3} mL)\n"
            f"4×/dia  →  {g4} gotas   ({ml4} mL)"
        )


class EquivCard(QFrame):
    """Exibe os dados de um medicamento na tela de equivalência."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(8)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("cardTitle")
        layout.addWidget(title_lbl)

        self._dose = QLabel()
        self._dose.setObjectName("totalVal")
        layout.addWidget(self._dose)

        self._conc = QLabel()
        layout.addWidget(self._conc)

        self._mg = QLabel()
        self._mg.setObjectName("freqVal")
        layout.addWidget(self._mg)
        layout.addStretch()

    def update(self, gotas: float, ml: float, conc: float,
               mg: float, mantido: bool = False) -> None:
        self._dose.setText(f"{gotas:.2f} gotas   ·   {ml:.2f} mL")
        self._conc.setText(f"Concentração: {conc} mg/mL")
        suffix = "  (mantido)" if mantido else ""
        self._mg.setText(f"Princípio ativo: {mg:.2f} mg{suffix}")


# ---------------------------------------------------------------------------
# Abas
# ---------------------------------------------------------------------------

class DoseTab(QWidget):
    """Aba de cálculo de dose mínima e máxima."""

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 16)
        layout.setSpacing(20)

        # --- Inputs ---
        group = QGroupBox("Dados do Medicamento e Paciente")
        from PySide6.QtWidgets import QGridLayout
        grid = QGridLayout(group)
        grid.setSpacing(12)
        grid.setColumnMinimumWidth(0, 230)
        grid.setColumnMinimumWidth(1, 140)

        self.conc      = _spinbox(0.01, 99999, 100.0, 0.1)
        self.gotas_ml  = _spinbox(1.0,  100.0,  20.0, 1.0, 0)
        self.peso      = _spinbox(0.01,  500.0,  20.0, 0.5)
        self.dose_min  = _spinbox(0.01, 9999.0,   2.5, 0.1)
        self.dose_max  = _spinbox(0.01, 9999.0,  25.0, 0.1)

        fields = [
            ("Concentração (mg/mL)",     self.conc),
            ("Gotas por mL",             self.gotas_ml),
            ("Peso do paciente (kg)",    self.peso),
            ("Dose mínima (mg/kg/dia)",  self.dose_min),
            ("Dose máxima (mg/kg/dia)",  self.dose_max),
        ]
        for row, (text, widget) in enumerate(fields):
            lbl = QLabel(text)
            lbl.setObjectName("inputLabel")
            grid.addWidget(lbl, row, 0)
            grid.addWidget(widget, row, 1)

        layout.addWidget(group)

        # --- Result cards ---
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        self.card_min = DoseCard("Dose Mínima", "#2563EB")
        self.card_max = DoseCard("Dose Máxima", "#DC2626")
        cards_row.addWidget(self.card_min)
        cards_row.addWidget(self.card_max)
        layout.addLayout(cards_row)
        layout.addStretch()

        for sb in [self.conc, self.gotas_ml, self.peso, self.dose_min, self.dose_max]:
            sb.valueChanged.connect(self._recalc)
        self._recalc()

    def _recalc(self) -> None:
        conc = self.conc.value()
        gml  = self.gotas_ml.value()
        peso = self.peso.value()

        def calc(dose_mg_kg: float) -> dict:
            mg = round(dose_mg_kg * peso, 2)
            ml = round(mg / conc, 2)
            g  = round(ml * gml, 2)
            return dict(
                mg=mg, ml=ml, g=g,
                ml1=ml,           ml2=round(ml / 2, 2),
                ml3=round(ml / 3, 2), ml4=round(ml / 4, 2),
                g1=g,             g2=round(g / 2, 2),
                g3=round(g / 3, 2),  g4=round(g / 4, 2),
            )

        for card, dose_kg in [
            (self.card_min, self.dose_min.value()),
            (self.card_max, self.dose_max.value()),
        ]:
            d = calc(dose_kg)
            card.update(**d)


class EquivTab(QWidget):
    """Aba de equivalência entre medicamentos."""

    def __init__(self) -> None:
        super().__init__()
        from PySide6.QtWidgets import QGridLayout

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 16)
        layout.setSpacing(20)

        # --- Med A + B ---
        meds_row = QHBoxLayout()
        meds_row.setSpacing(16)

        group_a = QGroupBox("Medicamento A  (origem)")
        grid_a = QGridLayout(group_a)
        grid_a.setSpacing(12)
        grid_a.setColumnMinimumWidth(0, 180)
        self.conc_a   = _spinbox(0.01, 99999, 100.0, 0.1)
        self.gotas_a  = _spinbox(1.0,  100.0,  20.0, 1.0, 0)
        grid_a.addWidget(QLabel("Concentração (mg/mL)"), 0, 0)
        grid_a.addWidget(self.conc_a, 0, 1)
        grid_a.addWidget(QLabel("Gotas por mL"), 1, 0)
        grid_a.addWidget(self.gotas_a, 1, 1)
        meds_row.addWidget(group_a)

        group_b = QGroupBox("Medicamento B  (destino)")
        grid_b = QGridLayout(group_b)
        grid_b.setSpacing(12)
        grid_b.setColumnMinimumWidth(0, 180)
        self.conc_b   = _spinbox(0.01, 99999,  50.0, 0.1)
        self.gotas_b  = _spinbox(1.0,  100.0,  25.0, 1.0, 0)
        grid_b.addWidget(QLabel("Concentração (mg/mL)"), 0, 0)
        grid_b.addWidget(self.conc_b, 0, 1)
        grid_b.addWidget(QLabel("Gotas por mL"), 1, 0)
        grid_b.addWidget(self.gotas_b, 1, 1)
        meds_row.addWidget(group_b)

        layout.addLayout(meds_row)

        # --- Dose de A ---
        dose_group = QGroupBox("Dose utilizada no Medicamento A")
        dose_vbox = QVBoxLayout(dose_group)
        dose_vbox.setSpacing(10)

        radio_row = QHBoxLayout()
        self.radio_gotas = QRadioButton("Em Gotas")
        self.radio_ml    = QRadioButton("Em mL")
        self.radio_gotas.setChecked(True)
        radio_row.addWidget(self.radio_gotas)
        radio_row.addWidget(self.radio_ml)
        radio_row.addStretch()
        dose_vbox.addLayout(radio_row)

        input_row = QHBoxLayout()
        self.dose_lbl = QLabel("Gotas de A:")
        self.dose_val = _spinbox(0.0, 99999, 20.0, 1.0, 1)
        input_row.addWidget(self.dose_lbl)
        input_row.addWidget(self.dose_val)
        input_row.addStretch()
        dose_vbox.addLayout(input_row)
        layout.addWidget(dose_group)

        # --- Result cards ---
        res_row = QHBoxLayout()
        res_row.setSpacing(16)
        self.card_a = EquivCard("Medicamento A  (original)")
        self.card_b = EquivCard("Equivalente — Medicamento B")
        res_row.addWidget(self.card_a)
        res_row.addWidget(self.card_b)
        layout.addLayout(res_row)
        layout.addStretch()

        for sb in [self.conc_a, self.gotas_a, self.conc_b, self.gotas_b, self.dose_val]:
            sb.valueChanged.connect(self._recalc)
        self.radio_gotas.toggled.connect(self._on_radio)
        self._recalc()

    def _on_radio(self) -> None:
        is_gotas = self.radio_gotas.isChecked()
        self.dose_lbl.setText("Gotas de A:" if is_gotas else "mL de A:")
        self.dose_val.setSingleStep(1.0 if is_gotas else 0.1)
        self._recalc()

    def _recalc(self) -> None:
        val     = self.dose_val.value()
        gotas_a = self.gotas_a.value()

        if self.radio_gotas.isChecked():
            ml_a = val / gotas_a
            g_a  = val
        else:
            ml_a = val
            g_a  = val * gotas_a

        mg_a  = ml_a * self.conc_a.value()
        ml_b  = mg_a / self.conc_b.value()
        g_b   = ml_b * self.gotas_b.value()

        self.card_a.update(g_a, ml_a, self.conc_a.value(), mg_a)
        self.card_b.update(g_b, ml_b, self.conc_b.value(), mg_a, mantido=True)


# ---------------------------------------------------------------------------
# Janela principal
# ---------------------------------------------------------------------------

STYLESHEET = """
* {
    font-family: "Cantarell", "Ubuntu", "Noto Sans", "DejaVu Sans", "Arial", sans-serif;
    font-size: 14px;
    color: #111827;
}
QMainWindow, QWidget {
    background-color: #F3F6FB;
}

/* ── Header ─────────────────────────────────────────── */
#header {
    background-color: #1E40AF;
}
#appTitle {
    color: #FFFFFF;
    font-size: 19px;
    font-weight: bold;
    background-color: transparent;
    padding: 15px 24px;
}

/* ── Tabs ────────────────────────────────────────────── */
QTabWidget::pane {
    border: none;
    background-color: #F3F6FB;
}
QTabBar {
    background-color: #1E40AF;
}
QTabBar::tab {
    background-color: transparent;
    color: #BFDBFE;
    padding: 10px 28px;
    border: none;
    font-size: 13px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #F3F6FB;
    color: #1E40AF;
    font-weight: bold;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:hover:!selected {
    background-color: rgba(255, 255, 255, 0.18);
    color: #FFFFFF;
}

/* ── Group boxes ─────────────────────────────────────── */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    margin-top: 14px;
    padding: 16px 14px 14px 14px;
    font-size: 13px;
    font-weight: bold;
    color: #374151;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
    color: #1E40AF;
}

/* ── Result cards ────────────────────────────────────── */
#card {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
}
#cardTitle {
    font-size: 14px;
    font-weight: bold;
    color: #1E40AF;
}
#totalVal {
    font-size: 14px;
    font-weight: bold;
    color: #111827;
}
#freqVal {
    font-size: 13px;
    color: #4B5563;
    line-height: 1.7;
}
#sep {
    border: none;
    border-top: 1px solid #E5E7EB;
    margin: 2px 0;
}

/* ── Inputs ──────────────────────────────────────────── */
#inputLabel {
    color: #374151;
}
QDoubleSpinBox {
    background-color: #F9FAFB;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    padding: 5px 8px;
    min-width: 120px;
    color: #111827;
}
QDoubleSpinBox:focus {
    border: 2px solid #3B82F6;
    background-color: #FFFFFF;
}
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    width: 18px;
    border: none;
    background-color: transparent;
}

/* ── Radio buttons ───────────────────────────────────── */
QRadioButton {
    background-color: transparent;
    color: #374151;
    spacing: 6px;
    font-size: 13px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
}
QRadioButton::indicator:unchecked {
    background-color: #FFFFFF;
    border: 2px solid #D1D5DB;
}
QRadioButton::indicator:checked {
    background-color: #3B82F6;
    border: 2px solid #3B82F6;
}

/* ── Footer ──────────────────────────────────────────── */
#footer {
    color: #9CA3AF;
    font-size: 11px;
    padding: 6px 0 8px 0;
    background-color: transparent;
}
"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Calculadora de Medicamentos")
        self.setMinimumSize(820, 580)
        self.setStyleSheet(STYLESHEET)
        self._build()

    def _build(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # Cabeçalho
        header = QFrame()
        header.setObjectName("header")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("💊  Calculadora de Medicamentos")
        title.setObjectName("appTitle")
        h_layout.addWidget(title)
        h_layout.addStretch()
        vbox.addWidget(header)

        # Abas
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(DoseTab(),  "  Cálculo de Dose  ")
        tabs.addTab(EquivTab(), "  Equivalência entre Medicamentos  ")
        vbox.addWidget(tabs, 1)

        # Rodapé
        footer = QLabel(
            f"© Petrus Costa {datetime.now().year}  ·  Calculadora para soluções medicamentosas."
        )
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(footer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.resize(920, 660)
    win.show()
    sys.exit(app.exec())
