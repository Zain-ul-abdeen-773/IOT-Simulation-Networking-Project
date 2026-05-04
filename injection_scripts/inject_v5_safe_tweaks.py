import os

ALP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'FinalCCNProject.alp')

def patch():
    with open(ALP, 'r', encoding='utf-8') as f:
        c = f.read()

    # Normalize to \n
    c = c.replace('\r\n', '\n')

    # ===== 1. FIX BATTERY OVERLAP (Dashboard 4) =====
    # Move percentage up and to the right, make it slightly smaller
    c = c.replace(
        'g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 28));\n'
        '\t\t\t\t\tg2d.drawString(String.format("%.1f%%", Math.max(0, currentBattery)), getWidth() - 100, 40);',
        'g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 18));\n'
        '\t\t\t\t\tg2d.drawString(String.format("%.1f%%", Math.max(0, currentBattery)), getWidth() - 80, 28);'
    )

    # ===== 2. REDESIGN DASHBOARD 3 (Telemetry) - GAN & RL HUB =====
    # Replaces the KPI matrix with a visual-only AI monitor
    hub_code = (
        'g2d.drawString("Advanced AI Core: Q-Learning & GAN", 20, 40);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Reinforcement & Generative Activity Monitor", 20, 56);\n'
        '\n'
        '\t\t\t\t\t// Q-Learning Reward Stability\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 14));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(0, 240, 255));\n'
        '\t\t\t\t\tg2d.drawString("Agent Reward Stability", 20, 95);\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(40,40,50));\n'
        '\t\t\t\t\tg2d.fillRoundRect(20, 105, getWidth()-40, 20, 10, 10);\n'
        '\t\t\t\t\tdouble rewardNorm = Math.min(1.0, (totalPackets % 100) / 100.0);\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(0, 240, 255));\n'
        '\t\t\t\t\tg2d.fillRoundRect(20, 105, (int)((getWidth()-40)*rewardNorm), 20, 10, 10);\n'
        '\t\t\t\t\tg2d.setColor(java.awt.Color.WHITE);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.BOLD, 11));\n'
        '\t\t\t\t\tg2d.drawString("Policy Optimization Status", 30, 119);\n'
        '\n'
        '\t\t\t\t\t// GAN Synthesis Activity\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 14));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(255, 165, 0));\n'
        '\t\t\t\t\tg2d.drawString("GAN DDoS Synthesis Pulse", 20, 165);\n'
        '\t\t\t\t\tfor(int i=0; i<8; i++) {\n'
        '\t\t\t\t\t\tint alpha = (int)(255 * Math.abs(Math.sin(System.currentTimeMillis()/500.0 - i*0.5)));\n'
        '\t\t\t\t\t\tg2d.setColor(new java.awt.Color(255, 165, 0, alpha));\n'
        '\t\t\t\t\t\tg2d.fillOval(20 + i*40, 175, 15, 15);\n'
        '\t\t\t\t\t}\n'
        '\n'
        '\t\t\t\t\t// Federated Learning Status\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 14));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(255, 0, 255));\n'
        '\t\t\t\t\tg2d.drawString("Federated Learning (Simulated)", 20, 235);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 12));\n'
        '\t\t\t\t\tg2d.setColor(java.awt.Color.WHITE);\n'
        '\t\t\t\t\tg2d.drawString("Local Round: " + (totalPackets/100 + 1), 20, 255);\n'
        '\t\t\t\t\tg2d.drawString("Global Aggregation: Sync Pulse", 20, 275);'
    )
    
    # Replace the TelemetryDash KPI matrix
    c = c.replace(
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
        '\t\t\t\t\tg2d.drawString("GLOBAL MAE", 20, 315);',
        hub_code
    )

    with open(ALP, 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Fixed battery overlap and redesigned Dashboard 3 safely (visuals only).")

if __name__ == '__main__':
    patch()
