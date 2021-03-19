# Atualização nas rotas da API 

As rotas foram alteradas, as mudanças foram:

* get_graphs > get_graphs_teacher
* get_question_data > get_questions
* get_class > get_classes

A readequação se da para deixar os nomes mais condizentes com o que realmente fazem hoje. Em especial, o get_graphs, já que está em planejamento o acesso de alunos a plataforma, 
com isso eles terão acesso a dados (menos que o professor), por isso a necessidade de diferenciar.

Deve haver novas rotas em breve com a possibilidade de consultas específicas, além de permitir um gerenciamento dos dados a distância.
