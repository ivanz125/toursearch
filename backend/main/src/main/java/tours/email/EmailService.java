package tours.email;

public interface EmailService {
    void sendMessage(String email, String monitoringName, int resultsCount);
}
