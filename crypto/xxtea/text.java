import java.nio.ByteBuffer;
import java.nio.IntBuffer;
import java.util.Arrays;

public class text {

    public static ByteBuffer useless(ByteBuffer payload, ByteBuffer key) {
        byte[] bArr = new byte[payload.limit() - payload.position()]; // .limit() is essentially .length() for ByteBuffer
        payload.get(bArr); // fills bArr with input from payload
        ByteBuffer smth = ByteBuffer.wrap(bArr);
        System.out.println(smth);
        System.out.println(smth.asIntBuffer());
        return smth;
        // return process(smth, key);
    }

    public static byte[] custom_xxtea_decryptBuffer(byte[] payload, byte[] key) {
        return useless(ByteBuffer.wrap(payload), ByteBuffer.wrap(key)).array();
        // converts the byte[] objects to ByteBuffer objects
    }

    private static String byteArrayToHexString(byte[] byteArray) {
        StringBuilder result = new StringBuilder();
        for (byte b : byteArray) {
            result.append(String.format("%02X", b));
        }
        return result.toString();
    }

    public static ByteBuffer process(ByteBuffer payload, ByteBuffer key) {
        decryptBuffer(payload.asIntBuffer(), key.asIntBuffer());
        byte[] byteArray = new byte[payload.remaining()];
        payload.get(byteArray);
        System.out.println(byteArrayToHexString(byteArray));
        return payload; //exit
    }

    public static IntBuffer decryptBuffer(IntBuffer payload, IntBuffer key) {
        if (key.limit() == 4) { // key length of four is correct
            if (payload.limit() < 2) {
                return payload;
            }
            int y = payload.get(0);
            int sum = ((52 / payload.limit()) + 6) * (-1640531527); // CUSTOM DELTA ****
            int lengthn = payload.limit();
            do {
                int e = (sum >>> 2) & 3;
                int p = payload.limit() - 1;
                while (p > 0) {
                    int z = payload.get(p - 1);
                    y = payload.get(p) - (((y ^ sum) + (z ^ key.get((p & 3) ^ e))) ^ (((z >>> 5) ^ (y << 2)) + ((y >>> 3) ^ (z << 4))));
                    payload.put(p, y);
                    p--;
                }
                int z = payload.get(lengthn - 1);
                y = payload.get(0) - (((y ^ sum) + (key.get(e ^ (p & 3)) ^ z)) ^ (((z >>> 5) ^ (y << 2)) + ((y >>> 3) ^ (z << 4))));
                payload.put(0, y);
                sum += 1640531527;
            } while (sum != 0);
            return payload;
        }
        throw new IllegalArgumentException("XXTEA needs a 128-bits key");
    }

    private static byte[] hexStringToByteArray(String hexString) {
            int length = hexString.length();
            if (length % 2 != 0) {
                throw new IllegalArgumentException("Hex string must have an even number of characters");
            }

            // takes two hex chars at a time and forms the binary from it
            byte[] byteArray = new byte[length / 2];
            for (int i = 0; i < length; i += 2) {
                byteArray[i / 2] = (byte) ((Character.digit(hexString.charAt(i), 16) << 4)
                        + Character.digit(hexString.charAt(i + 1), 16));
            }

            return byteArray;
        }

    public static void main(String[] args) {
        String hexString = "484c494f53305553012b001100000001fef81af2e55707cd74a0ad25cd8a70ba";

        try {
            byte[] payload = hexStringToByteArray(hexString);
            System.out.println(Arrays.toString(payload));
            System.out.println(payload.length);
            custom_xxtea_decryptBuffer(payload, "tuoroLreWlacrAoh".getBytes());
        }
        catch (IllegalArgumentException e) {
            System.out.println("Invalid hex string: " + e.getMessage());
        }
    }

}
