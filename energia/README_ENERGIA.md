# Contribuição de Energias Renováveis e Sustentáveis — CitizenTech

## Integrantes
Guilherme Guimarães - RM 572957
Filipe Gunther — RM 571131
Lucas Pinheiro — RM 573497

## Contexto e público
Público escolhido: moradores de residências brasileiras que desejam compreender a conta de luz, reduzir desperdício e avaliar geração solar fotovoltaica. O cenário numérico usa o consumo residencial médio nacional publicado pela EPE para dezembro de 2024 (179,7 kWh/mês), apenas como referência didática. Não representa a conta de uma família específica nem a média atual de São Paulo.

## Necessidade energética
Ajudar o morador a estimar o custo mensal do consumo e comparar duas estratégias para a mesma necessidade: (A) eficiência energética, reduzindo o consumo da residência; (B) geração solar fotovoltaica conectada à rede, que pode reduzir a energia comprada/compensada conforme regras e perfil de uso.

## Dados, unidades, período e premissas
- Consumo-base: 179,7 kWh/mês (EPE, dado de dezembro/2024).
- Tarifa efetiva ilustrativa: R$ 0,95/kWh. É uma premissa, não tarifa oficial. A ANEEL explica que o preço final da fatura inclui componentes tarifários, tributos e itens adicionais; deve-se usar a conta real para uma simulação individual.
- Eficiência: redução hipotética de 15% no consumo, investimento didático de R$ 250.
- Solar: sistema hipotético de 1,5 kWp; produtividade assumida de 110 kWh/kWp/mês; fração aproveitada/compensada de 80%; investimento hipotético de R$ 9.000.
- Período de comparação: mês e ano (12 meses). Payback é simples, sem desconto financeiro.
- Todos os valores que não são explicitamente atribuídos à EPE são hipóteses de modelagem, não medições, cotações ou garantias.

## Cálculos reproduzíveis
Fórmulas implementadas em `calculadora_energia.py`:
1. Custo-base mensal = consumo (kWh/mês) × tarifa efetiva (R$/kWh).
2. Economia por eficiência (kWh/mês) = consumo × percentual de redução.
3. Economia financeira = kWh economizados × tarifa efetiva.
4. Geração FV estimada = potência (kWp) × produtividade (kWh/kWp/mês).
5. Energia solar considerada para economia = mínimo(consumo, geração × fração aproveitada).
6. Economia solar = energia considerada para economia × tarifa efetiva.
7. Retorno simples = investimento inicial ÷ economia mensal.

### Resultado do cenário ilustrativo
Com as premissas acima:
- Base: 179,7 kWh/mês; R$ 170,72/mês modelados.
- Eficiência: 27,0 kWh/mês economizados; R$ 25,61/mês (R$ 307,29/ano); retorno simples aproximado de 9,8 meses sobre R$ 250.
- Solar: geração estimada de 165 kWh/mês; energia considerada para economia de 132 kWh/mês; R$ 125,40/mês (R$ 1.504,80/ano); retorno simples aproximado de 71,8 meses (6,0 anos) sobre R$ 9.000.

O retorno da eficiência não significa que toda residência alcançará 15% de redução ou que as medidas custarão R$ 250. O retorno solar não considera custo de disponibilidade, regras de compensação, tributos, custo de conexão, manutenção, degradação, financiamento, substituição de inversor, sombreamento ou sazonalidade. A geração real deve ser calculada para o endereço e telhado com dados do Atlas Solar do INPE e proposta técnica.

## Comparação das alternativas

