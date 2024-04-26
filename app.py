import sys
import random
from PyQt5.QtWidgets import QLabel ,QApplication, QWidget, QPushButton

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(800,600,800,600)
        self.setWindowTitle("Diabete Calculator")
        self.initUI()

    def initUI(self):
        self.calculate_button = QPushButton(self)
        self.calculate_button.setText("Calculate")
        self.calculate_button.move(380,300)
        self.calculate_button.clicked.connect(self.clicked)
        
        self.result_label = QLabel(self)
        self.result_label.setText("Press Button To Calculate")
        self.result_label.move(350,340)

    def clicked(self):
        prob: int = random.randint(0,10) * 10
        self.result_label.setText(f"Diabetes With {prob} probability")
        self.update()

    def update(self):
        self.result_label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())

