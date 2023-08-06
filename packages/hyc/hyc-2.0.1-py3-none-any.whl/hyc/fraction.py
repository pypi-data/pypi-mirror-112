from Fun_num import comprime
# 注意：在本模块中，分数用[分母,分子]的形式表示，如五分之一表示为[5,1]

# 约分
def red_fr(fraction):
    try:
        if coprime(fraction):
            return fraction
        else:
            _,common_div = hcf(fraction)
            for i in range(2):
                fraction[i] = int(fraction[i]/common_div)
            return fraction
    except:
        print('\n错误：请在red_fac函数的括号内填入一个分数!分数用[分母,分子]的形式表示。\nError[red_fac]:Please fill in a fraction in parenthese!The fraction here is expressed by [denominator,numerator].')

# 注意：请在该函数参数内填入一个分数

# 通分
def den_di(fraction_list):
    try:
        all_deno = []
        for i in fraction_list:
            all_deno.append(i[0])
            common_deno = lcm(all_deno)
            for i in fraction_list:
                common_mul = int(common_deno/i[0])
                for j in range(2):
                    i[j] *= common_mul
        return fraction_list
    except:
        print('\n错误：请在den_di函数的括号内填入一个分数列表!分数用[分母,分子]的形式表示。\nError[den_di]:Please fill in a fraction list in parenthese!The fraction here is expressed by [denominator,numerator].')

# 注意：请在该函数的参数内填入一个分数列表

# 最简分数
def simp_fr(fraction):
    try:
        if coprime(fraction):
            return True
        else:
            return False
    except:
        print('\n错误：请在simp_fr函数的括号内填入一个分数!分数用[分母,分子]的形式表示。\nError[simp_fr]:Please fill in a fraction in parenthese!The fraction here is expressed by [denominator,numerator].')

# 注意：请在该函数参数内填入一个分数

# 倒数
def opposide(fraction):
    try:
        fraction_opposide = []
        fraction_opposide.append(fraction[1])
        fraction_opposide.append(fraction[0])
        return fraction_opposide
    except:
        print('\n错误：请在opposide函数的括号内填入一个分数!分数用[分母,分子]的形式表示。\nError[opposide]:Please fill in a fraction in parenthese!The fraction here is expressed by [denominator,numerator].')

# 分数加法
def fra_ad(plus_fra_list):
    try:
        result = 0
        fraction_list = den_di(plus_fra_list)
        for i in fraction_list:
            result += i[1]
        fraction_sum = [fraction_list[0][0], result]
        return red_fr(fraction_sum)
    except:
        print('\n错误：请在fra_ad函数的括号内填入一个分数列表!分数用[分母,分子]的形式表示。\nError[fra_ad]:Please fill in a fraction list in parenthese!The fraction here is expressed by [denominator,numerator].')

# 注意：请在该函数的参数内填入一个分数列表，该函数可算出列表中所有分数之和

# 分数减法
def fra_sub(minuend, all_subtracted):
    try:
        if len(all_subtracted) > 1:
            subtracted = fra_ad(all_subtracted)
        else:
            subtracted = all_subtracted[0]
        new_minuend, new_subtracted = den_di([minuend, subtracted])
        new_minuend[1] -= new_subtracted[1]
        return red_fr(new_minuend)
    except:
        print('\n错误：请在fra_sub函数的括号内填入一个分数代表被减数，再填入一个分数列表表示所有减数!分数用[分母,分子]的形式表示。\nError[fra_sub]:Please fill in a fraction in parenthese to represent minuend, and then fill in a fraction list to represent all subtracted!The fraction here is expressed by [denominator,numerator].')


# 分数乘法
def fra_mult(fraction_list):
    try:
        all_deno = []
        all_mole = []
        for i in fraction_list:
            if type(i) == list and len(i) == 2:
                all_deno.append(i[0])
                all_mole.append(i[1])
        result = []
        product = 1
        for i in all_deno:
            product *= i
        result.append(product)
        product = 1
        for i in all_mole:
            product *= i
        result.append(product)
        return red_fr(result)
    except:
        print('\n错误：请在fra_mult函数的括号内填入一个分数!分数用[分母,分子]的形式表示。\nError[fra_mult]:Please fill in a fraction in parenthese!The fraction here is expressed by [denominator,numerator].')

# 注意：请在该函数的参数内填入一个分数列表，该函数可算出列表中所有分数之积

# 分数除法
def fra_divi(dividend, all_divisor):
    try:
        divisor = fra_mult(all_divisor)
        result = fra_mult([dividend, opposide(divisor)])
        return red_fr(result)
    except:
        print('\n错误：请在fra_divi函数的括号内填入一个分数代表被除数，再填入一个分数列表表示所有除数!分数用[分母,分子]的形式表示。\nError[fra_divi]:Please fill in a fraction in parenthese to represent dividend, and then fill in a fraction list to represent all divisor!The fraction here is expressed by [denominator,numerator].')
