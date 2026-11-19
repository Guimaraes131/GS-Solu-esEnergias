# CitizenTech - Assistente do Programa Acessa Cidade (GS 2026.2)

Grupo RotaCerta - turma 1CCR

Projeto da Global Solution 2026.2 de Prompt and Artificial Intelligence (FIAP), frente C: acessibilidade. O assistente responde perguntas de cidadaos sobre o Programa Acessa Cidade (Cartao Passe Livre, atendimento em Libras e unidades de atendimento) usando uma base de documentos da prefeitura, cita a fonte e diz que nao sabe quando a base nao tem a resposta.

Integrantes: Filipe Gunther (RM 571131), Lucas Pinheiro (RM 573497) e Guilherme Guimaraes (RM 572957). Modalidade: trio. Turma: 1CCR.

## Como rodar

1. Abrir 1_Notebook_GS2026_2.ipynb no Google Colab.
2. Runtime, Alterar tipo de ambiente de execucao, GPU T4.
3. Subir a pasta 2_base_documental para o ambiente do Colab (se esquecer, a celula da base recria os 3 documentos do grupo e o Run all nao para).
4. Runtime, Run all.

O modelo e local: o notebook instala o Ollama dentro do Colab e baixa o qwen2.5:7b (cerca de 4,7 GB, so na primeira vez). Nao existe chave de API, Secret nem servico pago, entao nenhuma chave aparece no notebook, no zip ou nos prints. Sem GPU o notebook troca sozinho para o qwen2.5:3b, que roda, mas bem mais devagar.

As versoes das bibliotecas estao fixas na celula de instalacao.

Para gerar o 3_avaliacao_ragas.json, o ground truth das 8 perguntas (secao 7) precisa estar escrito. Enquanto houver "ESCREVER AQUI", o notebook roda ate o fim mas pula o RAGAS. Com o ground truth escrito, o Run all gera o 3_avaliacao_ragas.json e o resultados_para_readme.md, que ficam no painel de arquivos do Colab (icone de pasta, a esquerda).

## Pipeline

Diagrama do fluxo:

```
documento (.txt com titulo, data e tema)
        |
        v
chunking (1000 caracteres, overlap 150)
        |
        v
embeddings multilingues (CPU)
        |
        v
indice ChromaDB (metadados doc_id e data_publicacao)
        |
        v
retriever (k=4) --> filtro de prompt injection
        |
        v
contexto ordenado pela data (mais novo primeiro)
        |
        v
prompt (fonte obrigatoria, "nao sei") --> ChatOllama qwen2.5:7b local --> parser
        |
        v
guardrails (escopo, LGPD, limite de confianca) --> resposta com (fonte: doc_id)
```

O agente fica ao lado do RAG: o LLM decide chamar consultar_status_unidade, verificar_atendimento ou buscar_na_base, com limite de 6 iteracoes. A interface Gradio chama o agente, mostra as fontes e as ferramentas usadas e tem botoes com perguntas prontas.

## Base documental e a armadilha

Os tres documentos foram escritos pelo grupo (nao foram copiados de nenhuma fonte) sobre um programa de acessibilidade ficticio da prefeitura. Cada um tem titulo, data_publicacao e tema.

- doc_01_guia (10/03/2026): servicos do Programa Acessa Cidade, horario da Central (unidade U-01), atendimento em Libras com agendamento, prazo de 15 dias uteis para o cartao, documentos, laudo de ate 5 anos, acompanhante e validade de 2 anos.
- doc_02_portaria (15/09/2026): suprime o atendimento de sabado desde 1 de outubro e reduz o prazo do cartao de 15 para 10 dias uteis.
- doc_03_comunicado (20/10/2026): fecha a Central de 21/10 a 30/11 para obras, move o atendimento para a unidade provisoria U-01A e informa que o atendimento em Libras passa a ser so por videochamada.

A armadilha tem tres partes. A primeira e de desatualizacao: o doc_01 ainda mostra atendimento aos sabados e prazo de 15 dias. A segunda e de contradicao: o doc_01 diz que o atendimento em Libras e presencial na Central, e o doc_03, mais recente, diz que ele e so por videochamada durante as obras. A terceira e de faixa condicional: o laudo medico so vale se tiver sido emitido ha no maximo 5 anos, entao um laudo de 3 anos serve e um de 7 nao, e o acompanhante gratuito so existe quando o laudo indicar. Os detalhes do laudo e do acompanhante ficam nas informacoes de apoio, no fim do doc_01, para testar o chunking. Para resolver, o contexto e ordenado pela data e o prompt manda valer o documento mais novo e avisar da contradicao.

## Decisoes tecnicas

Chunking: foram comparadas duas estrategias (500 sem overlap e 1000 com overlap 150) e a tabela esta na secao 1 do notebook. O teste checa se cada regra escondida (laudo de ate 5 anos, acompanhante, Libras com agendamento e sabado suprimido) cabe inteira em algum chunk. A v1 gerou 9 chunks e a v2 gerou 5, e nas duas as 4 regras ficaram inteiras, entao o teste sozinho nao separa uma da outra. Escolhemos a v2 (1000 com overlap 150) porque cada artigo ou paragrafo fica junto com o seu contexto e, com k=4, o retriever consegue trazer quase toda a base, incluindo o documento original e o que o altera. O custo e mandar mais texto para o prompt.

