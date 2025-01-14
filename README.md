<pre> Roteiro para processamento dos textos:</pre>

- 1 - ~~renomear tags modificacao com o ano de modificação;~~ (Feito!)
- 2 - ~~wrap texto modificado com as tags renomeadas, i.e. modificacao_$YEAR~~ (Feito!)
- 3 - extrair todos os textos que não foram modificados -> 1943_original;
- 4 - criar os subcorpora por ano
- 5 - checagem manual (bolsistas) -> Ana Clara
- 6 - limpeza (deletar tags descessárias; deletar metadados dentro de parênteses; caracteres especiais)
- 7 - anotação com UDPipe
      - seguir dois caminhos a partir daqui: checagem da anotação e análise linguística
- 8 - checagem manual (bolsistas)
- 9 - treinar modelo de anotação?
- 10 - a anotação é capaz de responder as seguintes perguntas de pesquisa:
    - houve aumento do uso do futuro em relação ao presente?
    - aumento ou não da frequência de ativas/passivas? Formação das passivas mudou: por exemplo, aumento do uso do auxiliar ser (assim como, estar e ficar); frequência do uso do "se" apassivador;
    - mudança na posição do sujeito? sujeito interposto (entre auxiliar e particípio como em: "podendo o consumidor exigir das partes viciadas“, e em passivas, como em "serão as pessoas jurídicas compelidas a cumpri-las")?
    - frequência de sujeito oculto (adaptar script já existente)
    - subordinadas foram bem anotadas? [pergunta pode ser expandida para linguística computacional]
