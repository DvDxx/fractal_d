

N = int(input())
sum1 = 0
sum2 = 0
q = []
for i in range(N):
    q.append(int(input()))
max_num = q[0]
max_index = 0
count = 0
for each in q:
    if each > max_num:
        max_num = q[count]
        max_index = count
    count += 1
q = q[max_index+1:]+q[:max_index]
sum1 = max_num
reverse = 1
while q:
    temp = 0
    if q[0] > q[-1]:
        temp = q.pop(0)
    else:
        temp = q.pop()
    if reverse:
        sum2 += temp
        reverse =0
    else:
        sum1 += temp
        reverse = 1
if sum1 > sum2:
    print(sum1-sum2)
else:
    print(sum2-sum1)
# try:
#     T = int(input())
#     while T:
#         a, b = map(int, input().strip().split())
#         print(a)
#         print(b)
#         data = list(map(int, input().strip().split()))
#         print(data)
#         data.sort()
#         print(max(data))
#         print(data)
#         T -= 1
# except EOFError:
#     raise