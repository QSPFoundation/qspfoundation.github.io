---
title: "Третий параметр RAND"
sidebar_position: 13
---

# Третий параметр RAND {#tretij_parametr_rand}

Эта статья ещё не написана, но я уже работаю над этим.

Пока что можете почитать статьи в интернете:

[Мода](https://ru.wikipedia.org/wiki/Мода_(статистика))

[Нормальное распределение](https://ru.wikipedia.org/wiki/Нормальное_распределение)

код для тестов распределения:

```qsp
local left, right, med = %arrpack('args')
 
local d, x, items
 
local N = 1000000
*pl 'Генерируем числа. Подождите...'
wait 0
loop local i=0 while i < N step i+=1:
    x = rand(LEFT, RIGHT, MED)
    d[x]+=1
end
local stars = 100
local total = 0
loop i = LEFT while i<=RIGHT step i+=1:
    items = d[i] * stars / N
     
    loop while items > 0 step items-=1:
        *p '*'
    end
    perc = d[i] * 1000/N
    *pl ' <<perc/10>>.<<perc MOD 10>>% <<d[i]>>'
    total += d[i]
end
'================== TOTAL: <<total>>'
```
