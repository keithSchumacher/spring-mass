from euler_method import generate_data
import pandas as pd




def create_data_for_sktime(n_inits, spring_constants=False):
    X_dict = {'x_1': [], 'x_2': []}
    y = []

    for _ in range(n_inits):
        X = generate_data(random_init=True, spring_constants=spring_constants)
        for i, x in enumerate(X):
            cols = iter(list(range(x.shape[1])))
            for x1 in cols:
                y.append(i)
                X_dict['x_1'].append(pd.Series(x[:, x1]))
                X_dict['x_2'].append(pd.Series(x[:, next(cols)]))
    X = pd.DataFrame(data=X_dict)
    y = pd.Series(y)
    return X, y
