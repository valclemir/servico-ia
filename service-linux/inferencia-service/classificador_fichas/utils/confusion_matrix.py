#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix


def plot_cm(Y, y_pred_inv):
    acc = accuracy_score(Y, y_pred_inv)
    print('Accuracy: {:.2f}'.format(acc*100))
    cm = confusion_matrix(Y, y_pred_inv, labels=['Baixo', 'Moderado', 'Alto'])
    print(cm)

    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, cmap='Blues', fmt='g', cbar=False)
    ax.set_xlabel('Modelo IA')
    ax.set_ylabel('Auditoria')
    #ax.set_title('Matriz de Confusão')
    ax.xaxis.set_ticklabels(['Baixo', 'Moderado', 'Alto'])
    ax.yaxis.set_ticklabels(['Baixo', 'Moderado', 'Alto'])
    ax.xaxis.set_label_position('top')
    plt.tight_layout()
    plt.show()
