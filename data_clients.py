import csv
import time

csv_file_path_clients = "clients.csv"
csv_file_path_reports_dates = "report_dates.csv" 
csv_file_path_train = "train.csv"     
csv_file_path_tran = "transactions.csv"
csv_file_currency = "currency_rk.csv"
csv_file_path_mcc_codes = "mcc_codes.csv"

def max_min_pre_norm(sArr):
    pre_arr = []
    for s in sArr:
        if s.startswith("БОЛЕЕ"):
            pre_arr.append(int(s.split(" ")[1]))
        elif s.startswith("Na"):
            pre_arr.append(0)
        elif s.startswith("ДО"):
            pre_arr.append(int(s.split(" ")[1]))
        elif s.startswith("ОТ"):
            tmp_s = s.split(" ")
            pre_arr.append(int(tmp_s[1]))
            pre_arr.append(int(tmp_s[3]))
    return min(pre_arr),max(pre_arr)

def pre_norm(sArr):
    tuple_max_min = max_min_pre_norm(sArr)
    res = []
    for s in sArr:
        if s.startswith("БОЛЕЕ"):
           res.append([int(s.split(" ")[1]) + 1, tuple_max_min[1]])
        elif s.startswith("NA"):
            res.append([0,0])
        elif s.startswith("ДО"):
            res.append([tuple_max_min[0], int(s.split(" ")[1])])
        elif s.startswith("ОТ"):
            tmp_s = s.split(" ")
            res.append([int(tmp_s[1]), int(tmp_s[3])])
    return res

def read_cliests(csv_file_path):
    user_ids = []
    reports = []
    employee_count_nms = []
    bankemplstatus_arr = []
    customer_ages = []
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            user_ids.append(int(row[0]))
            reports.append(int(row[1]))
            employee_count_nms.append(row[2])
            bankemplstatus_arr.append(int(row[3]))
            customer_ages.append(int(row[4]))
    return {
        "user_ids": user_ids,
        "reports": reports,
        "employee_count_nms": pre_norm(employee_count_nms),
        "bankemplstatus_arr": bankemplstatus_arr,
        "customer_ages": customer_ages
    }

def read_reports(csv_file_path):
    reports = []
    report_dt = []
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            reports.append(int(row[0]))
            reports.append(time.strptime(row[1],"%Y-%m-%d %H:%M:%S"))
    return {
        "reports": reports,
        "report_dt": report_dt
    }
    
def read_train(csv_file_path):
    user_ids = []
    targets = []
    times = []
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            user_ids.append(int(row[0]))
            targets.append(int(row[1]))
            times.append(int(row[2]))
    return {
        "user_ids": user_ids,
        "targets": targets,
        "times": times
    }

def read_currency_rk(csv_file_path):
    arr = []
    
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            arr.append(int(row[0]))
            
    return arr
def read_mcc_codes(csv_file_path):
    arr = []
    
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            arr.append(int(row[0]))
            
    return arr
def read_transactions(csv_file_path_tran,csv_file_currency,csv_file_path_mcc_codes):
    user_ids = []
    mcc_codes = []
    transaction_dttms = []
    transaction_amts = []
    codes = read_mcc_codes(csv_file_path_mcc_codes)
    currencies = read_currency_rk(csv_file_currency)
    with open(csv_file_path_tran, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            if int(row[1]) >= len(codes):
                break
            user_ids.append(int(row[0]))
            mcc_codes.append(codes[int(row[1])])
            currency = currencies[int(row[2])]
            transaction_amts.append(float(row[3])*currency)
            transaction_dttms.append(time.strptime(row[4],"%Y-%m-%d %H:%M:%S"))
            
    return {
        "user_ids": user_ids,
        "mcc_codes": mcc_codes,
        "transaction_dttms": transaction_dttms,
        "transaction_amts": transaction_amts
    }
    
def load_data():
    return {
        "clients": read_cliests(csv_file_path_clients),
        "train": read_train(csv_file_path_train),
        "reports_dates": read_reports(csv_file_path_reports_dates),
        "transactions": read_transactions(csv_file_path_tran,csv_file_currency,csv_file_path_mcc_codes)
    }

def normalize_min_max(inputs):
    new_inputs = [(x - min(inputs)) / (max(inputs) - min(inputs)) for x in inputs]
    return new_inputs

def conversion_second(inputs):
    new_inputs = []
    for i in inputs:
        time_struct = time.strptime(i, "%Y-%m-%d %H:%M:%S")
        new_inputs.append(time.mktime(time_struct))
    return new_inputs
