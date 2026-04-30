import re

def inject_premium_ui():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    main_start = content.find('<Name><![CDATA[Main]]></Name>')
    if main_start == -1: return
    
    premium_ui = """
			<AdditionalClassCode><![CDATA[
	public class HeavyDashboard extends javax.swing.JFrame {
		private java.util.ArrayList<Double> actualLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> predictedLatencies = new java.util.ArrayList<>();
		private java.util.ArrayList<Boolean> anomalies = new java.util.ArrayList<>();
		private java.util.ArrayList<Double> packetSizes = new java.util.ArrayList<>();
		private String lastError = "";
		
		private int totalAnomalies = 0;
		private double totalError = 0.0;
		
		private javax.swing.JPanel pnlTimePlot;
		private javax.swing.JPanel pnlScatter;
		private javax.swing.JPanel pnlHistogram;
		private javax.swing.JPanel pnlKPI;
		
		// Premium Colors
		private java.awt.Color bgDark = new java.awt.Color(13, 17, 23);
		private java.awt.Color panelDark = new java.awt.Color(22, 27, 34);
		private java.awt.Color neonCyan = new java.awt.Color(0, 240, 255);
		private java.awt.Color neonMagenta = new java.awt.Color(255, 0, 255);
		private java.awt.Color neonRed = new java.awt.Color(255, 60, 60);
		private java.awt.Color gridColor = new java.awt.Color(255, 255, 255, 15);
		
		public HeavyDashboard() {
			setTitle("Advanced Multi-Model AI Analytics - v2.0 Premium");
			setSize(1400, 900);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(2, 2, 15, 15));
			getContentPane().setBackground(bgDark);
			
			// Utility to draw rounded rects
			java.awt.geom.RoundRectangle2D.Float roundRect = new java.awt.geom.RoundRectangle2D.Float(0, 0, 0, 0, 20, 20);
			
			// 1. TimePlot (Top-Left)
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
						
						// Add 20% padding to max
						maxVal = maxVal * 1.2;
						
						int w = getWidth() - 60;
						int h = getHeight() - 90;
						double scaleY = h / maxVal;
						
						// Draw Grid
						g2d.setColor(gridColor);
						for(int i=0; i<=5; i++) {
							int yPos = 60 + i*(h/5);
							g2d.drawLine(30, yPos, 30+w, yPos);
							g2d.drawString(String.format("%.1fms", (5-i)*(maxVal/5)), 5, yPos - 5);
						}
						
						// Draw Predicted Line (Magenta)
						g2d.setColor(neonMagenta);
						g2d.setStroke(new java.awt.BasicStroke(3, java.awt.BasicStroke.CAP_ROUND, java.awt.BasicStroke.JOIN_ROUND));
						for(int i=0; i<n-1; i++) {
							double v1 = predictedLatencies.get(startIdx + i);
							double v2 = predictedLatencies.get(startIdx + i + 1);
							if(Double.isNaN(v1) || Double.isNaN(v2)) continue;
							int x1 = 30 + (i * w / (n-1));
							int y1 = 60 + h - (int)(v1 * scaleY);
							int x2 = 30 + ((i+1) * w / (n-1));
							int y2 = 60 + h - (int)(v2 * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
						
						// Draw Actual Line (Cyan)
						g2d.setColor(neonCyan);
						for(int i=0; i<n-1; i++) {
							double v1 = actualLatencies.get(startIdx + i);
							double v2 = actualLatencies.get(startIdx + i + 1);
							if(Double.isNaN(v1) || Double.isNaN(v2)) continue;
							int x1 = 30 + (i * w / (n-1));
							int y1 = 60 + h - (int)(v1 * scaleY);
							int x2 = 30 + ((i+1) * w / (n-1));
							int y2 = 60 + h - (int)(v2 * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
					}
				}
			};
			pnlTimePlot.setOpaque(false);
			
			// 2. Anomaly Scatter (Top-Right)
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
						int w = getWidth() - 60;
						int h = getHeight() - 90;
						
						double maxLat = 0.001, maxSize = 0.001;
						for (double l : actualLatencies) if (l > maxLat) maxLat = l;
						for (double s : packetSizes) if (s > maxSize) maxSize = s;
						
						// Draw Grid
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
			
			// 3. Error Histogram (Bottom-Left)
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
					g2d.drawString("AI Error Distribution Curve", 30, 40);
					
					if (actualLatencies.size() > 0) {
						int[] bins = new int[25];
						int maxBin = 0;
						for (int i=0; i<actualLatencies.size(); i++) {
							double err = Math.abs(actualLatencies.get(i) - predictedLatencies.get(i));
							if(Double.isNaN(err)) continue;
							// Buckets of 1ms (0 to 25ms)
							int b = Math.min((int)(err), 24); 
							bins[b]++;
							if (bins[b] > maxBin) maxBin = bins[b];
						}
						
						int w = getWidth() - 60;
						int h = getHeight() - 90;
						int barW = w / 25;
						
						for (int i=0; i<25; i++) {
							int barH = maxBin == 0 ? 0 : (int)(((double)bins[i] / maxBin) * h);
							
							// Gradient paint for bars
							java.awt.GradientPaint gp = new java.awt.GradientPaint(
								0, 60 + h - barH, neonMagenta,
								0, 60 + h, new java.awt.Color(100, 0, 150, 50)
							);
							g2d.setPaint(gp);
							g2d.fillRoundRect(30 + i*barW, 60 + h - barH, barW - 4, barH, 10, 10);
						}
					}
				}
			};
			pnlHistogram.setOpaque(false);
			
			// 4. KPI Matrix (Bottom-Right)
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
					g2d.drawString("Live Telemetry Matrix", 30, 40);
					
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
					g2d.drawString("NETWORK ANOMALIES DETECTED", 50, 270);
					
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.BOLD, 48));
					g2d.setColor(neonMagenta);
					double mae = actualLatencies.size() == 0 ? 0 : totalError / actualLatencies.size();
					g2d.drawString(String.format("%.3f ms", mae), 50, 360);
					g2d.setFont(new java.awt.Font("Segoe UI", java.awt.Font.PLAIN, 18));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("AI PREDICTION ERROR (MAE)", 50, 390);
					
					if (!lastError.isEmpty()) {
						g2d.setFont(new java.awt.Font("Consolas", java.awt.Font.PLAIN, 14));
						g2d.setColor(java.awt.Color.RED);
						g2d.drawString("ERR: " + lastError, 50, 430);
					}
				}
			};
			pnlKPI.setOpaque(false);
			
			add(pnlTimePlot);
			add(pnlScatter);
			add(pnlHistogram);
			add(pnlKPI);
		}
		
		public void addData(double actual, double predicted, double size, double anomalyScore) {
			javax.swing.SwingUtilities.invokeLater(new Runnable() {
				public void run() {
					try {
						actualLatencies.add(actual);
						predictedLatencies.add(predicted);
						packetSizes.add(size);
						
						double error = Math.abs(actual - predicted);
						if (!Double.isNaN(error)) {
							totalError += error;
						}
						
						// Anomaly model prediction. Usually negative means anomaly in OneClassSVM.
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
					} catch (Exception e) {
						lastError = "AddData Exception: " + e.getMessage();
						pnlKPI.repaint();
					}
				}
			});
		}
		
		public void logError(String err) {
			javax.swing.SwingUtilities.invokeLater(new Runnable() {
				public void run() {
					lastError = err;
					pnlKPI.repaint();
				}
			});
		}
	}
	
	public HeavyDashboard dashboard;
]]></AdditionalClassCode>"""

    content = re.sub(r'<AdditionalClassCode>.*?</AdditionalClassCode>', premium_ui.strip(), content, flags=re.DOTALL)
    
    # Update the packet hook to score BOTH models
    target_hook = r"""// 1\. Prepare features for Pre-Trained Random Forest Model.*?dashboard\.addData\(agent\.flow_duration, pred, agent\.packet_size\);"""
    
    new_hook = """// 1. Prepare features for AI Pipeline
            double[] rfFeatures = new double[]{agent.packet_size, agent.inter_arrival};
            double[] anomalyFeatures = new double[]{agent.packet_size, agent.inter_arrival, agent.flow_duration};
            
            // 2. Score offline models natively in Java!
            double pred = OfflineAiPredictor.score(rfFeatures);
            double anomalyScore = AnomalyModel.score(anomalyFeatures);
            
            // 3. Update Premium Multi-Graph Dashboard
            dashboard.addData(agent.flow_duration, pred, agent.packet_size, anomalyScore);"""
            
    content = re.sub(target_hook, new_hook, content, flags=re.DOTALL)

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected Premium Multi-Model UI!")

if __name__ == '__main__':
    inject_premium_ui()
