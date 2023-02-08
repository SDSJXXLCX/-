from uart import uart as U
from uart import dict
from info import info as I

myu = U()
myi = I()

if __name__ == '__main__':
    # print(S)
    myu.search()
    myu.updata(dict)
    myu.connect()
    myu.open()
    while True:
        try:
            myu.sent_info(myi.get_info())
        except:
            print('error')