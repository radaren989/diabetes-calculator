import sys
import csv
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

PATH = 'diabetes.csv'
PROCESSED_PATH = 'processed_diabetes.csv'

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.get_min_and_max()
        self.write_proccesed_csv()
        self.setGeometry(800, 600, 800, 600)
        self.setWindowTitle("Diabetes Calculator")
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: rgb(49, 54, 63);")

        main_layout = QVBoxLayout()
        input_layout = QGridLayout()

        self.field_names = ["Pregnancies", "Glucose", "Blood Pressure",
                            "Skin Thickness", "Insulin", "BMI",
                            "Diabetes Pedigree Function", "Age"]
        self.input_fields = []
        self.input_labels = []

        for i in range(8):
            input_label = QLabel(self)
            input_field = QLineEdit(self)
            
            input_label.setText(self.field_names[i] + f' {self.min_and_max[self.headers[i]]}')
            input_label.setStyleSheet("color: white; font-size: 14px;")
            input_field.setStyleSheet("background-color: white; color: black;")
            input_field.setFixedHeight(40) 
            
            self.input_labels.append(input_label)
            self.input_fields.append(input_field)
            
            input_layout.addWidget(input_label, i, 0)
            input_layout.addWidget(input_field, i, 1)

        self.PatientNumber_field = QLineEdit(self)
        self.PatientNumber_label = QLabel(self)
        
        self.PatientNumber_label.setText("Patient Number")
        self.PatientNumber_label.setStyleSheet("color: white; font-size: 14px;")
        self.PatientNumber_field.setStyleSheet("background-color: white; color black;")
        self.PatientNumber_field.setFixedHeight(40)

        input_layout.addWidget(self.PatientNumber_label, 8,0)
        input_layout.addWidget(self.PatientNumber_field, 8,1)

        main_layout.addLayout(input_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.calculate_button = QPushButton(self)
        self.calculate_button.setText("Calculate")
        self.calculate_button.setStyleSheet("background-color: green; color: white; font-size: 20px; padding: 20px;")
        self.calculate_button.clicked.connect(self.clicked)
        main_layout.addWidget(self.calculate_button, alignment=Qt.AlignHCenter)
        
        self.result_label = QLabel(self)
        self.result_label.setText("Press Button To Calculate")
        self.result_label.setStyleSheet("color: white; font-size: 14px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label, alignment=Qt.AlignHCenter)
        
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(main_layout)

    def clicked(self):
        if not self.check_input():
            return

        self.calculate_distance()
        
        # calculate probability
        outcomes = 0
        for value in self.nearest:
            outcomes += int(value[8])
        probability = (outcomes / self.patient_number) * 100
        
        self.result_label.setText(f"Diabetes with {probability}% probability")
        self.update_labels()

    def update_labels(self):
        self.result_label.adjustSize()
    
    def check_input(self) -> bool:
        self.input_numeric = []
        for i, value in enumerate(self.input_fields):
            try:
                float_val = float(value.text())
                if float_val < self.min_and_max[self.headers[i]][0] or float_val > self.min_and_max[self.headers[i]][1]:
                    raise AttributeError
                self.input_numeric.append(float_val)
            except ValueError:
                QMessageBox.warning(self, "Error!", "Inputs Must Be Numeric!")
                return False
            except AttributeError:
                QMessageBox.warning(self, "Error!", "Inputs Are Not In Supported Range!")
                return False
        
        try:
            self.patient_number = int(self.PatientNumber_field.text())
            if self.patient_number <= 0:
                raise AttributeError
        except ValueError:
                QMessageBox.warning(self, "Error!", "Patient Number Must Be Numeric!")
                return False
        except AttributeError:
                QMessageBox.warning(self, "Error!", "Inputs Are Not In Supported Range!")
                return False

        return True

    
    def write_proccesed_csv(self):
        with open(PATH, 'r' ) as readFile:
            reader = csv.reader(readFile)
            with open(PROCESSED_PATH, 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(next(reader))
            
                for data in reader:
                    float_data = [float(value) for value in data]
                    float_data = float_data[:-1]
                    processed = self.convert_to_standard(float_data)
                    writer.writerow(processed)

    def calculate_distance(self):
        self.nearest = []
        standard_input = self.convert_to_standard(self.input_numeric)

        distances = []
        with open(PROCESSED_PATH, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                float_row = [float(val) for val in row]
                distance = sum((x - y) ** 2 for x, y in zip(standard_input, float_row)) ** 0.5
                distances.append((i,distance))
        
        #distance has (index, value) pairs, lamda sort according to values
        distances = sorted(distances, key= lambda x:x[1])
        closest_lists_indices = [index for index,_ in distances[:self.patient_number]]
        with open(PATH, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                if i in closest_lists_indices:
                    self.nearest.append(row)
        
        print(self.nearest)

    def convert_to_standard(self, values: list):
        standard = []
        for i in range(8):
            min_val, max_val = self.min_and_max[self.headers[i]]
            standard.append((values[i] - min_val) / (max_val - min_val))
        
        return standard

    #def store_csv_in_buffer(self, path: str):
    #    self.csv_buffer = []
    #    self.headers = []

     #   with open(path, 'r') as file:
     #       csv_reader = csv.reader(file)
     #       self.headers = next(csv_reader)

      #      for row in csv_reader:
      #          self.csv_buffer.append([float(value) for value in row])
        
    def get_min_and_max(self):
        self.min_and_max = {}
        
        with open(PATH, 'r') as file:
            reader = csv.reader(file)
            self.headers = next(reader)
            
            for header in self.headers:
                self.min_and_max[header] = (float('inf'), float('-inf'))
            
            for row in reader:
                for i, value in enumerate(row):
                    current_min, current_max = self.min_and_max[self.headers[i]]
                    self.min_and_max[self.headers[i]] = (min(current_min, float(value)), max(current_max, float(value)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
