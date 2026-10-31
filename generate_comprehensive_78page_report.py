import os
import sys
from report_builder_base import AcademicReportBuilder
from report_chapters_part1 import generate_front_matter_and_ch1
from report_chapters_part2 import generate_ch2_and_ch3
from report_chapters_part3 import generate_ch4_and_ch5
from report_chapters_part4 import generate_ch6_ch7_ch8_and_appendices

def build_complete_report():
    output_filename = "PROJECT_REPORT_75_PAGES.docx"
    print(f"Initializing AcademicReportBuilder for {output_filename}...")
    builder = AcademicReportBuilder(filename=output_filename)

    print("Generating Front Matter & Chapter 1 (Pages 1 to 13)...")
    generate_front_matter_and_ch1(builder)

    print("Generating Chapter 2 & Chapter 3 (Pages 14 to 36)...")
    generate_ch2_and_ch3(builder)

    print("Generating Chapter 4 & Chapter 5 (Pages 37 to 61)...")
    generate_ch4_and_ch5(builder)

    print("Generating Chapter 6, Chapter 7, Chapter 8, References & Appendices (Pages 62 to 79)...")
    generate_ch6_ch7_ch8_and_appendices(builder)

    print("Saving document...")
    builder.save()
    print("Document successfully compiled!")

if __name__ == "__main__":
    build_complete_report()
