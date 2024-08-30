# dps_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

def create_dps_tab(config):
    dps_tab = QWidget()
    dps_layout = QVBoxLayout()
    for name, router in config.routers.items():
        dps_layout.addWidget(QLabel(f"DP {name}: {dp.__dict__}"))
    dps_tab.setLayout(dps_layout)
    return dps_tab