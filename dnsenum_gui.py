import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton,
                             QFileDialog, QVBoxLayout, QSpinBox, QMessageBox)
import subprocess

class DnsenumGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # General Layout
        self.layout = QVBoxLayout()

        # Domain Input
        self.domain_label = QLabel('Domain:')
        self.domain_input = QLineEdit(self)

        # DNS Server
        self.dnsserver_label = QLabel('DNS Server:')
        self.dnsserver_input = QLineEdit(self)

        # General Options
        self.enum_option = QCheckBox('--enum')
        self.noreverse_option = QCheckBox('--noreverse')
        self.nocolor_option = QCheckBox('--nocolor')
        self.private_option = QCheckBox('--private')
        self.verbose_option = QCheckBox('--verbose')

        # Timeout
        self.timeout_label = QLabel('Timeout:')
        self.timeout_input = QSpinBox(self)
        self.timeout_input.setValue(10)

        # Threads
        self.threads_label = QLabel('Threads:')
        self.threads_input = QSpinBox(self)
        self.threads_input.setValue(1)

        # Google Scraping Options
        self.pages_label = QLabel('Google Pages:')
        self.pages_input = QSpinBox(self)
        self.pages_input.setValue(5)

        self.scrap_label = QLabel('Google Scraping:')
        self.scrap_input = QSpinBox(self)
        self.scrap_input.setValue(15)

        # Brute Force Options
        self.file_label = QLabel('Subdomains File:')
        self.file_input = QLineEdit(self)
        self.file_button = QPushButton('Browse', self)
        self.file_button.clicked.connect(self.browse_file)

        self.recursion_option = QCheckBox('--recursion')

        # Whois Netrange Options
        self.delay_label = QLabel('Delay:')
        self.delay_input = QSpinBox(self)
        self.delay_input.setValue(3)

        self.whois_option = QCheckBox('--whois')

        # Reverse Lookup Options
        self.exclude_label = QLabel('Exclude:')
        self.exclude_input = QLineEdit(self)

        # Output Options
        self.output_label = QLabel('Output File:')
        self.output_input = QLineEdit(self)
        self.output_button = QPushButton('Browse', self)
        self.output_button.clicked.connect(self.browse_output)

        # Run Button
        self.run_button = QPushButton('Run dnsenum', self)
        self.run_button.clicked.connect(self.run_dnsenum)

        # Add widgets to layout
        self.layout.addWidget(self.domain_label)
        self.layout.addWidget(self.domain_input)
        self.layout.addWidget(self.dnsserver_label)
        self.layout.addWidget(self.dnsserver_input)
        self.layout.addWidget(self.enum_option)
        self.layout.addWidget(self.noreverse_option)
        self.layout.addWidget(self.nocolor_option)
        self.layout.addWidget(self.private_option)
        self.layout.addWidget(self.verbose_option)
        self.layout.addWidget(self.timeout_label)
        self.layout.addWidget(self.timeout_input)
        self.layout.addWidget(self.threads_label)
        self.layout.addWidget(self.threads_input)
        self.layout.addWidget(self.pages_label)
        self.layout.addWidget(self.pages_input)
        self.layout.addWidget(self.scrap_label)
        self.layout.addWidget(self.scrap_input)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_input)
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.recursion_option)
        self.layout.addWidget(self.delay_label)
        self.layout.addWidget(self.delay_input)
        self.layout.addWidget(self.whois_option)
        self.layout.addWidget(self.exclude_label)
        self.layout.addWidget(self.exclude_input)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_input)
        self.layout.addWidget(self.output_button)
        self.layout.addWidget(self.run_button)

        # Set main layout
        self.setLayout(self.layout)

        # Set window title
        self.setWindowTitle('Dnsenum GUI')

    def browse_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '/home')
            if file_name:
                self.file_input.setText(file_name)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open file: {e}')

    def browse_output(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '/home')
            if file_name:
                self.output_input.setText(file_name)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save file: {e}')

    def run_dnsenum(self):
        try:
            domain = self.domain_input.text().strip()
            if not domain:
                raise ValueError("Domain is required")

            dnsserver = self.dnsserver_input.text().strip()
            timeout = self.timeout_input.value()
            threads = self.threads_input.value()
            pages = self.pages_input.value()
            scrap = self.scrap_input.value()
            file = self.file_input.text().strip()
            delay = self.delay_input.value()
            exclude = self.exclude_input.text().strip()
            output = self.output_input.text().strip()

            options = []

            if self.enum_option.isChecked():
                options.append('--enum')
            if self.noreverse_option.isChecked():
                options.append('--noreverse')
            if self.nocolor_option.isChecked():
                options.append('--nocolor')
            if self.private_option.isChecked():
                options.append('--private')
            if self.verbose_option.isChecked():
                options.append('--verbose')
            if dnsserver:
                options.extend(['--dnsserver', dnsserver])
            if timeout:
                options.extend(['--timeout', str(timeout)])
            if threads:
                options.extend(['--threads', str(threads)])
            if pages:
                options.extend(['--pages', str(pages)])
            if scrap:
                options.extend(['--scrap', str(scrap)])
            if file:
                options.extend(['--file', file])
            if self.recursion_option.isChecked():
                options.append('--recursion')
            if delay:
                options.extend(['--delay', str(delay)])
            if self.whois_option.isChecked():
                options.append('--whois')
            if exclude:
                options.extend(['--exclude', exclude])
            if output:
                options.extend(['--output', output])

            command = ['dnsenum'] + options + [domain]

            # Print the command (for debugging purposes)
            print('Running command:', ' '.join(command))

            # Execute the command
            process = subprocess.run(command, capture_output=True, text=True)

            # Display the output
            QMessageBox.information(self, 'Dnsenum Output', process.stdout)

            # Display any errors
            if process.stderr:
                QMessageBox.warning(self, 'Dnsenum Error', process.stderr)
        except ValueError as ve:
            QMessageBox.warning(self, 'Input Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DnsenumGUI()
    ex.show()
    sys.exit(app.exec_())
