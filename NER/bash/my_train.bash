#!/bin/bash

#-------------------------------------------------------------------------------------
#                          Enviroment variables
#-------------------------------------------------------------------------------------

echo "train inside start"

nerdir=$(pwd)/NER

## NE list
nelist=$nerdir/data/NE.list 
## train data
train=$nerdir/anns/merged_train.iob

## training log
log=$nerdir/logs/temp.log

## an external dictionary
dict=$nerdir/data/dict.txt
## the maximum number of n for n-gram
feature=4

## where to save model params and vocab
model=$nerdir/models/temp.model
vocab=$nerdir/models/temp.vocab

## the minimum frequcnecy of words/chars for vocabs
freq_word=2
freq_char=2

## the hidden size of word/char embedding
hidden_word=512
hidden_char=64

## optimizer
opt=Adam
## the initial learnig rate
lr=1e-3

## for early stopping 
early_stopping=3
## eval model every eval_iter iterations
eval_iter=50

## the maximum number of iterations for training
max_iter=1000000

## mini-batch size
batch_size=10

## gpu number (use CPU if -1)
#gpu=0
gpu=-1

## use dictionary if true
#use_dict=true
use_dict=false


#-------------------------------------------------------------------------------------
#                          Main
#-------------------------------------------------------------------------------------

## create directory if it does not exist
#mkdir -p models logs

if $use_dict; then
    python -u $nerdir/scripts/train.py \
        --ne_list_path $nelist \
        --train_path $train \
        --model_path $model \
        --vocab_path $vocab \
        --dict_path $dict \
        --feature_n $feature \
        --freq_word $freq_word \
        --freq_char $freq_char \
        --hidden_word_size $hidden_word \
        --hidden_char_size $hidden_char \
        --optimizer $opt \
        --lr $lr \
        --early_stopping $early_stopping \
        --eval_iter $eval_iter \
        --max_iter $max_iter \
        --batch_size $batch_size \
        -g $gpu \
    2>&1 | tee $log

else
    python -u $nerdir/scripts/train.py \
        --ne_list_path $nelist \
        --train_path $train \
        --model_path $model \
        --vocab_path $vocab \
        --freq_word $freq_word \
        --freq_char $freq_char \
        --hidden_word_size $hidden_word \
        --hidden_char_size $hidden_char \
        --optimizer $opt \
        --lr $lr \
        --early_stopping $early_stopping \
        --eval_iter $eval_iter \
        --max_iter $max_iter \
        --batch_size $batch_size \
        -g $gpu \
    2>&1 | tee $log 

fi


echo "train inside end"