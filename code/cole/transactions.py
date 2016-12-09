import time
import datetime
from blockchain import blockexplorer
import re
import pandas as pd
import networkx as nx

def get_transactions(height, end, date):
    begin_height = height
    block = blockexplorer.get_block_height(height)[0]
    curr_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
    new_date = curr_date
    date_transactions = []
    # search between specified range for transactions
    while height < end:
        try:
            print(end - height)
            height = height + 1
            for block in blockexplorer.get_block_height(height):
                new_date = time.strftime('%Y-%m-%d', time.localtime(block.received_time))
                print(new_date)
                # keep list of all transactions 
                date_transactions = date_transactions + block.transactions
        except:
            time.sleep(10)
            height = height - 1


    input_nodes = nx.Graph()   
    #print(date_transactions[0:5])
    lines = []
    lines.append('tx_hash,in_out,address,time,value')
    for trns in date_transactions:
        # if block doesn't have any inputs, skip
        curr_nodes = []
        for inpt in trns.inputs:
            try:
                input_nodes.add_node(inpt.address)
                #add edges between all nodes in transaction
                input_nodes.add_edges_from([(inpt.address, out_addr) for out_addr in curr_nodes])
                curr_nodes.append(inpt.address)
                #print('input' + str(inpt.address))
                row = str(trns.hash) + ',' + 'in,' + str(inpt.address) + ',' + str(trns.time) + ',' + str(inpt.value)
                #print(row)
                lines.append(row)
            except AttributeError:
                pass
            
        for outpt in trns.outputs:
            try:
                row = str(trns.hash) + ',' + 'out,' + str(outpt.address) + ',' + str(trns.time) + ',' + str(outpt.value)
                lines.append(row)
            # if any attributes aren't found, as is the case with coinbase transactions, discard row
            except AttributeError:
                pass
    print(date)
    with open('transactions_' + str(date) + '.csv', 'w') as file_out:
        file_out.write('\n'.join(lines))

with open("dates.txt") as f:
    line = f.readline()
    date = re.split(',|\\n', line)[0]
    first = int(re.split(',|\\n', line)[1])
    index = 0
    for line in f.readlines():
        row = re.split(',|\\n', line)
        #starting block height parameter
        if index > 1:
            print(first)
            first = first + 1
            get_transactions(first, int(row[1]), date)
        date = row[0]
        first = int(row[1])
        index = index + 1
    
