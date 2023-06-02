import numpy as np
import os

def generateRandomAddresses(array_size: int) -> np.ndarray:
  """Generates a NumPy array of random addresses.

  Args:
    array_size: The number of addresses to generate.

  Returns:
    A NumPy array of random addresses.
  """
  addresses = np.random.randint(0, 2**16, size=array_size)

  return addresses.astype(str)

def generateRandomAddressPairs(n,m,processor :int  = 32) -> list:
    # return [{'from':i,'to':j} for i in generateRandomAddressesMP(n, int(processor/2)) 
            # for j in generateRandomAddressesMP(m, int(processor/2))]
    return [{'from':i,'to':j} for i in generateRandomAddresses(n) 
               for j in generateRandomAddresses(m)] 



import multiprocessing as mp

def generateRandomAddressesMP(array_size: int, process_count: int) -> list:
  """Generates a list of random addresses using multiple processes.

  Args:
    array_size: The number of addresses to generate.
    process_count: The number of processes to use.

  Returns:
    A list of random addresses.
  """
  addresses = []

  # Create a pool of processes.
  pool = mp.Pool(process_count)

  # Generate random addresses in each process.
  for i in range(process_count):
    address_list = pool.apply_async(generateRandomAddresses, args=(array_size // process_count,)).get()
    addresses.extend(address_list)

  # Wait for all processes to finish.
  pool.close()
  pool.join()

  return addresses

def map_address_to_float(addressBatch):
  """
  A naive mapping from an Ethereum address to a float.
  Args:
    address: The Ethereum address.

  Returns:
    A array of float array
  """

  # Convert the address to a hexadecimal string.
  import hashlib
  r = map(lambda x: [int(hashlib.sha3_256(x.encode("utf-8")).hexdigest(), 16) % (10 ** 16)/10**15] ,
           addressBatch)
  return r

# write a function to get blocks from ethereum and iterate each transaction and return from to pair
def getFromToPairsFromBlock(blockNumber):
    from web3 import Web3
    import requests
    from requests import adapters

    adapter = adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
    session = requests.Session()
    session.headers = {'Content-Type': 'application/json'}
    session.headers = {'x-apikey': os.environ['CHAINSTORAGE_SDK_AUTH_TOKEN']}
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    w3 = Web3(Web3.HTTPProvider('https://launchpad.coinbase.com/api/exp/chainnode/ethereum/mainnet', session=session))

    block = w3.eth.get_block(blockNumber,full_transactions=True)
    for tx in block.transactions: # type: ignore
        yield ({"from":tx['from'], "to":tx['to'], "hash":tx['hash'].hex()})