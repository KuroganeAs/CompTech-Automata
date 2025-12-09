import java.util.*;

public class Validator {

    // Check if a token is an operator
    private static boolean isOperator(String t) {
        return t.equals("+") || t.equals("-") || t.equals("*") || t.equals("/");
    }

    // Check number (digit atau multi-digit)
    private static boolean isNumber(String t) {
        return t.matches("\\d+");
    }

    // ==========================================
    // VALIDATE POSTFIX
    // ==========================================
    public static boolean validatePostfix(List<String> tokens) {
        int count = 0;

        for (String t : tokens) {
            if (isNumber(t)) {
                count++;
            } else if (isOperator(t)) {
                if (count < 2) return false;
                count--;  // consume 2 operands, push 1 → net -1
            } else if (t.equals("(") || t.equals(")")) {
                return false; // postfix tidak boleh ada kurung
            } else {
                return false; // token tidak dikenal
            }
        }

        return count == 1;
    }

    // ==========================================
    // VALIDATE PREFIX
    // ==========================================
    public static boolean validatePrefix(List<String> tokens) {
        int count = 0;

        // scan dari kanan ke kiri
        for (int i = tokens.size() - 1; i >= 0; i--) {
            String t = tokens.get(i);

            if (isNumber(t)) {
                count++;
            } else if (isOperator(t)) {
                if (count < 2) return false;
                count--;  // consume 2 operands, push 1
            } else if (t.equals("(") || t.equals(")")) {
                return false; // prefix tidak ada kurung
            } else {
                return false; // token tidak valid
            }
        }

        return count == 1;
    }

    // ==========================================
    // VALIDATE INFIX (sederhana)
    // ==========================================
    public static boolean validateInfix(List<String> tokens) {
        Stack<String> stack = new Stack<>();
        boolean lastWasOperator = true;

        for (String t : tokens) {
            if (isNumber(t)) {
                if (!lastWasOperator) return false;
                lastWasOperator = false;
            }
            else if (isOperator(t)) {
                if (lastWasOperator) return false;
                lastWasOperator = true;
            }
            else if (t.equals("(")) {
                stack.push(t);
                lastWasOperator = true;
            }
            else if (t.equals(")")) {
                if (stack.isEmpty()) return false;
                stack.pop();
            }
            else {
                return false;
            }
        }

        return !lastWasOperator && stack.isEmpty();
    }
}
