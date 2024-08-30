# routers_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

def create_routers_tab(config):
    routers_tab = QWidget()
    routers_layout = QVBoxLayout()
    for name, router in config.routers.items():
        routers_layout.addWidget(QLabel(f"Router {name}: {router.__dict__}"))
    routers_tab.setLayout(routers_layout)
    return routers_tab