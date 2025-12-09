import java.util.*;

public class Converter {

    private static boolean isOperator(String t) {
        return t.equals("+") || t.equals("-") || t.equals("*") || t.equals("/");
    }

    private static boolean isNumber(String t) {
        return t.matches("\\d+");
    }

    private static int precedence(String op) {
        switch (op) {
            case "+":
            case "-":
                return 1;
            case "*":
            case "/":
                return 2;
        }
        return 0;
    }

    // ======================================================
    // INFIX → POSTFIX
    // ======================================================
    public static List<String> infixToPostfix(List<String> tokens) {
        Stack<String> stack = new Stack<>();
        List<String> output = new ArrayList<>();

        for (String t : tokens) {

            if (isNumber(t)) {
                output.add(t);
            }
            else if (t.equals("(")) {
                stack.push(t);
            }
            else if (t.equals(")")) {
                while (!stack.isEmpty() && !stack.peek().equals("(")) {
                    output.add(stack.pop());
                }
                if (!stack.isEmpty() && stack.peek().equals("("))
                    stack.pop();
            }
            else if (isOperator(t)) {
                while (!stack.isEmpty() && isOperator(stack.peek()) &&
                        precedence(stack.peek()) >= precedence(t)) {
                    output.add(stack.pop());
                }
                stack.push(t);
            }
        }

        while (!stack.isEmpty()) {
            output.add(stack.pop());
        }

        return output;
    }

    // ======================================================
    // INFIX → PREFIX
    // ======================================================
    public static List<String> infixToPrefix(List<String> tokens) {
        // Reverse token list
        List<String> reversed = new ArrayList<>();
        for (int i = tokens.size() - 1; i >= 0; i--) {
            String t = tokens.get(i);
            // Tukar tanda kurung
            if (t.equals("(")) {
                reversed.add(")");
            } else if (t.equals(")")) {
                reversed.add("(");
            } else {
                reversed.add(t);
            }
        }

        // Konversi ke postfix dengan precedence dibalik
        Stack<String> stack = new Stack<>();
        List<String> output = new ArrayList<>();

        for (String t : reversed) {
            if (isNumber(t)) {
                output.add(t);
            }
            else if (t.equals("(")) {
                stack.push(t);
            }
            else if (t.equals(")")) {
                while (!stack.isEmpty() && !stack.peek().equals("(")) {
                    output.add(stack.pop());
                }
                if (!stack.isEmpty() && stack.peek().equals("("))
                    stack.pop();
            }
            else if (isOperator(t)) {
                // Untuk prefix, gunakan > bukan >=
                while (!stack.isEmpty() && isOperator(stack.peek()) &&
                        precedence(stack.peek()) > precedence(t)) {
                    output.add(stack.pop());
                }
                stack.push(t);
            }
        }

        while (!stack.isEmpty()) {
            output.add(stack.pop());
        }

        // Reverse hasil untuk mendapatkan prefix
        Collections.reverse(output);
        return output;
    }

    // ======================================================
    // POSTFIX → INFIX
    // ======================================================
    public static String postfixToInfix(List<String> tokens) {
        Stack<String> stack = new Stack<>();

        for (String t : tokens) {
            if (isNumber(t)) {
                stack.push(t);
            }
            else if (isOperator(t)) {
                String op2 = stack.pop();
                String op1 = stack.pop();
                String expr = "(" + op1 + " " + t + " " + op2 + ")";
                stack.push(expr);
            }
        }

        return stack.pop();
    }

    // ======================================================
    // PREFIX → INFIX
    // ======================================================
    public static String prefixToInfix(List<String> tokens) {
        Stack<String> stack = new Stack<>();

        // Scan dari kanan ke kiri
        for (int i = tokens.size() - 1; i >= 0; i--) {
            String t = tokens.get(i);

            if (isNumber(t)) {
                stack.push(t);
            }
            else if (isOperator(t)) {
                String op1 = stack.pop();
                String op2 = stack.pop();
                String expr = "(" + op1 + " " + t + " " + op2 + ")";
                stack.push(expr);
            }
        }

        return stack.pop();
    }
}