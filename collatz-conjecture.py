# simple program to test the collatz conjecture

def collatz(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1
def test_collatz(n):
    while n != 1:
        print(n, end=' ')
        n = collatz(n)
    print("Conjecture holds for this number.")
# test the function with a few numbers

while True:
    testnum = str(input("Enter a number to test the Collatz conjecture. Enter STOP to quit: "))
    if testnum.upper() == "STOP":
        break
    elif testnum.isdigit():
        test_collatz(int(testnum))
    else:
        print("Please enter a valid number or STOP to quit.")


