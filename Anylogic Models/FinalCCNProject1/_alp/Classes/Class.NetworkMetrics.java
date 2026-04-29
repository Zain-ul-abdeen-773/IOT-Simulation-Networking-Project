public class NetworkMetrics {
	// Kept public for backwards-compatibility with AnyLogic inspectors/user code
	public double totalLatency = 0;
	public int packetCount = 0;

	public double minLatency = Double.POSITIVE_INFINITY;
	public double maxLatency = Double.NEGATIVE_INFINITY;

	// Online variance (Welford)
	private double meanLatency = 0;
	private double m2Latency = 0;

	public void recordLatency(double latency) {
		totalLatency += latency;
		packetCount++;

		if (latency < minLatency) minLatency = latency;
		if (latency > maxLatency) maxLatency = latency;

		double delta = latency - meanLatency;
		meanLatency += delta / packetCount;
		double delta2 = latency - meanLatency;
		m2Latency += delta * delta2;
	}

	public double getAverageLatency() {
		return packetCount == 0 ? 0 : totalLatency / packetCount;
	}

	public double getMinLatency() {
		return packetCount == 0 ? 0 : minLatency;
	}

	public double getMaxLatency() {
		return packetCount == 0 ? 0 : maxLatency;
	}

	public double getStdDevLatency() {
		return packetCount < 2 ? 0 : Math.sqrt(m2Latency / (packetCount - 1));
	}

	public void reset() {
		totalLatency = 0;
		packetCount = 0;
		minLatency = Double.POSITIVE_INFINITY;
		maxLatency = Double.NEGATIVE_INFINITY;
		meanLatency = 0;
		m2Latency = 0;
	}
}