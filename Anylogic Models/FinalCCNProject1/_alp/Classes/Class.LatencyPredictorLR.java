public class LatencyPredictorLR {
	private final int featureCount;
	private final int trainTarget;

	private final java.util.ArrayList<double[]> trainX = new java.util.ArrayList<>();
	private final java.util.ArrayList<Double> trainY = new java.util.ArrayList<>();

	private boolean trained = false;
	// beta[0] = intercept, beta[i+1] = coefficient for feature i
	private double[] beta = null;

	// Online evaluation metrics (on post-train samples)
	private long evalCount = 0;
	private double sumAbsErr = 0;
	private double sumSqErr = 0;
	private double sumY = 0;
	private double sumY2 = 0;

	// Small ridge term to keep XtX invertible
	private final double ridgeLambda = 1e-6;

	public LatencyPredictorLR(int featureCount, int trainTarget) {
		this.featureCount = featureCount;
		this.trainTarget = Math.max(10, trainTarget);
	}

	public boolean isTrained() {
		return trained && beta != null;
	}

	public int getTrainSamplesCount() {
		return trainX.size();
	}

	public int getTrainTarget() {
		return trainTarget;
	}

	public long getEvalCount() {
		return evalCount;
	}

	public void addTrainingSample(double[] x, double y) {
		if (x == null || x.length != featureCount) return;
		if (Double.isNaN(y) || Double.isInfinite(y)) return;

		double[] copy = new double[featureCount];
		for (int i = 0; i < featureCount; i++) {
			double v = x[i];
			copy[i] = (Double.isNaN(v) || Double.isInfinite(v)) ? 0.0 : v;
		}

		trainX.add(copy);
		trainY.add(y);
	}

	public boolean trainIfReady() {
		if (isTrained()) return true;
		if (trainX.size() < trainTarget) return false;
		train();
		return isTrained();
	}

	public double predict(double[] x) {
		if (!isTrained() || x == null || x.length != featureCount) return Double.NaN;
		double y = beta[0];
		for (int i = 0; i < featureCount; i++) {
			double v = x[i];
			if (Double.isNaN(v) || Double.isInfinite(v)) v = 0.0;
			y += beta[i + 1] * v;
		}
		// Latency cannot be negative
		return y < 0 ? 0 : y;
	}

	public void updateEvaluation(double yTrue, double yPred) {
		if (Double.isNaN(yTrue) || Double.isInfinite(yTrue)) return;
		if (Double.isNaN(yPred) || Double.isInfinite(yPred)) return;

		double err = yPred - yTrue;
		evalCount++;
		sumAbsErr += Math.abs(err);
		sumSqErr += err * err;
		sumY += yTrue;
		sumY2 += yTrue * yTrue;
	}

	public double getMAE() {
		return evalCount == 0 ? Double.NaN : (sumAbsErr / evalCount);
	}

	public double getR2() {
		if (evalCount < 2) return Double.NaN;
		double sst = sumY2 - (sumY * sumY) / evalCount;
		if (sst <= 0) return Double.NaN;
		return 1.0 - (sumSqErr / sst);
	}

	public String coefficientsToString() {
		if (!isTrained()) return "";
		StringBuilder sb = new StringBuilder();
		sb.append(String.format("b0=%.6f", beta[0]));
		for (int i = 0; i < featureCount; i++) {
			sb.append(String.format(", b%d=%.6f", i + 1, beta[i + 1]));
		}
		return sb.toString();
	}

	private void train() {
		int n = trainX.size();
		int p = featureCount;
		int dim = p + 1; // intercept

		double[][] A = new double[dim][dim];
		double[] B = new double[dim];

		for (int row = 0; row < n; row++) {
			double[] x = trainX.get(row);
			double y = trainY.get(row);

			double[] xx = new double[dim];
			xx[0] = 1.0;
			for (int i = 0; i < p; i++) xx[i + 1] = x[i];

			for (int i = 0; i < dim; i++) {
				B[i] += xx[i] * y;
				for (int j = 0; j < dim; j++) {
					A[i][j] += xx[i] * xx[j];
				}
			}
		}

		for (int i = 0; i < dim; i++) {
			A[i][i] += ridgeLambda;
		}

		double[] solved = solveLinearSystem(A, B);
		if (solved == null) {
			trained = false;
			beta = null;
			return;
		}
		beta = solved;
		trained = true;
	}

	private static double[] solveLinearSystem(double[][] A, double[] b) {
		int n = b.length;
		double[][] aug = new double[n][n + 1];
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) aug[i][j] = A[i][j];
			aug[i][n] = b[i];
		}

		for (int col = 0; col < n; col++) {
			int pivot = col;
			double max = Math.abs(aug[col][col]);
			for (int r = col + 1; r < n; r++) {
				double v = Math.abs(aug[r][col]);
				if (v > max) {
					max = v;
					pivot = r;
				}
			}
			if (max < 1e-12) return null;
			if (pivot != col) {
				double[] tmp = aug[pivot];
				aug[pivot] = aug[col];
				aug[col] = tmp;
			}

			double pv = aug[col][col];
			for (int j = col; j < n + 1; j++) aug[col][j] /= pv;

			for (int r = 0; r < n; r++) {
				if (r == col) continue;
				double factor = aug[r][col];
				if (factor == 0) continue;
				for (int j = col; j < n + 1; j++) {
					aug[r][j] -= factor * aug[col][j];
				}
			}
		}

		double[] x = new double[n];
		for (int i = 0; i < n; i++) x[i] = aug[i][n];
		return x;
	}
}