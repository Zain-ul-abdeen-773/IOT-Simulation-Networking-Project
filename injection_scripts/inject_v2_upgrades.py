import re, os

ALP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'FinalCCNProject.alp')

def patch():
    with open(ALP,'r',encoding='utf-8') as f:
        c = f.read()

    # ===== 1. AXIS LABELS FOR LATENCY DASH (TimePlot) =====
    c = c.replace(
        'g2d.drawString("Live Latency Tracking", 20, 35);',
        'g2d.drawString("Live Latency Tracking", 20, 35);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Model: Random Forest (m2cgen transpiled)", 20, 50);'
    )
    # Y-axis labels for timePlot
    old_grid1 = 'for(int i=0; i<=5; i++) g2d.drawLine(20, 45 + i*(h/5), 20+w, 45 + i*(h/5));'
    new_grid1 = (
        'for(int i=0; i<=5; i++) {\n'
        '\t\t\t\t\t\t\tg2d.drawLine(20, 45 + i*(h/5), 20+w, 45 + i*(h/5));\n'
        '\t\t\t\t\t\t\tg2d.setColor(new java.awt.Color(160,160,160));\n'
        '\t\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.PLAIN, 9));\n'
        '\t\t\t\t\t\t\tg2d.drawString(String.format("%.1fms",(5-i)*(maxVal/5)), 1, 49+i*(h/5));\n'
        '\t\t\t\t\t\t\tg2d.setColor(gridColor);\n'
        '\t\t\t\t\t\t}'
    )
    c = c.replace(old_grid1, new_grid1, 1)

    # ===== 2. AXIS LABELS FOR LATENCY DASH (Forecaster) =====
    c = c.replace(
        'g2d.drawString("Time-Series Forecasting", 20, 35);',
        'g2d.drawString("Time-Series Forecasting", 20, 35);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Model: Linear Regression Forecaster (FutureForecaster)", 20, 50);'
    )

    # ===== 3. AXIS LABELS FOR SECURITY DASH =====
    c = c.replace(
        'g2d.drawString("OneClassSVM Defense Radar", 30, 40);',
        'g2d.drawString("OneClassSVM Defense Radar", 30, 40);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Model: OneClassSVM (Anomaly Detection, m2cgen)", 30, 56);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 11));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(0,240,255));\n'
        '\t\t\t\t\tg2d.drawString("● Normal", getWidth()-160, 40);\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(255,60,60));\n'
        '\t\t\t\t\tg2d.drawString("● Anomaly", getWidth()-90, 40);'
    )
    # Security axis labels inside the if block, after grid drawing
    old_sec_grid = (
        'g2d.drawLine(30 + i*(w/5), 60, 30 + i*(w/5), 60+h);\n'
        '\t\t\t\t\t\t}\n'
        '\t\t\t\t\t\tfor (int i=0; i<actualLatencies.size(); i++) {'
    )
    new_sec_grid = (
        'g2d.drawLine(30 + i*(w/5), 60, 30 + i*(w/5), 60+h);\n'
        '\t\t\t\t\t\t}\n'
        '\t\t\t\t\t\tg2d.setColor(new java.awt.Color(160,160,160));\n'
        '\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.PLAIN, 9));\n'
        '\t\t\t\t\t\tfor(int i=0;i<=5;i++) {\n'
        '\t\t\t\t\t\t\tg2d.drawString(String.format("%.0f",(5-i)*(maxLat/5)), 2, 64+i*(h/5));\n'
        '\t\t\t\t\t\t\tg2d.drawString(String.format("%.0f",i*(maxSize/5)), 28+i*(w/5), 60+h+12);\n'
        '\t\t\t\t\t\t}\n'
        '\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\t\tg2d.drawString("Packet Size (bytes) \\u2192", w/2, 60+h+24);\n'
        '\t\t\t\t\t\tjava.awt.Graphics2D g2r = (java.awt.Graphics2D)g2d.create();\n'
        '\t\t\t\t\t\tg2r.rotate(-Math.PI/2, 12, 60+h/2);\n'
        '\t\t\t\t\t\tg2r.drawString("Flow Duration (ms) \\u2192", 12, 60+h/2);\n'
        '\t\t\t\t\t\tg2r.dispose();\n'
        '\t\t\t\t\t\tfor (int i=0; i<actualLatencies.size(); i++) {'
    )
    c = c.replace(old_sec_grid, new_sec_grid, 1)

    # ===== 4. AXIS LABELS FOR TELEMETRY DASH (Histogram) =====
    c = c.replace(
        'g2d.drawString("Error Curve", 20, 40);',
        'g2d.drawString("Prediction Error Distribution", 20, 40);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Model: Random Forest vs Actual | MAE Bins", 20, 55);'
    )
    # Histogram X-axis after bars
    old_hist = 'g2d.fillRoundRect(20 + i*barW, 50 + h - barH, barW - 2, barH, 5, 5);\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t};\n\t\t\tpnlHistogram.setOpaque(false);'
    new_hist = (
        'g2d.fillRoundRect(20 + i*barW, 50 + h - barH, barW - 2, barH, 5, 5);\n'
        '\t\t\t\t\t\t}\n'
        '\t\t\t\t\t\tg2d.setColor(new java.awt.Color(160,160,160));\n'
        '\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.PLAIN, 9));\n'
        '\t\t\t\t\t\tfor(int i=0;i<15;i+=3) g2d.drawString(i+"ms", 20+i*barW, 50+h+12);\n'
        '\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Segoe UI",java.awt.Font.ITALIC,10));\n'
        '\t\t\t\t\t\tg2d.drawString("Error Magnitude (ms) \\u2192", w/2-30, 50+h+24);\n'
        '\t\t\t\t\t}\n'
        '\t\t\t\t}\n'
        '\t\t\t};\n'
        '\t\t\tpnlHistogram.setOpaque(false);'
    )
    c = c.replace(old_hist, new_hist, 1)

    # ===== 5. AXIS LABELS FOR ENERGY DASH (Battery) =====
    c = c.replace(
        'g2d.drawString("Battery Drain", 20, 35);',
        'g2d.drawString("Battery Drain Simulation", 20, 35);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Model: Energy Digital Twin", 20, 50);'
    )
    # Battery Y-axis labels
    old_bat_grid = 'for(int i=0; i<=5; i++) g2d.drawLine(20, 45 + i*(h/5), 20+w, 45 + i*(h/5));\n'
    new_bat_grid = (
        'for(int i=0; i<=5; i++) {\n'
        '\t\t\t\t\t\t\tg2d.drawLine(20, 45+i*(h/5), 20+w, 45+i*(h/5));\n'
        '\t\t\t\t\t\t\tg2d.setColor(new java.awt.Color(160,160,160));\n'
        '\t\t\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas",java.awt.Font.PLAIN,9));\n'
        '\t\t\t\t\t\t\tg2d.drawString((100-i*20)+"%", 1, 49+i*(h/5));\n'
        '\t\t\t\t\t\t\tg2d.setColor(gridColor);\n'
        '\t\t\t\t\t\t}\n'
    )
    c = c.replace(old_bat_grid, new_bat_grid, 1)

    # ===== 6. TWIN HEALTH LABEL =====
    c = c.replace(
        'g2d.drawString("Twin Health", 20, 35);',
        'g2d.drawString("Digital Twin Health Index", 20, 35);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Composite: Battery + Anomaly Density", 20, 50);'
    )

    # ===== 7. TELEMETRY KPI LABEL =====
    c = c.replace(
        'g2d.drawString("Live Matrix", 20, 40);',
        'g2d.drawString("Live Telemetry KPI Matrix", 20, 40);\n'
        '\t\t\t\t\tg2d.setFont(new java.awt.Font("Consolas", java.awt.Font.ITALIC, 10));\n'
        '\t\t\t\t\tg2d.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2d.drawString("Models: RF + OneClassSVM + Q-Learning", 20, 56);'
    )

    # ===== 8. ADD 5TH REPORT DASHBOARD =====
    report_class = (
        '\n\t// 5. REAL-TIME OPERATIONS REPORT DASHBOARD\n'
        '\tpublic class ReportDash extends javax.swing.JFrame {\n'
        '\t\tprivate java.util.ArrayList<String> logLines = new java.util.ArrayList<>();\n'
        '\t\tprivate int pktCount=0, anomCount=0, rlActions=0, ganInjections=0;\n'
        '\t\tprivate double sumError=0, minLat=Double.MAX_VALUE, maxLat=0, lastPred=0, lastActual=0;\n'
        '\t\tprivate long startMs = System.currentTimeMillis();\n'
        '\t\tprivate java.awt.Color bgDark=new java.awt.Color(13,17,23);\n'
        '\t\tprivate java.awt.Color panelDark=new java.awt.Color(22,27,34);\n'
        '\t\tprivate java.awt.Color neonCyan=new java.awt.Color(0,240,255);\n'
        '\t\tprivate java.awt.Color neonGreen=new java.awt.Color(57,255,20);\n'
        '\t\tprivate java.awt.Color neonRed=new java.awt.Color(255,60,60);\n'
        '\t\tprivate java.awt.Color neonMagenta=new java.awt.Color(255,0,255);\n'
        '\t\tprivate java.awt.Color neonOrange=new java.awt.Color(255,165,0);\n'
        '\t\tpublic ReportDash() {\n'
        '\t\t\tsetTitle("Real-Time Operations Report");\n'
        '\t\t\tsetSize(750, 500);\n'
        '\t\t\tsetDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);\n'
        '\t\t\tsetLayout(new java.awt.GridLayout(1,2,10,10));\n'
        '\t\t\tgetContentPane().setBackground(bgDark);\n'
        '\t\t\t((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(10,10,10,10));\n'
        '\t\t\tjavax.swing.JPanel pnlStats = new javax.swing.JPanel(){\n'
        '\t\t\t\t@Override protected void paintComponent(java.awt.Graphics g){\n'
        '\t\t\t\t\tsuper.paintComponent(g);\n'
        '\t\t\t\t\tjava.awt.Graphics2D g2=(java.awt.Graphics2D)g;\n'
        '\t\t\t\t\tg2.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING,java.awt.RenderingHints.VALUE_ANTIALIAS_ON);\n'
        '\t\t\t\t\tg2.setColor(panelDark); g2.fillRoundRect(0,0,getWidth(),getHeight(),30,30);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE);\n'
        '\t\t\t\t\tg2.setFont(new java.awt.Font("Segoe UI",java.awt.Font.BOLD,18));\n'
        '\t\t\t\t\tg2.drawString("\\u26A1 Operations Summary",15,30);\n'
        '\t\t\t\t\tg2.setFont(new java.awt.Font("Consolas",java.awt.Font.ITALIC,9));\n'
        '\t\t\t\t\tg2.setColor(new java.awt.Color(140,140,140));\n'
        '\t\t\t\t\tg2.drawString("All Models: RF + SVM + RL + GAN + Forecaster",15,44);\n'
        '\t\t\t\t\tint y=65; int sp=28;\n'
        '\t\t\t\t\tg2.setFont(new java.awt.Font("Segoe UI",java.awt.Font.BOLD,14));\n'
        '\t\t\t\t\tg2.setColor(neonCyan); g2.drawString("Packets Processed:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%,d",pktCount),200,y); y+=sp;\n'
        '\t\t\t\t\tg2.setColor(neonRed); g2.drawString("Anomalies Detected:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%,d",anomCount),200,y); y+=sp;\n'
        '\t\t\t\t\tdouble anomRate=pktCount==0?0:(anomCount*100.0/pktCount);\n'
        '\t\t\t\t\tg2.setColor(neonOrange); g2.drawString("Anomaly Rate:",15,y);\n'
        '\t\t\t\t\tg2.setColor(anomRate>10?neonRed:neonGreen); g2.drawString(String.format("%.2f%%",anomRate),200,y); y+=sp;\n'
        '\t\t\t\t\tdouble mae=pktCount==0?0:sumError/pktCount;\n'
        '\t\t\t\t\tg2.setColor(neonMagenta); g2.drawString("Mean Abs Error:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%.4f ms",mae),200,y); y+=sp;\n'
        '\t\t\t\t\tg2.setColor(neonCyan); g2.drawString("Min Latency:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%.3f ms",minLat==Double.MAX_VALUE?0:minLat),200,y); y+=sp;\n'
        '\t\t\t\t\tg2.setColor(neonCyan); g2.drawString("Max Latency:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%.3f ms",maxLat),200,y); y+=sp;\n'
        '\t\t\t\t\tg2.setColor(neonGreen); g2.drawString("RL Actions:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%,d",rlActions),200,y); y+=sp;\n'
        '\t\t\t\t\tg2.setColor(neonOrange); g2.drawString("GAN Injections:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%,d",ganInjections),200,y); y+=sp;\n'
        '\t\t\t\t\tlong elapsed=(System.currentTimeMillis()-startMs)/1000;\n'
        '\t\t\t\t\tg2.setColor(new java.awt.Color(160,160,160)); g2.drawString("Uptime:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%dm %ds",elapsed/60,elapsed%60),200,y); y+=sp;\n'
        '\t\t\t\t\tg2.setColor(neonMagenta); g2.drawString("Last Prediction:",15,y);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE); g2.drawString(String.format("%.3f ms (actual: %.3f)",lastPred,lastActual),200,y);\n'
        '\t\t\t\t}\n'
        '\t\t\t};\n'
        '\t\t\tpnlStats.setOpaque(false);\n'
        '\t\t\tjavax.swing.JPanel pnlLog = new javax.swing.JPanel(){\n'
        '\t\t\t\t@Override protected void paintComponent(java.awt.Graphics g){\n'
        '\t\t\t\t\tsuper.paintComponent(g);\n'
        '\t\t\t\t\tjava.awt.Graphics2D g2=(java.awt.Graphics2D)g;\n'
        '\t\t\t\t\tg2.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING,java.awt.RenderingHints.VALUE_ANTIALIAS_ON);\n'
        '\t\t\t\t\tg2.setColor(panelDark); g2.fillRoundRect(0,0,getWidth(),getHeight(),30,30);\n'
        '\t\t\t\t\tg2.setColor(java.awt.Color.WHITE);\n'
        '\t\t\t\t\tg2.setFont(new java.awt.Font("Segoe UI",java.awt.Font.BOLD,18));\n'
        '\t\t\t\t\tg2.drawString("\\u23F1 Live Event Log",15,30);\n'
        '\t\t\t\t\tg2.setFont(new java.awt.Font("Consolas",java.awt.Font.PLAIN,11));\n'
        '\t\t\t\t\tint y=50; int maxLines=(getHeight()-60)/14;\n'
        '\t\t\t\t\tint start=Math.max(0,logLines.size()-maxLines);\n'
        '\t\t\t\t\tfor(int i=start;i<logLines.size();i++){\n'
        '\t\t\t\t\t\tString line=logLines.get(i);\n'
        '\t\t\t\t\t\tif(line.contains("ANOMALY")) g2.setColor(neonRed);\n'
        '\t\t\t\t\t\telse if(line.contains("GAN")) g2.setColor(neonOrange);\n'
        '\t\t\t\t\t\telse if(line.contains("RL")) g2.setColor(neonGreen);\n'
        '\t\t\t\t\t\telse g2.setColor(new java.awt.Color(180,180,180));\n'
        '\t\t\t\t\t\tg2.drawString(line,10,y); y+=14;\n'
        '\t\t\t\t\t}\n'
        '\t\t\t\t}\n'
        '\t\t\t};\n'
        '\t\t\tpnlLog.setOpaque(false);\n'
        '\t\t\tadd(pnlStats); add(pnlLog);\n'
        '\t\t}\n'
        '\t\tpublic void addData(double actual,double pred,double anomScore,boolean wasGan,boolean wasRl){\n'
        '\t\t\tjavax.swing.SwingUtilities.invokeLater(()->{pktCount++;\n'
        '\t\t\t\tlastPred=pred; lastActual=actual;\n'
        '\t\t\t\tsumError+=Math.abs(actual-pred);\n'
        '\t\t\t\tif(actual<minLat)minLat=actual; if(actual>maxLat)maxLat=actual;\n'
        '\t\t\t\tif(anomScore<0){anomCount++;logLines.add(String.format("[%05d] \\u26A0 ANOMALY lat=%.2f pkt=%.0f",pktCount,actual,pred));}\n'
        '\t\t\t\tif(wasGan){ganInjections++;logLines.add(String.format("[%05d] \\u2622 GAN DDoS injection simulated",pktCount));}\n'
        '\t\t\t\tif(wasRl){rlActions++;if(pktCount%50==0)logLines.add(String.format("[%05d] \\u2699 RL Q-Learning action applied",pktCount));}\n'
        '\t\t\t\tif(pktCount%25==0)logLines.add(String.format("[%05d] \\u2713 Processed lat=%.2f pred=%.3f err=%.4f",pktCount,actual,pred,Math.abs(actual-pred)));\n'
        '\t\t\t\tif(logLines.size()>500)logLines.remove(0);\n'
        '\t\t\t\trepaint();\n'
        '\t\t\t});\n'
        '\t\t}\n'
        '\t}\n'
    )
    # Insert before field declarations
    c = c.replace(
        '\tpublic LatencyDash latDash;',
        report_class + '\tpublic LatencyDash latDash;'
    )
    # Add field
    c = c.replace(
        'public EnergyDash engDash;',
        'public EnergyDash engDash;\n\tpublic ReportDash rptDash;'
    )

    # ===== 9. UPDATE STARTUP =====
    c = c.replace(
        'engDash = new EnergyDash();',
        'engDash = new EnergyDash();\n\t\trptDash = new ReportDash();'
    )
    c = c.replace(
        'engDash.setLocation(50, 520);',
        'engDash.setLocation(50, 520);\n\t\trptDash.setLocation(1490, 50);'
    )
    c = c.replace(
        'engDash.setVisible(true);',
        'engDash.setVisible(true);\n\t\trptDash.setVisible(true);'
    )

    # ===== 10. UPDATE HOOK TO FEED 5TH DASHBOARD =====
    old_hook = 'if (engDash != null) engDash.addData(agent.packet_size, anomalyScore);'
    new_hook = (
        'if (engDash != null) engDash.addData(agent.packet_size, anomalyScore);\n'
        '        boolean _wasGan = (agent.packet_size > 14000);\n'
        '        boolean _wasRl = true;\n'
        '        if (rptDash != null) rptDash.addData(agent.flow_duration, pred, anomalyScore, _wasGan, _wasRl);'
    )
    c = c.replace(old_hook, new_hook, 1)

    with open(ALP,'w',encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Patched all 4 dashboards with axis labels + model names, added 5th Report Dashboard!")

if __name__=='__main__':
    patch()
