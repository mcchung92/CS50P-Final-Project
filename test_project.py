from project import connection, createsavefile
import datetime
import pytest

def main():
    test_connection()
    test_createsavefile()

def test_connection():
    with pytest.raises(SystemExit):
        connection("")
    with pytest.raises(SystemExit):
        connection("1.1.1.1")
    with pytest.raises(SystemExit):
        connection("hostname")

def test_createsavefile():
    savetime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    assert createsavefile() == "SIS Comparison_" + savetime + ".xlsx"


if __name__=="__main__":
    main()