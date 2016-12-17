import csv


def save_csv(data, fileName):
    # with 문을 사용하면 with 블록을 벗어나면 파일 객체 f 가 자동으로 close 되어 편리하다.
    print("CSV format save : ", fileName)
    with open(fileName, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for word, freq in data:
            writer.writerow([word, freq])


def save_txt(data, fileName):
    print("txt format save : ", fileName)
    with open(fileName, 'w') as f:
        for p in data:
            f.write(p + "\n")

