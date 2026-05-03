Resumo mínimo - Procedimento NMO/Dix

Dados necessários (entrada):
- Offset (x) em metros.
- Tempos de reflexão t(x) em milissegundos (ms) para cada reflector.

Relação física fundamental (NMO):
- t(x)^2 = t0^2 + x^2 / V^2

Procedimento essencial:
1. Preparação dos dados: converter t[ms] -> t[s] (t/1000); calcular x^2 e t^2.
2. Determinar t0 e V_NMO: ajustar t^2 vs x^2; t0 = sqrt(intercept); Vnmo = 1/sqrt(slope).
3. Velocidade intervalar (Dix): Vint = sqrt((Vrms_i^2 t_i - Vrms_{i-1}^2 t_{i-1})/(t_i - t_{i-1})).
4. Espessura e profundidade: dz = Vint * (t_i - t_{i-1})/2; z = sum(dz).

Gráficos obrigatórios por reflector:
- t^2 vs x^2 (scatter + regressão)
- t vs x (pontos + curva NMO)

Cuidados mínimos:
- intercepto < 0 => rever offsets ou aceitar t0 ~ 0.
- se t_i - t_{i-1} <= 0 => Dix inválido.

Entrega final:
- Tabela com t0, Vnmo, Vint, Espessura, Profundidade.
- 10 gráficos (5 reflectores x 2 gráficos cada).

Uma frase:
"Usando a relação hiperbólica do NMO, ajusta-se (t^2) vs (x^2) para obter (t_0) e (V_{NMO}); aplica-se Dix para calcular velocidades intervalares; converte-se tempo em profundidade; e apresenta-se tudo com gráficos no Excel."
