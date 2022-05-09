# csv bulshit
coins_list = ['test.csv']


def convert_data(value):
    fixed_value = []
    for x in value:
        x = float(x)
        fixed_value.append(x)

    return fixed_value

def rm_hours(target):
    outcome = []
    for x in target:
        x = x.replace(" 04:00:00", "")
        x = x.replace("-","/")
        outcome.append(x)


    return outcome

def yearly_data(csv_reader):
    x = 0
    rows = []
    for row in csv_reader:
        if x%10 == 0 and x <= 365:
            rows.append(row)
        x += 1
    
    return rows

def monthly_data(csv_reader):
    x = 0
    rows = []
    for row in csv_reader:
        if x >= 31:
            break

        rows.append(row)
        x += 1
    
    return rows

def all_data(csv_reader):
    rows = []
    x = 0
    for row in csv_reader:
        if x%10 == 0:
            rows.append(row)
        x += 1

    return rows

def get_from_csv(path, type):
    csv_file = open(path)
    csv_reader = csv.reader(csv_file)

    header = next(csv_reader)
    
    if type == '1y':
        rows = yearly_data(csv_reader)

    elif type == '1m':
        rows = monthly_data(csv_reader)

    elif type == 'all':
        rows = all_data(csv_reader)
    
    csv_file.close()
    
    return rows

def extract_csv_data(path,type):
    data = get_from_csv(path,type)

    date = [row[0] for row in data]
    value = [row[1] for row in data]
    date = rm_hours(date)
    value = convert_data(value)

    return date, value
