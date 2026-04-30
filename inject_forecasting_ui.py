import re

def inject_forecasting_ui():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    main_start = content.find('<Name><![CDATA[Main]]></Name>')
    if main_start == -1: return
    
    premium_ui = """
			<AdditionalClassCode><![CDATA[
	public class HeavyDashboard extends javax.swing.JFrame {
		public java.util.ArrayList<Double> actualLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> predictedLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Boolean> anomalies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> packetSizes = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> forecastedLatencies = new java.util.ArrayList<>();
		private String lastError = "";
		
		private int totalAnomalies = 0;
		private double totalError = 0.0;
		
		private javax.swing.JPanel pnlCenter;
		private javax.swing.JPanel pnlTimePlot;
		private javax.swing.JPanel pnlScatter;
		private javax.swing.JPanel pnlHistogram;
		private javax.swing.JPanel pnlKPI;
		private javax.swing.JPanel pnlForecaster;
		
		// Premium Colors
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);
		private java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);
		private java.awt.Color neonRed = new java.awt.Color(255, 60, 60);
		private java.awt.Color neonGreen = new java.awt.Color(57, 255, 20);
		private java.awt.Color gridColor = new java.awt.Color(255, 255, 255, 15);
		
		public HeavyDashboard() {
			setTitle("Advanced Multi-Model AI Analytics - v3.0 Forecasting Edition");
			setSize(1400, 1000);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.BorderLayout(15, 15));
			getContentPane().setBackground(bgDark);
			((javax.swing.JPanel)getContentPane()).setBorder(javax.swing.BorderFactory.createEmptyBorder(15,15,15,15));
			
			pnlCenter = new javax.swing.JPanel(new java.awt.GridLayout(2, 2, 15, 15));
			pnlCenter.setOpaque(false);
			
			// 1. TimePlot
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
						int w = getWidth() - 60;
						int h = getHeight() - 90;
						double scaleY = h / maxVal;
						g2d.setColor(gridColor);
						for(int i=0; i<=5; i++) {
							int yPos = 60 + i*(h/5);
							g2d.drawLine(30, yPos, 30+w, yPos);
						}
						g2d.setColor(neonMagenta);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							int x1 = 30 + (i * w / (n-1));
							int y1 = 60 + h - (int)(predictedLatencies.get(startIdx + i) * scaleY);
							int x2 = 30 + ((i+1) * w / (n-1));
							int y2 = 60 + h - (int)(predictedLatencies.get(startIdx + i + 1) * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
						g2d.setColor(neonCyan);
						for(int i=0; i<n-1; i++) {
							int x1 = 30 + (i * w / (n-1));
							int y1 = 60 + h - (int)(actualLatencies.get(startIdx + i) * scaleY);
							int x2 = 30 + ((i+1) * w / (n-1));
							int y2 = 60 + h - (int)(actualLatencies.get(startIdx + i + 1) * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
					}
				}
			};
			pnlTimePlot.setOpaque(false);
			
			// 2. Anomaly Scatter
			pnlScatter = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("OneClassSVM Anomaly Detection", 30, 40);
					if (actualLatencies.size() > 0) {
						int w = getWidth() - 60, h = getHeight() - 90;
						double maxLat = 0.001, maxSize = 0.001;
						for (double l : actualLatencies) if (l > maxLat) maxLat = l;
						for (double s : packetSizes) if (s > maxSize) maxSize = s;
						for (int i=0; i<actualLatencies.size(); i++) {
							int cx = 30 + (int)((packetSizes.get(i) / maxSize) * w);
							int cy = 60 + h - (int)((actualLatencies.get(i) / maxLat) * h);
							if (anomalies.get(i)) {
								g2d.setColor(new java.awt.Color(255, 60, 60, 200));
								g2d.fillOval(cx-8, cy-8, 16, 16);
								g2d.setColor(java.awt.Color.WHITE);
								g2d.drawOval(cx-8, cy-8, 16, 16);
							} else {
								g2d.setColor(new java.awt.Color(0, 240, 255, 120));
								g2d.fillOval(cx-4, cy-4, 8, 8);
							}
						}
					}
				}
			};
			pnlScatter.setOpaque(false);
			
			// 3. Histogram
			pnlHistogram = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("AI Error Distribution", 30, 40);
					if (actualLatencies.size() > 0) {
						int[] bins = new int[25];
						int maxBin = 0;
						for (int i=0; i<actualLatencies.size(); i++) {
							double err = Math.abs(actualLatencies.get(i) - predictedLatencies.get(i));
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
			
			// 4. KPI
			pnlKPI = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(panelDark);
					g2d.fillRoundRect(0, 0, getWidth(), getHeight(), 30, 30);
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 22));
					g2d.drawString("Live Telemetry", 30, 40);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 48));
					g2d.setColor(neonCyan);
					g2d.drawString(String.format("%,d", actualLatencies.size()), 50, 120);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 18));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("PACKETS PROCESSED", 50, 150);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 48));
					g2d.setColor(neonRed);
					g2d.drawString(String.format("%,d", totalAnomalies), 50, 240);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 18));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("ANOMALIES DETECTED", 50, 270);
				}
			};
			pnlKPI.setOpaque(false);
			
			pnlCenter.add(pnlTimePlot);
			pnlCenter.add(pnlScatter);
			pnlCenter.add(pnlHistogram);
			pnlCenter.add(pnlKPI);
			
			// 5. Forecaster Panel (Bottom)
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
					g2d.drawString("Time-Series AI Forecasting (t+10 packets)", 30, 40);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 14));
					g2d.setColor(neonGreen);
					g2d.drawString("■ Future Prediction", 450, 40);
					
					if (forecastedLatencies.size() > 1) {
						int n = Math.min(forecastedLatencies.size(), 150);
						int startIdx = forecastedLatencies.size() - n;
						double maxVal = 0.001;
						for(int i=0; i<n; i++) {
							double v = forecastedLatencies.get(startIdx + i);
							if (v > maxVal) maxVal = v;
						}
						maxVal = maxVal * 1.5;
						int w = getWidth() - 60, h = getHeight() - 70;
						double scaleY = h / maxVal;
						
						g2d.setColor(neonGreen);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							int x1 = 30 + (i * w / (n-1));
							int y1 = 40 + h - (int)(forecastedLatencies.get(startIdx + i) * scaleY);
							int x2 = 30 + ((i+1) * w / (n-1));
							int y2 = 40 + h - (int)(forecastedLatencies.get(startIdx + i + 1) * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
					}
				}
			};
			pnlForecaster.setOpaque(false);
			pnlForecaster.setPreferredSize(new java.awt.Dimension(1400, 250));
			
			add(pnlCenter, java.awt.BorderLayout.CENTER);
			add(pnlForecaster, java.awt.BorderLayout.SOUTH);
		}
		
		public void addData(double actual, double predicted, double size, double anomalyScore) {
			javax.swing.SwingUtilities.invokeLater(new Runnable() {
				public void run() {
					try {
						actualLatencies.add(actual);
						predictedLatencies.add(predicted);
						packetSizes.add(size);
						
						double error = Math.abs(actual - predicted);
						if (!Double.isNaN(error)) totalError += error;
						
						boolean isAnomaly = (anomalyScore < 0);
						if (isAnomaly) totalAnomalies++;
						anomalies.add(isAnomaly);
						
						if(actualLatencies.size() > 1000) {
							actualLatencies.remove(0);
							predictedLatencies.remove(0);
							packetSizes.remove(0);
							anomalies.remove(0);
						}
						pnlTimePlot.repaint();
						pnlScatter.repaint();
						pnlHistogram.repaint();
						pnlKPI.repaint();
					} catch (Exception e) {}
				}
			});
		}
		
		public void addForecast(double futureVal) {
			javax.swing.SwingUtilities.invokeLater(new Runnable() {
				public void run() {
					forecastedLatencies.add(futureVal);
					if(forecastedLatencies.size() > 1000) forecastedLatencies.remove(0);
					pnlForecaster.repaint();
				}
			});
		}
		
		public void logError(String err) {}
	}
	public HeavyDashboard dashboard;
]]></AdditionalClassCode>"""

    # We need to replace the old AdditionalClassCode block
    content = re.sub(r'<AdditionalClassCode>.*?</AdditionalClassCode>', premium_ui.strip(), content, flags=re.DOTALL)
    
    # Update the packet hook in Cloud_Received
    target_hook = r"""// 1\. Prepare features for AI Pipeline.*?dashboard\.addData\(agent\.flow_duration, pred, agent\.packet_size, anomalyScore\);"""
    
    new_hook = """// 1. Prepare features for AI Pipeline
            double[] rfFeatures = new double[]{agent.packet_size, agent.inter_arrival};
            double[] anomalyFeatures = new double[]{agent.packet_size, agent.inter_arrival, agent.flow_duration};
            
            // 2. Score offline models natively in Java!
            double pred = OfflineAiPredictor.score(rfFeatures);
            double anomalyScore = AnomalyModel.score(anomalyFeatures);
            
            // 3. Score Time-Series Forecaster
            if (dashboard.actualLatencies.size() >= 3) {
                int s = dashboard.actualLatencies.size();
                double[] window = new double[]{
                    dashboard.actualLatencies.get(s-3),
                    dashboard.actualLatencies.get(s-2),
                    dashboard.actualLatencies.get(s-1)
                };
                double futureLatency = FutureForecaster.score(window);
                dashboard.addForecast(futureLatency);
            }
            
            // 4. Update Premium Multi-Graph Dashboard
            dashboard.addData(agent.flow_duration, pred, agent.packet_size, anomalyScore);"""
            
    content = re.sub(target_hook, new_hook, content, flags=re.DOTALL)

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected Time-Series Forecaster UI!")

if __name__ == '__main__':
    inject_forecasting_ui()
