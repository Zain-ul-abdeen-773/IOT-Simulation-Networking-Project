import re

def inject_code(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to find the <ActiveObjectClass> block where <Name><![CDATA[Main]]></Name>
    # Then we find </Variables> inside it and insert <StartupCode> and <AdditionalClassCode>
    
    # Let's locate the Main block
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
	// Global datasets for charts
	public com.anylogic.engine.analysis.DataSet latencyDataset = new com.anylogic.engine.analysis.DataSet(100, new com.anylogic.engine.analysis.DataUpdater_x() {
		@Override
		public void update(com.anylogic.engine.analysis.DataSet _d) { }
	});
	public com.anylogic.engine.analysis.DataSet aiLatencyDataset = new com.anylogic.engine.analysis.DataSet(100, new com.anylogic.engine.analysis.DataUpdater_x() {
		@Override
		public void update(com.anylogic.engine.analysis.DataSet _d) { }
	});
]]></AdditionalClassCode>"""

    startup_code = """
			<StartupCode><![CDATA[
	// --- HEAVY UI GENERATION ---
	// 1. Dark Background
	com.anylogic.engine.presentation.ShapeRectangle bg = new com.anylogic.engine.presentation.ShapeRectangle(
		true, 0, 0, 1200, 800, null, 
		new java.awt.Color(11, 22, 48), 1.0, com.anylogic.engine.presentation.ShapeDrawMode.SHAPE_DRAW_2D
	);
	presentation.add(bg);

	// 2. Title Text
	com.anylogic.engine.presentation.ShapeText title = new com.anylogic.engine.presentation.ShapeText(
		com.anylogic.engine.presentation.ShapeDrawMode.SHAPE_DRAW_2D, true, 40, 30, 0, 0, 
		java.awt.Color.WHITE, "AI Network Analytics Engine",
		new java.awt.Font("SansSerif", java.awt.Font.BOLD, 28), com.anylogic.engine.presentation.ShapeText.ALIGN_LEFT
	);
	presentation.add(title);

	// 3. Time Plot
	com.anylogic.engine.analysis.TimePlot plot = new com.anylogic.engine.analysis.TimePlot(
		this, true, 40, 100, 600, 400,
		null, null,
		50.0, 10.0,
		com.anylogic.engine.analysis.Chart.SCALE_AUTO, 0, 0,
		com.anylogic.engine.analysis.Chart.GRID_DEFAULT, com.anylogic.engine.analysis.Chart.GRID_DEFAULT,
		java.awt.Color.DARK_GRAY, java.awt.Color.DARK_GRAY, java.awt.Color.WHITE
	);
	
	plot.addDataSet(latencyDataset, "Actual Latency", new java.awt.Color(34, 211, 238), true, com.anylogic.engine.analysis.Chart.INTERPOLATION_STEP, 2, com.anylogic.engine.analysis.Chart.POINT_NONE);
	plot.addDataSet(aiLatencyDataset, "AI Predicted", new java.awt.Color(124, 92, 255), true, com.anylogic.engine.analysis.Chart.INTERPOLATION_STEP, 2, com.anylogic.engine.analysis.Chart.POINT_NONE);
	plot.setTimeWindow(100.0);
	presentation.add(plot);
]]></StartupCode>"""

    new_content = content[:insert_pos] + startup_code + additional_code + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected heavy UI into Main!")

if __name__ == '__main__':
    inject_code('FinalCCNProject.alp')
