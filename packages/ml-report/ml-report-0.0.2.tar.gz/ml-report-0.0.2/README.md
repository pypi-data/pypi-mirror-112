# Purpose

**ml-report** is a Python module providing in-depth metrics and diagnostics for training and evaluating Machine Learning models.


# Installation

    pip install ml-report


# Usage

**ml-report** is designed to be powerful yet lightweight. 

    from ml_report import Report
    report = Report(...)
    report.fit(X, y)
    report.build_report()
