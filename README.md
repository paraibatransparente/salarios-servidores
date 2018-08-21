# Salários Servidores - TCE-PB

Script baixa os dados abertos do TCE-PB, extrai os salários dos servidores públicos estaduais e municipais, faz algumas limpezas e exporta uma base de dados SQLite.

## Requisitos
- Python >= 2.7
- Espaço em disco aproximado: 20 GB

## Gerando base de dados SQLite
> Duas bases independentes são geradas. Uma para a Esfera Estadual e outra para a Esfera Municipal

### Esfera Estadual (~ 2 gb)
```
python setup-sqlite.py estadual
```

### Esfera Municipal
```
python setup-sqlite.py municipal
```
