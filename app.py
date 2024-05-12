import sys
import csv
from PyQt5.QtWidgets import QLabel ,QApplication, QWidget, QPushButton, QLineEdit, QMessageBox

PATH = 'diabetes.csv'

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.store_csv_in_buffer(PATH)
        self.get_min_and_max()
        self.setGeometry(800,600,800,600)
        self.setWindowTitle("Diabete Calculator")
        self.initUI()

    def initUI(self):
        self.calculate_button = QPushButton(self)
        self.calculate_button.setText("Calculate")
        self.calculate_button.move(450,200)
        self.calculate_button.clicked.connect(self.clicked)
        
        self.result_label = QLabel(self)
        self.result_label.setText("Press Button To Calculate")
        self.result_label.move(420,250)

        self.field_names = ["Pregnancies","Glucose","Blood Pressure",
                            "Skin Thickness","Insulin","BMI",
                            "Diabetes Pedigree Function","Age"]
        self.input_fields = []
        self.input_labels = []

        for i in range(8):
            self.input_labels.append(QLabel(self))
            self.input_fields.append(QLineEdit(self))
            self.input_fields[i].move(50, 50+50*i)
            self.input_fields[i].resize(250,20)
            self.input_labels[i].setText(self.field_names[i]+f' {self.min_and_max[self.headers[i]]}')
            self.input_labels[i].move(50, 30+50*i)

    def clicked(self):
        if not self.check_input():
            return

        self.calculate_distance()
        
        #calculate probability
        probability: int = 0
        for value in self.nearest_five:
            probability += value[8]
        probability *= 20
        
        self.result_label.setText(f"Diabetes with {probability}% probability")
        self.update_labels()

    def update_labels(self):
        self.result_label.adjustSize()
    
    def check_input(self) -> bool:
        self.input_numeric = []
        for i,value in enumerate(self.input_fields):
            try:
                float_val = float(value.text())
                if float_val < self.min_and_max[self.headers[i]][0] or float_val > self.min_and_max[self.headers[i]][1]:
                    raise AttributeError
                self.input_numeric.append(float_val)
            except ValueError:
                QMessageBox.warning(self,"Error!", "Inputs Must Be Numeric!")
                return False
            except AttributeError:
                QMessageBox.warning(self,"Error!", "Inputs Are Not In Supported Range!")
                return False
        
        return True
    def calculate_distance(self):
        self.nearest_five = []
        standard_input = self.convert_to_standard(self.input_numeric)
        
        distances = []
        for i, value in enumerate(self.csv_buffer):
            distances.append((i,sum((x - y) ** 2 for x, y in zip(standard_input, self.convert_to_standard(value))) ** 0.5))
        
        #distance has (index, value) pairs, lamda sort according to values
        distances = sorted(distances, key= lambda x:x[1])
        closest_lists_indices = [index for index in distances[:5]]
        self.nearest_five = [self.csv_buffer[index] for index, _ in closest_lists_indices]

    def convert_to_standard(self, values:list):
        standard = []
        for i in range(8):
            min, max = self.min_and_max[self.headers[i]]
            standard.append((values[i] - min) / (max - min))
        
        return standard

    def store_csv_in_buffer(self, path: str):
        self.csv_buffer = []
        self.headers = []

        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            self.headers = next(csv_reader)

            for row in csv_reader:
                self.csv_buffer.append([float(value) for value in row])
        
    def get_min_and_max(self):
        self.min_and_max = {}
        for header in self.headers:
            self.min_and_max[header] = (float('inf'), float('-inf'))
        
        for row in self.csv_buffer:
            for i,value in enumerate(row):
                current_min, current_max = self.min_and_max[self.headers[i]]
                self.min_and_max[self.headers[i]] = (min(current_min, float(value)), max(current_max, float(value)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())

