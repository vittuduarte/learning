# %%
"""Quanto segudos existem em 42 minutos e 42 segundos?"""
minutos_em_segundos = ((42 * 60) + 42)
print(f"42min e 42s em segundos: {minutos_em_segundos}")
# %%
"""quantas milhas existem em 10 km?"""
milhas_por_km = 0.621
distancia_em_milhas = 10 * milhas_por_km

print(f"10km em milhas: {distancia_em_milhas}")
# %%
"""Se você correr 10km em 42 minutos e 42 segundos, 
	qual será o seu passo médio (tempo por milha em minutos e segundos)?"""

segundos_por_milha = minutos_em_segundos / distancia_em_milhas

pace_minutos = int(segundos_por_milha // 60)
pace_segundos = int(segundos_por_milha % 60)

print(f"Passo médio: {pace_minutos} minutos e {pace_segundos} segundos mph")

#%%
"""Qual é sua velocidade média em milhas por hora?"""
horas = minutos_em_segundos / 3600
mean_velocity = (distancia_em_milhas / horas)
print(f"Velocidade média: {round(mean_velocity, 2)} mph")
# %%
