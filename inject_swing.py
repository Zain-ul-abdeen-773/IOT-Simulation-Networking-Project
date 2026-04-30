import re

def inject_code(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    main_start = content.find('<Name><![CDATA[Main]]></Name>')
    if main_start == -1:
        print("Main agent not found")
        return
        
    variables_end = content.find('</Variables>', main_start)
    if variables_end == -1:
        print("</Variables> not found in Main")
        return

    insert_pos = variables_end + len('</Variables>')
    
    additional_code = """
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
		
		public HeavyDashboard() {
			setTitle("AI Analytics Multi-Graph Dashboard (Swing Pop-out)");
			setSize(1400, 900);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			setLayout(new java.awt.GridLayout(2, 2, 10, 10));
			getContentPane().setBackground(new java.awt.Color(5, 10, 20));
			
			// 1. TimePlot (Top-Left)
			pnlTimePlot = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(new java.awt.Color(11, 22, 48));
					g2d.fillRect(0, 0, getWidth(), getHeight());
					
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 20));
					g2d.drawString("Live Latency: Actual vs AI Predicted", 20, 30);
					
					if (actualLatencies.size() > 1) {
						int n = Math.min(actualLatencies.size(), 100);
						int startIdx = actualLatencies.size() - n;
						
						double maxVal = 0.001;
						for(int i=0; i<n; i++) {
							double v1 = actualLatencies.get(startIdx + i);
							double v2 = predictedLatencies.get(startIdx + i);
							if (!Double.isNaN(v1) && v1 > maxVal) maxVal = v1;
							if (!Double.isNaN(v2) && v2 > maxVal) maxVal = v2;
						}
						
						int w = getWidth() - 40;
						int h = getHeight() - 80;
						double scaleY = h / maxVal;
						
						g2d.setColor(new java.awt.Color(255, 255, 255, 30));
						for(int i=0; i<=5; i++) {
							g2d.drawLine(20, 50 + i*(h/5), 20+w, 50 + i*(h/5));
						}
						
						g2d.setColor(new java.awt.Color(34, 211, 238));
						g2d.setStroke(new java.awt.BasicStroke(2));
						for(int i=0; i<n-1; i++) {
							double v1 = actualLatencies.get(startIdx + i);
							double v2 = actualLatencies.get(startIdx + i + 1);
							if(Double.isNaN(v1) || Double.isNaN(v2)) continue;
							int x1 = 20 + (i * w / 100);
							int y1 = 50 + h - (int)(v1 * scaleY);
							int x2 = 20 + ((i+1) * w / 100);
							int y2 = 50 + h - (int)(v2 * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
						
						g2d.setColor(new java.awt.Color(124, 92, 255));
						for(int i=0; i<n-1; i++) {
							double v1 = predictedLatencies.get(startIdx + i);
							double v2 = predictedLatencies.get(startIdx + i + 1);
							if(Double.isNaN(v1) || Double.isNaN(v2)) continue;
							int x1 = 20 + (i * w / 100);
							int y1 = 50 + h - (int)(v1 * scaleY);
							int x2 = 20 + ((i+1) * w / 100);
							int y2 = 50 + h - (int)(v2 * scaleY);
							g2d.drawLine(x1, y1, x2, y2);
						}
						g2d.setColor(java.awt.Color.GRAY);
						g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.PLAIN, 12));
						g2d.drawString(String.format("Max Y: %.3fs", maxVal), 20, 45);
					}
				}
			};
			
			// 2. Anomaly Scatter (Top-Right)
			pnlScatter = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(new java.awt.Color(11, 22, 48));
					g2d.fillRect(0, 0, getWidth(), getHeight());
					
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 20));
					g2d.drawString("Anomaly Detection (Size vs Latency)", 20, 30);
					
					if (actualLatencies.size() > 0) {
						int w = getWidth() - 40;
						int h = getHeight() - 80;
						
						double maxLat = 0.001, maxSize = 0.001;
						for (double l : actualLatencies) if (l > maxLat) maxLat = l;
						for (double s : packetSizes) if (s > maxSize) maxSize = s;
						
						for (int i=0; i<actualLatencies.size(); i++) {
							int cx = 20 + (int)((packetSizes.get(i) / maxSize) * w);
							int cy = 50 + h - (int)((actualLatencies.get(i) / maxLat) * h);
							
							if (anomalies.get(i)) {
								g2d.setColor(new java.awt.Color(255, 50, 50, 200));
								g2d.fillOval(cx-5, cy-5, 10, 10);
							} else {
								g2d.setColor(new java.awt.Color(34, 211, 238, 100));
								g2d.fillOval(cx-3, cy-3, 6, 6);
							}
						}
					}
				}
			};
			
			// 3. Error Histogram (Bottom-Left)
			pnlHistogram = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(new java.awt.Color(11, 22, 48));
					g2d.fillRect(0, 0, getWidth(), getHeight());
					
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 20));
					g2d.drawString("AI Prediction Error Distribution", 20, 30);
					
					if (actualLatencies.size() > 0) {
						int[] bins = new int[20];
						int maxBin = 0;
						for (int i=0; i<actualLatencies.size(); i++) {
							double err = Math.abs(actualLatencies.get(i) - predictedLatencies.get(i));
							if(Double.isNaN(err)) continue;
							int b = Math.min((int)(err * 1000 / 50), 19); // 50ms buckets
							bins[b]++;
							if (bins[b] > maxBin) maxBin = bins[b];
						}
						
						int w = getWidth() - 40;
						int h = getHeight() - 60;
						int barW = w / 20;
						
						for (int i=0; i<20; i++) {
							int barH = maxBin == 0 ? 0 : (int)(((double)bins[i] / maxBin) * h);
							g2d.setColor(new java.awt.Color(124, 92, 255, 180));
							g2d.fillRect(20 + i*barW, 40 + h - barH, barW - 2, barH);
						}
					}
				}
			};
			
			// 4. KPI Matrix (Bottom-Right)
			pnlKPI = new javax.swing.JPanel() {
				@Override
				protected void paintComponent(java.awt.Graphics g) {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					g2d.setColor(new java.awt.Color(11, 22, 48));
					g2d.fillRect(0, 0, getWidth(), getHeight());
					
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 20));
					g2d.drawString("Live Telemetry & KPIs", 20, 30);
					
					g2d.setFont(new java.awt.Font("Consolas", java.awt.Font.BOLD, 32));
					
					g2d.setColor(new java.awt.Color(34, 211, 238));
					g2d.drawString("Total Packets : " + actualLatencies.size(), 40, 100);
					
					g2d.setColor(new java.awt.Color(255, 50, 50));
					g2d.drawString("Anomalies     : " + totalAnomalies, 40, 160);
					
					g2d.setColor(new java.awt.Color(124, 92, 255));
					double mae = actualLatencies.size() == 0 ? 0 : totalError / actualLatencies.size();
					g2d.drawString(String.format("AI Mean Error : %.4fs", mae), 40, 220);
					
					if (!lastError.isEmpty()) {
						g2d.setFont(new java.awt.Font("Consolas", java.awt.Font.PLAIN, 14));
						g2d.setColor(java.awt.Color.RED);
						g2d.drawString("ERR: " + lastError, 40, 300);
					}
				}
			};
			
			add(pnlTimePlot);
			add(pnlScatter);
			add(pnlHistogram);
			add(pnlKPI);
		}
		
		public void addData(double actual, double predicted, double size) {
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
						
						// Dynamic Anomaly Threshold
						// Anomaly if error is > 0.5s or > 50% of actual latency
						boolean isAnomaly = false;
						if (!Double.isNaN(error) && actual > 0.001) {
							if (error > 0.5 || error > actual * 0.5) {
								isAnomaly = true;
								totalAnomalies++;
							}
						}
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

    startup_code = """
			<StartupCode><![CDATA[
	// Initialize and show custom Swing UI Dashboard
	try {
		dashboard = new HeavyDashboard();
		dashboard.setVisible(true);
	} catch (Exception e) {
		System.out.println("Error creating dashboard: " + e.getMessage());
	}
]]></StartupCode>"""

    content = re.sub(r'<AdditionalClassCode>.*?</AdditionalClassCode>', '', content, flags=re.DOTALL)
    content = re.sub(r'<StartupCode>.*?</StartupCode>', '', content, flags=re.DOTALL)
    
    variables_end = content.find('</Variables>', main_start)
    insert_pos = variables_end + len('</Variables>')
    
    new_content = content[:insert_pos] + startup_code + additional_code + content[insert_pos:]
    
    # Update Hook for addData and training
    target = 'metrics.recordLatency( agent.flow_duration );'
    hook = target + """
    if (dashboard != null) {
        try {
            double[] features = new double[]{agent.packet_size, 0, 0, 0};
            
            // 1. Train AI Predictor online!
            if (aiPredictor != null) {
                aiPredictor.addTrainingSample(features, agent.flow_duration);
            }
            
            // 2. Make Prediction
            double pred = 0.0;
            if (aiPredictor != null) {
                pred = aiPredictor.predict(features);
            }
            
            // 3. Update Multi-Graph Dashboard
            dashboard.addData(agent.flow_duration, pred, agent.packet_size);
        } catch (Throwable e) { 
            dashboard.logError(e.toString()); 
        }
    }
"""
    if hook not in new_content:
        old_hook_regex = target + r'\s*if \(dashboard != null\).*?\}'
        new_content = re.sub(old_hook_regex, target, new_content, flags=re.DOTALL)
        new_content = new_content.replace(target, hook)

    # Patch MQTT_Buffer to maximumCapacity
    # We will search for the queue block and replace its maximumCapacity parameter
    # Wait, the best way to do this without breaking XML is to replace:
    # <Name><![CDATA[maximumCapacity]]></Name>
    # </Parameter>
    # With:
    # <Name><![CDATA[maximumCapacity]]></Name>
    # <Value Class="CodeValue"><Code><![CDATA[true]]></Code></Value>
    # </Parameter>
    
    # Or, to be very safe, let's just globally replace capacity 100 with 1000000 in Queue.
    # We already did that in the previous script? Let's check if the previous script ran.
    # The previous script did NOT run properly because of my regex, wait, it ran but did it replace?
    # Let's just ensure we inject <Value Class="CodeValue"><Code><![CDATA[true]]></Code></Value>
    # for maximumCapacity in the entire file. That's extremely safe.
    
    new_content = re.sub(r'<Name><!\[CDATA\[maximumCapacity\]\]></Name>\s*</Parameter>',
                         '<Name><![CDATA[maximumCapacity]]></Name>\n\t\t\t\t\t\t\t<Value Class="CodeValue">\n\t\t\t\t\t\t\t\t<Code><![CDATA[true]]></Code>\n\t\t\t\t\t\t\t</Value>\n\t\t\t\t\t\t</Parameter>',
                         new_content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected Ultimate Multi-Graph Dashboard successfully!")

if __name__ == '__main__':
    inject_code('FinalCCNProject.alp')
