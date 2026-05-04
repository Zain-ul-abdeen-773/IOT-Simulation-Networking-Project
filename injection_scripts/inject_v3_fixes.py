import os

ALP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'FinalCCNProject.alp')

def patch():
    with open(ALP, 'r', encoding='utf-8') as f:
        c = f.read()

    # Normalize to \n for matching
    c = c.replace('\r\n', '\n')

    # ===== FIX 1: Battery percentage overlapping title =====
    c = c.replace(
        'g2d.drawString("Battery Drain Simulation", 20, 35);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Model: Energy Digital Twin", 20, 50);\n'
        '\t\t\t\t\t\n'
        '\t\t\t\t\tjava.awt.Color battColor = currentBattery > 50 ? neonGreen : (currentBattery > 20 ? neonOrange : neonRed);\n'
        '\t\t\t\t\tg2d.setColor(battColor);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 28));\n'
        '\t\t\t\t\tg2d.drawString(String.format("%.1f%%", Math.max(0, currentBattery)), getWidth() - 100, 40);',

        'g2d.drawString("Battery Drain Simulation", 20, 28);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 9));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(120,120,120));\n'
        '\t\t\t\t\tg2d.drawString("Model: Energy Digital Twin", 20, 40);\n'
        '\t\t\t\t\tjava.awt.Color battColor = currentBattery > 50 ? neonGreen : (currentBattery > 20 ? neonOrange : neonRed);\n'
        '\t\t\t\t\tg2d.setColor(battColor);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 18));\n'
        '\t\t\t\t\tg2d.drawString(String.format("%.1f%%", Math.max(0, currentBattery)), getWidth() - 80, 28);',
        1
    )

    # ===== FIX 2: Add new tracking variables to TelemetryDash =====
    c = c.replace(
        'private double totalError = 0.0;\n'
        '\t\t\n'
        '\t\tprivate java.awt.Color bgDark = new java.awt.Color(13, 17, 23);\n'
        '\t\tprivate java.awt.Color panelDark = new java.awt.Color(22, 27, 34);\n'
        '\t\tprivate java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);\n'
        '\t\tprivate java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);\n'
        '\t\tprivate java.awt.Color neonRed = new java.awt.Color(255, 60, 60);',

        'private double totalError = 0.0;\n'
        '\t\tprivate double sumSqErr=0, sumActual=0, sumActSq=0, lastActual=0, lastPred=0;\n'
        '\t\t\n'
        '\t\tprivate java.awt.Color bgDark = new java.awt.Color(13, 17, 23);\n'
        '\t\tprivate java.awt.Color panelDark = new java.awt.Color(22, 27, 34);\n'
        '\t\tprivate java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);\n'
        '\t\tprivate java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);\n'
        '\t\tprivate java.awt.Color neonGreen = new java.awt.Color(57, 255, 20);\n'
        '\t\tprivate java.awt.Color neonOrange = new java.awt.Color(255, 165, 0);\n'
        '\t\tprivate java.awt.Color neonRed = new java.awt.Color(255, 60, 60);',
        1
    )

    # ===== FIX 3: Replace KPI panel with AI Model Pipeline Monitor =====
    old_kpi = (
        'g2d.drawString("Live Telemetry KPI Matrix", 20, 40);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Models: RF + OneClassSVM + Q-Learning", 20, 56);\n'
        '\t\t\t\t\t\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 42));\n'
        '\t\t\t\t\tg2d.setColor(neonCyan);\n'
        '\t\t\t\t\tg2d.drawString(String.format("%,d", totalPackets), 20, 110);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));\n'
        '\t\t\t\t\tg2d.setColor(java.awt.Color.LIGHT_GRAY);\n'
        '\t\t\t\t\tg2d.drawString("PACKETS", 20, 135);\n'
        '\t\t\t\t\t\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 42));\n'
        '\t\t\t\t\tg2d.setColor(neonRed);\n'
        '\t\t\t\t\tg2d.drawString(String.format("%,d", totalAnomalies), 20, 200);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));\n'
        '\t\t\t\t\tg2d.setColor(java.awt.Color.LIGHT_GRAY);\n'
        '\t\t\t\t\tg2d.drawString("ANOMALIES", 20, 225);\n'
        '\t\t\t\t\t\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 42));\n'
        '\t\t\t\t\tg2d.setColor(neonMagenta);\n'
        '\t\t\t\t\tdouble mae = totalPackets == 0 ? 0 : totalError / totalPackets;\n'
        '\t\t\t\t\tg2d.drawString(String.format("%.3f", mae), 20, 290);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));\n'
        '\t\t\t\t\tg2d.setColor(java.awt.Color.LIGHT_GRAY);\n'
        '\t\t\t\t\tg2d.drawString("GLOBAL MAE", 20, 315);'
    )

    new_kpi = (
        'g2d.drawString("AI Model Pipeline Monitor", 15, 30);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 9));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(120,120,120));\n'
        '\t\t\t\t\tg2d.drawString("Live inference pipeline status", 15, 42);\n'
        '\t\t\t\t\t// --- Accuracy Gauge Arc ---\n'
        '\t\t\t\t\tdouble mae = totalPackets == 0 ? 0 : totalError / totalPackets;\n'
        '\t\t\t\t\tdouble accuracy = Math.max(0, Math.min(100, 100.0 - mae * 10));\n'
        '\t\t\t\t\tint arcX = getWidth()/2 - 55, arcY = 48;\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(40,40,50));\n'
        '\t\t\t\t\tg2d.setStroke(new java.awt.BasicStroke(12, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));\n'
        '\t\t\t\t\tg2d.drawArc(arcX, arcY, 110, 110, 0, 180);\n'
        '\t\t\t\t\tjava.awt.Color accColor = accuracy > 80 ? neonGreen : (accuracy > 50 ? neonOrange : neonRed);\n'
        '\t\t\t\t\tg2d.setColor(accColor);\n'
        '\t\t\t\t\tg2d.drawArc(arcX, arcY, 110, 110, 180, -(int)(accuracy * 1.8));\n'
        '\t\t\t\t\tg2d.setStroke(new java.awt.BasicStroke(1));\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));\n'
        '\t\t\t\t\tg2d.drawString(String.format("%.1f%%", accuracy), arcX + 22, arcY + 80);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 10));\n'
        '\t\t\t\t\tg2d.setColor(java.awt.Color.LIGHT_GRAY);\n'
        '\t\t\t\t\tg2d.drawString("PREDICTION ACCURACY", arcX + 5, arcY + 96);\n'
        '\t\t\t\t\t// --- R-squared + RMSE ---\n'
        '\t\t\t\t\tdouble r2 = 0;\n'
        '\t\t\t\t\tif (totalPackets > 2) {\n'
        '\t\t\t\t\t\tdouble meanA = sumActual / totalPackets;\n'
        '\t\t\t\t\t\tdouble ssTot = sumActSq - totalPackets * meanA * meanA;\n'
        '\t\t\t\t\t\tr2 = ssTot > 0 ? 1.0 - (sumSqErr / ssTot) : 0;\n'
        '\t\t\t\t\t}\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 16));\n'
        '\t\t\t\t\tg2d.setColor(r2 > 0.7 ? neonCyan : neonOrange);\n'
        '\t\t\t\t\tg2d.drawString(String.format("R\\u00B2 = %.4f", r2), 15, 170);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 12));\n'
        '\t\t\t\t\tg2d.setColor(neonMagenta);\n'
        '\t\t\t\t\tg2d.drawString(String.format("RMSE = %.4f ms", totalPackets==0?0:Math.sqrt(sumSqErr/totalPackets)), 15, 190);\n'
        '\t\t\t\t\t// --- Model Status Indicators ---\n'
        '\t\t\t\t\tint sy = 215;\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 12));\n'
        '\t\t\t\t\tString[][] models = {{"Random Forest","Latency Pred"},{"OneClassSVM","Anomaly Det."},{"Q-Learning","Load Balance"},{"Lin. Regress.","Forecaster"},{"WGAN-GP","DDoS Synth."}};\n'
        '\t\t\t\t\tjava.awt.Color[] mColors = {neonCyan, neonRed, neonGreen, neonMagenta, neonOrange};\n'
        '\t\t\t\t\tfor (int mi=0; mi<5; mi++) {\n'
        '\t\t\t\t\t\tg2d.setColor(mColors[mi]);\n'
        '\t\t\t\t\t\tg2d.fillRoundRect(15, sy+mi*26-10, 8, 8, 4, 4);\n'
        '\t\t\t\t\t\tg2d.setColor(java.awt.Color.WHITE);\n'
        '\t\t\t\t\t\tg2d.drawString(models[mi][0], 28, sy+mi*26);\n'
        '\t\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.PLAIN, 10));\n'
        '\t\t\t\t\t\tg2d.drawString(models[mi][1]+" \\u2713", 140, sy+mi*26);\n'
        '\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 12));\n'
        '\t\t\t\t\t}'
    )
    c = c.replace(old_kpi, new_kpi, 1)

    # ===== FIX 4: Update addData to track R²/RMSE =====
    old_add = (
        'totalPackets++;\n'
        '\t\t\t\tdouble error = Math.abs(actual - predicted);\n'
        '\t\t\t\tif (!Double.isNaN(error)) {\n'
        '\t\t\t\t\ttotalError += error;\n'
        '\t\t\t\t\terrors.add(error);\n'
        '\t\t\t\t}\n'
        '\t\t\t\tif (anomalyScore < 0) totalAnomalies++;'
    )
    new_add = (
        'totalPackets++;\n'
        '\t\t\t\tlastActual=actual; lastPred=predicted;\n'
        '\t\t\t\tsumActual+=actual; sumActSq+=actual*actual;\n'
        '\t\t\t\tdouble error = Math.abs(actual - predicted);\n'
        '\t\t\t\tif (!Double.isNaN(error)) {\n'
        '\t\t\t\t\ttotalError += error;\n'
        '\t\t\t\t\tsumSqErr+=(actual-predicted)*(actual-predicted);\n'
        '\t\t\t\t\terrors.add(error);\n'
        '\t\t\t\t}\n'
        '\t\t\t\tif (anomalyScore < 0) totalAnomalies++;'
    )
    c = c.replace(old_add, new_add, 1)

    with open(ALP, 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Fixed battery overlap + replaced TelemetryDash KPI with AI Model Pipeline Monitor!")

if __name__ == '__main__':
    patch()
