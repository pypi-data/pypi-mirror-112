# UTestCell
utestcell is an IPython magic function that simplifies unit testing with Colab/Jupyter notebooks.

To activate utestcell in a Colab notebook:
```python
!pip install utestcell
%load_ext utestcell
```
Then add at the top of the cell
```python
%%utestcell
```

To use a test file stored on Github:
```python
#in cell #1
url = 'url of test.py file'
```
```python
#in cell #2
%%utestcell -u:$url
```

See a detailed explanation on my <a href="https://remibranco.com/?p=221">blog</a> and on the Github repo.
