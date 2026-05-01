import re

def inject_multi_dashboard():
    with open('../FinalCCNProject.alp', 'r', encoding='utf-8') as f:
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
		
		public LatencyDash() {
			setTitle("Latency & Forecasting Hub");
			setSize(700, 450);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(2, 1, 15, 15));
			getContentPane().setBackground(bgDark);
			((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(15,15,15,15));
			
			javax.swing.JPanel pnlTimePlot = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 20));
					g2d.drawString("Live Latency Tracking", 20, 35);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 12));
					g2d.setColor(neonCyan);
					g2d.drawString("■ Actual", 250, 35);
					g2d.setColor(neonMagenta);
					g2d.drawString("■ AI Predicted", 320, 35);
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
						int w = getWidth() - 40, h = getHeight() - 60;
						double scaleY = h / maxVal;
						g2d.setColor(gridColor);
						for(int i=0; i<=5; i++) g2d.drawLine(20, 45 + i*(h/5), 20+w, 45 + i*(h/5));
						g2d.setColor(neonMagenta);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							g2d.drawLine(20 + (i * w / (n-1)), 45 + h - (int)(predictedLatencies.get(startIdx + i) * scaleY),
										20 + ((i+1) * w / (n-1)), 45 + h - (int)(predictedLatencies.get(startIdx + i + 1) * scaleY));
						}
						g2d.setColor(neonCyan);
						for(int i=0; i<n-1; i++) {
							g2d.drawLine(20 + (i * w / (n-1)), 45 + h - (int)(actualLatencies.get(startIdx + i) * scaleY),
										20 + ((i+1) * w / (n-1)), 45 + h - (int)(actualLatencies.get(startIdx + i + 1) * scaleY));
						}
					}
				}
			};
			pnlTimePlot.setOpaque(false);
			
			javax.swing.JPanel pnlForecaster = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 20));
					g2d.drawString("Time-Series Forecasting", 20, 35);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 12));
					g2d.setColor(neonGreen);
					g2d.drawString("■ Predicted Future (t+10)", 300, 35);
					if (forecastedLatencies.size() > 1) {
						int n = Math.min(forecastedLatencies.size(), 150);
						int startIdx = forecastedLatencies.size() - n;
						double maxVal = 0.001;
						for(int i=0; i<n; i++) if (forecastedLatencies.get(startIdx + i) > maxVal) maxVal = forecastedLatencies.get(startIdx + i);
						maxVal = maxVal * 1.5;
						int w = getWidth() - 40, h = getHeight() - 60;
						double scaleY = h / maxVal;
						g2d.setColor(neonGreen);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							g2d.drawLine(20 + (i * w / (n-1)), 45 + h - (int)(forecastedLatencies.get(startIdx + i) * scaleY),
										20 + ((i+1) * w / (n-1)), 45 + h - (int)(forecastedLatencies.get(startIdx + i + 1) * scaleY));
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
			setSize(700, 450);
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
					g2d.drawString("OneClassSVM Defense Radar", 30, 40);
					if (actualLatencies.size() > 0) {
						int w = getWidth() - 60, h = getHeight() - 80;
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
		
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);
		private java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);
		private java.awt.Color neonRed = new java.awt.Color(255, 60, 60);
		
		public TelemetryDash() {
			setTitle("Telemetry Matrix");
			setSize(700, 450);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(1, 2, 15, 15));
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
					g2d.drawString("Live Matrix", 20, 40);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 42));
					g2d.setColor(neonCyan);
					g2d.drawString(String.format("%,d", totalPackets), 20, 110);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("PACKETS", 20, 135);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 42));
					g2d.setColor(neonRed);
					g2d.drawString(String.format("%,d", totalAnomalies), 20, 200);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("ANOMALIES", 20, 225);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 42));
					g2d.setColor(neonMagenta);
					double mae = totalPackets == 0 ? 0 : totalError / totalPackets;
					g2d.drawString(String.format("%.3f", mae), 20, 290);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("GLOBAL MAE", 20, 315);
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
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 18));
					g2d.drawString("Error Curve", 20, 40);
					
					if (errors.size() > 0) {
						int[] bins = new int[15];
						int maxBin = 0;
						for (double err : errors) {
							int b = Math.min((int)(err), 14); 
							bins[b]++;
							if (bins[b] > maxBin) maxBin = bins[b];
						}
						int w = getWidth() - 40, h = getHeight() - 70, barW = w / 15;
						for (int i=0; i<15; i++) {
							int barH = maxBin == 0 ? 0 : (int)(((double)bins[i] / maxBin) * h);
							java.awt.GradientPaint gp = new java.awt.GradientPaint(0, 50 + h - barH, neonMagenta, 0, 50 + h, new java.awt.Color(100, 0, 150, 50));
							g2d.setPaint(gp);
							g2d.fillRoundRect(20 + i*barW, 50 + h - barH, barW - 2, barH, 5, 5);
						}
					}
				}
			};
			pnlHistogram.setOpaque(false);
			
			add(pnlKPI);
			add(pnlHistogram);
		}
		public void addData(double actual, double predicted, double anomalyScore) {
			javax.swing.SwingUtilities.invokeLater(() -> {
				totalPackets++;
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

	// 4. ENERGY & DIGITAL TWIN DASHBOARD
	public class EnergyDash extends javax.swing.JFrame {
		private java.util.ArrayList<Double> batteryHistory = new java.util.ArrayList<>();
		private double currentBattery = 100.0;
		private double recentAnomalyDensity = 0.0;
		
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color neonGreen = new java.awt.Color(57, 255, 20);
		private java.awt.Color neonRed = new java.awt.Color(255, 60, 60);
		private java.awt.Color neonOrange = new java.awt.Color(255, 165, 0);
		private java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);
		private java.awt.Color gridColor = new java.awt.Color(255, 255, 255, 15);
		
		public EnergyDash() {
			setTitle("Energy & Digital Twin");
			setSize(700, 450);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(1, 2, 15, 15));
			getContentPane().setBackground(bgDark);
			((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(15,15,15,15));
			
			javax.swing.JPanel pnlBattery = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 20));
					g2d.drawString("Battery Drain", 20, 35);
					
					java.awt.Color battColor = currentBattery > 50 ? neonGreen : (currentBattery > 20 ? neonOrange : neonRed);
					g2d.setColor(battColor);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 28));
					g2d.drawString(String.format("%.1f%%", Math.max(0, currentBattery)), getWidth() - 100, 40);
					
					if (batteryHistory.size() > 1) {
						int n = batteryHistory.size();
						int w = getWidth() - 40, h = getHeight() - 60;
						double scaleY = h / 100.0; // Fixed 0 to 100%
						
						g2d.setColor(gridColor);
						for(int i=0; i<=5; i++) g2d.drawLine(20, 45 + i*(h/5), 20+w, 45 + i*(h/5));
						
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							double v1 = batteryHistory.get(i);
							double v2 = batteryHistory.get(i + 1);
							
							java.awt.Color segColor = v1 > 50 ? neonGreen : (v1 > 20 ? neonOrange : neonRed);
							g2d.setColor(segColor);
							
							g2d.drawLine(20 + (i * w / (n-1)), 45 + h - (int)(v1 * scaleY),
										20 + ((i+1) * w / (n-1)), 45 + h - (int)(v2 * scaleY));
						}
					}
				}
			};
			pnlBattery.setOpaque(false);
			
			javax.swing.JPanel pnlDigitalTwin = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 20));
					g2d.drawString("Twin Health", 20, 35);
					
					double healthScore = currentBattery - (recentAnomalyDensity * 50);
					if (healthScore < 0 || Double.isNaN(healthScore)) healthScore = 0;
					
					int cx = getWidth() / 2;
					int cy = getHeight() / 2 + 20;
					int radius = 80;
					
					g2d.setColor(gridColor);
					g2d.drawOval(cx - radius, cy - radius, radius*2, radius*2);
					g2d.drawOval(cx - radius/2, cy - radius/2, radius, radius);
					
					java.awt.Color healthColor = healthScore > 70 ? neonCyan : (healthScore > 30 ? neonOrange : neonRed);
					g2d.setColor(new java.awt.Color(healthColor.getRed(), healthColor.getGreen(), healthColor.getBlue(), 100));
					int coreR = (int)((healthScore / 100.0) * radius);
					g2d.fillOval(cx - coreR, cy - coreR, coreR*2, coreR*2);
					g2d.setColor(healthColor);
					g2d.drawOval(cx - coreR, cy - coreR, coreR*2, coreR*2);
					
					g2d.setFont(new java.awt.Font("Consolas", java.awt.Font.BOLD, 14));
					g2d.setColor(java.awt.Color.WHITE);
					g2d.drawString(String.format("Health: %.1f%%", healthScore), cx - 50, cy - radius - 10);
				}
			};
			pnlDigitalTwin.setOpaque(false);
			
			add(pnlBattery);
			add(pnlDigitalTwin);
		}
		
		public void addData(double packetSize, double anomalyScore) {
			javax.swing.SwingUtilities.invokeLater(() -> {
				currentBattery -= (0.005 + packetSize * 0.00002);
				if (currentBattery < 0) currentBattery = 0;
				batteryHistory.add(currentBattery);
				
				// Keep full history but cap at extremely high number to prevent OOM
				if (batteryHistory.size() > 10000) batteryHistory.remove(0);
				
				double isAnomaly = anomalyScore < 0 ? 1.0 : 0.0;
				recentAnomalyDensity = (recentAnomalyDensity * 0.95) + (isAnomaly * 0.05);
				
				repaint();
			});
		}
	}
	
	public LatencyDash latDash;
	public SecurityDash secDash;
	public TelemetryDash telDash;
	public EnergyDash engDash;
]]></AdditionalClassCode>"""

    # Replace old AdditionalClassCode
    content = re.sub(r'<AdditionalClassCode>.*?</AdditionalClassCode>', multi_ui.strip(), content, flags=re.DOTALL)
    
    # Update StartupCode
    startup = """			<StartupCode><![CDATA[
	try {
		latDash = new LatencyDash();
		secDash = new SecurityDash();
		telDash = new TelemetryDash();
		engDash = new EnergyDash();
		
		// Perfect 4-Quadrant 1080p fit
		latDash.setLocation(50, 50);
		secDash.setLocation(770, 50);
		telDash.setLocation(770, 520);
		engDash.setLocation(50, 520);
		
		latDash.setVisible(true);
		secDash.setVisible(true);
		telDash.setVisible(true);
		engDash.setVisible(true);
	} catch (Exception e) {}
]]></StartupCode>"""
    content = re.sub(r'<StartupCode>.*?</StartupCode>', startup.strip(), content, flags=re.DOTALL)
    
    # Fix the method signature call in Cloud_Received hook
    content = content.replace("telDash.addData(agent.flow_duration, pred, anomalyScore, agent.packet_size);",
                              "telDash.addData(agent.flow_duration, pred, anomalyScore);")

    with open('../FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected the 4-Dashboard Architecture!")

if __name__ == '__main__':
    inject_multi_dashboard()
