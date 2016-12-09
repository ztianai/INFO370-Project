from blockchain import blockexplorer as be
import time
import sqlite3

conn = sqlite3.connect('/Volumes/My Passport/Data/blockchain.db')
cur = conn.cursor()

pattern = '%Y-%m-%d'

dates = open('dates.txt', 'r').read().split('\n')
block_id = 1

def insert_block(block):
  print block
  stmt = "INSERT INTO BLOCK(range_time, height, main_chain, block_time, hash, received_time) VALUES(?,?,?,?,?,?)"
  cur.execute(stmt, block)
  return cur.lastrowid

def insert_trans(trans):
  stmt = "INSERT INTO TRANS(block, time, hash) VALUES(?,?,?)"
  cur.execute(stmt, trans)
  return cur.lastrowid

def insert_input(input):
  stmt = "INSERT INTO TRAN_INPUT(trans, value, address) VALUES(?,?,?)"
  cur.execute(stmt, trans)
  return cur.lastrowid

def insert_output(output):
  stmt = "INSERT INTO TRAN_OUTPUT(trans, value, address) VALUES(?,?,?)"
  cur.execute(stmt, output)
  return cur.lastrowid

for date in dates:
  t = int(time.mktime(time.strptime(date, pattern)) * 1000)
  blocks = be.get_blocks(time=t)
  for b in blocks:
    block = be.get_block(b.hash)
    block_insert = [date, block.height, int(block.main_chain), block.time, block.hash, block.received_time]
    block_id = insert_block(block_insert)
    for trans in block.transactions:
      trans_insert = [block_id, trans.time, trans.hash]
      trans_id = insert_trans(trans_insert)
      for i in trans.inputs:
        print i.__dict__
        i_insert = [trans_id, i.value, i.address]
        insert_input(i_insert)
      for o in trans.outputs:
        o_insert = [trans_id, o.value, o.address]
        insert_output(o_insert)



    