package finalccnproject;

import java.util.HashMap;

public class QTableBalancer {
    private static HashMap<String, Double> qTable = new HashMap<>();
    private static double alpha = 0.1; // Learning rate
    private static double gamma = 0.9; // Discount factor
    private static double epsilon = 0.2; // Exploration rate
    
    // State is simply the queue size range (e.g. "Low", "Medium", "High", "Critical")
    // Action is the delay multiplier (0.5, 1.0, 2.0)
    
    public static String getState(int queueSize) {
        if (queueSize < 10) return "Low";
        if (queueSize < 50) return "Medium";
        if (queueSize < 100) return "High";
        return "Critical";
    }
    
    public static double chooseAction(String state) {
        if (Math.random() < epsilon) {
            // Explore
            double r = Math.random();
            if (r < 0.33) return 0.5;
            if (r < 0.66) return 1.0;
            return 2.0;
        }
        
        // Exploit
        double bestQ = -9999;
        double bestAction = 1.0;
        double[] actions = {0.5, 1.0, 2.0};
        for (double a : actions) {
            String key = state + "_" + a;
            double q = qTable.getOrDefault(key, 0.0);
            if (q > bestQ) {
                bestQ = q;
                bestAction = a;
            }
        }
        return bestAction;
    }
    
    public static void update(String state, double action, double reward, String nextState) {
        String key = state + "_" + action;
        double oldQ = qTable.getOrDefault(key, 0.0);
        
        double maxNextQ = -9999;
        double[] actions = {0.5, 1.0, 2.0};
        for (double a : actions) {
            double q = qTable.getOrDefault(nextState + "_" + a, 0.0);
            if (q > maxNextQ) maxNextQ = q;
        }
        
        double newQ = oldQ + alpha * (reward + gamma * maxNextQ - oldQ);
        qTable.put(key, newQ);
    }
}
