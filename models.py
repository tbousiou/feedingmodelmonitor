import numpy as np

base_models = [
    {'name': 'Base model 1', 'base_type':0, 'pa': 15, 'pb': 0.0022},
    {'name': 'Base model 2', 'base_type':1, 'pa': 15, 'pb': 0.0022, 'pc': 4, 'pd': 0.0045}
]


base_model_1 = {
    'name': 'Base model 1',
    'model_id': 0,
    'params': {
        'a': 15.0,
        'b': 0.0022
    },
    'latex': r'''DMI = a \cdot \left( 1-e^{-b\cdot BW} \right)'''
}


base_model_2 = {
    'name': 'Base model 2',
    'model_id': 1,
    'params': {
        'a': 15.0,
        'b': 0.0022,
        'c': 10.0,
        'd': 0.3
    },
    'latex': r'''\begin{equation*}
DMI=\begin{cases}
    BW^{0.75}\cdot \left( 0.2435\cdot NE_{m} -0.0466\cdot NE_{m}^{2} -0.1128 \right)/NE_{m} \quad &\text{if} \, 5\leq T\leq 20 \\
    DMI\cdot \left ( 1-\left ( \left ( T-20 \right ) \cdot 0.005922 \right ) \right ) \quad &\text{if } \,  T> 20^{o} \\
    DMI\cdot \left ( 1-\left ( \left ( 5-T \right ) \cdot 0.004644\right ) \right ) \quad &\text{if } \,  T< 5^{o} \\
    NE_{m} \in \left ( 1.24, 1.55 \right )
  \end{cases}
\end{equation*}'''
}


def dmi0(bw,a,b):
    return a * (1 - np.exp(-b*bw))

def dmi1(bw,a,b,c,d,t=20,nem=1):

    #dmi = np.power(bw,0.75) * (0.2435*nem - 0.0466 * np.power(nem,2) - 0.1128) / nem
    dmi = np.power(bw,0.75) * (a*nem - 0.0466 * np.power(nem,2) - 0.1128) / nem
    if t < 5:
        dmi = dmi * (1-((5-t)*0.004644))
    elif t > 20:
        dmi = dmi * (1-((t-20)*0.005922))
    
    return dmi
    

