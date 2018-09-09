package tours.util;

import java.security.MessageDigest;

public class Utils {

    public static String md5(String s) {
        try {
            MessageDigest md5 = MessageDigest.getInstance("MD5");
            byte[] bytes = md5.digest(s.getBytes());
            StringBuffer sb = new StringBuffer();
            for (int i = 0; i < bytes.length; ++i) {
                sb.append(Integer.toHexString((bytes[i] & 0xFF) | 0x100).substring(1, 3));
            }
            return sb.toString();
        }
        catch (Exception ex) {
            return null;
        }
    }
}
