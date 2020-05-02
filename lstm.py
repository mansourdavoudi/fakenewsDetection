import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from scipy import stats



def create_dataset(X, y, time_steps=1, step=1):
  Xs, ys = [], []
  print(len(X),"---------------")
  for i in range(0, len(X) - time_steps, step):
    v = X.iloc[i:(i + time_steps)].values
    labels = y.iloc[i: i + time_steps]
    Xs.append(v)
    ys.append(stats.mode(labels)[0][0])
  return np.array(Xs), np.array(ys).reshape(-1, 1)


column_names = [
  'user_id',
  'activity',
  'timestamp',
  'x_axis',
  'y_axis',
  'z_axis'
]

df = pd.read_csv(
  'WISDM_ar_v1.1_raw.txt',
  header=None,
  names=column_names
)
df.z_axis.replace(regex=True, inplace=True, to_replace=r';', value=r'')
df['z_axis'] = df.z_axis.astype(np.float64)
df.dropna(axis=0, how='any', inplace=True)
df.shape

df_train = df[df['user_id'] <= 30]
df_test = df[df['user_id'] > 30]

scale_columns = ['x_axis', 'y_axis', 'z_axis']

scaler = RobustScaler()

scaler = scaler.fit(df_train[scale_columns])

df_train.loc[:, scale_columns] = scaler.transform(
  df_train[scale_columns].to_numpy()
)

df_test.loc[:, scale_columns] = scaler.transform(
  df_test[scale_columns].to_numpy()
)

TIME_STEPS = 200
STEP = 40

X_train, y_train = create_dataset(
    df_train[['x_axis', 'y_axis', 'z_axis']],
    df_train.activity,
    TIME_STEPS,
    STEP
)

X_test, y_test = create_dataset(
    df_test[['x_axis', 'y_axis', 'z_axis']],
    df_test.activity,
    TIME_STEPS,
    STEP
)