| Critério | Eficiência energética | Solar fotovoltaica |
|---|---|---|
| Ação | Reduz demanda por hábitos/equipamentos eficientes | Gera eletricidade renovável no local |
| Economia modelada | 27,0 kWh/mês; R$ 25,61/mês | 132,0 kWh/mês aproveitados; R$ 125,40/mês |
| Investimento adotado | R$ 250 (hipótese) | R$ 9.000 (hipótese) |
| Retorno simples | 9,8 meses | 6,0 anos |
| Viabilidade | Menor barreira inicial; depende das medidas e hábitos | Exige telhado/área adequada, avaliação técnica e capital/financiamento |
| Impacto ambiental | Menor demanda e necessidade de geração/transmissão | Fonte renovável na operação; há impactos de fabricação, transporte e descarte dos módulos |

As alternativas podem ser combinadas: reduzir desperdício antes de dimensionar o sistema solar evita superdimensionamento. Os valores de economia não devem ser somados sem recalcular o consumo após eficiência.

## Integração ao CitizenTech
O módulo `calculadora_energia.py` contém cálculo determinístico (sem pedir ao LLM para fazer aritmética) e uma função de resposta curta. O notebook principal importa o módulo e disponibiliza a ferramenta `consultar_energia` ao agente. A interface atual pode receber perguntas de energia após executar a seção de integração indicada no notebook.

## Testes funcionais reproduzíveis
Execute `python -m unittest discover -s energia -p 'test_*.py'` na raiz do repositório. Os testes verificam valores-base, limites e validação de entradas. Isso não substitui teste de usabilidade com pessoas.

## Testes com usuários — pendente de execução
Não foram inventados participantes, comentários ou resultados. Registre após testar com pelo menos 3 pessoas, sem coletar dados pessoais:

| Cenário/pergunta | O que observar | Comentário real | Ajuste realizado |
|---|---|---|---|
| “Quanto gasto com 180 kWh?” | Entende kWh e custo estimado? | PREENCHER | PREENCHER |
| “Vale a pena colocar energia solar?” | Entende que é estimativa e não garantia? | PREENCHER | PREENCHER |
| “Qual dado preciso para personalizar?” | Identifica tarifa, consumo e endereço/telhado como necessários? | PREENCHER | PREENCHER |

## Referências
1. EPE. Workshop/estudo com consumo médio residencial por região e Brasil, dezembro/2024 (Brasil: 179,7 kWh/mês). https://www.epe.gov.br/sites-pt/areas-de-atuacao/energia-eletrica/WorkshopCOPAM/EPE_COPAM_Workshop_Mercado_Consumo_IV%20TRI%202024.pdf
2. ANEEL. Tarifas e Informações Econômico-Financeiras — ranking de tarifas vigentes e observação de que valores publicados não incluem necessariamente tributos, bandeiras e iluminação pública. https://www.gov.br/aneel/pt-br/centrais-de-conteudos/relatorios-e-indicadores/tarifas-e-informacoes-economico-financeiras
3. MME. Entenda cada item cobrado na conta de luz e como acompanhar o consumo (publicado em 03/07/2026, atualizado em 04/11/2026). https://www.gov.br/mme/pt-br/assuntos/secretarias/secretaria-nacional-energia-eletrica/mais-noticias/entenda-cada-item-cobrado-na-conta-de-luz-e-como-acompanhar-o-consumo
4. INPE/MCTI. Atlas Brasileiro de Energia Solar — acesso a dados climatológicos de potencial solar em escala mensal por localização. https://www.gov.br/pt-br/servicos/obter-dados-do-atlas-brasileiro-de-energia-solar-atlas-solar
5. ANEEL. Custo da energia que chega aos consumidores — geração, transmissão, distribuição, encargos e tributos. https://www.gov.br/aneel/pt-br/assuntos/tarifas/entenda-a-tarifa/custo-da-energia-que-chega-aos-consumidores

## Limitações
O cenário é nacional e didático, sem conta de luz real, endereço, distribuidora, orientação/inclinação do telhado ou cotação. A produtividade FV e fração aproveitada são hipóteses. O simulador não substitui dimensionamento por profissional habilitado, consulta à distribuidora ou análise das regras vigentes de compensação da geração distribuída. O sistema deve apresentar os números como estimativas e solicitar dados reais para personalização.
