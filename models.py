
import numpy as np

class model1:
    def __init__(self, name='Base Model 1', a=15, b=0.0022):
        self.name = name
        self.a = a
        self.b = b
        self.latex = r'''DMI = a \cdot \left( 1-e^{-b\cdot BW} \right)'''

    def dmicalc(self, bw):
        return self.a * (1 - np.exp(-self.b*bw))

class model2:
    def __init__(self, name='Base Model 2', a=0., b=0.0022, t=20, nem=1.24):
        self.name = name
        self.a = a
        self.b = b
        self.t = t
        self.nem = nem
        #self.latex = r'''DMI = BW^{0.75}\cdot \left( 0.2435\cdot NE_{m} -0.0466\cdot NE_{m}^{2} -0.1128 \right)/NE_{m}'''
        self.latex = r'''\begin{equation*}
DMI=\begin{cases}
    BW^{0.75}\cdot \left( 0.2435\cdot NE_{m} -0.0466\cdot NE_{m}^{2} -0.1128 \right)/NE_{m} \quad &\text{if} \, 5\leq T\leq 20 \\
    DMI\cdot \left ( 1-\left ( \left ( T-20 \right ) \cdot 0.005922 \right ) \right ) \quad &\text{if } \,  T> 20^{o} \\
    DMI\cdot \left ( 1-\left ( \left ( 5-T \right ) \cdot 0.004644\right ) \right ) \quad &\text{if } \,  T< 5^{o} \\
    NE_{m} \in \left ( 1.24, 1.55 \right )
  \end{cases}
\end{equation*}'''

    def dmicalc(self, bw):
        nem = self.nem

        dmi = np.power(bw,0.75) * (0.2435*nem - 0.0466 * np.power(nem,2) - 0.1128) / nem

        if self.t < 5:
            dmi = dmi * (1-((5-self.t)*0.004644))
        elif self.t > 20:
            dmi = dmi * (1-((self.t-20)*0.005922))
        
        return dmi
        
    

