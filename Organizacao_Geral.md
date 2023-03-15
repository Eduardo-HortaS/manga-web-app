
# Protótipo Django

## Criar protótipo Django com formulário e validação código UniProt, para estudar os conceitos de MVT (Model, Views, Templates).

    Views: Receber a requisição do clique do botão, junto com a codigo uniprot fornecido pelo usuário, buscar no UniProt por dados adicionais (nome da proteína, sequência, features), armazenar no banco de dados usando o models e retornar uma tela para o usuário usando um template.

    Models: Criar as classes que definem seu banco de dados, fazer a migração para criar o banco de dados.

    Templates: Criar uma página HTML, chamada pela view, que recebe os dados do models e mostra pro usuário.

# Solution

    App Level

forms.py:

### Holds a form for storing the UniProt ID sent by the user, but how much validation should I work with here? At the moment, I only see reason to concern myself with the proper length, since an invalid output from UniProt API should suffice later on. 

models.py: 

### Holds a model that stores UniProt ID, protein name, sequence and features. Gotta think about how to take these infos from a JSON output and convert it properly.

views.py

### Presents the form to the user, parses the UniProt JSON output for additional data given a valid ID, links the data to the model and sends a template back to the user revealing the model's data.

    Project Level