# -*- coding: utf-8 -*-
"""
TSTCalc - A QGIS plugin to calculate true stratigraphic thickness
"""
import os
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import Qt
from qgis.core import Qgis
import numpy as np

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tst_calc_dialog.ui'))

class TSTCalcDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(TSTCalcDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Set validators for input fields
        double_validator = QtGui.QDoubleValidator()
        strike_validator = QtGui.QDoubleValidator(0.0, 360.0, 2)
        dip_validator = QtGui.QDoubleValidator(0.0, 90.0, 2)
        
        # Plane orientation
        self.strikeInput.setValidator(strike_validator)
        self.dipInput.setValidator(dip_validator)
        
        # Point 1 coordinates
        self.x1Input.setValidator(double_validator)
        self.y1Input.setValidator(double_validator)
        self.z1Input.setValidator(double_validator)
        
        # Point 2 coordinates
        self.x2Input.setValidator(double_validator)
        self.y2Input.setValidator(double_validator)
        self.z2Input.setValidator(double_validator)
        
        # Connect signals for live updates
        self.inputs = [self.strikeInput, self.dipInput,
                      self.x1Input, self.y1Input, self.z1Input,
                      self.x2Input, self.y2Input, self.z2Input]
        
        for input_field in self.inputs:
            input_field.textChanged.connect(self.update_result)
        
        self.clearButton.clicked.connect(self.clear_fields)

    def update_result(self):
        """Update the TST calculation whenever any input changes."""
        try:
            # Check if all fields have valid numbers
            if not all(input_field.text() for input_field in self.inputs):
                self.resultLabel.setText("Enter all values...")
                return
                
            # Get plane orientation
            strike = float(self.strikeInput.text())
            dip = float(self.dipInput.text())
            
            # Get coordinates
            x1 = float(self.x1Input.text())
            y1 = float(self.y1Input.text())
            z1 = float(self.z1Input.text())
            x2 = float(self.x2Input.text())
            y2 = float(self.y2Input.text())
            z2 = float(self.z2Input.text())
            
            # Validate ranges
            if not (0 <= strike <= 360):
                self.resultLabel.setText("Strike must be 0-360°")
                return
            if not (0 <= dip <= 90):
                self.resultLabel.setText("Dip must be 0-90°")
                return
            
            # Calculate TST
            tst = self.calculate_tst(strike, dip, x1, y1, z1, x2, y2, z2)
            self.resultLabel.setText(f"True Stratigraphic Thickness: {tst:.1f} meters")
            
        except ValueError:
            self.resultLabel.setText("Invalid number format")

    def calculate_tst(self, strike, dip, x1, y1, z1, x2, y2, z2):
        """Calculate True Stratigraphic Thickness between two points."""
        # Convert angles to radians
        strike_rad = np.radians(strike)
        dip_rad = np.radians(dip)
        
        # Calculate horizontal displacement
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        
        # Calculate horizontal distance
        horiz_dist = np.sqrt(dx**2 + dy**2)
        
        # Calculate apparent dip in direction of horizontal displacement
        # Get bearing of horizontal displacement
        if dx == 0 and dy == 0:
            # Vertical section
            return abs(dz * np.cos(dip_rad))
            
        bearing = np.arctan2(dx, dy)  # Note: arctan2(dx,dy) gives bearing from north
        if bearing < 0:
            bearing += 2 * np.pi
            
        # Calculate apparent dip
        apparent_dip = np.arctan(np.tan(dip_rad) * 
                                np.cos(bearing - strike_rad))
        
        # Calculate TST using vertical distance and horizontal displacement
        tst = dz * np.cos(apparent_dip) - horiz_dist * np.sin(apparent_dip)
        
        return abs(tst)  # Return absolute value as thickness is always positive
    
    def clear_fields(self):
        """Clear all input fields and result."""
        for input_field in self.inputs:
            input_field.clear()
        self.resultLabel.setText("Enter values to calculate TST")
