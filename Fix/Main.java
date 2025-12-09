import java.util.*;

public class Main {

    private static void printList(List<String> list) {
        for (int i = 0; i < list.size(); i++) {
            if (i > 0) System.out.print(" ");
            System.out.print(list.get(i));
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("=== PDA Math Notation Validator & Converter ===");
        System.out.print("Masukkan ekspresi: ");
        String expr = sc.nextLine().trim();

        System.out.println("Pilih notasi input:");
        System.out.println("1. Infix");
        System.out.println("2. Postfix");
        System.out.println("3. Prefix");
        System.out.print("Pilihan (1/2/3): ");
        String choice = sc.nextLine().trim();

        // Tokenize input
        List<String> tokens = Tokenizer.tokenize(expr);

        try {
            switch (choice) {

                // ===============================
                // INIFX
                // ===============================
                case "1":
                    System.out.println("-> Mengecek Infix...");
                    boolean validInfix = Validator.validateInfix(tokens);
                    System.out.println("Valid: " + validInfix);

                    if (validInfix) {
                        List<String> postfix = Converter.infixToPostfix(tokens);
                        List<String> prefix = Converter.infixToPrefix(tokens);

                        System.out.print("Postfix: ");
                        printList(postfix);

                        System.out.print("Prefix : ");
                        printList(prefix);
                    }
                    break;

                // ===============================
                // POSTFIX
                // ===============================
                case "2":
                    System.out.println("-> Mengecek Postfix...");
                    boolean validPost = Validator.validatePostfix(tokens);
                    System.out.println("Valid: " + validPost);

                    if (validPost) {
                        String infix = Converter.postfixToInfix(tokens);
                        List<String> prefix = Converter.infixToPrefix(Tokenizer.tokenize(infix));

                        System.out.println("Infix  : " + infix);

                        System.out.print("Prefix : ");
                        printList(prefix);
                    }
                    break;

                // ===============================
                // PREFIX
                // ===============================
                case "3":
                    System.out.println("-> Mengecek Prefix...");
                    boolean validPre = Validator.validatePrefix(tokens);
                    System.out.println("Valid: " + validPre);

                    if (validPre) {
                        String infix = Converter.prefixToInfix(tokens);
                        List<String> postfix = Converter.infixToPostfix(Tokenizer.tokenize(infix));

                        System.out.println("Infix  : " + infix);

                        System.out.print("Postfix: ");
                        printList(postfix);
                    }
                    break;

                default:
                    System.out.println("Pilihan tidak valid!");
            }

        } catch (Exception e) {
            System.out.println("Terjadi kesalahan saat memproses konversi.");
            System.out.println("Detail: " + e.getMessage());
        }

        sc.close();
    }
}
