# 1621

# direct: 1620
# indirect: 1620+1619+1618

# 1313010
# 1314630
from collections import defaultdict

lines = open("input.txt").readlines()

parents = {}

orbits = defaultdict(lambda: [])
for line in lines:
  parent, child = line.strip().split(')')
  orbits[parent].append(child)

paths = {}
def load_paths(node, path):
  paths[node] = path
  children = orbits[node]
  for child in children:
    load_paths(child, path + [node])
    # paths[child] = path + [node]

load_paths('COM', [])

# Part 1
print(sum([len(path) for path in paths.values()]))

# Part 2
from_path = paths['YOU']
to_path = paths['SAN']

parent = 'TZF'

slug_1 = ['8YX', 'XPH', 'BQ3', 'NCN', '9NT', 'QLS', 'RVC', 'B28', 'HWT', 'J3N', '87R', 'CJY', 'C9W', 'R89', '6YY',
          'XMS', '1P6', 'G2M', 'RJK', 'H5J', 'KQN', 'G8S', 'KYD', 'QBW', '3X6', '17C', '4PN', 'LJN', 'L45', '67L',
          'KJ4', 'XVL', 'FYB', 'QMS', '63P', '3GN', '1RD', 'TLJ', 'D9H', 'MX5', 'N6B', 'CSK', 'CW2', '6D9', '7PQ',
          'T8B', '9HT', 'JDX', '1QP', 'QGQ', 'H6H', '7VG', '1RJ', 'YT8', '4NT', 'W65', 'TSS', 'T9Z', 'RF6', '72T',
          'QRZ', 'HBM', 'G72', '4RB', 'DCB', '979', '14L', 'K2J', 'R5Q', '76Z', 'MN6', '784', 'B9P', 'FCY', 'YS1',
          '2MQ', '2J8', 'CNH', '2CG', '6CR', 'P27', 'TBJ', '8X4', 'LHJ', 'DDT', 'ZHL', 'L16', '82K', '51T', '6ZR',
          'HM1', '4QJ', 'KPL', 'B7L', 'HD5', 'G7N', 'LKC', 'DGR', '3VK', '7LX', 'WVR', 'Q14', 'Y1D', 'F7Q', 'WF4',
          '5M9', 'JP1', 'CNL', 'DLS', '7F3', 'KF6', 'NYH', 'L3T', '3SC', '9JM', 'YYX', '892', '16R', 'XQY', 'WBC',
          'XTW', '1N9', 'D98', 'MPC', '6SK', '42D', 'T4V', 'T5Y', 'CCL', 'RSP', '65G', 'WF1', 'JKG', 'P1V', '8PP',
          'NVK', 'BPW', 'S8S', '4G8', '9FY', 'YQR', 'ZJD', 'JWX', 'FRR', 'MYY', '5ML', 'Z5D', 'NM9', 'Q7S', 'SH7',
          'J2R', '78S', 'FB6', 'KZG', '45H', '5XR', 'BJ4', 'DQ1', 'BRG', 'Q54', '6C8', '3YZ', '9M6', 'J25', 'QS4',
          'CVW', 'YL6', 'J28', 'NWT', '7QQ', 'GMW', 'MMJ', 'PZY', '8KZ', '2LH', 'G22', 'LCX', 'VN9', 'M1S', '7J3',
          'PNH', 'CBP', 'F18', 'KR6', '3XH', 'WCC', 'VM1', '8JT', 'CKN', 'WD1', 'WC6', 'RJC', '42P', '1JB', '8CJ',
          'LGV', 'S38', '9HZ', 'KWM', '4BZ', '6YL', '6YM', 'TXQ', 'QTQ', 'LYT', 'JP2', 'T9K', 'DFV', 'LRL', '6GN',
          'G56', 'B5P', 'ZL2', '5VB', 'N4J', 'P97', '3JC', 'DF4', '4QQ', 'Z2B', 'BRS', 'WCY', 'BR6', 'Y97', '83C',
          'GBV', 'D8T', '444', '97J', '7CW', 'HB4', 'VP4', 'CFW', 'FRX', 'XFM', 'S6K', 'L7T', 'CLJ', '1F3', 'XH9',
          'JXX', 'MSV', '1JL', 'TS3', '5SP', 'FYJ', 'L7F', 'MVB', 'GQJ', '8Z3', 'BP1', 'Z48']
slug_2 = ['H63', 'FRK', 'H7W', 'FLS', 'C1R', '9SN', 'DJM', 'LDF', 'MDW', 'T7W', '8R4', '6HL', 'XKN', '6DL', 'F95',
          'K2K', 'KXT', 'QB8', '8KY', 'T1F', 'PJT', 'QQY', 'KQ9', 'ZD4', 'WZ1', 'ZFN', 'D2N', '8ZR', 'VMB', 'TZG',
          'KF8', 'YWH', 'M64', 'KWF', 'WKY', '9G5', 'YZ2', '2HF', '4DS', '6PP', 'ZZV', '591', 'RZ2', '99R', 'RT8',
          'HHG', 'NTT', 'D4Q', 'GV5', 'XFB', 'WX3', '4HG', 'T18', 'BVX', 'K7S', 'H28', 'TF8', 'XPG', 'X77', 'ZF8',
          'Y61', 'XDS', '7BL', '2Y6', 'TYP', 'JPV', '884', '91C', 'MGX', '45K', '5ZR', '12S', 'Y9S', '37Y', '8TM',
          'Y19', '2RN', 'D4V', 'KQ1', '8T3', 'V6P', 'TQF', 'DRD', '56Z', 'BZK', 'JT4', '9CW', 'RQL', 'KVX', 'QJ8',
          'ZQK', 'N6T', 'ZFR', 'TYR', '4KJ', '4B3', '9MY', 'B6F', '6NZ', 'JZM', 'HT6', '6FK', '7C3', 'ZDQ', 'QN6',
          '5M5', 'R6N', 'XWF', 'M37', 'JT6', 'H6Y', 'Q7Z', '6T9', 'VXS', 'DW6', 'W77', 'TK2', '9PP', 'TZC', 'KGN',
          '93V', 'HSQ', '89W', 'YVF', 'MZ5', 'M3Y', '959', 'RDN', 'WSY', '5LM', '5V9', 'XNH', 'VMX', 'NPW', 'ZZL',
          '23X', 'LC3', '6KT', 'V8F', '2K7', 'WKZ', '4XJ', '1T7', 'FFC', '87T']

print(from_path)
print(to_path)

print(len(slug_1 + slug_2))

print(set(from_path).intersection(to_path))

# COM

# 1621 BAD
