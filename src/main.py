import time
import random


buffsize = 0
row = 0
col = 0
list_sequence = []
matrix = []
buffhasil = ''
maxSeq =[]


def main():
    global buffhasil, list_sequence, matrix, buffsize
    print("===== MENU UTAMA =====")
    print("1. Input File")
    print("2. Input manual/Random")
    print("3. Exit")
    pilihan = int(input("Pilihan (1/2/3) : "))
    if (pilihan==1):
        file_loc = input("Masukkan alamat file: ")
        inputfile(file_loc)
        x = []
        start = time.time()
        for col in range(len(matrix[0])):
            find_sequences(matrix, [], [], 0, col, True, x)
        list_hasil = Solve(x, list_sequence)
        end = time.time()
        duration = round((end-start)*1000)
        output(list_hasil, x)

        print(f'{duration} ms')
        buffhasil+=f'{duration} ms'
        saveFile()
    elif (pilihan==2):
        tokenCnt = int(input("Masukkan jumlah token unik : "))
        token = input("Masukkan token : ")
        token = token.split()
        buffsize = int(input("Masukkan ukuran buffer : "))
        size = input("Masukkan ukuran matrix : ")
        size = size.split()
        col = int(size[0])
        row = int(size[1])
        for i in range(row):
            matrix.append([])
            for j in range(col):
                rand_int = random.randint(0,tokenCnt-1)
                matrix[i].append(token[rand_int])

        SeqCnt = int(input("Masukkan jumlah sekuens : "))
        maxSeqSize = int(input("Masukkan ukuran maksimal seqkuens : "))
        for i in range(SeqCnt):#generate sequence
            seq = generateRandomSeq(token, maxSeqSize)
            while(seq in list_sequence):
                seq = generateRandomSeq(token, maxSeqSize)
            reward = random.randint(0,50)
            list_sequence.append([seq, reward])

        #output matrix and sequences
        print("Matrix: ")
        for row in matrix:
            print(' '.join(map(str, row)))
        for i in range(len(list_sequence)):
            sequences = ' '.join(list_sequence[i][0][j:j+2] for j in range(0, len(list_sequence[i][0]), 2))
            print(f'Sequence: {sequences}')
            print(f'Reward: {list_sequence[i][1]}')

        x=[]
        start = time.time()
        for i in range(len(matrix[0])):
            find_sequences(matrix, [], [], 0, i, True, x)
        list_hasil = Solve(x, list_sequence)
        end = time.time()
        duration = round((end-start)*1000)

        output(list_hasil,x)
        print(f'{duration} ms')
        buffhasil+=f'{duration} ms'
        saveFile()
        
def printmatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(f'{matrix[i][j]}')
            if (j<len(matrix[0])-1):
                print(" ")
        print("\n")

def saveFile():
    global buffhasil
    saveChoice = input("Apakah anda ingin menyimpan solusi? (y/n) ")
    if (saveChoice in ['y', 'Y']):
        outputName = input("Masukkan nama file: ")
        with open ("../test/"+outputName, "w") as file:
            file.write(buffhasil)

def generateRandomSeq(tokens, maxSeqSize):
    global list_sequence
    sequence = ''
    sequence_size = random.randint(2,maxSeqSize)
    for _ in range(sequence_size):
        token = random.choice(tokens)
        sequence += token
    return sequence




def inputfile(filename):
    global buffsize, col, row, matrix, list_sequence
    contents = []
    with open('../test/'+filename, 'r') as file:
        for line in file:
            contents.append(line)
    buffsize = int(contents[0])
    size = contents[1].split()
    col = int(size[0])
    row = int(size[1])
    for i in range(row):
        matCol = contents[2+i].split()
        matrix.append(matCol)
    SeqCnt = int(contents[2+row])
    for i in range(0,SeqCnt*2,2):
        list_sequence.append([contents[3+row+i].replace(" ", '').strip(), int(contents[4+row+i])])




def find_sequences(matrix, visited, path, row, col, is_horizontal, arrseq):
    global buffsize
    # Append the current cell to the path
    path.append(matrix[row][col])
    visited.append([row,col])

    # Basis rekursi
    if len(path) <= buffsize:
        arrseq.append([path[:], visited[:]])
        # print(arrs)

    # Define possible moves (vertically first, then horizontally)
    if (len(path)<buffsize):
        if is_horizontal:
            for i in range(len(matrix)):
                new_row, new_col = i,col
                if [new_row,new_col] not in visited:
                    find_sequences(matrix, visited.copy(), path.copy(), new_row, new_col, not is_horizontal, arrseq)
        else:
            for i in range(len(matrix[0])):
                new_row, new_col = row,i
                if [new_row,new_col] not in visited:
                    find_sequences(matrix, visited.copy(), path.copy(), new_row, new_col, not is_horizontal,arrseq)

def Solve(Seqs, reward):
    global list_sequence, maxSeq
    list_hasil = []
    # print(Seqs)
    for sequence in Seqs:
        hasil = 0
        answer = ''.join(sequence[0])
        # print(answer)
        for x in reward:
            # print(answer, x[0], x[1])
            if x[0] in answer:
                hasil+=x[1]
        list_hasil.append(hasil)
    # print(list_hasil)
    maxVal = max(list_hasil)
    max_indexes = [index for index, value in enumerate(list_hasil) if value == maxVal]
    solutions = []
    for i in range(len(max_indexes)):
        solutions.append(Seqs[max_indexes[i]])
    maxSeq = []
    if (len(solutions)<=1):
        maxSeq = solutions[0]
    else:
        for i in range(len(solutions)-1):
            if (i==0):
                maxSeq = solutions[i]
            if (len(maxSeq[0])>len(solutions[i+1][0])):
                maxSeq = solutions[i+1]

    return list_hasil

def output(list_hasil, list_sequence):
    global buffhasil, maxSeq
    print(max(list_hasil))
    buffhasil+=f'{max(list_hasil)}\n'
    sequence = ' '.join(maxSeq[0])
    print(sequence)
    buffhasil+=f'{sequence}\n'
    for i in range(len(maxSeq[1])):#print koordinat
        print(f'{maxSeq[1][i][1]+1}, {maxSeq[1][i][0]+1}')
        buffhasil+=f'{maxSeq[1][i][1]+1}, {maxSeq[1][i][0]+1}\n'

main()