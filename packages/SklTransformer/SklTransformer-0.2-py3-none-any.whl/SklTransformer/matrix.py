import numpy as np
from sklearn.metrics import accuracy_score

def compute_metrics(p):
    pred, labels = p
    pred = np.argmax(pred, axis=1)

    accuracy = accuracy_score(y_true=labels, y_pred=pred)

    return {"accuracy": accuracy}

if __name__ == '__main__':
    main()
