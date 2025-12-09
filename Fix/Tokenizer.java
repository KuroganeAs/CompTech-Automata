import java.util.*;

public class Tokenizer {

    /**
     * Tokenize an expression string into a list of tokens.
     * Token dapat berupa:
     * - angka multi-digit (contoh: 123)
     * - operator: + - * /
     * - tanda kurung: ( )
     * Spasi akan diabaikan.
     */
    public static List<String> tokenize(String expr) {
        List<String> tokens = new ArrayList<>();
        StringBuilder number = new StringBuilder();

        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);

            if (Character.isDigit(ch)) {
                // Kumpulkan digit multi-digit
                number.append(ch);
            } else {
                // Jika sebelumnya ada angka, simpan dulu
                if (number.length() > 0) {
                    tokens.add(number.toString());
                    number.setLength(0);
                }

                // Jika bukan spasi, tambahkan sebagai token
                if (!Character.isWhitespace(ch)) {
                    tokens.add(String.valueOf(ch));
                }
            }
        }

        // Token terakhir jika berupa angka
        if (number.length() > 0) {
            tokens.add(number.toString());
        }

        return tokens;
    }
}
