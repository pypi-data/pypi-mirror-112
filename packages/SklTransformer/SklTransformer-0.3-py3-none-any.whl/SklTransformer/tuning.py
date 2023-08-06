from typing import Callable, List, Optional, Tuple
import torch
import call
import matrix
from transformers import TrainingArguments, Trainer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import EarlyStoppingCallback
from transformers import BertModel, BertTokenizer



class Tuning():
    def __init__(
        self,
       
        sentences_train=None,
        labels_train=None,
        sentences_val=None,
        labels_val=None,
        tokenizer_name=None,
        model_name=None,
        labels=None,
        epoch=10,
        save_path='',
        max_length: int = 512,
        
    ):
    
        sentences_train = ["[CLS] " + sentence + " [SEP]" for sentence in sentences_train]
        sentences_val = ["[CLS] " + sentence + " [SEP]" for sentence in sentences_val]
        sentences_train= list(sentences_train)
        labels_train = list(labels_train)
        sentences_val= list(sentences_val)
        labels_val = list(labels_val)

        # Define pretrained tokenizer and model
        #model_name = "/content/drive/MyDrive/bert/bert_acj/checkpoint-10500"
        tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
        model = BertForSequenceClassification.from_pretrained(model_name, num_labels=labels)

        X_train_tokenized = tokenizer(sentences_train, padding=True, truncation=True, max_length=max_length)
        X_val_tokenized = tokenizer(sentences_val, padding=True, truncation=True, max_length=max_length)


        train_dataset = call.Dataset(X_train_tokenized, labels_train)
        val_dataset = call.Dataset(X_val_tokenized, labels_val)

        #print(val_dataset)


        # Define Trainer
        args = TrainingArguments(
            output_dir=save_path+"bert",
            evaluation_strategy="steps",
            eval_steps=3000,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=epoch,
            save_steps=3000,
            load_best_model_at_end=True,
        )
        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=matrix.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
        )
        # Train pre-trained model

        print('Fine tuning supervised transformer based LM')
     
        trainer.train()
      
      
        trainer.save_model()
        
        tokenizer.save_pretrained(save_path+"bert")


        print('Tranied !!')
        self.save_path = save_path+"bert"


                
    def output(self):
        tokenizer = BertTokenizer.from_pretrained(self.save_path)

        bert_model = BertModel.from_pretrained(self.save_path)

        return tokenizer, bert_model


if __name__ == '__main__':
    main()
