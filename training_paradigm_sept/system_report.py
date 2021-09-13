"""
system_report() prints a system report of calibrations and tastes
"""

def system_report(lines):
    line_no = 1
    print(67 * "-")
    print("SYSTEM REPORT:")
    for i in lines:
        print("line: " + str(line_no) + "    opentime: " + str(i.opentime) + " s" + "   taste: " + str(i.taste))
        line_no = line_no + 1