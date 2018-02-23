def gcdlcm(a, b):
    gcd_a = [x for x in range(1, a+1) if x%a == 0]
    gcd_b = [x for x in range(1, b+1) if x%b == 0]
    gcd = min(list(set(gcd_a + gcd_b)))
    lcm_val=lcm(a, b, gcd)
    answer = [gcd, lcm_val]
    return answer

def lcm(a, b, gcd):
    if gcd == 0:
        return 0
    else:
        return int(abs((a*b)/gcd))

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(gcdlcm(3,12))
