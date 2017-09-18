file_output = open("input22.txt", 'w')
N=20
file_output.write("BFS\n")
file_output.write(str(N) + "\n")
file_output.write(str(N) + "\n")
for i in range(0,N):
    if i != 0:
        file_output.write("\n")
    for j in range(0,N-1):
        file_output.write(str(0))

