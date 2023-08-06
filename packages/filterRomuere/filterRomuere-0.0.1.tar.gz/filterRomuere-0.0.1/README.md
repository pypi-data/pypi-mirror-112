filterRomuere
=============

#### Esse é um pacote que faz uma transformação em uma imagem aplicando um filtro de agrupamento.
#### Veja o exemplo de resultado do pacote:

![Imagem de entrada.](imgs/SanFrancisco.png)

![Imagem de entrada.](imgs/SanFrancisco_saida.png)

## Instalação:

` pip install filterRomuere `

## Uso:

```
import filterRomuere as fr
img = 'imgs/imagemdeentrada.png'
filter = fr.filterRomuere(img)
filter.apply_filter()
```
