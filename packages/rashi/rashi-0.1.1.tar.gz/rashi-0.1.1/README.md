# Rashi

Developed by Crian69 (c) 2021
A simple package that scrapes out `rashi fals` from https://www.hamropatro.com/rashifal

## Installing The Package

```python
pip install rashi
```

## Examples of How To Use

Getting The Required Rashi Fal

```python
from rashi import Zodiacs, Length, getRashiFal

horo = getRashiFal(Zodiacs.Meen, Length.Weekly) #Gets The Rashi Fal As NamedTuple -> Rashi(rashi:str, date: str)

print(horo.rashi) #the actual rashi
print(horo.date) #the date till which the rashi is valid

# Other Code
```

All the available Zodiacs types are:

<ol>
<li>Mesh</li>
<li>Mithun</li>
<li>Singha</li>
<li>Tula</li>
<li>Dhanu</li>
<li>Kumbha</li>
<li>Brish</li>
<li>Karkat</li>
<li>Kanya</li>
<li>Brischik</li>
<li>Makar</li>
<li>Meen</li>
</ol>

All the available Length types are:

<ol>
<li>Daily</li>
<li>Weekly</li>
<li>Monthly</li>
<li>Yearly</li>
</ol>
