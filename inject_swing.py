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
		private String lastError = "";
		
		private javax.swing.JPanel panel = new javax.swing.JPanel() {
			@Override
			protected void paintComponent(java.awt.Graphics g) {
				try {
					super.paintComponent(g);
					java.awt.Graphics2D g2d = (java.awt.Graphics2D) g;
					g2d.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
					
					// Draw background
					g2d.setColor(new java.awt.Color(11, 22, 48));
					g2d.fillRect(0, 0, getWidth(), getHeight());
					
					// Draw title
					g2d.setColor(java.awt.Color.WHITE);
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 28));
					g2d.drawString("AI Network Analytics Engine (Swing)", 30, 50);
					
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.PLAIN, 16));
					g2d.setColor(java.awt.Color.LIGHT_GRAY);
					g2d.drawString("Live Packets Processed: " + actualLatencies.size(), 30, 80);
					
					if (!lastError.isEmpty()) {
						g2d.setColor(java.awt.Color.RED);
						g2d.drawString("Error: " + lastError, 30, 100);
					}
					
					// Draw Grid
					g2d.setColor(new java.awt.Color(255, 255, 255, 30));
					for(int i=0; i<10; i++) {
						g2d.drawLine(30, 120 + i*40, 800, 120 + i*40);
					}
					
					// Draw Chart Data
					if (actualLatencies.size() > 1) {
						int n = Math.min(actualLatencies.size(), 100);
						int startIdx = actualLatencies.size() - n;
						
						// Auto-scale
						double maxVal = 0.001;
						for(int i=0; i<n; i++) {
							double v1 = actualLatencies.get(startIdx + i);
							double v2 = predictedLatencies.get(startIdx + i);
							if (!Double.isNaN(v1) && v1 > maxVal) maxVal = v1;
							if (!Double.isNaN(v2) && v2 > maxVal) maxVal = v2;
						}
						double scaleY = 380.0 / maxVal;
						
						// Actual Latency Line (Cyan)
						g2d.setColor(new java.awt.Color(34, 211, 238));
						g2d.setStroke(new java.awt.BasicStroke(3));
						for(int i=0; i<n-1; i++) {
							double v1 = actualLatencies.get(startIdx + i);
							double v2 = actualLatencies.get(startIdx + i + 1);
							if(Double.isNaN(v1) || Double.isNaN(v2)) continue;
							
							int x1 = 30 + (i * 770 / 100);
							int y1 = 500 - (int)(v1 * scaleY);
							int x2 = 30 + ((i+1) * 770 / 100);
							int y2 = 500 - (int)(v2 * scaleY);
							g2d.drawLine(x1, Math.max(120, y1), x2, Math.max(120, y2));
						}
						
						// Predicted Latency Line (Purple)
						g2d.setColor(new java.awt.Color(124, 92, 255));
						for(int i=0; i<n-1; i++) {
							double v1 = predictedLatencies.get(startIdx + i);
							double v2 = predictedLatencies.get(startIdx + i + 1);
							if(Double.isNaN(v1) || Double.isNaN(v2)) continue;
							
							int x1 = 30 + (i * 770 / 100);
							int y1 = 500 - (int)(v1 * scaleY);
							int x2 = 30 + ((i+1) * 770 / 100);
							int y2 = 500 - (int)(v2 * scaleY);
							g2d.drawLine(x1, Math.max(120, y1), x2, Math.max(120, y2));
						}
						
						// Draw max scale value
						g2d.setColor(java.awt.Color.GRAY);
						g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.PLAIN, 12));
						g2d.drawString(String.format("Max Y: %.3fs", maxVal), 30, 115);
					}
					
					// Draw Legend
					g2d.setColor(new java.awt.Color(34, 211, 238));
					g2d.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 16));
					g2d.drawString("— Actual Latency", 30, 540);
					g2d.setColor(new java.awt.Color(124, 92, 255));
					g2d.drawString("— AI Predicted", 250, 540);
				} catch (Exception e) {
					lastError = "Paint Exception: " + e.getMessage();
				}
			}
		};
		
		public HeavyDashboard() {
			setTitle("AI Analytics Dashboard (Swing Pop-out)");
			setSize(850, 600);
			setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
			add(panel);
		}
		
		public void addData(double actual, double predicted) {
			javax.swing.SwingUtilities.invokeLater(new Runnable() {
				public void run() {
					try {
						actualLatencies.add(actual);
						predictedLatencies.add(predicted);
						if(actualLatencies.size() > 500) {
							actualLatencies.remove(0);
							predictedLatencies.remove(0);
						}
						panel.repaint();
					} catch (Exception e) {
						lastError = "AddData Exception: " + e.getMessage();
					}
				}
			});
		}
		
		public void logError(String err) {
			javax.swing.SwingUtilities.invokeLater(new Runnable() {
				public void run() {
					lastError = err;
					panel.repaint();
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
    
    target = 'metrics.recordLatency( agent.flow_duration );'
    hook = target + """
    if (dashboard != null) {
        try {
            double pred = 0.0;
            if (aiPredictor != null) {
                pred = aiPredictor.predict(new double[]{agent.packet_size, 0, 0, 0});
            }
            dashboard.addData(agent.flow_duration, pred);
        } catch (Throwable e) { 
            dashboard.logError(e.toString()); 
        }
    }
"""
    if hook not in new_content:
        old_hook_regex = target + r'\s*if \(dashboard != null\).*?\}'
        new_content = re.sub(old_hook_regex, target, new_content, flags=re.DOTALL)
        new_content = new_content.replace(target, hook)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected Thread-Safe Swing Dashboard successfully!")

if __name__ == '__main__':
    inject_code('FinalCCNProject.alp')
