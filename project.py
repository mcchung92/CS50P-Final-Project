import re
import sys
import telnetlib
import xlsxwriter as excel
import datetime, time
import pandas as pd


def main():
    ipaddress = getipaddress()
    connection(ipaddress)
    commandsets = SIScommandselection()
    filename = createsavefile()
    SIScommandcheck(filename, commandsets, ipaddress)


def getipaddress():
    """Ask for IP and validate"""
    while True:
        ip = input("What is the IP address of the unit? ")
        try:
            if re.search(r"^[\d]+\.[\d]+\.[\d]+\.[\d]+$", ip):
                octet = ip.split(".")
                # Check each octet to make sure it is in range (0-255)
                for value in octet:
                    if int(value) > 255:
                        break
                else:
                    return ip
            else:
                ...
        except Exception:
            ...


def connection(ip):
    """Tests the connection of the IP address"""

    try:
        tn = telnetlib.Telnet(ip, 23, timeout=0.5)
        print("Connection OK")
        # Sleep implemented to let user know connection was ok
        time.sleep(2)
    except:
        sys.exit("Connection Failed")


def SIScommandselection():
    """Asks users which sets of commands to test"""

    prompt = """
Please select which commands to test, one at a time.
Type "done" once you are finished

1. Input Switches
2. Input Configuration
3. Output Configuration
4. Effect Configuration
5. Miscellaneous

Selected:"""

    print(prompt)
    setcommands = []
    options = ["1", "2", "3", "4", "5"]
    while True:
        choice = input(f"\nWhich would you like to test? ")
        if (choice in options) and (choice not in setcommands):
            setcommands.append(choice)
            print(prompt, *setcommands)
        elif choice == "done":
            return setcommands
        else:
            print(prompt, *setcommands)


def createsavefile():
    """
    Creates a Excel doc with the filename including the current date/time
    Inside the excel doc, it will create worksheets based on the SIS command sets chosen
    """

    savedatetime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = "SIS Comparison_" + savedatetime + ".xlsx"
    workbook = excel.Workbook(filename)
    workbook.close()
    return filename


def SIScommandcheck(filename, commandset, ipaddress):
    """
    Connects to the unit and then sends the selected commands.
    Commands are in an excel sheet "CommandsList.xlsx"
    When sending commands, it will wait for a response from the unit and will compare it with the expected response for that particular command.
    Once finished, it will write and then highlight the correct/incorrect response to the file created previously.
    """

    tn = telnetlib.Telnet(ipaddress, 23, timeout=0.5)
    while True:
        line = tn.read_until(b"\n", timeout=0.5)
        if b"Password:" in line:
            break
    tn.write(("extron\n").encode())
    while True:
        line = tn.read_until(b"\n", timeout=0.5)
        if b"Login Administrator\r\n" in line:
            break

    SISfile = pd.read_excel("CommandsList.xlsx")
    # converts str list to int list
    intcommandset = [eval(i) for i in commandset]
    # Search SET for only the chosen setcommands
    chosensetcommands = SISfile.loc[SISfile["SET"].isin(intcommandset)]
    newSISdf = {}
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []

    for index, row in chosensetcommands.iterrows():
        for number in range(row["Lower Limit"], row["Upper Limit"] + 1):
            sentcommand = row["Command"].replace("varx", str(number))
            expectedresponse = row["Response"].replace(
                "varx", str(number).zfill(int(row["Padding"]))
            )
            tn.write((sentcommand + "\n").encode())
            while True:
                response = tn.read_until(b"\n", timeout=0.5)
                if b"" in response:
                    break
            # Append rows to lists to help create new dataframe late
            col1.append(row["SET"])
            col2.append(row["Command Description"])
            col3.append(sentcommand)
            col4.append("b'" + expectedresponse + "\\r\\n'")
            col5.append(response)
            # Take lists and create dict for dataframe
            newSISdf = {
                "Set": col1,
                "Command Description": col2,
                "Sent Command": col3,
                "Expected Response": col4,
                "Received Response": col5,
            }

    # Create new dataframe
    df = pd.DataFrame(newSISdf)
    newfile = pd.ExcelWriter(filename, engine="xlsxwriter")
    # Write data to excel file created earlier
    df.to_excel(newfile, sheet_name="Output")
    workbook = newfile.book
    worksheet = newfile.sheets["Output"]
    # Formats to help visualize the comparison
    format1 = workbook.add_format({"bg_color": "red"})      # Incorrect response
    format2 = workbook.add_format({"bg_color": "green"})    # Matching response

    worksheet.conditional_format(
        "F2:F200",
        {"type": "cell", "criteria": "!=", "value": "E2:E200", "format": format1},
    )

    worksheet.conditional_format(
        "F2:F200",
        {"type": "cell", "criteria": "==", "value": "E2:E200", "format": format2},
    )
    newfile.close()


if __name__ == "__main__":
    main()
