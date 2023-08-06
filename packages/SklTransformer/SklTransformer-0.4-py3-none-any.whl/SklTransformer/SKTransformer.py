from typing import Callable, List, Optional, Tuple
import tuning
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
import torch
from typing import Callable, List, Optional, Tuple
import torch
import call
import matrix
from transformers import TrainingArguments, Trainer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import EarlyStoppingCallback
from transformers import BertModel, BertTokenizer



class SKTransformer(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            tokenizer_name,
            model_name,
            fine_tuning=False,
            X_train=None,
            y_train=None,
            X_val=None,
            y_val=None,
            labels=None,
            nub_epoch=10,
            save_path='',
            max_length: int = 512,
            embedding_func: Optional[Callable[[torch.tensor], torch.tensor]] = None,
            embedding_func1: Optional[Callable[[torch.tensor], torch.tensor]] = None,
    ):

        if fine_tuning==True:
        
            bert = tuning.Tuning(sentences_train=X_train, labels_train=y_train, 
                            sentences_val=X_val, labels_val=y_val, 
                            tokenizer_name =tokenizer_name, model_name= model_name, 
                            labels=labels, epoch=nub_epoch, max_length=max_length, save_path=save_path)
            self.tokenizer, self.model = bert.output()
        else:
            self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
            self.model = BertModel.from_pretrained(model_name)




        self.model.eval()
        self.max_length = max_length
        self.embedding_func = embedding_func
        self.embedding_func1 = embedding_func1

        if self.embedding_func is None:
            self.embedding_func = lambda x: x[1][0].squeeze()

        if self.embedding_func1 is None:
            self.embedding_func1 = lambda x: x[0][:, 0, :].squeeze()

    def _tokenize(self, text: str) -> Tuple[torch.tensor, torch.tensor]:
        # Tokenize the text with the provided tokenizer
        tokenized_text = self.tokenizer.encode_plus(text,
                                                    add_special_tokens=True,
                                                    max_length=self.max_length
                                                    )["input_ids"]

        # Create an attention mask telling BERT to use all words
        attention_mask = [1] * len(tokenized_text)

        # bert takes in a batch so we need to unsqueeze the rows
        return (
            torch.tensor(tokenized_text).unsqueeze(0),
            torch.tensor(attention_mask).unsqueeze(0),
        )

    def _tokenize_and_predict(self, text: str) -> torch.tensor:
        tokenized, attention_mask = self._tokenize(text)

        embeddings = self.model(tokenized, attention_mask)
        #return torch.cat((self.embedding_func(embeddings).unsqueeze(0),self.embedding_func1(embeddings).unsqueeze(0)), 1).squeeze()
        return self.embedding_func(embeddings)+self.embedding_func1(embeddings)

    def transform(self, text: List[str]):
        if isinstance(text, pd.Series):
            text = text.tolist()

        with torch.no_grad():
            return torch.stack([self._tokenize_and_predict(string) for string in text])

    def fit(self, X, y=None):
        """No fitting necessary so we just return ourselves"""
        return self