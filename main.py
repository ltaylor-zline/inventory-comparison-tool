#!/usr/bin/env python3

import csv
from pprint import pprint
from collections import defaultdict

def float_diff(row, key1, key2):
    if(row.__contains__(key1) and row.__contains__(key2)):
        return '{:.2f}'.format(float(row[key1]) - float(row[key2]))
    return 0.0

def int_diff(row, key1, key2):
    if(row.__contains__(key1) and row.__contains__(key2) and row[key1] != '' and row[key2] != ''):
        return int(row[key1]) - int(row[key2])
    return 0.0

def calc_err(row, key1, key2):
    if(row.__contains__(key1) and row.__contains__(key2) and row[key1] != '' and row[key2] != ''):
        val1 = float(row[key1])
        if(val1 == 0):
            if(float(row[key2]) == 0):
                return '0.00%'
            else:
                return '{:.2f}%'.format(-100 * float(row[key2]))
        return '{:.2f}%'.format(100.0 * (val1 - float(row[key2])) / val1)
    return '0.00%'

def make_diff_from_joined(row):
    difference_row = {}
    difference_row['SKU'] = row['SKU']
    difference_row['sales_velo_diff'] = float_diff(row, 'Sales Velocity/mo', 'Monthly Sales Velocity')
    difference_row['sales_velo_err'] = calc_err(row, 'Sales Velocity/mo', 'Monthly Sales Velocity')
    difference_row['adj_sales_velo_diff'] = float_diff(row, 'Adjusted Sales Velocity/mo', 'Monthly Sales Velocity')
    difference_row['adj_sales_velo_err'] = calc_err(row, 'Adjusted Sales Velocity/mo', 'Monthly Sales Velocity')
    difference_row['stock_diff'] = int_diff(row, 'Total On Hand', 'Stock')
    difference_row['thirty_day_sales_diff'] = int_diff(row, '30 Days Sales', 'Thirty Day Sales')
    difference_row['thirty_day_sales_err'] = calc_err(row, '30 Days Sales', 'Thirty Day Sales')
    return difference_row

def read_from_csv(filename):
    result = []
    with open(filename, 'r') as data:
        for row in csv.DictReader(data):
            result.append(row)
    return result

def join_lists_of_dicts(list_of_list_of_dicts, key):
    d = defaultdict(dict)
    for l in list_of_list_of_dicts:
        for row in l:
            d[row[key]].update(row)
    res = list(d.values())
    return res

def write_to_csv(filename, output):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = output[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in output:
            writer.writerow(row)

def get_abs_val_avg(rows, key):
    return sum(map(lambda r: abs(float(r[key][:-1])), rows))

if __name__ == '__main__':
    print('Reading data from CSV files')
    print()

    inv_planner_rows = read_from_csv('data/inv-planner-export.csv')

    sales_velo_rows = read_from_csv('data/sales-velo-report.csv')

    inv_data_rows = read_from_csv('data/inventory-report.csv')

    print('----INV PLANNER----')
    pprint(inv_planner_rows[:5])

    print()
    print('----SALES VELO----')
    pprint(sales_velo_rows[:5])

    print()
    print('----INVENTORY REPORT----')
    pprint(inv_data_rows[:5])

    res = join_lists_of_dicts((inv_planner_rows, sales_velo_rows, inv_data_rows), 'SKU')

    print()
    print('----JOINED RESULT----')
    pprint(res[:5])

    output = list(map(make_diff_from_joined, res))

    print()
    print('----DIFFERENCES----')
    pprint(output[:10])

    print()
    print('Writing to file data/result.csv...')
    write_to_csv('data/result.csv', output)
    print()

    print('----STATISTICS----')
    print('avg_err_adj_sales_velo=' + str(get_abs_val_avg(output[:100], 'adj_sales_velo_err')))
