#%%
#Utilize a divisão pelo piso e o operador de módulo para calcular o número de dias desde 1° de janeiro de 1970 e o horário atual em horas, minutos e segundos.
from time import time

now = int(time())
print(f"Total de segundos desde 1970: {now}")

seconds_in_a_minute = 60
seconds_in_a_hour = 3600 #60 * 60
seconds_in_a_day = 86400 #24 * 3600

days = now // seconds_in_a_day
hours = (now // seconds_in_a_day) % 24
minutes = (now // hours) % 60
seconds = now % 60

print(f"Dias: {days}, {hours}:{minutes}:{seconds}")

