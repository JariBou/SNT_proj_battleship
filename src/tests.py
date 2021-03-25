def test():
    List = ['5', '7', 'q', '8']
    for i in List:
        try:
            print(int(i))
        except Exception:
            print('HOOOOO')


if __name__ == '__main__':
    test()

