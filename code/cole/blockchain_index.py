import time
import datetime
from blockchain.exceptions import APIException
from blockchain import blockexplorer
from dateutil.relativedelta import relativedelta
from urllib.error import HTTPError

curr_block_height = 277198

def get_transactions(height):
    fail = True
    while fail:
        try:
            block = blockexplorer.get_block_height(height)[0]
            fail = False
        except:
            fail = True

    curr_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
    new_date = curr_date
    date_transactions = []
    #while curr_date == new_date:
    while True:
        height = height + 1
        for block in blockexplorer.get_block_height(height):
            new_date = time.strftime('%Y-%m-%d-%H-%m-%s', time.localtime(block.received_time))
            print(block.received_time)
            #dt = "%d-%02d-%02d-%02d-%02d-%02d"%(block_datetime.year, block_datetime.month, block_datetime.day, block_datetime.hour, block_datetime.minute, block_datetime.second)
            #field specification: ["in", transaction_key, referent_transaction_key, index, public_key, date]   
            date_transactions = date_transactions + block.transactions
    #print(len(date_transactions))
    return


def find_date_height(date, curr_block_height):
    unix_time = int(time.mktime(date.timetuple()))
    block_time = get_time(curr_block_height)
    while unix_time > block_time:
        print(curr_block_height)
        curr_block_height = curr_block_height + 500
        block_time = get_time(curr_block_height)
    while unix_time < block_time:
        curr_block_height = curr_block_height - 100
        block_time = get_time(curr_block_height)
    while unix_time > block_time:
        curr_block_height = curr_block_height + 50
        block_time = get_time(curr_block_height)
    while unix_time < block_time:
        curr_block_height = curr_block_height - 10
        block_time = get_time(curr_block_height)
    while unix_time > block_time:
        curr_block_height = curr_block_height + 1
        block_time = get_time(curr_block_height)
    return curr_block_height

def get_time(height):
    try:
        return blockexplorer.get_block_height(height)[0].received_time
    except KeyError:
        return get_time(height + 1)
    except APIException:
        time.sleep(20)
        return get_time(height)

def print_block(block):
    try:
        print(block.value)
        print(block.tx_index)
        print(block.address)
        print(block.n)
    except AttributeError:
        pass

def find_start_blocks():
    dates = []
    date = datetime.datetime.strptime('2013-12-27', '%Y-%m-%d')
    end_date = datetime.datetime.strptime('2014-11-6', '%Y-%m-%d')
    while date < end_date:
        curr = find_date_height(date, curr_block_height)
        row = str(date.strftime('%Y-%m-%d')) + ',' + str(curr)
        print(row)
        date = date + datetime.timedelta(days=7)
        dates.append(row)

    with open('dates.txt', 'w') as date_out:
        date_out.write('\n'.join(dates))

find_start_blocks()