## Stock prediction
https://www.kaggle.com/datasets/svaningelgem/nasdaq-daily-stock-prices

---

Using a daily updated dataset from kaggle I implimented my sorting algorithm with stock algorithms/indicators to do stock predictions.

---

### Indicator inspiration
```
//
// @author LazyBear 
// List of all my indicators: https://www.tradingview.com/v/4IneGo8h/
//
study(shorttitle = "SQZMOM_LB", title="Squeeze Momentum Indicator [LazyBear]", overlay=false)

length = input(20, title="BB Length")
mult = input(2.0,title="BB MultFactor")
lengthKC=input(20, title="KC Length")
multKC = input(1.5, title="KC MultFactor")

useTrueRange = input(true, title="Use TrueRange (KC)", type=bool)

// Calculate BB
source = close
basis = sma(source, length)
dev = multKC * stdev(source, length)
upperBB = basis + dev
lowerBB = basis - dev

// Calculate KC
ma = sma(source, lengthKC)
range = useTrueRange ? tr : (high - low)
rangema = sma(range, lengthKC)
upperKC = ma + rangema * multKC
lowerKC = ma - rangema * multKC

sqzOn  = (lowerBB > lowerKC) and (upperBB < upperKC)
sqzOff = (lowerBB < lowerKC) and (upperBB > upperKC)
noSqz  = (sqzOn == false) and (sqzOff == false)

val = linreg(source  -  avg(avg(highest(high, lengthKC), lowest(low, lengthKC)),sma(close,lengthKC)), 
            lengthKC,0)

bcolor = iff( val > 0, 
            iff( val > nz(val[1]), lime, green),
            iff( val < nz(val[1]), red, maroon))
scolor = noSqz ? blue : sqzOn ? black : gray 
plot(val, color=bcolor, style=histogram, linewidth=4)
plot(0, color=scolor, style=cross, linewidth=2)

```

![analyzed](https://cdn.discordapp.com/attachments/845065484315131924/1250288883757744178/Screenshot_2024-06-11_at_8.20.41_PM.png?ex=666a65c3&is=66691443&hm=8254644a87bcdc5f4992465ca17f5143d134786ebf9ae7d6b4f86d47e4929179&)
