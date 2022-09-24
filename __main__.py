import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazAutoPerfecto import App_AutoPerfecto
from src.logica.Logica import Logica

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = Logica()

    app = App_AutoPerfecto(sys.argv, logica)
    sys.exit(app.exec_())