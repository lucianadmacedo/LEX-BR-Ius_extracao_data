<pre> Roteiro para processamento dos textos:</pre>

- 1 - extrair todos os textos que não foram modificados -> 1943_original;
- 2 - deletar tags descessárias; Quais?
- 3 - renomear tags modificacao com o ano de modificação;
- 4 - wrap texto modificado com as tags renomeadas, i.e. modificacao_$YEAR
- 5 - criar os subcorpora
- 6 - checagem manual (bolsistas)
- 7 - anotação com UDPipe
- 8 - checagem manual (bolsistas)
- 9 - treinar modelo de anotação?
- 10 - a anotação é capaz de responder as seguintes perguntas de pesquisa:
    - houve aumento do uso do futuro em relação ao presente?
    - aumento ou não da frequência de ativas/passivas? Formação das passivas mudou: por exemplo, aumento do uso do auxiliar ser (assim como, estar e ficar); frequência do uso do "se" apassivador;
    - mudança na posição do sujeito? sujeito interposto (entre auxiliar e particípio como em: "podendo o consumidor exigir das partes viciadas“, e em passivas, como em "serão as pessoas jurídicas compelidas a cumpri-las")?
    - frequência de sujeito oculto (adaptar script já existente)
    - subordinadas foram bem anotadas? [pergunta pode ser expandida para linguística computacional]