k=4: a base so tem 3 documentos (5 chunks na v2), entao k=4 tende a trazer o original e o documento que o altera juntos, que e o que as perguntas de armadilha precisam. O lado ruim e que traz chunks que nao ajudam, o que pode baixar o context_precision.

Tools: o modelo so decide chamar e o codigo calcula. verificar_atendimento calcula se a Central esta aberta num horario de dia util e quando abre ou fecha. consultar_status_unidade devolve o status da unidade (U-01 ou U-01A). Id de unidade invalido, dia invalido ou hora invalida devolve erro controlado e o agente explica sem quebrar.

Modelo local: o qwen2.5:7b roda na GPU T4 do Colab via Ollama, o que tira a dependencia de chave e de servico externo. O briefing cita o Ollama Cloud com chave nos Secrets, mas o grupo decidiu usar o modelo local. Para o notebook nao travar: espera o servidor do Ollama subir (em vez de um tempo fixo), limita cada resposta a 700 tokens, mantem o modelo carregado na GPU, poe teto de 120 s no agente e tem try/except nas respostas da interface e do RAGAS. Os embeddings rodam na CPU para a GPU ficar toda com o LLM.

Guardrails: filtro de fora de escopo, bloqueio de dado pessoal (LGPD), filtro de prompt injection nos trechos recuperados e resposta "nao ha informacao na base" quando nao ha contexto. Os filtros de escopo e LGPD ignoram acento. Cada um e demonstrado na secao 6.

## Avaliacao

O RAGAS roda sobre 8 perguntas (4 simples e 4 de armadilha) com ground truth escrito pelo grupo (o Filipe escreveu as 8 respostas), e o resultado sai em 3_avaliacao_ragas.json. O juiz e o mesmo qwen2.5:7b local e o embeddings e o multilingue local, ambos passados explicitamente. Como o juiz e um modelo de 7B, mais fraco que um juiz grande, os valores devem ser lidos como comparativos (chunking v1 x v2, k=4 x k=6) e nao como valor absoluto. Para o juiz local nao travar, o RAGAS roda com 2 chamadas em paralelo, timeout de 600 s por chamada e answer_relevancy com strictness 1.

Resultados medidos: [PREENCHER depois do Run all com o conteudo de resultados_para_readme.md, e escrever a explicacao dos numeros e a melhoria com o numero antes e depois]. Nenhum valor foi estimado.

## Limitacoes e custo

A base e pequena e simulada, e as tabelas de unidades e horario das tools estao fixas no codigo. Para producao seriam necessarios dados reais da prefeitura, revisao de LGPD e infraestrutura propria. Cada pergunta feita ao RAG gasta 1 chamada ao modelo, e ao agente ate 6, mais as chamadas do juiz na avaliacao. Com o modelo local nao ha custo em dinheiro: o custo e tempo de GPU do Colab (a primeira execucao baixa o modelo e o RAGAS e a etapa mais demorada) e a qualidade fica limitada a um modelo de 7B. Sem GPU o notebook usa o qwen2.5:3b e fica lento.

## Prints

Os arquivos ficam na pasta prints.

---

# Contribuição adicional — Soluções em Energias Renováveis e Sustentáveis

A contribuição de energia foi adicionada ao CitizenTech sem remover a frente original de acessibilidade. O agente agora dispõe da ferramenta `consultar_energia`, que calcula estimativas de consumo residencial, economia por eficiência energética e geração solar fotovoltaica. A interface inclui perguntas prontas sobre energia.

## Arquivos novos
- `energia/calculadora_energia.py`: cálculos determinísticos e respostas da ferramenta do agente.
- `energia/dados_cenario.csv`: dados e premissas do cenário, com unidades e classificação da origem.
- `energia/test_calculadora_energia.py`: testes automatizados.
- `energia/README_ENERGIA.md`: contexto, fórmulas, resultados, comparação, referências, limitações e protocolo de testes com usuários.

## Execução e validação
Mantenha a pasta `energia` ao lado do notebook e execute o notebook em ordem. A ferramenta de energia é registrada na seção 4 e fica disponível na interface. Para testar o módulo sem iniciar o LLM, execute na raiz do projeto:

```bash
python -m unittest discover -s energia -p 'test_*.py' -v
python energia/calculadora_energia.py
```

Os números são estimativas ilustrativas e não devem ser apresentados como tarifa vigente, orçamento ou economia garantida. Antes de uma orientação individual, substitua consumo e tarifa pelos dados da fatura e valide o potencial solar no Atlas do INPE e com avaliação técnica.

**Testes com usuários:** o protocolo está documentado em `energia/README_ENERGIA.md`, mas ainda precisa ser executado e preenchido pela equipe. Não foram fabricados participantes, comentários ou resultados.
