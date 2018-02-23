def water_melon(n):
    str = "";
    for x in range(1, n+1):
        if x%2==0:
            str+="박"
        else:
            str+="수"
    return str

def water_melon_2(n):
    str = "수박"*n
    return str[:n]


# 실행을 위한 테스트코드입니다.
print("n이 3인 경우: " + water_melon(3));
print("n이 4인 경우: " + water_melon_2(4));

