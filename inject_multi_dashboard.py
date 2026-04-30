import re

def inject_multi_dashboard():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    main_start = content.find('<Name><![CDATA[Main]]></Name>')
    if main_start == -1: return
    
    multi_ui = """
			<AdditionalClassCode><![CDATA[
	// 1. LATENCY DASHBOARD
	public class LatencyDash extends javax.swing.JFrame {
		public java.util.ArrayList<Double> actualLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> predictedLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> forecastedLatencies = new java.util.ArrayList<>();
		
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);
		private java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);
		private java.awt.Color neonGreen = new java.awt.Color(57, 255, 20);
		private java.awt.Color gridColor = new java.awt.Color(255, 255, 255, 15);
		
		private javax.swing.JPanel pnlTimePlot;
		private javax.swing.JPanel pnlForecaster;
		
		public LatencyDash() {
			setTitle("Latency & Forecasting Hub");
			setSize(800, 900);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(2, 1, 15, 15));
			getContentPane().setBackground(bgDark);
			((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(15,15,15,15));
			
			pnlTimePlot = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("Live Latency Tracking", 30, 40);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 14));
					g2d.setColor(neonCyan);
					g2d.drawString("■ Actual", 300, 40);
					g2d.setColor(neonMagenta);
					g2d.drawString("■ AI Predicted", 380, 40);
					if (actualLatencies.size() > 1) {
						int n = Math.min(actualLatencies.size(), 150);
						int startIdx = actualLatencies.size() - n;
						double maxVal = 0.001;
						for(int i=0; i<n; i++) {
							double v1 = actualLatencies.get(startIdx + i);
							double v2 = predictedLatencies.get(startIdx + i);
							if (!Double.isNaN(v1) && v1 > maxVal) maxVal = v1;
							if (!Double.isNaN(v2) && v2 > maxVal) maxVal = v2;
						}
						maxVal = maxVal * 1.2;
						int w = getWidth() - 60, h = getHeight() - 90;
						double scaleY = h / maxVal;
						g2d.setColor(gridColor);
						for(int i=0; i<=5; i++) g2d.drawLine(30, 60 + i*(h/5), 30+w, 60 + i*(h/5));
						g2d.setColor(neonMagenta);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							g2d.drawLine(30 + (i * w / (n-1)), 60 + h - (int)(predictedLatencies.get(startIdx + i) * scaleY),
										30 + ((i+1) * w / (n-1)), 60 + h - (int)(predictedLatencies.get(startIdx + i + 1) * scaleY));
						}
						g2d.setColor(neonCyan);
						for(int i=0; i<n-1; i++) {
							g2d.drawLine(30 + (i * w / (n-1)), 60 + h - (int)(actualLatencies.get(startIdx + i) * scaleY),
										30 + ((i+1) * w / (n-1)), 60 + h - (int)(actualLatencies.get(startIdx + i + 1) * scaleY));
						}
					}
				}
			};
			pnlTimePlot.setOpaque(false);
			
			pnlForecaster = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("Time-Series AI Forecasting", 30, 40);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 14));
					g2d.setColor(neonGreen);
					g2d.drawString("■ Predicted Future (t+10)", 350, 40);
					if (forecastedLatencies.size() > 1) {
						int n = Math.min(forecastedLatencies.size(), 150);
						int startIdx = forecastedLatencies.size() - n;
						double maxVal = 0.001;
						for(int i=0; i<n; i++) if (forecastedLatencies.get(startIdx + i) > maxVal) maxVal = forecastedLatencies.get(startIdx + i);
						maxVal = maxVal * 1.5;
						int w = getWidth() - 60, h = getHeight() - 70;
						double scaleY = h / maxVal;
						g2d.setColor(neonGreen);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							g2d.drawLine(30 + (i * w / (n-1)), 40 + h - (int)(forecastedLatencies.get(startIdx + i) * scaleY),
										30 + ((i+1) * w / (n-1)), 40 + h - (int)(forecastedLatencies.get(startIdx + i + 1) * scaleY));
						}
					}
				}
			};
			pnlForecaster.setOpaque(false);
			
			add(pnlTimePlot);
			add(pnlForecaster);
		}
		
		public void addData(double actual, double predicted) {
			javax.swing.SwingUtilities.invokeLater(() -> {
				actualLatencies.add(actual);
				predictedLatencies.add(predicted);
				if(actualLatencies.size() > 1000) { actualLatencies.remove(0); predictedLatencies.remove(0); }
				repaint();
			});
		}
		public void addForecast(double futureVal) {
			javax.swing.SwingUtilities.invokeLater(() -> {
				forecastedLatencies.add(futureVal);
				if(forecastedLatencies.size() > 1000) forecastedLatencies.remove(0);
				repaint();
			});
		}
	}

	// 2. SECURITY DASHBOARD
	public class SecurityDash extends javax.swing.JFrame {
		private java.util.ArrayList<Double> actualLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> packetSizes = new java.util.ArrayList<>();
		private java.util.ArrayList<Boolean> anomalies = new java.util.ArrayList<>();
		
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color gridColor = new java.awt.Color(255, 255, 255, 15);
		
		public SecurityDash() {
			setTitle("Security & Anomaly Radar");
			setSize(800, 600);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(1, 1, 15, 15));
			getContentPane().setBackground(bgDark);
			((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(15,15,15,15));
			
			javax.swing.JPanel pnlScatter = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("OneClassSVM GAN Defense Radar", 30, 40);
					if (actualLatencies.size() > 0) {
						int w = getWidth() - 60, h = getHeight() - 90;
						double maxLat = 0.001, maxSize = 0.001;
						for (double l : actualLatencies) if (l > maxLat) maxLat = l;
						for (double s : packetSizes) if (s > maxSize) maxSize = s;
						g2d.setColor(gridColor);
						for(int i=0; i<=5; i++) {
							g2d.drawLine(30, 60 + i*(h/5), 30+w, 60 + i*(h/5));
							g2d.drawLine(30 + i*(w/5), 60, 30 + i*(w/5), 60+h);
						}
						for (int i=0; i<actualLatencies.size(); i++) {
							int cx = 30 + (int)((packetSizes.get(i) / maxSize) * w);
							int cy = 60 + h - (int)((actualLatencies.get(i) / maxLat) * h);
							if (anomalies.get(i)) {
								g2d.setColor(new java.awt.Color(255, 60, 60, 200));
								g2d.fillOval(cx-10, cy-10, 20, 20);
								g2d.setColor(java.awt.Color.WHITE);
								g2d.drawOval(cx-10, cy-10, 20, 20);
							} else {
								g2d.setColor(new java.awt.Color(0, 240, 255, 120));
								g2d.fillOval(cx-4, cy-4, 8, 8);
							}
						}
					}
				}
			};
			pnlScatter.setOpaque(false);
			add(pnlScatter);
		}
		public void addData(double actual, double size, double anomalyScore) {
			javax.swing.SwingUtilities.invokeLater(() -> {
				actualLatencies.add(actual);
				packetSizes.add(size);
				anomalies.add(anomalyScore < 0);
				if(actualLatencies.size() > 1000) { actualLatencies.remove(0); packetSizes.remove(0); anomalies.remove(0); }
				repaint();
			});
		}
	}

// 3. TELEMETRY DASHBOARD
	public class TelemetryDash extends javax.swing.JFrame {
		private java.util.ArrayList<Double> errors = new java.util.ArrayList<>();
		private int totalAnomalies = 0, totalPackets = 0;
		private double totalError = 0.0;
		private double batteryLife = 100.0;
		
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);
		private java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);
		private java.awt.Color neonRed = new java.awt.Color(255, 60, 60);
		private java.awt.Color neonGreen = new java.awt.Color(57, 255, 20);
		
		public TelemetryDash() {
			setTitle("Telemetry & AI Error Analysis");
			setSize(600, 900);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(2, 1, 15, 15));
			getContentPane().setBackground(bgDark);
			((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(15,15,15,15));
			
			javax.swing.JPanel pnlKPI = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("Live Telemetry Matrix", 30, 40);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 36));
					g2d.setColor(neonCyan);
					g2d.drawString(String.format("%,d", totalPackets), 40, 100);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("PACKETS PROCESSED", 40, 130);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 36));
					g2d.setColor(neonRed);
					g2d.drawString(String.format("%,d", totalAnomalies), 40, 200);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("GAN ANOMALIES BLOCKED", 40, 230);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 36));
					g2d.setColor(neonMagenta);
					double mae = totalPackets == 0 ? 0 : totalError / totalPackets;
					g2d.drawString(String.format("%.3f ms", mae), 40, 300);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("RL/AI GLOBAL MAE", 40, 330);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 36));
					if (batteryLife > 50) g2d.setColor(neonGreen);
					else if (batteryLife > 20) g2d.setColor(java.awt.Color.ORANGE);
					else g2d.setColor(neonRed);
					g2d.drawString(String.format("%.2f %%", Math.max(0, batteryLife)), 40, 400);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("AVG IOT BATTERY LIFE", 40, 430);
				}
			};
			pnlKPI.setOpaque(false);
			
			javax.swing.JPanel pnlHistogram = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("AI Error Distribution Curve", 30, 40);
					
					if (errors.size() > 0) {
						int[] bins = new int[25];
						int maxBin = 0;
						for (double err : errors) {
							int b = Math.min((int)(err), 24); 
							bins[b]++;
							if (bins[b] > maxBin) maxBin = bins[b];
						}
						int w = getWidth() - 60, h = getHeight() - 90, barW = w / 25;
						for (int i=0; i<25; i++) {
							int barH = maxBin == 0 ? 0 : (int)(((double)bins[i] / maxBin) * h);
							java.awt.GradientPaint gp = new java.awt.GradientPaint(0, 60 + h - barH, neonMagenta, 0, 60 + h, new java.awt.Color(100, 0, 150, 50));
							g2d.setPaint(gp);
							g2d.fillRoundRect(30 + i*barW, 60 + h - barH, barW - 4, barH, 10, 10);
						}
					}
				}
			};
			pnlHistogram.setOpaque(false);
			
			add(pnlKPI);
			add(pnlHistogram);
		}
		public void addData(double actual, double predicted, double anomalyScore, double packetSize) {
			javax.swing.SwingUtilities.invokeLater(() -> {
				totalPackets++;
				// Drain battery simulated logic (0.00005% drain per byte)
				batteryLife -= (packetSize * 0.00005);
				
				double error = Math.abs(actual - predicted);
				if (!Double.isNaN(error)) {
					totalError += error;
					errors.add(error);
				}
				if (anomalyScore < 0) totalAnomalies++;
				if(errors.size() > 1000) errors.remove(0);
				repaint();
			});
		}
	}
	
	public LatencyDash latDash;
	public SecurityDash secDash;
	public TelemetryDash telDash;
]]></AdditionalClassCode>"""

    # Replace old AdditionalClassCode
    content = re.sub(r'<AdditionalClassCode>.*?</AdditionalClassCode>', multi_ui.strip(), content, flags=re.DOTALL)
    
    # Update StartupCode
    startup = """			<StartupCode><![CDATA[
	try {
		latDash = new LatencyDash();
		secDash = new SecurityDash();
		telDash = new TelemetryDash();
		
		// Position them beautifully across the screen
		latDash.setLocation(50, 50);
		secDash.setLocation(900, 50);
		telDash.setLocation(900, 700);
		
		latDash.setVisible(true);
		secDash.setVisible(true);
		telDash.setVisible(true);
	} catch (Exception e) {}
]]></StartupCode>"""
    content = re.sub(r'<StartupCode>.*?</StartupCode>', startup.strip(), content, flags=re.DOTALL)
    
    # Update Cloud_Received hook
    target_hook = r"""// 3\. Score Time-Series Forecaster.*?dashboard\.addData\(agent\.flow_duration, pred, agent\.packet_size, anomalyScore\);"""
    
    new_hook = """// 3. Score Time-Series Forecaster
            if (latDash != null && latDash.actualLatencies.size() >= 3) {
                int s = latDash.actualLatencies.size();
                double[] window = new double[]{
                    latDash.actualLatencies.get(s-3),
                    latDash.actualLatencies.get(s-2),
                    latDash.actualLatencies.get(s-1)
                };
                double futureLatency = FutureForecaster.score(window);
                latDash.addForecast(futureLatency);
            }
            
            // 4. Update Multi-Dashboard Ecosystem
            if (latDash != null) latDash.addData(agent.flow_duration, pred);
            if (secDash != null) secDash.addData(agent.flow_duration, agent.packet_size, anomalyScore);
            if (telDash != null) telDash.addData(agent.flow_duration, pred, anomalyScore, agent.packet_size);"""
            
    content = re.sub(target_hook, new_hook, content, flags=re.DOTALL)

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected the 3-Dashboard Architecture!")

if __name__ == '__main__':
    inject_multi_dashboard()
