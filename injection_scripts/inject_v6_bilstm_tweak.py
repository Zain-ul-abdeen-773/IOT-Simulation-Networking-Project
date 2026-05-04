import os

ALP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'FinalCCNProject.alp')

def patch():
    with open(ALP, 'r', encoding='utf-8') as f:
        c = f.read()

    # Change Linear Regression to BiLSTM
    c = c.replace(
        'g2d.drawString("Model: Linear Regression Forecaster (FutureForecaster)", 20, 50);',
        'g2d.drawString("Model: BiLSTM Forecaster (FutureForecaster)", 20, 50);'
    )

    with open(ALP, 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Updated Forecaster model name to BiLSTM.")

if __name__ == '__main__':
    patch()
