#!/bin/bash

#-------------------------------------------------------------------------------------
#                          Enviroment variables
#-------------------------------------------------------------------------------------

echo "bash inside start"

nerdir=$(pwd)/NER

## NE list
nelist=$nerdir/data/NE.list 
## test data
test=$nerdir/data/parsed_test.iob
## where to save model predictions
result=$nerdir/results/temp.iob2

## an external dictionary
dict=$nerdir/data/dict.txt
## the maximum number of n for n-gram
feature=4

## where to save model params and vocab
model=$nerdir/models/temp001.model
vocab=$nerdir/models/temp001.vocab

## the hidden size of word/char embedding
hidden_word=512
hidden_char=64

## use dictionary if true
#use_dict=true
use_dict=false

text=$nerdir/data/splitted_text.txt

#-------------------------------------------------------------------------------------
#                          Main
#-------------------------------------------------------------------------------------

##mkdir -p $nerdir/results

## predict tags 
if $use_dict; then
    python $nerdir/scripts/test.py \
        --test_path $test \
        --model_path $model \
        --vocab_path $vocab \
        --dict_path $dict \
        --feature_n $feature \
        --hidden_word_size $hidden_word \
        --hidden_char_size $hidden_char \
	--text_path $text \
    > $result
else
    python $nerdir/scripts/test.py \
        --test_path $test \
        --model_path $model \
        --vocab_path $vocab \
        --hidden_word_size $hidden_word \
        --hidden_char_size $hidden_char \
	--text_path $text \
    > $result
fi
## calculate precision, recall, and f-measure
#python scripts/accuracy.py \
#    --ref $test \
#   --hyp $result


echo "bash inside end"