"""Calculadora didática de consumo, eficiência energética e energia solar.

Os valores padrão são premissas de um cenário ilustrativo, não uma proposta comercial.
Edite os parâmetros com dados da conta de luz, endereço e orçamento reais.
"""
from dataclasses import dataclass, asdict

@dataclass
class PremissasEnergia:
    consumo_mensal_kwh: float = 179.7
    tarifa_efetiva_rs_kwh: float = 0.95
    economia_eficiencia_pct: float = 15.0
    custo_medidas_eficiencia_rs: float = 250.0
    potencia_solar_kwp: float = 1.5
    produtividade_solar_kwh_kwp_mes: float = 110.0
    fracao_energia_solar_aproveitada: float = 0.80
    investimento_solar_rs: float = 9000.0
    horizonte_anos: int = 10


def calcular(p: PremissasEnergia = PremissasEnergia()):
    if p.consumo_mensal_kwh <= 0 or p.tarifa_efetiva_rs_kwh <= 0:
        raise ValueError('Consumo e tarifa devem ser positivos.')
    if not 0 <= p.economia_eficiencia_pct <= 100:
        raise ValueError('Percentual de economia deve estar entre 0 e 100.')
    if not 0 <= p.fracao_energia_solar_aproveitada <= 1:
        raise ValueError('Fração aproveitada deve estar entre 0 e 1.')
    if p.potencia_solar_kwp < 0 or p.investimento_solar_rs < 0:
        raise ValueError('Potência e investimento não podem ser negativos.')

    base_kwh = p.consumo_mensal_kwh
    custo_base = base_kwh * p.tarifa_efetiva_rs_kwh
    economia_ef_kwh = base_kwh * p.economia_eficiencia_pct / 100
    economia_ef_rs = economia_ef_kwh * p.tarifa_efetiva_rs_kwh
    solar_gerada = p.potencia_solar_kwp * p.produtividade_solar_kwh_kwp_mes
    solar_aproveitada = min(base_kwh, solar_gerada * p.fracao_energia_solar_aproveitada)
    economia_solar_rs = solar_aproveitada * p.tarifa_efetiva_rs_kwh
    payback_ef_meses = p.custo_medidas_eficiencia_rs / economia_ef_rs if economia_ef_rs else None
    payback_solar_meses = p.investimento_solar_rs / economia_solar_rs if economia_solar_rs else None
    return {
        'premissas': asdict(p),
        'cenario_base': {'consumo_kwh_mes': base_kwh, 'custo_rs_mes': custo_base, 'custo_rs_ano': custo_base*12},
        'eficiencia': {'economia_kwh_mes': economia_ef_kwh, 'economia_rs_mes': economia_ef_rs,
                       'economia_rs_ano': economia_ef_rs*12, 'investimento_rs': p.custo_medidas_eficiencia_rs,
                       'retorno_simples_meses': payback_ef_meses,
                       'consumo_apos_kwh_mes': base_kwh-economia_ef_kwh},
        'solar': {'geracao_estimada_kwh_mes': solar_gerada, 'energia_aproveitada_estimada_kwh_mes': solar_aproveitada,
                  'economia_rs_mes': economia_solar_rs, 'economia_rs_ano': economia_solar_rs*12,
                  'investimento_rs': p.investimento_solar_rs, 'retorno_simples_meses': payback_solar_meses,
                  'consumo_rede_modelado_kwh_mes': max(0, base_kwh-solar_aproveitada)},
        'observacao': ('Estimativa simplificada: não inclui custo de disponibilidade, demanda, impostos/bandeiras variáveis, '
                       'degradação, manutenção, financiamento, custo de conexão, regras de compensação da GD ou variação sazonal. '
                       'A economia real depende da distribuidora, perfil horário, telhado, sombreamento e orçamento.')
    }


def resposta_assistente(pergunta: str) -> str:
    r = calcular()
    q = (pergunta or '').lower()
    b, e, s = r['cenario_base'], r['eficiencia'], r['solar']
    if any(x in q for x in ['solar', 'fotovolta', 'painel', 'placa']):
        return (f"No cenário ilustrativo, o consumo é {b['consumo_kwh_mes']:.1f} kWh/mês. "
                f"Um sistema de {r['premissas']['potencia_solar_kwp']:.1f} kWp teria geração estimada de "
                f"{s['geracao_estimada_kwh_mes']:.1f} kWh/mês. Aplicando aproveitamento modelado de "
                f"{r['premissas']['fracao_energia_solar_aproveitada']*100:.0f}%, a energia considerada para economia é "
                f"{s['energia_aproveitada_estimada_kwh_mes']:.1f} kWh/mês, ou R$ {s['economia_rs_mes']:.2f}/mês. "
                f"Com investimento hipotético de R$ {s['investimento_rs']:.2f}, o retorno simples seria "
                f"{s['retorno_simples_meses']/12:.1f} anos. Não é orçamento nem garantia de geração.")
    if any(x in q for x in ['econom', 'eficien', 'desperdi', 'reduzir', 'consum']):
        return (f"No cenário ilustrativo, o consumo é {b['consumo_kwh_mes']:.1f} kWh/mês e o custo modelado é "
                f"R$ {b['custo_rs_mes']:.2f}/mês. Uma redução hipotética de "
                f"{r['premissas']['economia_eficiencia_pct']:.0f}% economizaria {e['economia_kwh_mes']:.1f} kWh "
                f"ou R$ {e['economia_rs_mes']:.2f}/mês. O investimento estimado para as medidas foi fixado em "
                f"R$ {e['investimento_rs']:.2f}; substitua por orçamento real.")
    return (f"Cenário residencial didático: {b['consumo_kwh_mes']:.1f} kWh/mês e R$ {b['custo_rs_mes']:.2f}/mês. "
            f"Eficiência: economia estimada de R$ {e['economia_rs_mes']:.2f}/mês. "
            f"Solar: economia modelada de R$ {s['economia_rs_mes']:.2f}/mês. "
            "Pergunte sobre eficiência energética ou energia solar para detalhes. Valores são premissas ilustrativas.")

if __name__ == '__main__':
    import json
    print(json.dumps(calcular(), ensure_ascii=False, indent=2))
